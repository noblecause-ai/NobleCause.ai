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
import json
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

    # gemini-flash-latest: aktueller, günstiger Flash-Alias. Die gepinnten
    # 2.x-flash-Varianten sind für neue Keys 404/deprecated; der stabile Alias
    # überlebt einzelne Modell-Retirements. Das Pipeline-Modell (gemini-2.5-pro)
    # lebt separat weiter — hier zählt nur die Key-Gültigkeit.
    #
    # Client BEWUSST in einer Variable halten: das Inline-genai.Client().…-Muster
    # lässt den referenzlosen Client im SDK-Fehlerpfad schließen und maskiert den
    # echten Fehler (z. B. 404/401) als "client has been closed". Die Diagnose
    # darf sich nicht selbst verschleiern.
    client = genai.Client()
    client.models.generate_content(
        model="gemini-flash-latest",
        contents=".",
        config=types.GenerateContentConfig(max_output_tokens=16),
    )


# (name, env-var, ping-fn) — env-var ist der Secret-Name; google-genai liest
# GEMINI_API_KEY (oder GOOGLE_API_KEY, bevorzugt). Projekt-Konvention: GEMINI_API_KEY.
PROVIDERS = [
    ("anthropic", "ANTHROPIC_API_KEY", ping_anthropic),
    ("openai", "OPENAI_API_KEY", ping_openai),
    ("google", "GEMINI_API_KEY", ping_google),
]


def main():
    config = json.loads((HERE / 'config.json').read_text())
    from process_config import feature_enabled
    if '--live-council' in sys.argv or feature_enabled(config, 'live_council'):
        import openrouter
        from cost_bounds import InputBounds
        from envtools import load_env, require_keys
        from live_session import settings
        cfg = settings(config)
        observe = (config.get('regular_operation') or {}).get('cost_mode') == 'observe'
        if not observe:
            bounds = InputBounds(cfg.get('input_bounds', {}), HERE.parent)
            for spec in cfg['models']:
                bounds.policy(spec)
        load_env(HERE, HERE.parent)
        require_keys('OPENROUTER_API_KEY')
        from council_state import chair_for
        weekly = '--weekly' in sys.argv
        seats = [chair_for(config,json.loads((HERE.parent/'schedule.json').read_text()))[0]] if weekly else cfg['models']
        import openrouter_scout
        from process_config import configured_scouts
        from live_debate import chair_response_format
        key = openrouter_scout.key_state()
        print(f"OpenRouter-Key: {key['limit_remaining']} Credits verbleiben; Limit {key['limit']}, ohne Rücksetzung.")
        if os.environ.get('GITHUB_OUTPUT'):
            with open(os.environ['GITHUB_OUTPUT'],'a') as output:
                output.write(f"remaining={key['limit_remaining']}\nlow_budget={'true' if openrouter.amount(key['limit_remaining']) < 10 else 'false'}\n")
        credit = openrouter.decode(openrouter.http('GET','/credits'))['data']
        if openrouter.amount(credit['total_credits']) <= openrouter.amount(credit['total_usage']):
            raise openrouter.OpenRouterError('Kein Kontoguthaben')
        errors = []
        for spec in seats:
            try:
                openrouter.endpoint_preflight(spec)
                openrouter.endpoint_preflight({**spec, 'response_format':chair_response_format([m['model'] for m in cfg['models']]),
                    'openrouter':{**spec['openrouter'],'reasoning_effort':spec['chair_reasoning_effort']}})
                print(f"Rat/Vorsitz: {spec['model']} · {spec['openrouter']['endpoint']} OK")
            except openrouter.OpenRouterError as exc:
                errors.append(f"{spec['model']} · {spec['openrouter']['endpoint']}: {exc}")
        catalog = openrouter.decode(openrouter.http('GET','/models'))
        from urllib.parse import quote
        for scout in configured_scouts(config):
            endpoints = openrouter.decode(openrouter.http('GET','/models/'+quote(scout['model'],safe='/')+'/endpoints'))
            try:
                openrouter_scout.endpoint_check(scout,catalog,endpoints)
                print(f"Scout: {scout['model']} · {scout['openrouter']['endpoint']} OK")
            except ValueError as exc:
                errors.append(f"Scout {scout['model']}: {exc}")
        print('Anschlussprüfung abgeschlossen; keine Inferenz.')
        if observe:
            print('Kostenbeobachtung aktiv: kein belegter Input-Bound und keine Abschlussreserve; Key-Limit bleibt unverändert.')
        if openrouter.amount(key['limit_remaining']) < 10:
            print('::warning::Weniger als 10 Credits verfügbar; Budget vor dem nächsten Sitzungszyklus prüfen.')
        if errors:
            sys.exit('\n'.join(errors))
        return
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
