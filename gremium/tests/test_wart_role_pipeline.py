"""Der Wochenlauf hält Recherche und Governance als zwei API-Rollen auseinander."""

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


HERE = Path(__file__).resolve().parent
GREMIUM = HERE.parent
REPO = GREMIUM.parent
sys.path.insert(0, str(GREMIUM))

import run_wart  # noqa: E402


SCOUT_TEXT = (
    '```json\n{"search_queries":["q"],"findings":[],"rejected_findings":[],'
    '"delta_assessment":"Keine wesentliche Änderung."}\n```'
)


def test_weekly_run_uses_opus_scout_then_fable_wart(tmp_path, monkeypatch):
    session_dir = tmp_path / "sessions" / "2026-08"
    session_dir.mkdir(parents=True)
    (session_dir / "session.json").write_text(
        json.dumps(
            {
                "id": "2026-08",
                "number": 4,
                "date": "2026-08-06",
                "question": "Welche Organisationen?",
                "recommendations": [],
            }
        )
    )
    (tmp_path / "schedule.json").write_text("{}")

    calls = []
    scout_text = SCOUT_TEXT
    wart_text = '```json\n{"convene":false,"convene_rationale":"Kein Kriterium erfüllt."}\n```'

    def fake_scout(cfg, system, user, raw_dir):
        calls.append(("scout", cfg["model"]))
        return (
            scout_text,
            {"input_tokens": 100, "output_tokens": 50, "web_search_requests": 1},
            {"stop_reason": "end_turn"},
            ["q"],
        )

    def fake_wart(cfg, system, user, raw_dir):
        calls.append(("wart", cfg["model"]))
        return wart_text, {"input_tokens": 30, "output_tokens": 10}, {"stop_reason": "end_turn"}

    monkeypatch.setattr(run_wart, "ROOT", tmp_path)
    monkeypatch.setattr(run_wart, "load_env", lambda *a, **k: None)
    monkeypatch.setattr(run_wart, "require_keys", lambda *a, **k: None)
    monkeypatch.setattr(run_wart, "call_scout", fake_scout)
    monkeypatch.setattr(run_wart, "call_wart_decision", fake_wart)
    monkeypatch.setattr(sys, "argv", ["run_wart.py", "--date", "2026-08-24"])

    run_wart.main()

    assert calls == [("scout", "claude-opus-5"), ("wart", "claude-fable-5")]
    entry = json.loads((tmp_path / "journal" / "2026-08-24" / "entry.json").read_text())
    assert entry["model"] == "claude-opus-5"
    assert entry["decision_model"] == "claude-fable-5"
    assert entry["convene"] is False
    assert entry["search_queries"] == ["q"]
    assert entry["content_md"] == ""
    assert entry["delta_assessment"] == "Keine wesentliche Änderung."
    assert (
        tmp_path / "journal" / "2026-08-24" / "raw" / "scout-content.md"
    ).read_text() == SCOUT_TEXT
    assert entry["costs"]["components"]["scout"]["web_search_requests"] == 1


def test_two_scouts_run_same_prompt_and_publish_exact_divergence(tmp_path, monkeypatch):
    monkeypatch.setattr(run_wart, "ROOT", tmp_path)
    raw_dir = tmp_path / "journal" / "x" / "raw"
    raw_dir.mkdir(parents=True)
    scouts = [
        {"family": "openai", "model": "scout-a", "label": "A"},
        {"family": "mistral", "model": "scout-b", "label": "B"},
    ]
    seen = []

    def fake_scout(cfg, system, user, target):
        seen.append((cfg["model"], system, user, target.name))
        topic = "shared" if cfg["model"] == "scout-a" else "other"
        text = (
            '```json\n{"search_queries":["q"],"findings":['
            f'{{"pillar":"A","topic":"{topic}","source":"s"}}],'
            '"rejected_findings":[],"delta_assessment":"d"}\n```'
        )
        return text, {"input_tokens": 1, "output_tokens": 1, "web_search_requests": 1}, {"stop_reason": "end_turn"}, ["q"]

    reports, failures, divergence = run_wart.collect_scout_reports(
        scouts, "same-system", "same-user", raw_dir, caller=fake_scout
    )
    assert [(x[1], x[2]) for x in seen] == [("same-system", "same-user")] * 2
    assert [x[3] for x in seen] == ["scout-1", "scout-2"]
    assert len(reports) == 2 and failures == []
    assert divergence["overlap_percent"] == 0.0
    dossier = run_wart.combined_scout_dossier(reports, failures, divergence)
    assert "Scout 1: A" in dossier and "Scout 2: B" in dossier
    assert "exact_structured_finding_keys" in dossier


def test_one_of_two_scouts_may_fail_but_failure_stays_visible(tmp_path, monkeypatch):
    monkeypatch.setattr(run_wart, "ROOT", tmp_path)
    raw_dir = tmp_path / "journal" / "x" / "raw"
    raw_dir.mkdir(parents=True)
    scouts = [
        {"family": "openai", "model": "scout-a"},
        {"family": "mistral", "model": "scout-b"},
    ]

    def fake_scout(cfg, system, user, target):
        if cfg["model"] == "scout-a":
            return "", {"input_tokens": 0, "output_tokens": 0, "web_search_requests": 0}, {"stop_reason": "refusal"}, []
        return SCOUT_TEXT, {"input_tokens": 1, "output_tokens": 1, "web_search_requests": 1}, {"stop_reason": "end_turn"}, ["q"]

    reports, failures, divergence = run_wart.collect_scout_reports(
        scouts, "system", "user", raw_dir, caller=fake_scout
    )
    assert [r["config"]["model"] for r in reports] == ["scout-b"]
    assert failures[0]["model"] == "scout-a"
    assert failures[0]["reason"] == "stop_reason=refusal"
    assert failures[0]["usage"]["web_search_requests"] == 0
    assert divergence is None


def test_two_scout_refusals_write_record_without_wart_decision(tmp_path, monkeypatch):
    session_dir = tmp_path / "sessions" / "2026-08"
    session_dir.mkdir(parents=True)
    (session_dir / "session.json").write_text(
        json.dumps(
            {
                "id": "2026-08",
                "number": 4,
                "date": "2026-08-06",
                "question": "Welche Organisationen?",
                "recommendations": [],
            }
        )
    )
    original_next_session = "2026-09-05T12:00:00Z"
    (tmp_path / "schedule.json").write_text(
        json.dumps({"next_session": original_next_session, "unknown": "erhalten"})
    )
    scouts = [
        {
            "family": "anthropic",
            "model": "scout-a",
            "label": "A",
            "usd_per_1m_input": 1,
            "usd_per_1m_output": 1,
        },
        {
            "family": "anthropic",
            "model": "scout-b",
            "label": "B",
            "usd_per_1m_input": 1,
            "usd_per_1m_output": 1,
        },
    ]

    def fake_scout(cfg, system, user, raw_dir):
        return (
            "Teiltext, der nicht als Dossier gilt.",
            {"input_tokens": 10, "output_tokens": 2, "web_search_requests": 1},
            {"stop_reason": "refusal"},
            [f"query-{cfg['model']}"],
        )

    def forbidden_wart(*args, **kwargs):
        raise AssertionError("Bei doppelter Verweigerung darf der Wart nicht entscheiden")

    monkeypatch.setattr(run_wart, "ROOT", tmp_path)
    monkeypatch.setattr(run_wart, "load_env", lambda *a, **k: None)
    monkeypatch.setattr(run_wart, "require_keys", lambda *a, **k: None)
    monkeypatch.setattr(run_wart, "configured_scouts", lambda config: scouts)
    monkeypatch.setattr(run_wart, "call_scout", fake_scout)
    monkeypatch.setattr(run_wart, "call_wart_decision", forbidden_wart)
    monkeypatch.setattr(sys, "argv", ["run_wart.py", "--date", "2026-09-14"])

    run_wart.main()

    entry = json.loads((tmp_path / "journal/2026-09-14/entry.json").read_text())
    assert entry["schema_version"] == 2
    assert entry["kind"] == "refusal"
    assert entry["refusal"] is True
    assert [item["model"] for item in entry["refusals"]] == ["scout-a", "scout-b"]
    assert all(item["stop_reason"] == "refusal" for item in entry["refusals"])
    assert "convene" not in entry and "convene_rationale" not in entry
    assert entry["search_queries"] == ["query-scout-a", "query-scout-b"]
    Draft202012Validator(
        json.loads((REPO / "schema/journal.schema.json").read_text())
    ).validate(entry)

    schedule = json.loads((tmp_path / "schedule.json").read_text())
    assert schedule["last_journal"] == "/journal/2026-09-14/"
    assert schedule["next_session"] == original_next_session
    assert schedule["unknown"] == "erhalten"
