"""Rollen- und Besetzungsvertrag für künftige Läufe."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _config():
    return json.loads((ROOT / "config.json").read_text())


def test_scout_and_wart_are_distinct_offices():
    config = _config()
    assert config["scout"]["model"] == "claude-opus-5"
    assert config["wart"]["model"] == "claude-fable-5"
    assert config["scout"]["model"] != config["wart"]["model"]


def test_council_has_one_strongest_production_model_per_family():
    config = _config()
    assert config["model_policy"] == {
        "council": "strongest_production_model_per_family",
        "preview_models_allowed": False,
    }
    by_family = {spec["family"]: spec["model"] for spec in config["models"]}
    assert by_family == {
        "anthropic": "claude-fable-5",
        "openai": "gpt-5.6-sol",
        "google": "gemini-3.7-flash",
    }
    assert len(by_family) == len(config["models"])
    assert config["scout"]["model"] not in by_family.values()
