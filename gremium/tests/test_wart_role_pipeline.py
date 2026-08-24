"""Der Wochenlauf hält Recherche und Governance als zwei API-Rollen auseinander."""

import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
GREMIUM = HERE.parent
sys.path.insert(0, str(GREMIUM))

import run_wart  # noqa: E402


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
    scout_text = (
        '```json\n{"search_queries":["q"],"findings":[],"rejected_findings":[],'
        '"delta_assessment":"Keine wesentliche Änderung."}\n```'
    )
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
    assert entry["costs"]["components"]["scout"]["web_search_requests"] == 1
