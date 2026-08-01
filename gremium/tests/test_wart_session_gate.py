"""§1 — Der Wart wählt die jüngste Sitzung deterministisch.

`run_wart.latest_session()` sortiert nach `(number, date)` (identisch zu
`run_session.prior_session()` und `content.js`), nicht nach dem Datumsstring allein.
`assert_current_session()` ist ein hartes Gate: eine `session_ref`, die nicht die
höchste Sitzungsnummer trägt, bricht laut ab, statt still publiziert zu werden.

Belegt Kimi-Befund B1: Alle drei Bestandssitzungen tragen `2026-07-07`; ohne den
Nummern-Schlüssel entschied die iterdir()-Reihenfolge des Runners, und der Wart
recherchierte am 20./27.07. gegen die überholte Sitzung 1.
"""

import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
GREMIUM = HERE.parent
sys.path.insert(0, str(GREMIUM))

import run_wart  # noqa: E402


def _make_sessions(root, specs):
    """specs: Liste (id, number, date). Legt sessions/<id>/session.json an."""
    sdir = root / "sessions"
    sdir.mkdir(parents=True, exist_ok=True)
    for sid, number, date in specs:
        d = sdir / sid
        d.mkdir(parents=True, exist_ok=True)
        (d / "session.json").write_text(json.dumps({"number": number, "date": date}))


@pytest.fixture
def repo(tmp_path, monkeypatch):
    monkeypatch.setattr(run_wart, "ROOT", tmp_path)
    return tmp_path


def test_latest_session_picks_highest_number_same_date(repo):
    # Alle drei tragen dasselbe Datum — die Wahl darf nicht von Name/iterdir abhängen.
    _make_sessions(repo, [
        ("2026-07", 1, "2026-07-07"),
        ("2026-07b", 2, "2026-07-07"),
        ("2026-07c", 3, "2026-07-07"),
    ])
    sid, session = run_wart.latest_session()
    assert sid == "2026-07c"
    assert session["number"] == 3


def test_latest_session_number_beats_later_date(repo):
    # Die Nummer ist die Wahrheit: höhere Nummer mit früherem Datum bleibt die jüngste.
    _make_sessions(repo, [
        ("2026-07", 1, "2026-07-07"),
        ("2026-08", 2, "2026-06-01"),
    ])
    sid, _ = run_wart.latest_session()
    assert sid == "2026-08"


def test_gate_passes_for_current(repo):
    _make_sessions(repo, [
        ("2026-07", 1, "2026-07-07"),
        ("2026-07c", 3, "2026-07-07"),
    ])
    run_wart.assert_current_session("2026-07c")  # kein SystemExit


def test_gate_aborts_for_stale(repo):
    _make_sessions(repo, [
        ("2026-07", 1, "2026-07-07"),
        ("2026-07c", 3, "2026-07-07"),
    ])
    # Exakt der Befund: der Wart würde auf Sitzung 1 zeigen, obwohl 3 die aktuelle ist.
    with pytest.raises(SystemExit):
        run_wart.assert_current_session("2026-07")


def test_gate_aborts_for_unknown_ref(repo):
    _make_sessions(repo, [("2026-07c", 3, "2026-07-07")])
    with pytest.raises(SystemExit):
        run_wart.assert_current_session("2026-99")
