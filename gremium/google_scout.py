"""Google-Search-Adapter für den vorhandenen Scout-Vertrag."""

import json


REFUSAL_REASONS = {"SAFETY", "BLOCKLIST", "PROHIBITED_CONTENT", "RECITATION"}


def _queries(raw):
    found = []
    for candidate in raw.get("candidates") or []:
        metadata = candidate.get("grounding_metadata") or {}
        for query in metadata.get("web_search_queries") or []:
            query = str(query).strip()
            # Jeder von Google gemeldete Query-Eintrag ist eine abrechenbare
            # Suchanfrage. Gleicher Wortlaut darf hier deshalb nicht
            # dedupliziert werden; die spätere öffentliche Leseliste kann das.
            if query:
                found.append(query)
    return found


def _stop_reason(raw):
    candidates = raw.get("candidates") or []
    if candidates:
        reason = str(candidates[0].get("finish_reason") or "").upper()
        if reason == "STOP":
            return "end_turn"
        if reason in REFUSAL_REASONS:
            return "refusal"
        return reason.lower() or "unknown"
    prompt_feedback = raw.get("prompt_feedback") or {}
    if prompt_feedback.get("block_reason"):
        return "refusal"
    return "unknown"


def call_google_scout(scout_cfg, system, user, raw_dir, raw_filename):
    """Ruft Gemini mit Search Grounding auf und normalisiert nur den Stop-Grund.

    Die vollständige Provider-Antwort bleibt unter ``provider_response`` erhalten.
    Abgerechnete Suchanfragen entsprechen allen nichtleeren Queries aus
    ``grounding_metadata``.
    """
    from google import genai
    from google.genai import types

    client = genai.Client()
    print(f"  Modell: {scout_cfg['model']}")
    print("  Web-Suche: Google Search Grounding")
    print("  Starte API-Call …")
    response = client.models.generate_content(
        model=scout_cfg["model"],
        contents=user,
        config=types.GenerateContentConfig(
            system_instruction=system,
            max_output_tokens=scout_cfg.get("max_output_tokens", 8192),
            tools=[types.Tool(google_search=types.GoogleSearch())],
        ),
    )
    provider_raw = response.model_dump(mode="json")
    queries = _queries(provider_raw)
    raw = {
        "provider": "google",
        "stop_reason": _stop_reason(provider_raw),
        "provider_response": provider_raw,
    }
    (raw_dir / raw_filename).write_text(
        json.dumps(raw, indent=2, ensure_ascii=False, default=str)
    )

    metadata = response.usage_metadata
    usage = {
        "input_tokens": metadata.prompt_token_count or 0,
        "output_tokens": (metadata.candidates_token_count or 0)
        + (metadata.thoughts_token_count or 0),
        "web_search_requests": len(queries),
    }
    text = response.text or ""
    if queries:
        print("  Suchanfragen (API):")
        for query in queries:
            print(f"    · {query}")
    print(
        f"  Tokens: {usage['input_tokens']} in / {usage['output_tokens']} out · "
        f"Suchen: {usage['web_search_requests']}"
    )
    return text, usage, raw, queries
