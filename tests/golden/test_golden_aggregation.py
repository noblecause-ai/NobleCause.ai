"""Golden-Test: Reproduzierbarkeit der publizierten Aggregation.

Reproduziert die `recommendations` der drei publizierten Sitzungen aus ihren
committeten Roh-Schlussvoten (`sessions/<id>/raw/r2-*.json`) mit dem aktuellen
Aggregator und prüft sie gegen den committeten `session.json`-Stand.

Zweck: JEDE Änderung am Aggregator ODER an organizations.json, die eine der drei
publizierten Sitzungen anders ausgäbe, färbt diesen Test ROT. Das ist die
Reproduzierbarkeits-Garantie, die einen späteren Rewrite verantwortbar macht.

Reine Charakterisierung — kein Verhalten wird geändert. Wiederverwendung der
anbieter-spezifischen Roh-Extraktion aus gremium/reaggregate.py.
"""

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
GREMIUM = REPO / "gremium"
sys.path.insert(0, str(GREMIUM))

import organizations  # noqa: E402
import reaggregate  # noqa: E402
import run_session  # noqa: E402

organizations.load_registry(REPO / "organizations.json")

SESSIONS = ["2026-07", "2026-07b", "2026-07c"]


def _reproduce(sid):
    sdir = REPO / "sessions" / sid
    session = json.loads((sdir / "session.json").read_text())
    votes = reaggregate.final_votes_from_raw(sdir, session)
    recs, unresolved = run_session.aggregate_recommendations(votes)
    return recs, unresolved, session


# ---- Kern-Netz: strikte Reproduktion aus den Rohvoten ----------------------

@pytest.mark.parametrize("sid", SESSIONS)
def test_reproduction_matches_published(sid):
    recs, unresolved, session = _reproduce(sid)
    assert recs == session["recommendations"], (
        f"{sid}: reproduzierte Aggregation weicht vom publizierten "
        f"session.json ab — Aggregator oder Registry hat sich geändert."
    )
    assert unresolved == session.get("unresolved_votes", [])


# ---- Dokumentierte Invarianten (menschenlesbar, pinnen die Ist-Fakten) -----

def _pillar(recs, p):
    return next(r for r in recs if r["pillar"] == p)


def test_2026_07c_all_four_consensus_with_spend_links():
    session = json.loads((REPO / "sessions" / "2026-07c" / "session.json").read_text())
    recs = session["recommendations"]
    for p in ("A", "B", "C", "D"):
        r = _pillar(recs, p)
        assert r["has_consensus"] is True, f"2026-07c Säule {p} sollte Konsens sein"
        assert r["donation_url"], f"2026-07c Säule {p} braucht einen Spendenweg"
    assert _pillar(recs, "A")["organization"] == "Helen Keller International"
    assert _pillar(recs, "B")["organization"] == "Against Malaria Foundation"
    assert _pillar(recs, "C")["organization"] == "Nuclear Threat Initiative (NTI)"
    assert _pillar(recs, "D")["organization"] == "Lead Exposure Elimination Project (LEEP)"


def test_2026_07c_conditional_marked_on_pillar_a_only():
    session = json.loads((REPO / "sessions" / "2026-07c" / "session.json").read_text())
    recs = session["recommendations"]
    a = _pillar(recs, "A")
    assert a["convergence"]["conditional_count"] == 1
    opus = next(v for v in a["convergence"]["votes"] if v["model"] == "Claude Opus")
    assert opus["conditional"] is True and "konditional" in opus["reservation"]
    # Säule B (AMF) beruht auf KEINEM Vorbehalt.
    assert _pillar(recs, "B")["convergence"]["conditional_count"] == 0


def test_2026_07_pillar_a_stays_dissent_no_false_merge():
    # HKI / IGN / Evidence Action sind drei verschiedene Orgs -> korrekt kein Konsens.
    session = json.loads((REPO / "sessions" / "2026-07" / "session.json").read_text())
    a = _pillar(session["recommendations"], "A")
    assert a["has_consensus"] is False
    orgs = {v["organization"] for v in a["individual_votes"]}
    assert len(orgs) == 3
    # Jedes Einzelvotum trägt organization_id + (aufgelöste) donation_url.
    for v in a["individual_votes"]:
        assert v.get("organization_id")


def test_donation_urls_come_from_registry_not_votes():
    reg = {o["id"]: o.get("donation_url")
           for o in json.loads((REPO / "organizations.json").read_text())["organizations"]}
    for sid in SESSIONS:
        session = json.loads((REPO / "sessions" / sid / "session.json").read_text())
        for r in session["recommendations"]:
            if r.get("has_consensus"):
                assert r["donation_url"] == reg[r["organization_id"]], (
                    f"{sid} {r['pillar']}: donation_url stammt nicht aus der Registry"
                )
