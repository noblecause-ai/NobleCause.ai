"""Tests für `reaggregate.py --backfill-votes`.

Belegt die Rekonstruktion des abgeleiteten Strukturfelds
`rounds[].votes[].recommendations[]` aus den unveränderten Rohvoten (r1/r2),
ohne Roh-, Prosa-, Aggregat- oder Korrekturfelder anzufassen. Alles läuft über
einen tmp-Root und eine Fixture-Registry; keine produktive Rekorddatei wird
berührt. Kein API-Aufruf.
"""

import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
GREMIUM = HERE.parent
sys.path.insert(0, str(GREMIUM))

import organizations  # noqa: E402
import reaggregate  # noqa: E402
from run_session import extract_json_block, structured_vote_recs  # noqa: E402

SID = "test-backfill"
REGISTRY = {
    "schema_version": 1,
    "organizations": [
        {"id": "org-a", "canonical_name": "Org A", "aliases": ["Org A"]},
        {"id": "org-b", "canonical_name": "Org B", "aliases": ["Org B"]},
    ],
}
RAW_JSON = {
    "recommendations": [
        {"pillar": "A", "organization": "Org A", "title": "TA",
         "confidence": 0.9, "conditional": False, "reservation": None},
        {"pillar": "B", "organization": "Org B", "title": "TB",
         "confidence": 0.8, "conditional": True, "reservation": "weil"},
    ]
}
RAW_TEXT = "Vorwort des Modells.\n```json\n" + json.dumps(RAW_JSON, ensure_ascii=False) + "\n```\n"


def _raw_anthropic():
    # Anbieter-Format, das reaggregate.text_of('anthropic') liest.
    return {"content": [{"type": "text", "text": RAW_TEXT}]}


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """tmp-Rekordbaum mit einer Sitzung, deren r1/r2-Einzelvoten nur Säule A
    tragen (Säule B fehlt im abgeleiteten Feld, ist aber im Rohvotum vorhanden)."""
    monkeypatch.setattr(reaggregate, "ROOT", tmp_path)
    (tmp_path / "organizations.json").write_text(json.dumps(REGISTRY, ensure_ascii=False))
    organizations.load_registry(tmp_path / "organizations.json")
    # Erwartete strukturierte Voten aus dem Rohvotum (A + B).
    full = structured_vote_recs(extract_json_block(RAW_TEXT))
    a_only = [r for r in full if r["pillar"] == "A"]
    assert [r["pillar"] for r in full] == ["A", "B"]  # Fixture-Selbstcheck

    sdir = tmp_path / "sessions" / SID
    (sdir / "raw").mkdir(parents=True)
    for prefix in ("r1", "r2"):
        (sdir / "raw" / f"{prefix}-anthropic.json").write_text(
            json.dumps(_raw_anthropic(), ensure_ascii=False))
    session = {
        "schema_version": 2,
        "id": SID,
        "participants": [{"model": "m1", "family": "anthropic", "label": "M1"}],
        "rounds": [
            {"kind": "initial_vote", "round": 1,
             "votes": [{"model": "m1", "content_md": "roher Text r1",
                        "recommendations": [dict(r) for r in a_only]}]},
            {"kind": "final_vote", "round": 2,
             "votes": [{"model": "m1", "content_md": "roher Text r2",
                        "recommendations": [dict(r) for r in a_only]}]},
        ],
        "summary": "unveränderliche Leserfassung",
        "dissent_md": "unveränderlicher Dissens",
        "recommendations": [{"pillar": "A", "has_consensus": True, "organization_id": "org-a"}],
        "unresolved_votes": [],
        "correction_notice": [{"date": "2026-08-06", "text": "Nachtrag"}],
        "costs": {"currency": "EUR", "total": 1.0},
    }
    (sdir / "session.json").write_text(json.dumps(session, indent=2, ensure_ascii=False))
    return {"root": tmp_path, "sdir": sdir, "full": full}


def _raw_hashes(sdir):
    import hashlib
    return {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted((sdir / "raw").glob("*.json"))
    }


# 1 · Dry-Run schreibt nichts.
def test_backfill_dry_run_writes_nothing(repo):
    sfile = repo["sdir"] / "session.json"
    before = sfile.read_bytes()
    changed = reaggregate.backfill_votes(SID, write=False)
    assert changed is True  # es GIBT eine Ergänzung
    assert sfile.read_bytes() == before  # aber nichts geschrieben


# 2 · Write rekonstruiert die fehlende Säule B aus r1/r2.
def test_backfill_write_reconstructs_from_raw(repo):
    reaggregate.backfill_votes(SID, write=True)
    session = json.loads((repo["sdir"] / "session.json").read_text())
    for rd in session["rounds"]:
        pillars = [r["pillar"] for r in rd["votes"][0]["recommendations"]]
        assert pillars == ["A", "B"], f"{rd['kind']}: erwartet A+B, war {pillars}"
        assert rd["votes"][0]["recommendations"] == repo["full"]


# 3 · Roh-/Prosa-/Aggregat-/Korrekturfelder bleiben unverändert.
def test_backfill_leaves_other_fields_untouched(repo):
    raw_before = _raw_hashes(repo["sdir"])
    before = json.loads((repo["sdir"] / "session.json").read_text())
    reaggregate.backfill_votes(SID, write=True)
    after = json.loads((repo["sdir"] / "session.json").read_text())
    assert _raw_hashes(repo["sdir"]) == raw_before  # Rohvoten byte-gleich
    for key in ("summary", "dissent_md", "recommendations", "unresolved_votes",
                "correction_notice", "costs", "participants", "id"):
        assert after[key] == before[key], f"Feld {key} unerlaubt geändert"
    # content_md je Runde/Vote unverändert.
    for rb, ra in zip(before["rounds"], after["rounds"]):
        assert ra["kind"] == rb["kind"] and ra["round"] == rb["round"]
        assert ra["votes"][0]["content_md"] == rb["votes"][0]["content_md"]
        # Säule A objektgleich (nur B ergänzt, A nicht verändert).
        a_before = [r for r in rb["votes"][0]["recommendations"] if r["pillar"] == "A"]
        a_after = [r for r in ra["votes"][0]["recommendations"] if r["pillar"] == "A"]
        assert a_after == a_before


# 4 · Zweiter Write ist idempotent.
def test_backfill_second_write_idempotent(repo):
    reaggregate.backfill_votes(SID, write=True)
    written = (repo["sdir"] / "session.json").read_bytes()
    changed = reaggregate.backfill_votes(SID, write=True)
    assert changed is False  # nichts mehr zu ergänzen
    assert (repo["sdir"] / "session.json").read_bytes() == written
