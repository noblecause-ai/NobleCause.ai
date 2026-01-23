"""Model Selector for dynamically selecting best/cheapest models from OpenRouter.

This module provides functionality to query OpenRouter's models API and select
the best or cheapest models from each provider for use in deliberations.
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import httpx

logger = logging.getLogger(__name__)

# Default fallback models if API fails
DEFAULT_MODELS = [
    {"id": "claude", "model": "anthropic/claude-3.5-sonnet", "name": "Claude"},
    {"id": "gpt4", "model": "openai/gpt-4o", "name": "GPT-4"},
    {"id": "gemini", "model": "google/gemini-2.5-pro", "name": "Gemini"},
]

# Cheapest models for testing (fallback if API fails)
DEFAULT_CHEAPEST_MODELS = [
    {"id": "claude", "model": "anthropic/claude-3-haiku", "name": "Claude Haiku"},
    {"id": "gpt4", "model": "openai/gpt-3.5-turbo", "name": "GPT-3.5 Turbo"},
    {"id": "gemini", "model": "google/gemini-flash", "name": "Gemini Flash"},
]


class ModelSelector:
    """Selects models from OpenRouter API based on criteria."""

    OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"

    def __init__(self, api_key: Optional[str] = None, cache_ttl: int = 86400):
        """Initialize the model selector.

        Args:
            api_key: Optional API key. If not provided, reads from OPENROUTER_API_KEY env var.
            cache_ttl: Cache TTL in seconds (default: 86400 = 24 hours).
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        self.cache_ttl = cache_ttl
        self._cache: Optional[Dict[str, Any]] = None
        self._cache_timestamp: Optional[datetime] = None

    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for API requests."""
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers

    async def _fetch_models(self) -> Optional[List[Dict[str, Any]]]:
        """Fetch models from OpenRouter API.

        Returns:
            List of model dictionaries, or None if fetch fails.
        """
        # Check cache first
        if self._cache and self._cache_timestamp:
            age = (datetime.utcnow() - self._cache_timestamp).total_seconds()
            if age < self.cache_ttl:
                logger.debug(f"Using cached models (age: {age:.0f}s)")
                return self._cache.get('models')

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.OPENROUTER_MODELS_URL,
                    headers=self._get_headers(),
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                models = data.get('data', [])

                # Update cache
                self._cache = {'models': models}
                self._cache_timestamp = datetime.utcnow()
                logger.info(f"Fetched {len(models)} models from OpenRouter API")
                return models

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching models: {e.response.status_code}")
            return None
        except httpx.TimeoutException:
            logger.error("Timeout fetching models from OpenRouter")
            return None
        except Exception as e:
            logger.error(f"Error fetching models: {type(e).__name__}: {e}")
            return None

    def _is_experimental(self, model_id: str) -> bool:
        """Check if model is experimental/preview.

        Args:
            model_id: Model identifier (e.g., "google/gemini-exp-1114").

        Returns:
            True if model appears to be experimental.
        """
        experimental_keywords = ['exp', 'experimental', 'preview', 'beta', 'test']
        model_lower = model_id.lower()
        return any(keyword in model_lower for keyword in experimental_keywords)

    def _score_model(self, model_data: Dict[str, Any], prefer_expensive: bool = True) -> float:
        """Score a model based on capabilities.

        Args:
            model_data: Model data from OpenRouter API.
            prefer_expensive: If True, prefer more expensive models (for production).
                             If False, prefer cheaper models (for testing).

        Returns:
            Score (higher = better).
        """
        model_id = model_data.get('id', '')
        context_length = model_data.get('context_length', 0)
        pricing = model_data.get('pricing', {})

        # Base score from context length (normalized)
        score = min(context_length / 1000000.0, 1.0) * 100

        # Pricing factor (convert strings to float)
        prompt_price_str = pricing.get('prompt', '0') or '0'
        completion_price_str = pricing.get('completion', '0') or '0'
        try:
            prompt_price = float(prompt_price_str)
            completion_price = float(completion_price_str)
        except (ValueError, TypeError):
            prompt_price = 0.0
            completion_price = 0.0
        avg_price = (prompt_price + completion_price) / 2

        if prefer_expensive:
            # Prefer more expensive models (often more capable)
            # Higher price = higher score (capped at 50 points)
            price_score = min(avg_price * 1000, 50)
        else:
            # Prefer cheaper models (for testing)
            # Lower price = higher score
            # Invert: cheaper models get higher scores (max when price = 0)
            price_score = max(50 - (avg_price * 10000), 0)  # Scale up multiplier for better differentiation

        score += price_score

        # Name pattern bonuses
        model_lower = model_id.lower()
        if 'pro' in model_lower or 'ultra' in model_lower:
            score += 10
        if 'sonnet' in model_lower or 'opus' in model_lower:
            score += 5

        # Penalty for experimental (unless explicitly enabled)
        if self._is_experimental(model_id):
            score -= 20

        return score

    def _filter_by_provider(
        self,
        models: List[Dict[str, Any]],
        provider: str
    ) -> List[Dict[str, Any]]:
        """Filter models by provider prefix.

        Args:
            models: List of model dictionaries.
            provider: Provider name (e.g., "anthropic", "openai", "google").

        Returns:
            Filtered list of models.
        """
        prefix = f"{provider}/"
        return [m for m in models if m.get('id', '').startswith(prefix)]

    async def select_best_models(
        self,
        providers: List[str] = ["anthropic", "openai", "google"],
        exclude_experimental: bool = True
    ) -> List[Dict[str, str]]:
        """Select best model from each provider.

        Args:
            providers: List of provider names to select from.
            exclude_experimental: Whether to exclude experimental models.

        Returns:
            List of agent model configurations.
        """
        # Check for environment override
        override = os.getenv('AGENT_MODELS_OVERRIDE')
        if override:
            try:
                models = json.loads(override)
                logger.info(f"Using model override from AGENT_MODELS_OVERRIDE: {len(models)} models")
                return models
            except json.JSONDecodeError as e:
                logger.warning(f"Invalid AGENT_MODELS_OVERRIDE JSON: {e}, using API selection")

        models = await self._fetch_models()
        if not models:
            logger.warning("Failed to fetch models, using defaults")
            return DEFAULT_MODELS

        selected = []
        for provider in providers:
            provider_models = self._filter_by_provider(models, provider)
            if not provider_models:
                logger.warning(f"No models found for provider: {provider}")
                continue

            # Filter experimental if requested
            if exclude_experimental:
                provider_models = [
                    m for m in provider_models
                    if not self._is_experimental(m.get('id', ''))
                ]

            if not provider_models:
                logger.warning(f"No non-experimental models found for provider: {provider}")
                continue

            # Score and select best
            scored = [
                (self._score_model(m, prefer_expensive=True), m)
                for m in provider_models
            ]
            scored.sort(reverse=True, key=lambda x: x[0])
            best_model = scored[0][1]

            # Convert to agent format
            model_id = best_model.get('id', '')
            agent_id = provider.lower()
            agent_name = best_model.get('name', model_id.split('/')[-1])

            selected.append({
                "id": agent_id,
                "model": model_id,
                "name": agent_name
            })

            logger.info(
                f"Selected {agent_name} ({model_id}) for {provider} "
                f"(score: {scored[0][0]:.1f})"
            )

        if not selected:
            logger.warning("No models selected, using defaults")
            return DEFAULT_MODELS

        return selected

    async def select_cheapest_models(
        self,
        providers: List[str] = ["anthropic", "openai", "google"]
    ) -> List[Dict[str, str]]:
        """Select cheapest available model from each provider.

        Used for live integration testing to minimize costs.

        Args:
            providers: List of provider names to select from.

        Returns:
            List of agent model configurations with cheapest models.
        """
        models = await self._fetch_models()
        if not models:
            logger.warning("Failed to fetch models, using default cheapest models")
            return DEFAULT_CHEAPEST_MODELS

        selected = []
        for provider in providers:
            provider_models = self._filter_by_provider(models, provider)
            if not provider_models:
                logger.warning(f"No models found for provider: {provider}")
                continue

            # Score for cheapest (prefer_expensive=False)
            scored = [
                (self._score_model(m, prefer_expensive=False), m)
                for m in provider_models
            ]
            scored.sort(reverse=True, key=lambda x: x[0])
            cheapest_model = scored[0][1]

            # Convert to agent format
            model_id = cheapest_model.get('id', '')
            agent_id = provider.lower()
            agent_name = cheapest_model.get('name', model_id.split('/')[-1])
            pricing = cheapest_model.get('pricing', {})
            prompt_price_str = pricing.get('prompt', '0') or '0'
            completion_price_str = pricing.get('completion', '0') or '0'
            try:
                prompt_price = float(prompt_price_str)
                completion_price = float(completion_price_str)
            except (ValueError, TypeError):
                prompt_price = 0.0
                completion_price = 0.0

            selected.append({
                "id": agent_id,
                "model": model_id,
                "name": agent_name
            })

            logger.info(
                f"Selected cheapest {agent_name} ({model_id}) for {provider} "
                f"(prompt: ${prompt_price:.6f}/1K, completion: ${completion_price:.6f}/1K)"
            )

        if not selected:
            logger.warning("No models selected, using default cheapest models")
            return DEFAULT_CHEAPEST_MODELS

        return selected
