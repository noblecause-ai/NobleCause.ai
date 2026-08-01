#!/usr/bin/env python3
"""Schema-Tor: validiert den Rekord gegen schema/**, bevor er committet wird.

Läuft als Workflow-Schritt VOR dem Commit (session.yml, wart.yml). Schlägt eine
Validierung fehl → Exit 1: keine Publikation. Der failure()-Zweig des Workflows
sichert die Rohartefakte und meldet ein Issue. Die Schemas liegen seit dem
Rekord-Stamm im Repo — hier werden sie erstmals durchgesetzt statt nur dokumentiert.

Aufruf:
  python3 schema_gate.py sessions   # alle sessions/*/session.json
  python3 schema_gate.py journal    # alle journal/*/entry.json   (§6)
  python3 schema_gate.py all        # beides (Default)
"""

import json
import sys
from pathlib import Path

import jsonschema

HERE = Path(__file__).parent
ROOT = HERE.parent


def _validator(schema_name):
    schema = json.loads((ROOT / "schema" / schema_name).read_text())
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema)


def validate_tree(subdir, filename, schema_name, label):
    """Validiert jede <subdir>/*/<filename> gegen <schema_name>. Gibt die Anzahl
    fehlerhafter Dateien zurück (0 = alles gültig)."""
    validator = _validator(schema_name)
    base = ROOT / subdir
    checked = failures = 0
    for d in sorted(base.iterdir()) if base.exists() else []:
        f = d / filename
        if not (d.is_dir() and f.exists()):
            continue
        checked += 1
        data = json.loads(f.read_text())
        errs = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        if errs:
            failures += 1
            print(f"✗ {f.relative_to(ROOT)} — {len(errs)} Schemafehler:")
            for e in errs:
                loc = "/".join(str(p) for p in e.path) or "(root)"
                print(f"    @{loc}: {e.message}")
        else:
            print(f"✓ {f.relative_to(ROOT)}")
    print(f"{label}: {checked} geprüft, {failures} fehlerhaft.")
    return failures


def main(argv):
    what = argv[1] if len(argv) > 1 else "all"
    total = 0
    if what in ("sessions", "all"):
        total += validate_tree("sessions", "session.json", "session.schema.json", "Sitzungen")
    if what in ("journal", "all"):
        total += validate_tree("journal", "entry.json", "journal.schema.json", "Journal")
    if total:
        sys.exit(f"Schema-Tor: {total} Datei(en) verletzen das Schema — keine Publikation.")
    print("Schema-Tor: alles gültig.")


if __name__ == "__main__":
    main(sys.argv)
