"""Shared env/key handling for the gremium scripts.

Two responsibilities, deliberately in one place so run_wart.py and
run_session.py cannot drift apart:

  load_env()    — local convenience: read gremium/.env + repo-root .env,
                  but NEVER in CI. In CI the Actions secret environment is
                  the single source of truth; a stale/absent .env must never
                  paper over a missing secret (that hid the 401 once).
  require_keys() — hard fail-fast before any API call if a key is missing or
                  empty. Never logs the value, at most its length.
"""

import os
import sys
from pathlib import Path


def load_env(here: Path, root: Path):
    """Load gremium/.env then repo-root .env into os.environ — never in CI.

    GitHub Actions (and most CI) set CI=true; there the secret environment is
    authoritative and the .env fallback is disabled on purpose.
    """
    if os.environ.get("CI") == "true":
        return
    for env_file in (here / ".env", root / ".env"):
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"'))


def require_keys(*names):
    """Abort (exit 1) if any named env var is unset or empty. Never logs values."""
    missing = [n for n in names if not os.environ.get(n, "").strip()]
    if missing:
        for n in missing:
            print(f"FEHLER: {n} fehlt oder ist leer.", file=sys.stderr)
        print(
            f"Abbruch: {len(missing)} Key(s) fehlen oder sind leer — kein API-Call.",
            file=sys.stderr,
        )
        sys.exit(1)
    for n in names:
        print(f"  {n}: gesetzt ({len(os.environ[n])} Zeichen)")
