"""Tests for OpenRouterAdapter LLM Gateway."""

import unittest
from unittest.mock import patch, Mock
import httpx
import pytest

from noble_cause_steward.llm.open_router_adapter import OpenRouterAdapter


class TestOpenRouterAdapter(unittest.TestCase):
    """Test cases for OpenRouterAdapter."""

    @patch.dict('os.environ', {'OPENROUTER_API_KEY': 'test-api-key-12345'})
    def test_adapter_initializes_with_api_key(self):
        """Test that adapter correctly initializes with API key from environment."""
        adapter = OpenRouterAdapter()
        
        # Assert that the adapter correctly reads the API key
        self.assertEqual(adapter.api_key, 'test-api-key-12345')
        
        # Assert that authorization headers are properly constructed
        expected_headers = {
            'Authorization': 'Bearer test-api-key-12345',
            'Content-Type': 'application/json'
        }
        self.assertEqual(adapter.headers, expected_headers)

    @patch('httpx.post')
    def test_generate_completion_successful(self, mock_post):
        """Test successful completion generation from OpenRouter API."""
        # Configure mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'This is a test completion response.'
                    }
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Initialize adapter with test API key
        with patch.dict('os.environ', {'OPENROUTER_API_KEY': 'test-api-key'}):
            adapter = OpenRouterAdapter()
        
        # Call generate_completion method
        result = adapter.generate_completion(
            prompt="Test prompt",
            model="openai/gpt-3.5-turbo"
        )
        
        # Assert that the returned text matches the mocked response
        self.assertEqual(result, 'This is a test completion response.')
        
        # Verify that httpx.post was called with correct parameters
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertIn('https://openrouter.ai/api/v1/chat/completions', call_args[1]['url'])
        self.assertIn('Authorization', call_args[1]['headers'])

    @patch('httpx.post')
    def test_generate_completion_handles_api_error(self, mock_post):
        """Test that adapter handles API errors gracefully."""
        # Configure mock to raise HTTPStatusError
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        
        http_error = httpx.HTTPStatusError(
            message="500 Server Error",
            request=Mock(),
            response=mock_response
        )
        mock_post.side_effect = http_error
        
        # Initialize adapter with test API key
        with patch.dict('os.environ', {'OPENROUTER_API_KEY': 'test-api-key'}):
            adapter = OpenRouterAdapter()
        
        # Call generate_completion method and expect graceful error handling
        result = adapter.generate_completion(
            prompt="Test prompt",
            model="openai/gpt-3.5-turbo"
        )
        
        # Assert that the method handles the error gracefully
        # (returns None or raises a custom exception)
        self.assertIsNone(result)
        
        # Verify that httpx.post was called
        mock_post.assert_called_once()


if __name__ == '__main__':
    unittest.main()