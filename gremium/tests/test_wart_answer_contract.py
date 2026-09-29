"""Strikte, getrennte Verträge für Scout-Recherche und Wart-Entscheid."""

import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
GREMIUM = HERE.parent
sys.path.insert(0, str(GREMIUM))

import run_wart  # noqa: E402


def fenced(payload):
    """Baut eine Wart-Antwort mit Dossier-Prosa + JSON-Block (wie das Modell liefert)."""
    body = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
    return f"## Dossier\n\nEtwas Prosa.\n\n```json\n{body}\n```\n"


def test_no_prose_fallback_function_left():
    # Der Prosa-Parser, den die Datennaht verbietet, ist entfernt.
    assert not hasattr(run_wart, "fallback_from_markdown")


def test_scout_contract_has_evidence_but_no_governance_decision():
    payload = {
        "search_queries": ["q1"],
        "findings": [],
        "rejected_findings": [],
        "delta_assessment": "Keine wesentliche Änderung.",
    }
    assert run_wart.parse_scout_answer(fenced(payload)) == payload


def test_scout_convene_is_a_role_violation():
    payload = {
        "search_queries": ["q1"],
        "findings": [],
        "rejected_findings": [],
        "delta_assessment": "Keine wesentliche Änderung.",
        "convene": False,
    }
    with pytest.raises(SystemExit):
        run_wart.parse_scout_answer(fenced(payload))


def test_wart_decision_contract_requires_boolean_and_rationale():
    valid = fenced({"convene": False, "convene_rationale": "Kein Kriterium erfüllt."})
    assert run_wart.parse_wart_decision(valid)["convene"] is False
    with pytest.raises(SystemExit):
        run_wart.parse_wart_decision(fenced({"convene": "false", "convene_rationale": "x"}))
    with pytest.raises(SystemExit):
        run_wart.parse_wart_decision(fenced({"convene": False, "convene_rationale": ""}))


@pytest.mark.parametrize("render", [json.dumps, fenced])
def test_json_presentation_does_not_change_decision(render):
    payload = {"convene": False, "convene_rationale": 'Ein Zeichen } ist kein Objektende; "Beleg" bleibt Text.'}
    assert run_wart.parse_wart_decision(render(payload)) == payload


@pytest.mark.parametrize("text", [
    'Keine Sitzung notwendig.',
    '{"convene":false,"convene_rationale":"x"',
    '{"convene":false,"convene_rationale":"x"} zusätzlicher Text',
    '[{"convene":false,"convene_rationale":"x"}]',
    '{"convene":"false","convene_rationale":"x"}',
])
def test_bare_json_does_not_enable_prose_fallback_or_boolean_coercion(text):
    with pytest.raises(SystemExit):
        run_wart.parse_wart_decision(text)


def test_paid_september_28_responses_preserve_decision_and_scout_failure():
    raw = GREMIUM.parent / "journal/2026-09-28/raw"
    chair = json.loads((raw / "chair-weekly-openai-response.json").read_text())
    text = chair["choices"][0]["message"]["content"]
    assert run_wart.parse_wart_decision(text) == json.loads(text)
    assert run_wart.parse_wart_decision(text)["convene"] is False
    grok = json.loads((raw / "scout-1/openrouter-response.json").read_text())
    with pytest.raises(SystemExit):
        run_wart.parse_scout_answer(grok["choices"][0]["message"]["content"])
