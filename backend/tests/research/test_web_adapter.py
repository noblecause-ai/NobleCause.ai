"""Tests for WebAdapter utility."""

import pytest
from unittest.mock import Mock, patch
import httpx

from noble_cause_steward.research.web_adapter import WebAdapter


class TestWebAdapter:
    """Test cases for WebAdapter utility."""

    def setup_method(self):
        """Set up test fixtures."""
        self.web_adapter = WebAdapter()

    @patch('noble_cause_steward.research.web_adapter.httpx.get')
    def test_fetch_successful_page(self, mock_get):
        """Test successful page fetch returns correct HTML content."""
        # Arrange
        expected_html = "<html><body><h1>Test Page</h1></body></html>"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = expected_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        test_url = "https://example.com/test-page"
        
        # Act
        result = self.web_adapter.fetch(test_url)
        
        # Assert
        assert result == expected_html
        mock_get.assert_called_once_with(test_url, timeout=30)
        mock_response.raise_for_status.assert_called_once()

    @patch('noble_cause_steward.research.web_adapter.httpx.get')
    def test_fetch_handles_not_found_error(self, mock_get):
        """Test that 404 HTTP error is handled gracefully."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404 Not Found",
            request=Mock(),
            response=mock_response
        )
        mock_get.return_value = mock_response
        
        test_url = "https://example.com/nonexistent-page"
        
        # Act
        result = self.web_adapter.fetch(test_url)
        
        # Assert
        assert result is None
        mock_get.assert_called_once_with(test_url, timeout=30)

    @patch('noble_cause_steward.research.web_adapter.httpx.get')
    def test_fetch_handles_connection_error(self, mock_get):
        """Test that network connection error is handled gracefully."""
        # Arrange
        mock_get.side_effect = httpx.ConnectError("Connection failed")
        
        test_url = "https://unreachable-site.com"
        
        # Act
        result = self.web_adapter.fetch(test_url)
        
        # Assert
        assert result is None
        mock_get.assert_called_once_with(test_url, timeout=30)

    @patch('noble_cause_steward.research.web_adapter.httpx.get')
    def test_fetch_handles_timeout_error(self, mock_get):
        """Test that timeout error is handled gracefully."""
        # Arrange
        mock_get.side_effect = httpx.TimeoutException("Request timed out")
        
        test_url = "https://slow-site.com"
        
        # Act
        result = self.web_adapter.fetch(test_url)
        
        # Assert
        assert result is None
        mock_get.assert_called_once_with(test_url, timeout=30)

    @patch('noble_cause_steward.research.web_adapter.httpx.get')
    def test_fetch_with_custom_timeout(self, mock_get):
        """Test fetch with custom timeout parameter."""
        # Arrange
        expected_html = "<html><body>Custom timeout test</body></html>"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = expected_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        test_url = "https://example.com"
        custom_timeout = 60
        
        # Act
        result = self.web_adapter.fetch(test_url, timeout=custom_timeout)
        
        # Assert
        assert result == expected_html
        mock_get.assert_called_once_with(test_url, timeout=custom_timeout)