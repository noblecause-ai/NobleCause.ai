"""OpenRouter LLM Gateway Adapter.

This module provides the OpenRouterAdapter class for communicating with
the OpenRouter API to generate LLM completions.
"""

import os
from typing import Optional
import httpx


class OpenRouterAdapter:
    """Adapter for OpenRouter LLM API communication."""
    
    def __init__(self):
        """Initialize the OpenRouter adapter.
        
        Reads the OPENROUTER_API_KEY from environment variables and
        prepares authorization headers.
        
        Raises:
            ValueError: If OPENROUTER_API_KEY is not found in environment variables.
        """
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def generate_completion(self, prompt: str, model: str) -> Optional[str]:
        """Generate a completion using the OpenRouter API.
        
        Args:
            prompt: The input prompt for the LLM.
            model: The model identifier to use for completion.
            
        Returns:
            The generated completion text, or None if an error occurred.
        """
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            response = httpx.post(
                url=url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            response_data = response.json()
            return response_data['choices'][0]['message']['content']
            
        except httpx.HTTPStatusError:
            return None
        except Exception:
            return None
    
    def generate_completion_with_system(self, system_message: str, user_message: str, model: str) -> Optional[str]:
        """Generate a completion using the OpenRouter API with separate system and user messages.
        
        Args:
            system_message: The system prompt/context for the LLM.
            user_message: The user input prompt for the LLM.
            model: The model identifier to use for completion.
            
        Returns:
            The generated completion text, or None if an error occurred.
        """
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }
        
        try:
            response = httpx.post(
                url=url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            response_data = response.json()
            return response_data['choices'][0]['message']['content']
            
        except httpx.HTTPStatusError:
            return None
        except Exception:
            return None