"""Fix 2 (Codex) — der Voll-Pfad-Test, der beim ersten Mal fehlte.

Kein Test baute den PERSISTIERTEN Rekord und schickte ihn durchs Schema-Tor: der
Aggregator-Test rief nur die Aggregation, der Schema-Test prüfte nur alte gültige
Sitzungen. Deshalb war die Suite grün, während ein Modell mit ungültigem `conditional`
die ganze Sitzung am Tor scheitern liess (der Blocker für Sitzung 4).

Dieser Test deckt den vollen Pfad: Modellantwort (fehlendes / String-`conditional`) →
`structured_vote_recs` (Writer) → vollständige `session.json` → `schema_gate`, plus die
Bestätigung, dass der Aggregator das Votum als `votes_invalid` führt. Ohne Fix 1
(`conditional` boolean|null) scheitert Schritt 3.
"""

import json
import shutil
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
GREMIUM = HERE.parent
REPO = GREMIUM.parent
sys.path.insert(0, str(GREMIUM))

import organizations  # noqa: E402
import run_session  # noqa: E402
import schema_gate  # noqa: E402

MINI = {"schema_version": 1, "organizations": [
    {"id": "hki", "canonical_name": "Helen Keller International",
     "aliases": ["Helen Keller Intl", "Helen Keller International (HKI)"],
     "donation_url": "https://hki.example/donate"}]}


@pytest.fixture(autouse=True)
def _registry(tmp_path):
    p = tmp_path / "organizations.json"
    p.write_text(json.dumps(MINI))
    organizations.load_registry(p)
    yield


@pytest.mark.parametrize("bad_rec", [
    # conditional fehlt ganz
    {"pillar": "A", "organization": "Helen Keller Intl", "title": "x",
     "donation_url": "u", "confidence": 0.7},
    # conditional ist ein String (in Python truthy, aber kein JSON-Boolean)
    {"pillar": "A", "organization": "Helen Keller Intl", "title": "x",
     "donation_url": "u", "confidence": 0.7, "conditional": "false"},
])
def test_invalid_conditional_full_path_publishes_marked(bad_rec, tmp_path, monkeypatch):
    bad = {"recommendations": [bad_rec]}
    good = {"recommendations": [{"pillar": "A", "organization": "Helen Keller International (HKI)",
            "title": "y", "donation_url": "u", "confidence": 0.7,
            "conditional": False, "reservation": None}]}

    # 1) Writer: das persistierte Rohvotum trägt conditional=null (markiert, nicht geraten).
    svr = run_session.structured_vote_recs(bad)
    assert svr and svr[0]["conditional"] is None and svr[0]["reservation"] is None

    # 2) Aggregator: das ungültige Votum ist kein Kandidat und zählt votes_invalid.
    aggr, _ = run_session.aggregate_recommendations(
        [{"label": "Opus", "parsed": bad}, {"label": "GPT", "parsed": good}])
    a = next(r for r in aggr if r["pillar"] == "A")
    assert a["votes_valid"] == 1 and a["votes_invalid"] >= 1

    # 3) Voller Rekord: echte Sitzung als Vorlage, das null-conditional-Rohvotum injizieren.
    #    OHNE Fix 1 (conditional boolean|null) würde das Schema-Tor hier scheitern — genau
    #    der Produktivabbruch, den die alte Suite nicht sah. Statt Sitzung 4 auszulassen,
    #    muss der Rekord publiziert werden, mit der Markierung.
    base = json.loads((REPO / "sessions/2026-07c/session.json").read_text())
    voted_round = next(r for r in base["rounds"] if r.get("votes"))
    voted_round["votes"][0]["recommendations"] = svr
    (tmp_path / "schema").mkdir()
    shutil.copy(REPO / "schema/session.schema.json", tmp_path / "schema/session.schema.json")
    out = tmp_path / "sessions" / "2026-07c"
    out.mkdir(parents=True)
    (out / "session.json").write_text(json.dumps(base, ensure_ascii=False))
    monkeypatch.setattr(schema_gate, "ROOT", tmp_path)
    assert schema_gate.validate_tree("sessions", "session.json", "session.schema.json", "S") == 0
