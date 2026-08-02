"""P10 — Ein vorhandenes Tagesjournal ist kein CI-Fehler.

Der Idempotenz-Wächter in `run_wart.main()` (ein zweiter Lauf am selben Tag darf den
unveränderlichen Eintrag nicht überschreiben) beendet den Lauf sauber mit **Exit 0**
und einer sichtbaren Meldung — nicht als Fehler. Jeder ANDERE Abbruch bleibt
`sys.exit(!=0)`; genau daran hängt die Workflow-Bedingung in `.github/workflows/wart.yml`,
Schritt „Fehler als Issue melden": `if: failure()` greift nur bei Exit != 0. Der
Sonderfall trägt also ein eng umrissenes Erfolgssignal (0), kein pauschales `|| true`.

Belegt Befund P10: der korrekte Abbruch löste bislang (Exit != 0) einen falschen
CI-Alarm aus.
"""

import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
GREMIUM = HERE.parent
sys.path.insert(0, str(GREMIUM))

import run_wart  # noqa: E402


@pytest.fixture
def repo(tmp_path, monkeypatch):
    # ROOT auf den Testbaum umbiegen; API-Key-Pfad neutralisieren (wir testen die
    # frühen Gates, nicht den Modell-Call).
    monkeypatch.setattr(run_wart, "ROOT", tmp_path)
    monkeypatch.setattr(run_wart, "load_env", lambda *a, **k: None)
    monkeypatch.setattr(run_wart, "require_keys", lambda *a, **k: None)
    return tmp_path


def _make_session(root, sid="2026-07c", number=3, date="2026-07-07"):
    d = root / "sessions" / sid
    d.mkdir(parents=True, exist_ok=True)
    (d / "session.json").write_text(json.dumps({"number": number, "date": date}))


def _run_main(monkeypatch, date):
    monkeypatch.setattr(sys, "argv", ["run_wart.py", "--date", date])
    with pytest.raises(SystemExit) as exc:
        run_wart.main()
    return exc.value.code


def test_existing_journal_exits_clean_no_alarm(repo, monkeypatch, capsys):
    # Gültige, aktuelle Sitzung + bereits vorhandenes Tagesjournal.
    _make_session(repo)
    date = "2026-08-03"
    (repo / "journal" / date).mkdir(parents=True)

    code = _run_main(monkeypatch, date)

    assert code == 0, f"vorhandenes Tagesjournal muss Exit 0 sein (kein Alarm), war {code!r}"
    out = capsys.readouterr().out
    assert "existiert bereits" in out, "der No-op muss im Log sichtbar bleiben"
    # Der Wächter greift VOR dem Schreiben: kein raw/-Verzeichnis angelegt.
    assert not (repo / "journal" / date / "raw").exists()


def test_real_error_still_exits_nonzero_alarm_stays(repo, monkeypatch):
    # Kein Tagesjournal -> der Idempotenz-Wächter greift NICHT. Stattdessen ein echter
    # Fehlerpfad (sessions/ vorhanden, aber keine session.json): der Lauf muss weiterhin
    # mit Exit != 0 abbrechen, damit `if: failure()` im Workflow den CI-Alarm auslöst.
    (repo / "journal").mkdir(parents=True, exist_ok=True)  # aber NICHT das Datum
    (repo / "sessions").mkdir(parents=True, exist_ok=True)  # leer -> "keine session.json"

    code = _run_main(monkeypatch, "2026-08-03")

    assert code not in (0, None), f"echter Fehler muss Exit != 0 bleiben (Alarm), war {code!r}"
