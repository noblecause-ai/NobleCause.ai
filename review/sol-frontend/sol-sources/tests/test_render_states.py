from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build", ROOT / "build.py")
build = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(build)

SESSION = {
    "presentation": {
        "pillar_labels": {"A": "Investition in die Zukunft"},
        "pillar_symbols": {"A": "Keimling"},
    }
}


def test_no_consensus_renders_each_link():
    card = build.recommendation_card(
        SESSION,
        {
            "pillar": "A",
            "has_consensus": False,
            "title": "",
            "organization": None,
            "donation_url": None,
            "confidence": None,
            "rationale_md": "",
            "individual_votes": [
                {
                    "model": "Claude Opus",
                    "organization": "Organisation Eins",
                    "title": "Ansatz Eins",
                    "donation_url": "https://example.org/one",
                },
                {
                    "model": "GPT",
                    "organization": "Organisation Zwei",
                    "title": "Ansatz Zwei",
                    "donation_url": "https://example.org/two",
                },
                {
                    "model": "Gemini Pro",
                    "organization": "Organisation Drei",
                    "title": "Ansatz Drei",
                    "donation_url": "https://example.org/three",
                },
            ],
        },
    )
    assert "Keine Einigung" in card
    assert card.count("Zu dieser Organisation") == 3
    assert "Organisation Eins" in card
    assert "Organisation Zwei" in card
    assert "Organisation Drei" in card


def test_focus_rule_is_deterministic():
    session = {
        "recommendations": [
            {"pillar": "A", "has_consensus": True, "confidence": 0.6, "convergence": {"count": 3, "total": 3}},
            {"pillar": "D", "has_consensus": True, "confidence": 0.7, "convergence": {"count": 3, "total": 3}},
            {"pillar": "B", "has_consensus": True, "confidence": 0.9, "convergence": {"count": 2, "total": 3}},
        ]
    }
    assert build.focus_recommendation(session)["pillar"] == "D"
