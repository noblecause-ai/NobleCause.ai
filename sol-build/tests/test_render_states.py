from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build", ROOT / "build.py")
build = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(build)

# Präsentations-Konstante + Registry setzen (statt der früheren presentation.*-Datenfelder).
build.CONFIG = {
    "pillar_labels": {"A": "Investition in die Zukunft"},
    "pillar_symbols": {"A": "Keimling"},
    "focus_rule": "…",
}
build.REGISTRY = {
    "org-eins": {"beschreibung": "Tut Eins."},
    "org-zwei": {"beschreibung": "Tut Zwei."},
    "org-drei": {"beschreibung": "Tut Drei."},
}


def test_no_consensus_renders_each_link():
    card = build.recommendation_card(
        {"participants": [], "rounds": []},
        {
            "pillar": "A",
            "has_consensus": False,
            "title": "",
            "organization": None,
            "donation_url": None,
            "confidence": None,
            "individual_votes": [
                {"model": "Claude Opus", "organization": "Organisation Eins", "organization_id": "org-eins",
                 "title": "Ansatz Eins", "donation_url": "https://example.org/one"},
                {"model": "GPT", "organization": "Organisation Zwei", "organization_id": "org-zwei",
                 "title": "Ansatz Zwei", "donation_url": "https://example.org/two"},
                {"model": "Gemini Pro", "organization": "Organisation Drei", "organization_id": "org-drei",
                 "title": "Ansatz Drei", "donation_url": "https://example.org/three"},
            ],
        },
    )
    assert "Keine Einigung" in card
    assert card.count("Zu dieser Organisation") == 3
    assert "Organisation Eins" in card and "Organisation Zwei" in card and "Organisation Drei" in card


def test_no_invented_reason_only_factual_beschreibung():
    """F1: die Karte trägt KEIN rationale_md, sondern nur die faktische Registry-beschreibung."""
    card = build.recommendation_card(
        {"participants": [], "rounds": [{"kind": "initial_vote", "votes": []}, {"kind": "final_vote", "votes": []}]},
        {
            "pillar": "A", "has_consensus": True, "title": "…",
            "organization": "Org Eins", "organization_id": "org-eins",
            "donation_url": "https://example.org/one", "confidence": 0.7,
            "rationale_md": "ERFUNDENE VERGLEICHENDE BEHAUPTUNG",
            "convergence": {"count": 3, "total": 3, "conditional_count": 0, "models": [], "votes": []},
        },
    )
    assert "ERFUNDENE VERGLEICHENDE BEHAUPTUNG" not in card
    assert "Tut Eins." in card  # faktische beschreibung


def test_focus_rule_is_deterministic():
    session = {
        "recommendations": [
            {"pillar": "A", "has_consensus": True, "confidence": 0.6, "convergence": {"count": 3, "total": 3}},
            {"pillar": "D", "has_consensus": True, "confidence": 0.7, "convergence": {"count": 3, "total": 3}},
            {"pillar": "B", "has_consensus": True, "confidence": 0.9, "convergence": {"count": 2, "total": 3}},
        ]
    }
    assert build.focus_recommendation(session)["pillar"] == "D"
