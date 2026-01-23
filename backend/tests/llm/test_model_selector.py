"""Tests for the ModelSelector class."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import json
import os

from noble_cause_steward.llm.model_selector import (
    ModelSelector,
    DEFAULT_MODELS,
    DEFAULT_CHEAPEST_MODELS
)


class TestModelSelector:
    """Tests for ModelSelector."""

    @pytest.fixture
    def mock_models_response(self):
        """Mock OpenRouter models API response."""
        return {
            "data": [
                {
                    "id": "anthropic/claude-3.5-sonnet",
                    "name": "Claude 3.5 Sonnet",
                    "context_length": 200000,
                    "pricing": {"prompt": "0.003", "completion": "0.015"}
                },
                {
                    "id": "anthropic/claude-3-haiku",
                    "name": "Claude 3 Haiku",
                    "context_length": 200000,
                    "pricing": {"prompt": "0.00025", "completion": "0.00125"}
                },
                {
                    "id": "openai/gpt-4o",
                    "name": "GPT-4o",
                    "context_length": 128000,
                    "pricing": {"prompt": "0.0025", "completion": "0.01"}
                },
                {
                    "id": "openai/gpt-3.5-turbo",
                    "name": "GPT-3.5 Turbo",
                    "context_length": 16385,
                    "pricing": {"prompt": "0.0005", "completion": "0.0015"}
                },
                {
                    "id": "google/gemini-2.5-pro",
                    "name": "Gemini 2.5 Pro",
                    "context_length": 1000000,
                    "pricing": {"prompt": "0.00125", "completion": "0.01"}
                },
                {
                    "id": "google/gemini-flash",
                    "name": "Gemini Flash",
                    "context_length": 1000000,
                    "pricing": {"prompt": "0.000075", "completion": "0.0003"}
                },
                {
                    "id": "google/gemini-exp-1114",
                    "name": "Gemini Experimental",
                    "context_length": 40960,
                    "pricing": {"prompt": "0.001", "completion": "0.005"}
                }
            ]
        }

    @pytest.fixture
    def selector(self):
        """Create a ModelSelector instance."""
        return ModelSelector(api_key="test-key")

    @pytest.mark.asyncio
    async def test_select_best_models_success(self, selector, mock_models_response):
        """Test successful model selection."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_models_response
            mock_response.raise_for_status = MagicMock()
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )

            models = await selector.select_best_models()

            assert len(models) == 3
            model_ids = [m["model"] for m in models]
            assert "anthropic/claude-3.5-sonnet" in model_ids
            assert "openai/gpt-4o" in model_ids
            assert "google/gemini-2.5-pro" in model_ids

    @pytest.mark.asyncio
    async def test_select_cheapest_models_success(self, selector, mock_models_response):
        """Test cheapest model selection."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_models_response
            mock_response.raise_for_status = MagicMock()
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )

            models = await selector.select_cheapest_models()

            assert len(models) == 3
            model_ids = [m["model"] for m in models]
            assert "anthropic/claude-3-haiku" in model_ids
            assert "openai/gpt-3.5-turbo" in model_ids
            assert "google/gemini-flash" in model_ids

    @pytest.mark.asyncio
    async def test_select_best_models_excludes_experimental(self, selector, mock_models_response):
        """Test that experimental models are excluded by default."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_models_response
            mock_response.raise_for_status = MagicMock()
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )

            models = await selector.select_best_models(exclude_experimental=True)

            model_ids = [m["model"] for m in models]
            assert "google/gemini-exp-1114" not in model_ids

    @pytest.mark.asyncio
    async def test_select_best_models_api_failure_fallback(self, selector):
        """Test fallback to defaults when API fails."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                side_effect=Exception("API failure")
            )

            models = await selector.select_best_models()

            assert models == DEFAULT_MODELS

    @pytest.mark.asyncio
    async def test_select_cheapest_models_api_failure_fallback(self, selector):
        """Test fallback to cheapest defaults when API fails."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                side_effect=Exception("API failure")
            )

            models = await selector.select_cheapest_models()

            assert models == DEFAULT_CHEAPEST_MODELS

    @pytest.mark.asyncio
    async def test_environment_override(self, selector, mock_models_response):
        """Test that AGENT_MODELS_OVERRIDE environment variable works."""
        override_models = [
            {"id": "test-claude", "model": "anthropic/claude-3-haiku", "name": "Test Claude"},
            {"id": "test-gpt", "model": "openai/gpt-3.5-turbo", "name": "Test GPT"}
        ]

        with patch.dict(os.environ, {'AGENT_MODELS_OVERRIDE': json.dumps(override_models)}):
            models = await selector.select_best_models()

            assert models == override_models

    @pytest.mark.asyncio
    async def test_caching(self, selector, mock_models_response):
        """Test that models are cached."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_models_response
            mock_response.raise_for_status = MagicMock()
            mock_get = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__.return_value.get = mock_get

            # First call
            models1 = await selector.select_best_models()
            # Second call (should use cache)
            models2 = await selector.select_best_models()

            # Should only call API once
            assert mock_get.call_count == 1
            assert models1 == models2

    def test_is_experimental(self, selector):
        """Test experimental model detection."""
        assert selector._is_experimental("google/gemini-exp-1114") is True
        assert selector._is_experimental("google/gemini-pro") is False
        assert selector._is_experimental("anthropic/claude-3.5-sonnet") is False
        assert selector._is_experimental("openai/gpt-4-preview") is True

    def test_score_model(self, selector):
        """Test model scoring."""
        model_data = {
            "id": "anthropic/claude-3.5-sonnet",
            "context_length": 200000,
            "pricing": {"prompt": "0.003", "completion": "0.015"}
        }

        score_expensive = selector._score_model(model_data, prefer_expensive=True)
        score_cheap = selector._score_model(model_data, prefer_expensive=False)

        # Expensive preference should give higher score for this model
        assert score_expensive > score_cheap
