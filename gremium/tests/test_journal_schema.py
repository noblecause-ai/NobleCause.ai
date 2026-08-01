"""§6 — EIN Journal-Schema für alle Eintragstypen (Wart-Nachtrag).

Gemeinsame Kopffelder Pflicht, Typspezifisches optional, additionalProperties: true.
Abnahmetest ist der Bestand: alle vorhandenen Einträge (Research, Vertretung,
Einberufung, Bootstrap, Kommission) validieren unverändert. Ein Eintrag ohne ein
Kopffeld wird gefangen (Schema-Tor → keine Publikation).
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

import schema_gate  # noqa: E402


def test_existing_journal_validates():
    # Der Abnahmetest: der gesamte Bestand geht unverändert durch.
    assert schema_gate.validate_tree(
        "journal", "entry.json", "journal.schema.json", "Journal"
    ) == 0


def _tmp_repo(tmp_path):
    (tmp_path / "schema").mkdir()
    shutil.copy(REPO / "schema/journal.schema.json", tmp_path / "schema/journal.schema.json")
    return tmp_path


def _valid_entry():
    # Ein minimaler gültiger Eintrag (nur Kopffelder).
    return {
        "schema_version": 1, "date": "2026-08-10", "session_ref": "2026-07",
        "convene": False, "convene_rationale": "—", "delta_assessment": "x",
        "findings": [], "rejected_findings": [], "search_queries": [],
        "content_md": "x", "costs": {}, "actions_run_url": None,
    }


def test_missing_common_field_is_caught(tmp_path, monkeypatch):
    _tmp_repo(tmp_path)
    e = _valid_entry()
    del e["session_ref"]  # Kopffeld fehlt
    d = tmp_path / "journal" / "2026-08-10"
    d.mkdir(parents=True)
    (d / "entry.json").write_text(json.dumps(e))
    monkeypatch.setattr(schema_gate, "ROOT", tmp_path)
    assert schema_gate.validate_tree("journal", "entry.json", "journal.schema.json", "J") == 1


def test_extra_field_is_allowed(tmp_path, monkeypatch):
    _tmp_repo(tmp_path)
    e = _valid_entry()
    e["type"] = "commission"
    e["commission_ref"] = "commissions/2026-08-10"
    e["irgendein_neues_feld"] = "additionalProperties: true"
    d = tmp_path / "journal" / "2026-08-10"
    d.mkdir(parents=True)
    (d / "entry.json").write_text(json.dumps(e))
    monkeypatch.setattr(schema_gate, "ROOT", tmp_path)
    assert schema_gate.validate_tree("journal", "entry.json", "journal.schema.json", "J") == 0


def test_commission_entry_validates(tmp_path, monkeypatch):
    # Kommission: type gesetzt, session_ref null, kein model — muss durchgehen.
    _tmp_repo(tmp_path)
    d = tmp_path / "journal" / "2026-07-27b"
    d.mkdir(parents=True)
    shutil.copy(REPO / "journal/2026-07-27b/entry.json", d / "entry.json")
    monkeypatch.setattr(schema_gate, "ROOT", tmp_path)
    assert schema_gate.validate_tree("journal", "entry.json", "journal.schema.json", "J") == 0
