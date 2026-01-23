"""Async OpenRouter LLM Gateway Adapter.

This module provides async methods for communicating with the OpenRouter API,
including streaming support for real-time responses.
"""

import os
import logging
from typing import Optional, AsyncGenerator, List, Dict, Any
import httpx

logger = logging.getLogger(__name__)


class AsyncOpenRouterAdapter:
    """Async adapter for OpenRouter LLM API communication."""

    OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the async OpenRouter adapter.

        Args:
            api_key: Optional API key. If not provided, reads from OPENROUTER_API_KEY env var.

        Raises:
            ValueError: If no API key is provided or found in environment.
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")

        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    async def generate_completion(
        self,
        messages: List[Dict[str, str]],
        model: str,
        timeout: float = 60.0
    ) -> Optional[str]:
        """Generate a completion using the OpenRouter API.

        Args:
            messages: List of message dicts with 'role' and 'content' keys.
            model: The model identifier to use for completion.
            timeout: Request timeout in seconds.

        Returns:
            The generated completion text, or None if an error occurred.
        """
        payload = {
            "model": model,
            "messages": messages
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=self.OPENROUTER_API_URL,
                    headers=self.headers,
                    json=payload,
                    timeout=timeout
                )
                response.raise_for_status()

                response_data = response.json()
                content = response_data['choices'][0]['message']['content']
                logger.debug(f"Generated completion for model {model}: {len(content)} chars")
                return content

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from OpenRouter: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.TimeoutException:
            logger.error(f"Timeout waiting for response from model {model}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error generating completion: {type(e).__name__}: {e}")
            return None

    async def generate_completion_stream(
        self,
        messages: List[Dict[str, str]],
        model: str,
        timeout: float = 120.0
    ) -> AsyncGenerator[str, None]:
        """Generate a streaming completion using the OpenRouter API.

        Args:
            messages: List of message dicts with 'role' and 'content' keys.
            model: The model identifier to use for completion.
            timeout: Request timeout in seconds.

        Yields:
            Chunks of the generated completion text as they arrive.
        """
        payload = {
            "model": model,
            "messages": messages,
            "stream": True
        }

        try:
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    url=self.OPENROUTER_API_URL,
                    headers=self.headers,
                    json=payload,
                    timeout=timeout
                ) as response:
                    response.raise_for_status()

                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data = line[6:]
                            if data == "[DONE]":
                                break

                            try:
                                import json
                                chunk = json.loads(data)
                                delta = chunk.get("choices", [{}])[0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    yield content
                            except json.JSONDecodeError:
                                logger.warning(f"Failed to parse streaming chunk: {data}")
                                continue

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from OpenRouter stream: {e.response.status_code}")
            raise
        except httpx.TimeoutException:
            logger.error(f"Timeout waiting for streaming response from model {model}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in streaming completion: {type(e).__name__}: {e}")
            raise

    async def generate_completion_with_system(
        self,
        system_message: str,
        user_message: str,
        model: str,
        timeout: float = 60.0
    ) -> Optional[str]:
        """Generate a completion with separate system and user messages.

        Args:
            system_message: The system prompt/context for the LLM.
            user_message: The user input prompt for the LLM.
            model: The model identifier to use for completion.
            timeout: Request timeout in seconds.

        Returns:
            The generated completion text, or None if an error occurred.
        """
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        return await self.generate_completion(messages, model, timeout)

    async def generate_completion_with_system_stream(
        self,
        system_message: str,
        user_message: str,
        model: str,
        timeout: float = 120.0
    ) -> AsyncGenerator[str, None]:
        """Generate a streaming completion with separate system and user messages.

        Args:
            system_message: The system prompt/context for the LLM.
            user_message: The user input prompt for the LLM.
            model: The model identifier to use for completion.
            timeout: Request timeout in seconds.

        Yields:
            Chunks of the generated completion text as they arrive.
        """
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        async for chunk in self.generate_completion_stream(messages, model, timeout):
            yield chunk
