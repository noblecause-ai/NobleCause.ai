"""Tests für die wiederholbare, additive commission-2-Bestellung.

Deckt genau die Wiederholbarkeits-Invarianten aus dem CC-Auftrag ab: Auswahl nur
neuer Modelle, additive Registratur ohne Berührung des Bestands, Version/Pending/
Asset der neuen Einträge, laute Fehler bei Leere/Doppel-ID, unveränderter
COMMISSION_FRAME, Journal-Typ und unberührtes schedule.json. Alle API-Aufrufe
sind gestubbt; kein Test schreibt in die echten commissions/, journal/ oder
models.json.
"""

import copy
import hashlib
import json
import sys
import types
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
GREMIUM = HERE.parent
REPO = GREMIUM.parent
sys.path.insert(0, str(GREMIUM))

import prompts  # noqa: E402
import run_commission  # noqa: E402


NEW_IDS = ["claude-opus-5", "gpt-5.6-sol", "gemini-3.5-flash"]


def _config():
    return {"models": [
        {"model": "claude-opus-5", "family": "anthropic", "label": "Claude Opus"},
        {"model": "gpt-5.6-sol", "family": "openai", "label": "GPT"},
        {"model": "gemini-3.5-flash", "family": "google", "label": "Gemini"},
    ]}


def _registry_v1():
    """Repräsentativer v1-Bestand (drei Sitzinhaber der ersten Epoche)."""
    return {
        "schema_version": 1,
        "note": "Registratur-Notiz mit historischer Aussage zur Bestellung 2026-07-27.",
        "models": [
            {"model": "claude-opus-4-8", "model_label": "Claude Opus (Anthropic)",
             "convened": "2026-07-07", "ordered": "2026-07-27",
             "nachtragsbestellung": True, "motiv": "…", "begruendung": "…",
             "person": None, "warden_review": {"decision": "accepted"},
             "renders": 1, "attempt": 1,
             "asset": "/media/medallions/claude-opus-4-8.avif", "version": 1},
            {"model": "gpt-5.2", "model_label": "GPT (OpenAI)",
             "convened": "2026-07-07", "ordered": "2026-07-27",
             "nachtragsbestellung": True, "motiv": "…", "begruendung": "…",
             "person": None, "warden_review": {"decision": "accepted"},
             "renders": 1, "attempt": 1,
             "asset": "/media/medallions/gpt-5.2.avif", "version": 1},
            {"model": "gemini-2.5-pro", "model_label": "Gemini Pro (Google)",
             "convened": "2026-07-07", "ordered": "2026-07-27",
             "nachtragsbestellung": True, "motiv": "…", "begruendung": "…",
             "person": "Florence Nightingale", "warden_review": {"decision": "accepted"},
             "renders": 1, "attempt": 1,
             "asset": "/media/medallions/gemini-2.5-pro.avif", "version": 1},
        ],
    }


def _args(commission_id="commission-2", convened="2026-08-06",
          date="2026-08-07", dry_run=False):
    return types.SimpleNamespace(
        date=date, commission_id=commission_id, convened=convened, dry_run=dry_run)


def _stub_call_model(spec, system, frame, max_tokens, raw_dir, tag):
    return (
        f"MOTIV: Ein geprägtes Messingrelief für {spec['label']}.\n\n"
        f"BEGRÜNDUNG: Weil das Motiv {spec['label']} entspricht.",
        {"input_tokens": 5, "output_tokens": 7},
    )


@pytest.fixture
def root(tmp_path):
    """tmp-Repowurzel mit v1-Registratur — Ausgangsstand vor commission-2."""
    (tmp_path / "models.json").write_text(
        json.dumps(_registry_v1(), ensure_ascii=False, indent=2))
    return tmp_path


@pytest.fixture(autouse=True)
def _no_env(monkeypatch):
    """Non-Dry-Läufe in Tests dürfen keine Keys/kein .env verlangen."""
    monkeypatch.setattr(run_commission, "load_env", lambda *a, **k: None)
    monkeypatch.setattr(run_commission, "require_keys", lambda *a, **k: None)


# 1 · Bestand v1 + aktuelle Config → exakt die drei neuen IDs
def test_select_exactly_three_new():
    new = run_commission.select_new_models(_config()["models"], _registry_v1()["models"])
    assert [m["model"] for m in new] == NEW_IDS


# 2 · Alte Registratureinträge bleiben nach dem Append objektgleich + Reihenfolge
def test_old_entries_unchanged_after_append(root):
    before = copy.deepcopy(json.loads((root / "models.json").read_text()))
    run_commission._run(root, _config(), _args(), call_model_fn=_stub_call_model)
    after = json.loads((root / "models.json").read_text())
    assert after["models"][:3] == before["models"]      # objektgleich, gleiche Reihenfolge
    assert after["note"] == before["note"]              # historische Aussage bleibt
    assert len(after["models"]) == 6


# 3 · Neue Einträge: Version 2, pending, asset null, convened 2026-08-06
def test_new_entries_v2_pending(root):
    run_commission._run(root, _config(), _args(), call_model_fn=_stub_call_model)
    new = json.loads((root / "models.json").read_text())["models"][3:]
    assert [m["model"] for m in new] == NEW_IDS
    for m in new:
        assert m["version"] == 2
        assert m["warden_review"]["decision"] == "pending"
        assert m["asset"] is None
        assert m["person"] is None
        assert m["convened"] == "2026-08-06"
        assert m["ordered"] == "2026-08-07"
        assert m["nachtragsbestellung"] is True
        assert m["attempt"] == 1


# 4 · Bereits registrierte aktuelle ID wird nicht erneut bestellt
def test_registered_id_not_reordered():
    reg = _registry_v1()["models"] + [
        {"model": "claude-opus-5", "version": 2, "warden_review": {"decision": "pending"}}]
    new = run_commission.select_new_models(_config()["models"], reg)
    assert [m["model"] for m in new] == ["gpt-5.6-sol", "gemini-3.5-flash"]


# 5 · Leere Bestellmenge bricht vor call_model und vor Output-Verzeichnissen ab
def test_empty_order_aborts_before_write(root):
    config = {"models": [
        {"model": "claude-opus-4-8", "family": "anthropic", "label": "Claude Opus"}]}
    called = []

    def _spy(*a, **k):
        called.append(1)
        return ("", {})

    with pytest.raises(SystemExit):
        run_commission._run(root, config, _args(), call_model_fn=_spy)
    assert not called
    assert not (root / "commissions" / "2026-08-07").exists()
    assert not (root / "journal" / "2026-08-07").exists()


# 6 · Doppelte Config- oder Registratur-ID bricht laut ab
def test_duplicate_config_id_aborts():
    dup = _config()["models"] + [
        {"model": "claude-opus-5", "family": "anthropic", "label": "Dup"}]
    with pytest.raises(SystemExit):
        run_commission.select_new_models(dup, [])


def test_duplicate_registry_id_aborts():
    reg = _registry_v1()["models"] + [{"model": "claude-opus-4-8", "version": 1}]
    with pytest.raises(SystemExit):
        run_commission.select_new_models(_config()["models"], reg)


def test_unknown_family_aborts():
    bad = [{"model": "x-1", "family": "mistral", "label": "X"}]
    with pytest.raises(SystemExit):
        run_commission.select_new_models(bad, [])


# 7 · Commission-Output: nur neue Modelle + unveränderter COMMISSION_FRAME + Hash
def test_commission_output_frame_and_models(root):
    run_commission._run(root, _config(), _args(), call_model_fn=_stub_call_model)
    comm = json.loads((root / "commissions" / "2026-08-07" / "commission.json").read_text())
    assert [o["model"] for o in comm["orders"]] == NEW_IDS
    assert comm["frame"] == prompts.COMMISSION_FRAME
    assert comm["frame_sha256"] == hashlib.sha256(
        prompts.COMMISSION_FRAME.encode("utf-8")).hexdigest()
    assert comm["id"] == "commission-2"
    assert comm["convened"] == "2026-08-06"
    assert comm["ordered"] == "2026-08-07"


# 8 · Journal-Typ commission; schedule.json unberührt
def test_journal_type_and_schedule_untouched(root):
    (root / "schedule.json").write_text('{"sentinel": true}')
    run_commission._run(root, _config(), _args(), call_model_fn=_stub_call_model)
    entry = json.loads((root / "journal" / "2026-08-07" / "entry.json").read_text())
    assert entry["type"] == "commission"
    assert entry["schema_version"] == 1
    assert "Nachbestellung" in entry["delta_assessment"]
    assert json.loads((root / "schedule.json").read_text()) == {"sentinel": True}


def _record_snapshot(repo):
    """{relativer Pfad: bytes} über models.json + alle Dateien der beiden
    Rekordbäume (commissions/, journal/). Verzeichnis-mtime ist kein Vertrag —
    verglichen werden ausschließlich Dateiinhalte."""
    files = {}
    root_model = repo / "models.json"
    if root_model.is_file():
        files["models.json"] = root_model.read_bytes()
    for tree in ("commissions", "journal"):
        base = repo / tree
        if base.is_dir():
            for path in sorted(base.rglob("*")):
                if path.is_file():
                    files[str(path.relative_to(repo))] = path.read_bytes()
    return files


# 9 · Ein tmp-Root-Lauf fasst KEINEN realen Rekord an — zustandsfest, ohne
#     datierte Negativannahme über einen heute gültigen Rekordpfad.
def test_real_records_untouched(root):
    before = _record_snapshot(REPO)
    run_commission._run(root, _config(), _args(), call_model_fn=_stub_call_model)
    after = _record_snapshot(REPO)
    # Objekt-/Bytegleichheit über models.json + beide Rekordbäume: der reale
    # Rekord bleibt unangetastet, unabhängig davon, welche Datumspfade heute
    # bereits gültig existieren.
    assert after == before
    # Nachweis, dass der Lauf wirklich gegen tmp lief (und nur dort schrieb).
    assert (root / "commissions" / "2026-08-07" / "commission.json").is_file()
    assert (root / "journal" / "2026-08-07" / "entry.json").is_file()


# Zusatz: COMMISSION_FRAME wird bytegleich verwendet (kein Prompt-Umbau)
def test_frame_is_prompts_frame(root):
    result = run_commission._run(root, _config(), _args(), call_model_fn=_stub_call_model)
    assert result["commission"]["frame"] == prompts.COMMISSION_FRAME


# --- Nachbesserung 2026-08-07 -------------------------------------------------

# P1 (§1) · Fehlender Key bricht VOR jeder Verzeichnisanlage und vor call_model ab
def test_missing_key_aborts_before_any_write(root, monkeypatch):
    def _boom(*a, **k):
        raise SystemExit("missing key")

    monkeypatch.setattr(run_commission, "require_keys", _boom)
    called = []
    with pytest.raises(SystemExit):
        run_commission._run(
            root, _config(), _args(dry_run=False),
            call_model_fn=lambda *a, **k: called.append(1) or ("", {}))
    assert not called
    assert not (root / "commissions" / "2026-08-07").exists()
    assert not (root / "journal" / "2026-08-07").exists()


# P1 (§2) · Leere ID in Config bzw. Registratur bricht laut ab
def test_empty_config_id_aborts():
    with pytest.raises(SystemExit):
        run_commission.select_new_models(
            [{"model": "", "family": "anthropic", "label": "X"}], [])


def test_empty_registry_id_aborts():
    with pytest.raises(SystemExit):
        run_commission.select_new_models(_config()["models"], [{"model": "", "version": 1}])


def test_missing_label_aborts():
    with pytest.raises(SystemExit):
        run_commission.select_new_models([{"model": "x-1", "family": "anthropic"}], [])


# P1 (§3) · Bereits vergebene commission-id bricht vor Write/API ab
def test_duplicate_commission_id_aborts(root):
    old = root / "commissions" / "2026-07-27"
    old.mkdir(parents=True)
    (old / "commission.json").write_text(json.dumps({"id": "commission-1"}))
    called = []
    with pytest.raises(SystemExit):
        run_commission._run(
            root, _config(), _args(commission_id="commission-1"),
            call_model_fn=lambda *a, **k: called.append(1) or ("", {}))
    assert not called
    assert not (root / "commissions" / "2026-08-07").exists()


def test_whitespace_commission_id_aborts(root):
    with pytest.raises(SystemExit):
        run_commission._run(root, _config(), _args(commission_id="   "),
                            call_model_fn=_stub_call_model)


# P2 (§4) · Kalendarisch ungültiges Datum wird vor Write/API abgewiesen
def test_invalid_calendar_date_aborts(root):
    called = []
    with pytest.raises(SystemExit):
        run_commission._run(
            root, _config(), _args(date="2026-02-30"),
            call_model_fn=lambda *a, **k: called.append(1) or ("", {}))
    assert not called
    assert not (root / "commissions" / "2026-02-30").exists()


# P2 (§5) · Journal-Prosa: Grammatik + tatsächlicher Selektor
def test_journal_prose_grammar_and_selector(root):
    run_commission._run(root, _config(), _args(), call_model_fn=_stub_call_model)
    entry = json.loads((root / "journal" / "2026-08-07" / "entry.json").read_text())
    assert "Sitzmodellen" in entry["delta_assessment"]
    assert "Sitzmodell(en)" not in entry["delta_assessment"]
    assert "noch nicht in der Medaillon-Registratur steht" in entry["content_md"]
    assert "deren Medaillon noch fehlt" not in entry["content_md"]
