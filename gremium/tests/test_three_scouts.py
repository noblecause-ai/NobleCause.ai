"""Approved roster and three-report plumbing; no live adapter is implied."""
import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "gremium"))

import process_config as process
import prompts
import run_session
import run_wart
from scout_context import historical_comparison


def config():
    return json.loads((ROOT / "gremium/config.json").read_text())


def test_approved_roster_matches_measured_endpoints_without_activating_incomplete_transport():
    cfg = config()
    assert cfg["features"]["three_scouts"]["selection_status"] == "approved"
    assert cfg["features"]["three_scouts"]["enabled"] is False
    assert process.configured_scouts(cfg) == [cfg["scout"]]
    cfg["features"]["three_scouts"]["enabled"] = True
    scouts = process.configured_scouts(cfg)
    assert [(s["model"], s["openrouter"]["endpoint"], s["research_role"]) for s in scouts] == [
        ("x-ai/grok-4.6", "xai/zdr", "discovery"),
        ("perplexity/sonar-pro", "perplexity", "regional"),
        ("anthropic/claude-opus-5", "anthropic", "counterevidence"),
    ]
    assert scouts[2]["max_web_search_uses"] == 4
    assert scouts[2]["openrouter"]["reasoning_effort"] == "medium"
    # The approved future five-member council still has an outside family.
    cfg["models"] = json.loads((ROOT / "gremium/openrouter-candidates.json").read_text())["models"]
    assert process.configured_scouts(cfg) == scouts


@pytest.mark.parametrize("mutation, message", [
    (lambda c: c["features"]["two_scouts"].update(enabled=True), "gleichzeitig"),
    (lambda c: c["scouts"].pop(), "genau drei"),
    (lambda c: c["scouts"].__setitem__(0, None), "family und model"),
    (lambda c: c["scouts"][0].update(family="anthropic"), "verschiedenen Familien"),
    (lambda c: c["scouts"][0].update(research_role="regional"), "je genau einmal"),
    (lambda c: c["scouts"][0].pop("research_context"), "research_context=blind"),
    (lambda c: c.update(models=copy.deepcopy(c["scouts"])), "außerhalb des Rats"),
])
def test_three_scout_invariants(mutation, message):
    cfg = config()
    cfg["features"]["three_scouts"]["enabled"] = True
    mutation(cfg)
    with pytest.raises(ValueError, match=message):
        process.configured_scouts(cfg)


def test_gateway_scout_cannot_accidentally_use_direct_anthropic_sdk(tmp_path, monkeypatch):
    opus = config()["scouts"][2]
    seen = []
    def gateway(spec, system, user, directory):
        seen.append(spec)
        return "gateway result"
    monkeypatch.setattr(run_wart.openrouter_scout, "call_scout", gateway)
    for caller in (run_wart.call_scout, run_session.call_scout_dossier):
        assert caller(opus, "system", "user", tmp_path) == "gateway result"
    assert seen == [opus, opus]
    assert not list(tmp_path.iterdir())


def test_profiles_are_distinct_and_legacy_prompts_stay_exact():
    assert prompts.scout_system_for({}, "original") == "original"
    rendered = [prompts.scout_system_for(s, "base") for s in config()["scouts"]]
    assert len(set(rendered)) == 3
    assert all("base" not in p for p in rendered)
    assert all("höchstens 4 Findings" in p and '"findings"' in p for p in rendered)
    assert "mindestens zwei" in rendered[1]
    assert "Nullresultaten" in rendered[2]
    with pytest.raises(ValueError, match="Unbekannte"):
        prompts.scout_system_for({"research_role": "typo"}, "base")


def test_divergence_distinguishes_all_shared_pair_shared_and_unique():
    def report(topics):
        return {"findings": [{"pillar": "A", "topic": t, "source": "https://example.test/" + t} for t in topics]}
    result = process.scout_divergence([
        report(["all", "ab", "a"]), report(["all", "ab", "b"]), report(["all", "c"]),
    ])
    assert result["overlap_percent"] == 20.0
    assert [p["overlap_percent"] for p in result["pairwise"]] == [50.0, 25.0, 25.0]
    assert [r["findings"][0][1] for r in result["unique_by_report"]] == ["a", "b", "c"]


@pytest.mark.parametrize("failed_index", [None, 2])
def test_three_independent_calls_preserve_failure_and_report_identity(tmp_path, monkeypatch, failed_index):
    monkeypatch.setattr(run_wart, "ROOT", tmp_path)
    seen = []
    def caller(spec, system, user, raw_dir):
        index = len(seen) + 1
        seen.append((system, user, raw_dir.name))
        if index == failed_index:
            raise RuntimeError("visible provider failure")
        text = '```json\n' + json.dumps({"search_queries": [], "findings": [],
            "rejected_findings": [], "delta_assessment": "own result " + str(index)}) + '\n```'
        return text, {"input_tokens": 1, "output_tokens": 1}, {"stop_reason": "end_turn"}, []
    reports, failures, divergence = run_wart.collect_scout_reports(
        config()["scouts"], "base", "shared public context", tmp_path / "raw", caller=caller
    )
    assert len(seen) == 3 and len({s[0] for s in seen}) == 3
    assert [s[1] for s in seen] == ["shared public context"] * 3
    assert [s[2] for s in seen] == ["scout-1", "scout-2", "scout-3"]
    assert divergence["report_scout_indices"] == ([1, 3] if failed_index else [1, 2, 3])
    assert len(reports) == (2 if failed_index else 3)
    assert len(failures) == (1 if failed_index else 0)
    if failed_index:
        assert "visible provider failure" in failures[0]["reason"]


def test_oversized_dossier_is_not_silently_trimmed(tmp_path, monkeypatch):
    monkeypatch.setattr(run_wart, "ROOT", tmp_path)
    def caller(spec, system, user, raw_dir):
        findings = [{}] * (11 if spec["research_role"] == "regional" else 0)
        text = '```json\n' + json.dumps({"search_queries": [], "findings": findings,
            "rejected_findings": [], "delta_assessment": "own result"}) + '\n```'
        return text, {"input_tokens": 1, "output_tokens": 1}, {"stop_reason": "end_turn"}, []
    reports, failures, _ = run_wart.collect_scout_reports(
        config()["scouts"], "base", "user", tmp_path / "raw", caller=caller
    )
    assert len(reports) == 2
    assert failures[0]["model"] == "perplexity/sonar-pro"
    assert "max_findings" in failures[0]["reason"]
    assert failures[0]["usage"]["output_tokens"] == 1


def test_weekly_record_contains_all_three_reports_with_stubbed_transport(tmp_path, monkeypatch):
    cfg = config()
    cfg["features"]["three_scouts"]["enabled"] = True
    for scout in cfg["scouts"]:
        # Only exercise the orchestration/record path; never attest a live adapter.
        scout.update(usd_per_1m_input=1, usd_per_1m_output=1)
    here = tmp_path / "gremium"
    here.mkdir()
    (here / "config.json").write_text(json.dumps(cfg))
    session_dir = tmp_path / "sessions/2026-08"
    session_dir.mkdir(parents=True)
    (session_dir / "session.json").write_text(json.dumps({
        "id": "2026-08", "number": 4, "date": "2026-08-06",
        "question": "Do EARLIER_QUESTION_ORGANIZATIONS still merit support?",
        "recommendations": [{"pillar": "A", "has_consensus": True,
                             "organization": "EARLIER_RECOMMENDATION", "title": "old"}],
    }))
    journal_dir = tmp_path / "journal/2026-09-14"
    journal_dir.mkdir(parents=True)
    repeated_finding = {"pillar": "A", "topic": "Rediscovered intervention", "source": "https://example.test/study"}
    (journal_dir / "entry.json").write_text(json.dumps({
        "date": "2026-09-14", "findings": [{**repeated_finding, "summary": "EARLIER_JOURNAL_RESULT"}],
    }))
    (tmp_path / "schedule.json").write_text("{}")
    calls = []
    def scout_call(spec, system, user, raw_dir):
        for forbidden in ("EARLIER_", "https://example.test/study", "SCOUT_RESULT_", "2026-08-06"):
            assert forbidden not in system + user
        assert "2026-09-20" in user
        calls.append(spec["research_role"])
        text = '```json\n' + json.dumps({"search_queries": [], "findings": [repeated_finding],
            "rejected_findings": [], "delta_assessment": "SCOUT_RESULT_" + spec["research_role"]}) + '\n```'
        return text, {"input_tokens": 10, "output_tokens": 1}, {"stop_reason": "end_turn"}, []
    def compare(*args):
        assert calls == ["discovery", "regional", "counterevidence"]
        calls.append("comparison")
        return historical_comparison(*args)
    def wart_call(spec, system, user, raw_dir):
        assert calls == ["discovery", "regional", "counterevidence", "comparison"]
        assert "EARLIER_RECOMMENDATION" in user and "EARLIER_JOURNAL_RESULT" in user
        assert "journal/2026-09-14/entry.json" in user
        assert all("SCOUT_RESULT_" + role in user for role in calls[:3])
        calls.append("wart")
        return ('```json\n{"convene":false,"convene_rationale":"Rediscovery retained."}\n```',
                {"input_tokens": 1, "output_tokens": 1, "billed_usd": "0.001"}, {"stop_reason": "end_turn"})
    monkeypatch.setattr(run_wart, "ROOT", tmp_path)
    monkeypatch.setattr(run_wart, "HERE", here)
    monkeypatch.setattr(run_wart, "load_env", lambda *a: None)
    monkeypatch.setattr(run_wart, "require_keys", lambda *a: None)
    monkeypatch.setattr(run_wart, "validate_scout_transport", lambda *a: None)
    monkeypatch.setattr(run_wart, "call_scout", scout_call)
    monkeypatch.setattr(run_wart, "historical_comparison", compare)
    monkeypatch.setattr(run_wart, "call_wart_decision", wart_call)
    monkeypatch.setattr(sys, "argv", ["run_wart.py", "--date", "2026-09-20"])
    run_wart.main()
    entry = json.loads((tmp_path / "journal/2026-09-20/entry.json").read_text())
    assert [s["model"] for s in entry["scouts"]] == [s["model"] for s in cfg["scouts"]]
    assert [s["research_role"] for s in entry["scouts"]] == ["discovery", "regional", "counterevidence"]
    assert len(entry["costs"]["components"]["scouts"]) == 3
    assert entry["scout_divergence"]["report_scout_indices"] == [1, 2, 3]
    assert entry["research_mode"] == "blind_then_compare"
    assert entry["findings"] == [repeated_finding] * 3
    assert calls[-1] == "wart"


@pytest.mark.parametrize("led_by_wart", [False, True])
def test_session_brief_does_not_read_previous_recommendations(led_by_wart):
    class UnreadableHistory(dict):
        def get(self, *args):
            raise AssertionError("History must not be read for a blind Scout prompt")
    brief = run_session.scout_dossier_prompt(
        config()["scouts"], "Review EARLIER_QUESTION_ORGANIZATIONS", "2026-09-20",
        "EARLIER_SESSION", UnreadableHistory(recommendations="EARLIER_RECOMMENDATION"), led_by_wart,
    )
    assert prompts.SCOUT_BLIND_QUESTION in brief and "2026-09-20" in brief
    assert "EARLIER_" not in brief
    # Founding research also works without an earlier session.
    assert brief == run_session.scout_dossier_prompt(
        config()["scouts"], "Review EARLIER_QUESTION_ORGANIZATIONS", "2026-09-20", None, None, led_by_wart,
    )
    explicit = run_session.scout_dossier_prompt(
        config()["scouts"], "Review EARLIER_QUESTION_ORGANIZATIONS", "2026-09-20", None, None,
        led_by_wart, scout_question="Current independent search question",
    )
    assert "Current independent search question" in explicit and "EARLIER_" not in explicit


def test_comparison_uses_only_prior_structured_journal_findings(tmp_path):
    for date, findings in [("2026-09-14", [{"topic": "OLD", "source": "exact-source"}]),
                           ("2026-09-20", [{"topic": "SAME_DAY"}]),
                           ("2026-09-21", [{"topic": "FUTURE"}]),
                           ("2026-09-07", [])]:
        directory = tmp_path / "journal" / date
        directory.mkdir(parents=True)
        (directory / "entry.json").write_text(json.dumps({
            "date": date, "findings": findings, "content_md": "PROSE_ONLY",
        }))
    (tmp_path / ".env").write_text("DO_NOT_READ_THIS")
    context = historical_comparison(tmp_path, "2026-09-20", None, None)
    assert "OLD" in context and "exact-source" in context
    assert "journal/2026-09-14/entry.json" in context
    assert all(s not in context for s in ("SAME_DAY", "FUTURE", "PROSE_ONLY", "DO_NOT_READ_THIS"))


@pytest.mark.parametrize("led_by_wart", [False, True])
def test_session_calls_keep_history_and_opening_out_of_scout_inputs(tmp_path, monkeypatch, led_by_wart):
    cfg = config()
    cfg["features"]["three_scouts"]["enabled"] = True
    # Synthetic direct transport: this test checks contexts, not gateway support.
    for scout in cfg["scouts"]:
        scout.update(transport="api", usd_per_1m_input=1, usd_per_1m_output=1)
    here = tmp_path / "gremium"
    here.mkdir()
    (here / "config.json").write_text(json.dumps(cfg))
    (here / "sources.md").write_text("COUNCIL_SOURCES_ONLY")
    (tmp_path / "manifest.md").write_text("COUNCIL_MANIFEST_ONLY")
    prior_dir = tmp_path / "sessions/2026-08"
    prior_dir.mkdir(parents=True)
    (prior_dir / "session.json").write_text(json.dumps({
        "number": 4, "date": "2026-08-06", "question": "EARLIER_QUESTION",
        "recommendations": [{"pillar": "A", "has_consensus": True,
                             "organization": "EARLIER_ORGANIZATION", "title": "old"}],
    }))
    calls = []
    class ReachedCouncil(Exception):
        pass
    def scout_call(spec, system, user, raw_dir):
        assert all(s not in system + user for s in ("EARLIER_", "OPENING_HISTORY", "COUNCIL_", "SCOUT_RESULT_"))
        calls.append(spec["research_role"])
        text = "SCOUT_RESULT_" + spec["research_role"] + '\n```json\n' + json.dumps({
            "search_queries": [], "findings": [], "rejected_findings": [], "delta_assessment": "Evidence summary",
        }) + '\n```'
        return text, {"input_tokens": 1, "output_tokens": 1}, {"stop_reason": "end_turn"}, []
    def council_call(spec, system, user, *args, **kwargs):
        assert calls == ["discovery", "regional", "counterevidence"]
        assert "EARLIER_ORGANIZATION" in user
        assert all("SCOUT_RESULT_" + role in user for role in calls)
        assert ("OPENING_HISTORY" in user) == led_by_wart
        raise ReachedCouncil()
    monkeypatch.setattr(run_session, "ROOT", tmp_path)
    monkeypatch.setattr(run_session, "HERE", here)
    monkeypatch.setattr(run_session, "load_env", lambda *a: None)
    monkeypatch.setattr(run_session, "require_keys", lambda *a: None)
    monkeypatch.setattr(run_session, "validate_scout_transport", lambda *a: None)
    monkeypatch.setattr(run_session.openrouter, "required_keys", lambda *a: [])
    monkeypatch.setattr(run_session, "call_scout_dossier", scout_call)
    monkeypatch.setattr(run_session, "call_model", council_call)
    monkeypatch.setattr(run_session, "call_wart_simple", lambda *a, **kw: (
        "OPENING_HISTORY", {"input_tokens": 1, "output_tokens": 1, "billed_usd": "0.001"}, {"stop_reason": "end_turn"},
    ))
    monkeypatch.setattr(sys, "argv", [
        "run_session.py", "--question", "Review EARLIER_QUESTION_ORGANIZATIONS",
        "--title", "Test", "--session-id", "2026-09-test",
        "--led-by-wart" if led_by_wart else "--with-dossier",
    ])
    with pytest.raises(ReachedCouncil):
        run_session.main()
    raw = tmp_path / "sessions/2026-09-test/raw"
    assert "EARLIER_" not in (raw / "prompt-r0-wart.txt").read_text()
    assert "EARLIER_ORGANIZATION" in (raw / "prompt-history-comparison.txt").read_text()
