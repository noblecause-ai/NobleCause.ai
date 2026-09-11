"""Deliberation 0.5: strukturierte Erwiderung, sichtbarer Ausfall, gültiger Rekord."""

import json
import shutil
import sys
from pathlib import Path

import pytest


HERE = Path(__file__).resolve().parent
GREMIUM = HERE.parent
REPO = GREMIUM.parent
sys.path.insert(0, str(GREMIUM))

import run_session  # noqa: E402
import schema_gate  # noqa: E402


def fenced(payload):
    return "Wortlaut davor.\n```json\n" + json.dumps(payload) + "\n```"


def test_addressed_challenge_accepts_only_a_named_other_participant():
    parsed = run_session.parse_addressed_challenge(
        fenced(
            {
                "target_model_id": "model-b",
                "stance": "dispute",
                "claim": "Die Finanzierungslücke beträgt X.",
                "challenge": "Die Quelle misst Zusagen statt Auszahlungen.",
                "why_decisive": "Die Rangfolge hängt an der realen Lücke.",
                "evidence_question": "Welche Auszahlungen sind belegt?",
            }
        ),
        "model-a",
        ["model-a", "model-b", "model-c"],
    )
    assert parsed["target_model_id"] == "model-b"
    assert parsed["stance"] == "dispute"
    assert parsed["evidence_question"].endswith("belegt?")


@pytest.mark.parametrize(
    "payload, message",
    [
        ({}, "target_model_id"),
        (
            {
                "target_model_id": "model-a",
                "stance": "dispute",
                "claim": "x",
                "challenge": "y",
                "why_decisive": "z",
            },
            "keine fremde",
        ),
        (
            {
                "target_model_id": "model-b",
                "stance": "refuse",
                "claim": "x",
                "challenge": "y",
                "why_decisive": "z",
            },
            "stance",
        ),
        (
            {
                "target_model_id": "model-b",
                "stance": "support",
                "claim": "",
                "challenge": "y",
                "why_decisive": "z",
            },
            "claim",
        ),
    ],
)
def test_addressed_challenge_contract_fails_loudly(payload, message):
    with pytest.raises(ValueError, match=message):
        run_session.parse_addressed_challenge(
            fenced(payload), "model-a", ["model-a", "model-b"]
        )


def test_only_valid_challenges_are_forwarded_to_target():
    exchanges = [
        {
            "model": "model-a",
            "target_model_id": "model-b",
            "status": "valid",
            "stance": "support",
            "claim": "c",
            "challenge": "x",
            "why_decisive": "d",
            "evidence_question": None,
        },
        {
            "model": "model-c",
            "target_model_id": None,
            "status": "invalid",
            "failure": "kein JSON",
        },
    ]
    prompt_section = run_session.challenges_for_model(exchanges, "model-b")
    assert "Erwiderung von model-a" in prompt_section
    assert "Haltung: support" in prompt_section
    assert "model-c" not in prompt_section
    assert "keine" in prompt_section


def test_05_record_with_valid_and_failed_exchange_passes_schema(tmp_path, monkeypatch):
    session = json.loads((REPO / "sessions/2026-08/session.json").read_text())
    models = [p["model"] for p in session["participants"]]
    session["deliberation_version"] = "0.5"
    session["prompts"]["addressed_challenge"] = "publizierte Vorlage"
    session["rounds"].insert(
        -1,
        {
            "round": 1.75,
            "kind": "addressed_challenge",
            "exchanges": [
                {
                    "model": models[0],
                    "status": "valid",
                    "content_md": "Wortlaut",
                    "target_model_id": models[1],
                    "stance": "refine",
                    "claim": "c",
                    "challenge": "x",
                    "why_decisive": "d",
                    "evidence_question": None,
                },
                {
                    "model": models[1],
                    "status": "invalid",
                    "content_md": "unstrukturierter Wortlaut",
                    "target_model_id": None,
                    "failure": "kein strukturierter JSON-Block",
                    "raw_artifact": "raw/challenge-openai.json",
                },
                {
                    "model": models[2],
                    "status": "valid",
                    "content_md": "Begründete Zustimmung.",
                    "target_model_id": models[0],
                    "stance": "support",
                    "claim": "c2",
                    "challenge": "x2",
                    "why_decisive": "d2",
                    "evidence_question": None,
                },
            ],
        },
    )
    (tmp_path / "schema").mkdir()
    shutil.copy(REPO / "schema/session.schema.json", tmp_path / "schema/session.schema.json")
    out = tmp_path / "sessions" / "synthetic-05"
    out.mkdir(parents=True)
    (out / "session.json").write_text(json.dumps(session, ensure_ascii=False))
    monkeypatch.setattr(schema_gate, "ROOT", tmp_path)
    assert schema_gate.validate_tree("sessions", "session.json", "session.schema.json", "S") == 0
