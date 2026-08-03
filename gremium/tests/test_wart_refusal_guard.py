"""Teil 1 (B) — Refusal-Guard für die Fable-Zulieferer-Calls der Sitzung.

Bei einer Verweigerung (stop_reason != end_turn) wurde bisher der Teiltext übernommen —
81 Byte Anlauf standen als echtes Dossier im Rekord (`if wart_dossier:` war wahr). Der
Guard `wart_step_result` übernimmt keinen Teiltext mehr und liefert stattdessen einen
Marker {stop_reason, at, raw_artifact}, der die ABWESENHEIT begründet. Die Sitzung läuft
weiter (Dossier ist Zulieferer, nicht Sitzung). Der Marker steht im Vertrag (schema).
"""

import json
import sys
from pathlib import Path

import jsonschema
import pytest

HERE = Path(__file__).resolve().parent
GREMIUM = HERE.parent
REPO = GREMIUM.parent
sys.path.insert(0, str(GREMIUM))

import run_session  # noqa: E402

SCHEMA = json.loads((REPO / "schema" / "session.schema.json").read_text())


def _validate(record):
    jsonschema.validate(record, SCHEMA)


def _base_record():
    # Ein gültiger Bestands-Rekord als Grundlage — nur GELESEN, sessions/ bleibt unverändert.
    return json.loads((REPO / "sessions" / "2026-07c" / "session.json").read_text())


# ---------- der Guard: kein Teiltext bei Verweigerung ----------

def test_refusal_takes_no_partial_text():
    text, marker = run_session.wart_step_result(
        "Ich beginne mit der Recherche...", {"stop_reason": "refusal"}, "r0-wart.json"
    )
    assert text is None, "bei Verweigerung darf KEIN Teiltext übernommen werden"
    assert marker["stop_reason"] == "refusal"
    assert marker["raw_artifact"] == "raw/r0-wart.json"
    assert isinstance(marker["at"], str) and marker["at"]


def test_end_turn_takes_text_normal_case():
    text, marker = run_session.wart_step_result(
        "vollständiges Dossier", {"stop_reason": "end_turn"}, "r0-wart.json"
    )
    assert text == "vollständiges Dossier"
    assert marker is None


def test_other_abnormal_stop_reason_also_guarded():
    # max_tokens (abgeschnitten) ist ebenfalls kein end_turn → kein Teiltext, Marker mit Grund.
    text, marker = run_session.wart_step_result(
        "abgeschnittener Anfang", {"stop_reason": "max_tokens"}, "moderation-wart.json"
    )
    assert text is None
    assert marker["stop_reason"] == "max_tokens"


# ---------- Schema-Tor: Verweigerungs-Rekord besteht, Normalfall auch ----------

def test_normal_record_still_passes_schema():
    _validate(_base_record())  # Bestand bleibt gültig — Normalfall grün


def test_refusal_record_passes_schema_with_marker_and_no_dossier():
    rec = _base_record()
    rec.pop("wart_dossier", None)  # kein Dossier im Rekord
    rec["wart_dossier_refusal"] = {
        "stop_reason": "refusal",
        "at": "2026-08-06T12:00:00+00:00",
        "raw_artifact": "raw/r0-wart.json",
    }
    _validate(rec)  # Rekord MIT Marker, OHNE Dossier besteht das Tor
    # die Sitzung läuft durch — die anderen Bestandteile sind vollständig da:
    assert rec.get("recommendations"), "Empfehlungen fehlen"
    assert rec.get("rounds"), "Runden fehlen"
    assert "wart_dossier" not in rec


def test_refusal_marker_incomplete_is_rejected_by_contract():
    # Feld im Rekord, aber unvollständig → das Tor muss es abweisen (Kimi-P9: im Vertrag, nicht nur da).
    rec = _base_record()
    rec["wart_dossier_refusal"] = {"stop_reason": "refusal"}  # at + raw_artifact fehlen
    with pytest.raises(jsonschema.ValidationError):
        _validate(rec)


# ---------- Kurzfassung: DEGRADIEREN, nicht abstürzen (Steward-Entscheid) ----------

def _summary_args(tmp_path):
    # summary_prompt gesetzt → Wart-Pfad (led_by_wart, der für Sitzung 4 relevante Fall).
    return dict(
        question="Testfrage",
        final_votes=[{"label": "M", "text": "Ein Schlussvotum ohne JSON-Block."}],
        recommendations=[{"pillar": "A", "has_consensus": True, "organization": "X",
                          "convergence": {"count": 3, "total": 3}}],
        dissent_md="kein Dissens",
        summarizer={"model": "claude-fable-5", "max_output_tokens": 1024, "label": "Wart"},
        raw_dir=tmp_path,
        summary_prompt="{question} {final_votes} {aggregation} {dissent_md}",
    )


def test_summary_refusal_degrades_not_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(
        run_session, "call_anthropic",
        lambda *a, **k: ("Ich beginne...", {"input_tokens": 10, "output_tokens": 5}, {"stop_reason": "refusal"}),
    )
    summary, highlights, usage, refusal = run_session.generate_summary(**_summary_args(tmp_path))
    assert summary == "", "bei Verweigerung wird degradiert (leere Kurzfassung), nicht abgebrochen"
    assert highlights == []
    assert refusal["stop_reason"] == "refusal"
    assert refusal["raw_artifact"] == "raw/summary-wart.json"


def test_summary_end_turn_is_parsed_normally(tmp_path, monkeypatch):
    good = '```json\n{"summary": "kurze Fassung", "dissent_highlights": []}\n```'
    monkeypatch.setattr(
        run_session, "call_anthropic",
        lambda *a, **k: (good, {"input_tokens": 10, "output_tokens": 5}, {"stop_reason": "end_turn"}),
    )
    summary, highlights, usage, refusal = run_session.generate_summary(**_summary_args(tmp_path))
    assert summary == "kurze Fassung"
    assert refusal is None


def test_summary_refusal_record_passes_schema(tmp_path):
    rec = _base_record()
    rec["summary"] = ""  # leere Kurzfassung — required string, "" besteht das Tor
    rec["summary_refusal"] = {
        "stop_reason": "refusal",
        "at": "2026-08-06T12:00:00+00:00",
        "raw_artifact": "raw/summary-wart.json",
    }
    _validate(rec)
    assert rec.get("recommendations") and rec.get("rounds")
