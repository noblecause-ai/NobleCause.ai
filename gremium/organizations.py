"""Deterministische Organisations-Registry für den Aggregator.

Löst die Organisations-Strings aus Modell-Voten gegen die kuratierte
`organizations.json` (Repo-Root) auf — per Alias-Match, KEIN Fuzzy-Matching,
KEIN Modell. Ein LLM in der Aggregation wäre Verfassungsbruch.

Kernregel: Ein Votum wird NIE stillschweigend verworfen. Ein unbekannter
Org-String liefert `resolve() -> None`; der Aufrufer muss ihn als
'nicht zuordenbar' ausweisen, nicht als Dissens verbuchen.
"""

import json
import re
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent

_REGISTRY = None


def _norm(s):
    """Vergleichsnormalisierung: nur zum Abgleich gegen bekannte Aliasse,
    NIE zum Clustern unbekannter Strings."""
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def load_registry(path=None):
    """organizations.json laden, Alias->id-Map bauen, Alias-Kollisionen hart melden."""
    global _REGISTRY
    path = Path(path) if path else (ROOT / "organizations.json")
    data = json.loads(path.read_text())
    orgs = data["organizations"]
    alias_map = {}
    for o in orgs:
        for name in [o["canonical_name"], *o.get("aliases", [])]:
            n = _norm(name)
            if not n:
                continue
            if n in alias_map and alias_map[n] != o["id"]:
                raise ValueError(
                    f"Alias-Kollision in organizations.json: '{name}' zeigt auf "
                    f"'{alias_map[n]}' und '{o['id']}'"
                )
            alias_map[n] = o["id"]
    _REGISTRY = {"orgs": orgs, "by_id": {o["id"]: o for o in orgs}, "alias_map": alias_map}
    return _REGISTRY


def _registry():
    return _REGISTRY if _REGISTRY is not None else load_registry()


def resolve(org_string):
    """Org-id für den Organisations-String eines Votums, oder None (unbekannt)."""
    return _registry()["alias_map"].get(_norm(org_string))


def get(org_id):
    """Registry-Eintrag zu einer id (canonical_name, donation_url, …)."""
    return _registry()["by_id"].get(org_id)
