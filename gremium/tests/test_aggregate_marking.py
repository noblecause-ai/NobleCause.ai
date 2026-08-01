"""§4 — Vollständigkeit, Markierung, Gleichstand, Doppelvotum (Codex #3, Kimi P1/P3).

Die Sitzung trägt immer alle vier Bereiche; fehlende gültige Voten werden markiert
(votes_valid/votes_invalid) statt den Bereich zu überspringen. Gleichstand ist kein
stiller Konsens. Ein Modell mit Mehrfach-Votum in einer Säule wird gewarnt.
"""

import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
GREMIUM = HERE.parent
sys.path.insert(0, str(GREMIUM))

import organizations  # noqa: E402
import run_session  # noqa: E402

FIXTURE = {
    "schema_version": 1,
    "organizations": [
        {"id": "hki", "canonical_name": "Helen Keller International",
         "aliases": ["Helen Keller Intl", "Helen Keller International (HKI)"],
         "donation_url": "https://hki.example/donate"},
        {"id": "amf", "canonical_name": "Against Malaria Foundation",
         "aliases": ["Against Malaria Foundation (AMF)"],
         "donation_url": "https://amf.example/donate"},
    ],
}


@pytest.fixture(autouse=True)
def _registry(tmp_path):
    p = tmp_path / "organizations.json"
    p.write_text(json.dumps(FIXTURE))
    organizations.load_registry(p)
    yield


def vote(label, *recs):
    return {"label": label, "parsed": {"recommendations": list(recs)}}


def rec(pillar, org, conf=0.7, conditional=False, reservation=None):
    # conditional ist seit §5 Pflichtfeld; Default false.
    return {"pillar": pillar, "title": f"{org} intervention", "organization": org,
            "donation_url": "https://model.example/x", "confidence": conf,
            "conditional": conditional, "reservation": reservation}


def pillar(recs, p):
    return next(r for r in recs if r["pillar"] == p)


def test_all_four_pillars_always_present():
    # Nur Säule A hat Voten — B/C/D dürfen NICHT fehlen, sondern markiert erscheinen.
    votes = [vote("Opus", rec("A", "Helen Keller Intl")),
             vote("GPT", rec("A", "Helen Keller International (HKI)")),
             vote("Gemini", rec("A", "Against Malaria Foundation"))]
    recs, _ = run_session.aggregate_recommendations(votes)
    assert {r["pillar"] for r in recs} == {"A", "B", "C", "D"}
    b = pillar(recs, "B")
    assert b["has_consensus"] is False
    assert b["votes_valid"] == 0
    assert b["votes_invalid"] == 3
    assert "nicht auswertbar" in b["rationale_md"]
    assert "Rohdaten liegen im Protokoll" in b["rationale_md"]


def test_all_unparseable_marks_every_area():
    votes = [{"label": m, "parsed": None} for m in ("Opus", "GPT", "Gemini")]
    recs, _ = run_session.aggregate_recommendations(votes)
    assert {r["pillar"] for r in recs} == {"A", "B", "C", "D"}
    for r in recs:
        assert r["votes_valid"] == 0 and r["votes_invalid"] == 3
        assert r["has_consensus"] is False


def test_partial_failure_counts_valid_and_invalid():
    votes = [vote("Opus", rec("A", "Helen Keller Intl")),
             vote("GPT", rec("A", "Helen Keller International (HKI)")),
             {"label": "Gemini", "parsed": None}]  # unlesbar
    a = pillar(run_session.aggregate_recommendations(votes)[0], "A")
    assert a["has_consensus"] is True  # zwei gültige konvergieren
    assert a["votes_valid"] == 2 and a["votes_invalid"] == 1
    assert "1 Modell(e) ohne auswertbares Votum" in a["rationale_md"]


def test_tie_is_not_silent_consensus():
    # 2-2-Gleichstand (nur über ein Doppelvotum erreichbar): HKI(Opus,GPT) vs AMF(Gemini,GPT).
    votes = [vote("Opus", rec("A", "Helen Keller Intl")),
             vote("Gemini", rec("A", "Against Malaria Foundation")),
             vote("GPT", rec("A", "Helen Keller International (HKI)"),
                  rec("A", "Against Malaria Foundation (AMF)"))]
    a = pillar(run_session.aggregate_recommendations(votes)[0], "A")
    assert a["has_consensus"] is False
    assert a["tie"] is True
    assert any("Empfehlungen abgegeben" in w for w in a.get("warnings", []))


def test_double_vote_warns_even_on_consensus():
    votes = [vote("Opus", rec("A", "Helen Keller Intl")),
             vote("GPT", rec("A", "Helen Keller International (HKI)"),
                  rec("A", "Helen Keller Intl"))]
    a = pillar(run_session.aggregate_recommendations(votes)[0], "A")
    assert a["has_consensus"] is True
    assert any("GPT" in w for w in a.get("warnings", []))


def test_split_without_double_vote_is_dissent_not_tie():
    # Zwei Modelle, zwei verschiedene Orgs (je 1 Träger) → Dissens, aber KEIN tie:
    # tie greift nur bei max_support>=2 mit mehr als einem Führer. Ein 1-1-Split ist
    # gewöhnlicher Dissens, kein Gleichstand-Sonderfall.
    votes = [vote("Opus", rec("A", "Helen Keller Intl")),
             vote("GPT", rec("A", "Against Malaria Foundation"))]
    a = pillar(run_session.aggregate_recommendations(votes)[0], "A")
    assert a["has_consensus"] is False
    assert a["tie"] is False
    assert a["votes_valid"] == 2 and a["votes_invalid"] == 0
