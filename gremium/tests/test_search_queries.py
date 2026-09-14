import run_session


def test_api_queries_are_canonical_over_model_report():
    text = """## Suchanfragen

1. `modell-formulierung`

### Geprüft, nicht verwendet

- keine Suchanfrage
"""

    assert run_session.recorded_search_queries(text, ["tatsächliche API-Anfrage"]) == [
        "tatsächliche API-Anfrage"
    ]


def test_model_report_is_clean_fallback_without_api_queries():
    text = """## Suchanfragen

1. `erste Anfrage`
2. "zweite Anfrage"
- dritte Anfrage

### Geprüft, nicht verwendet

- Erläuterung, keine Suchanfrage
"""

    assert run_session.recorded_search_queries(text, []) == [
        "erste Anfrage",
        "zweite Anfrage",
        "dritte Anfrage",
    ]


def test_unstructured_prose_is_not_promoted_to_query():
    text = """## Suchanfragen

Keine Suche durchgeführt.
"""

    assert run_session.extract_search_queries(text) == []
