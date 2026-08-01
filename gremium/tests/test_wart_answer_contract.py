"""§2 — Strikter Vertrag für die Wart-Antwort (Codex #4 / Wart-Entscheid B).

`parse_wart_answer(text)` akzeptiert convene ausschließlich als JSON-true/false.
Jeder andere Typ — insbesondere der String "false", der in Python wahr ist — ist
Vertragsverletzung und bricht den Lauf ab, BEVOR ein Journal-Eintrag entsteht. Kein
Prosa-Fallback (die entfernte fallback_from_markdown-Funktion).
"""

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


def _valid(**over):
    base = {"delta_assessment": "Keine neue Evidenz.", "convene": False,
            "search_queries": ["q1"], "findings": [], "convene_rationale": "—"}
    base.update(over)
    return base


def test_valid_convene_false_returns_parsed():
    parsed = run_wart.parse_wart_answer(fenced(_valid(convene=False)))
    assert parsed["convene"] is False


def test_valid_convene_true_returns_parsed():
    parsed = run_wart.parse_wart_answer(fenced(_valid(convene=True)))
    assert parsed["convene"] is True


def test_convene_string_false_aborts():
    # Der Kernbefund: "false" als String ist in Python truthy — darf NICHT als
    # Einberufung JA (oder überhaupt) durchgehen.
    with pytest.raises(SystemExit):
        run_wart.parse_wart_answer(fenced(_valid(convene="false")))


def test_convene_string_true_aborts():
    with pytest.raises(SystemExit):
        run_wart.parse_wart_answer(fenced(_valid(convene="true")))


def test_convene_number_aborts():
    with pytest.raises(SystemExit):
        run_wart.parse_wart_answer(fenced(_valid(convene=1)))


def test_convene_missing_aborts():
    payload = _valid()
    del payload["convene"]
    with pytest.raises(SystemExit):
        run_wart.parse_wart_answer(fenced(payload))


def test_no_json_block_aborts():
    # Kein Fallback aus Prosa: fehlt der Block, scheitert der Lauf laut.
    with pytest.raises(SystemExit):
        run_wart.parse_wart_answer("## Dossier\n\nNur Prosa, **Nicht einberufen**.\n")


def test_missing_delta_aborts():
    payload = _valid(convene=False)
    payload["delta_assessment"] = ""
    with pytest.raises(SystemExit):
        run_wart.parse_wart_answer(fenced(payload))


def test_no_prose_fallback_function_left():
    # Der Prosa-Parser, den die Datennaht verbietet, ist entfernt.
    assert not hasattr(run_wart, "fallback_from_markdown")
