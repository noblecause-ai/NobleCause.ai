import sys
from pathlib import Path

import pytest


GREMIUM = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GREMIUM))

from process_config import configured_scouts, feature_enabled, scout_divergence  # noqa: E402


def base_config():
    return {
        "scout": {"family": "anthropic", "model": "solo"},
        "wart": {"family": "anthropic", "model": "wart"},
        "models": [
            {"family": "anthropic", "model": "rat-a"},
            {"family": "openai", "model": "rat-o"},
            {"family": "google", "model": "rat-g"},
        ],
        "features": {"two_scouts": {"enabled": False}},
    }


def test_new_processes_are_explicitly_opt_in():
    config = base_config()
    assert feature_enabled(config, "two_scouts") is False
    assert feature_enabled(config, "deliberation_0_5") is False
    assert [s["model"] for s in configured_scouts(config)] == ["solo"]


def test_single_scout_still_requires_family_and_model():
    config = base_config()
    config["scout"] = {"family": "anthropic"}
    with pytest.raises(ValueError, match="family und model"):
        configured_scouts(config)


def test_two_scouts_require_two_families_and_one_outside_council():
    config = base_config()
    config["features"]["two_scouts"]["enabled"] = True
    config["scouts"] = [
        {"family": "openai", "model": "scout-a"},
        {"family": "mistral", "model": "scout-b"},
    ]
    assert [s["model"] for s in configured_scouts(config)] == ["scout-a", "scout-b"]


@pytest.mark.parametrize(
    "scouts, message",
    [
        ([{"family": "openai", "model": "a"}], "genau zwei"),
        (
            [{"family": "openai", "model": "a"}, {"family": "openai", "model": "b"}],
            "verschiedenen Familien",
        ),
        (
            [{"family": "openai", "model": "a"}, {"family": "google", "model": "b"}],
            "außerhalb des Rats",
        ),
        (
            [{"family": "mistral", "model": "wart"}, {"family": "xai", "model": "b"}],
            "Scout und Wart",
        ),
    ],
)
def test_two_scout_invariants_fail_loudly(scouts, message):
    config = base_config()
    config["features"]["two_scouts"]["enabled"] = True
    config["scouts"] = scouts
    with pytest.raises(ValueError, match=message):
        configured_scouts(config)


def test_divergence_is_exact_and_auditable():
    a = {"findings": [
        {"pillar": "A", "topic": "Funding", "source": "https://a.example"},
        {"pillar": "B", "topic": "Trial", "source": "https://b.example"},
    ]}
    b = {"findings": [
        {"pillar": "a", "topic": " funding ", "source": "https://a.example"},
        {"pillar": "D", "topic": "Blind spot", "source": "https://d.example"},
    ]}
    result = scout_divergence([a, b])
    assert result["method"] == "exact_structured_finding_keys"
    assert result["overlap_percent"] == 33.3
    assert len(result["shared"]) == 1
    assert len(result["only_a"]) == 1
    assert len(result["only_b"]) == 1
