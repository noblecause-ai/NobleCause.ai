#!/usr/bin/env python3
"""Canary: prüft, dass alle drei Provider-Keys gesetzt UND live erreichbar sind.

Läuft in CI (preflight.yml, täglich 05:30 UTC) und via workflow_dispatch. Pro
Provider ein minimaler Live-Call mit winzigem Output-Budget. Gibt pro Provider
OK/FAIL aus, ohne je einen Key-Wert zu zeigen. Exit 1, sobald ein Provider
fehlschlägt — dann feuert der Fehler-Issue-Step im Workflow.

Die Canary-Modelle sind bewusst günstig/robust gewählt (Haiku, Flash mit
abgeschaltetem Thinking), nicht die teuren Council-Modelle: getestet wird die
Key-Gültigkeit je Anbieter, nicht ein bestimmtes Modell. Der Key ist pro Anbieter
derselbe wie in der Pipeline.

Kein load_env: der Canary läuft ausschließlich in CI, wo die Secret-Umgebung die
einzige Wahrheit ist.
"""

import os
import sys
from pathlib import Path

HERE = Path(__file__).parent


def ping_anthropic():
    import anthropic

    anthropic.Anthropic().messages.create(
        model="claude-haiku-4-5",
        max_tokens=1,
        messages=[{"role": "user", "content": "."}],
    )


def ping_openai():
    from openai import OpenAI

    # 16 = dokumentiertes Minimum der Responses-API ≙ „max_tokens=1".
    OpenAI().responses.create(model="gpt-5.2", max_output_tokens=16, input=".")


def ping_google():
    from google import genai
    from google.genai import types

    # Flash + thinking_budget=0: kleinstmöglicher Call ohne dass ein Denkbudget
    # das 1-Token-Limit sprengt (pro kann Thinking nicht abschalten → Flash).
    genai.Client().models.generate_content(
        model="gemini-2.5-flash",
        contents=".",
        config=types.GenerateContentConfig(
            max_output_tokens=1,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
    )


# (name, env-var, ping-fn) — env-var ist der Secret-Name; google-genai liest
# GEMINI_API_KEY (oder GOOGLE_API_KEY, bevorzugt). Projekt-Konvention: GEMINI_API_KEY.
PROVIDERS = [
    ("anthropic", "ANTHROPIC_API_KEY", ping_anthropic),
    ("openai", "OPENAI_API_KEY", ping_openai),
    ("google", "GEMINI_API_KEY", ping_google),
]


def main():
    results = {}
    for name, key_env, ping in PROVIDERS:
        # (a) Key gesetzt & nicht leer — nie den Wert zeigen.
        if not os.environ.get(key_env, "").strip():
            print(f"{name}: FAIL ({key_env} fehlt oder ist leer)")
            results[name] = False
            continue
        # (b) minimaler Live-Call.
        try:
            ping()
            print(f"{name}: OK")
            results[name] = True
        except Exception as e:  # noqa: BLE001
            # Nur Exception-Typ + gekürzter Text; SDK-Fehler enthalten den Key nicht.
            print(f"{name}: FAIL ({type(e).__name__}: {str(e)[:200]})")
            results[name] = False

    ok = all(results.values())
    print()
    print("Canary-Ergebnis: " + ("alle Provider OK" if ok else "mindestens ein Provider FAIL"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
