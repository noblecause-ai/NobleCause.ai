import json
import sys
import types
from pathlib import Path


GREMIUM = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GREMIUM))

import google_scout  # noqa: E402


class _Usage:
    prompt_token_count = 12
    candidates_token_count = 7
    thoughts_token_count = 3


class _Response:
    usage_metadata = _Usage()
    text = "Dossier"

    def model_dump(self, mode="json"):
        assert mode == "json"
        return {
            "candidates": [
                {
                    "finish_reason": "STOP",
                    "grounding_metadata": {
                        "web_search_queries": ["alpha", "beta", "alpha", ""]
                    },
                }
            ]
        }


def test_google_scout_normalizes_grounding_metadata(tmp_path, monkeypatch):
    seen = {}

    class Client:
        class Models:
            def generate_content(self, **kwargs):
                seen.update(kwargs)
                return _Response()

        models = Models()

    fake_types = types.SimpleNamespace(
        GoogleSearch=lambda: "search",
        Tool=lambda **kwargs: kwargs,
        GenerateContentConfig=lambda **kwargs: kwargs,
    )
    monkeypatch.setitem(sys.modules, "google", types.SimpleNamespace(genai=types.SimpleNamespace(Client=Client)))
    monkeypatch.setitem(sys.modules, "google.genai", types.SimpleNamespace(types=fake_types))

    text, usage, raw, queries = google_scout.call_google_scout(
        {"model": "gemini-test", "max_output_tokens": 99},
        "system",
        "user",
        tmp_path,
        "raw.json",
    )

    assert text == "Dossier"
    assert usage == {"input_tokens": 12, "output_tokens": 10, "web_search_requests": 3}
    assert queries == ["alpha", "beta", "alpha"]
    assert raw["stop_reason"] == "end_turn"
    assert seen["model"] == "gemini-test"
    assert seen["config"]["tools"] == [{"google_search": "search"}]
    assert json.loads((tmp_path / "raw.json").read_text()) == raw


def test_google_safety_finish_is_a_visible_refusal():
    raw = {"candidates": [{"finish_reason": "SAFETY"}]}
    assert google_scout._stop_reason(raw) == "refusal"


def test_google_prompt_block_is_a_visible_refusal():
    raw = {"prompt_feedback": {"block_reason": "SAFETY"}}
    assert google_scout._stop_reason(raw) == "refusal"
