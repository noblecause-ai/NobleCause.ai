"""Golden-Test: Determinismus-Garantien des Backends.

Nagelt die deterministischen Funktionen fest, damit ein späterer Rewrite sie nicht
unbemerkt bricht. Rein lesend, außer advance_schedule — dessen ROOT wird auf ein
Temp-Verzeichnis umgelenkt, damit die echte schedule.json NIE angefasst wird.

Hinweis (siehe audit/findings.md): run_wart.latest_session() sortiert NUR nach
Datum und ist bei Datums-Gleichstand nicht deterministisch (Dateisystem-Ordnung) —
derselbe Bug-Typ wie die frühere „jüngste Sitzung" im Frontend. Er ist hier NICHT
golden-testbar (der Bug verhindert eine deterministische Zusicherung); dokumentiert,
nicht umgangen. run_session.prior_session() dagegen sortiert nach Nummer und IST
deterministisch — das wird unten festgenagelt.
"""

import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GREMIUM = REPO / "gremium"
sys.path.insert(0, str(GREMIUM))

import run_session  # noqa: E402


def test_resolve_session_id_picks_next_free_suffix():
    sd = REPO / "sessions"
    # 2026-07, -07b, -07c existieren -> nächster freier ist -07d.
    assert run_session.resolve_session_id(sd, "2026-07") == "2026-07d"
    # Freie Basis bleibt unverändert.
    assert run_session.resolve_session_id(sd, "2099-01") == "2099-01"


def test_prior_session_is_deterministic_by_number():
    # prior_session sortiert nach (number, date) absteigend -> Nummern eindeutig.
    pid, prior = run_session.prior_session()
    assert pid == "2026-07c"
    assert prior["number"] == 3


def test_advance_schedule_plus_30_days_preserves_other_fields(tmp_path, monkeypatch):
    # ROOT umlenken -> echte schedule.json unangetastet.
    shutil.copy(REPO / "schedule.json", tmp_path / "schedule.json")
    before = json.loads((REPO / "schedule.json").read_text())
    monkeypatch.setattr(run_session, "ROOT", tmp_path)
    run_session.advance_schedule("2026-08-08")
    after = json.loads((tmp_path / "schedule.json").read_text())
    assert after["next_session"] == "2026-09-07T12:00:00Z"  # +30 Tage @ T12:00:00Z
    assert after["next_research"] == before["next_research"]
    assert after["last_journal"] == before["last_journal"]
    # Beweis: echte Datei unverändert.
    assert json.loads((REPO / "schedule.json").read_text()) == before
