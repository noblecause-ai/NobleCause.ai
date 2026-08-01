"""§3 — Schema-Tor für session.json (Wart-Regel 3).

Validierung gegen schema/session.schema.json vor dem Commit. Die drei Bestands-
sitzungen gehen durch (Vorprüfung des Wart-Entscheids); eine absichtlich vertrags-
widrige Sitzung wird gefangen und bricht den Lauf ab (keine Publikation).
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


def test_existing_sessions_validate():
    # Gegen den echten Rekord-Stamm: alle drei Bestandssitzungen sind schemakonform.
    assert schema_gate.validate_tree(
        "sessions", "session.json", "session.schema.json", "Sitzungen"
    ) == 0


def _tmp_repo(tmp_path):
    (tmp_path / "schema").mkdir()
    shutil.copy(REPO / "schema/session.schema.json", tmp_path / "schema/session.schema.json")
    return tmp_path


def test_invalid_session_is_caught(tmp_path, monkeypatch):
    _tmp_repo(tmp_path)
    sdir = tmp_path / "sessions" / "2026-99"
    sdir.mkdir(parents=True)
    (sdir / "session.json").write_text("{}")  # Pflichtfelder fehlen komplett
    monkeypatch.setattr(schema_gate, "ROOT", tmp_path)
    assert schema_gate.validate_tree(
        "sessions", "session.json", "session.schema.json", "Sitzungen"
    ) == 1


def test_main_exits_on_invalid(tmp_path, monkeypatch):
    _tmp_repo(tmp_path)
    sdir = tmp_path / "sessions" / "2026-99"
    sdir.mkdir(parents=True)
    (sdir / "session.json").write_text(json.dumps({"schema_version": 1}))
    monkeypatch.setattr(schema_gate, "ROOT", tmp_path)
    with pytest.raises(SystemExit):
        schema_gate.main(["schema_gate.py", "sessions"])


def test_main_passes_on_valid(tmp_path, monkeypatch):
    _tmp_repo(tmp_path)
    sdir = tmp_path / "sessions" / "2026-07c"
    sdir.mkdir(parents=True)
    shutil.copy(REPO / "sessions/2026-07c/session.json", sdir / "session.json")
    monkeypatch.setattr(schema_gate, "ROOT", tmp_path)
    schema_gate.main(["schema_gate.py", "sessions"])  # kein SystemExit
