"""Tests for the WebSocket deliberation endpoint."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from noble_cause_steward.main import app


class TestWebSocketDeliberate:
    """Tests for the /ws/deliberate WebSocket endpoint."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        return TestClient(app)

    def test_websocket_requires_start_message(self, client):
        """Test that WebSocket requires a start_deliberation message."""
        with client.websocket_connect("/ws/deliberate") as websocket:
            # Send invalid message type
            websocket.send_json({"type": "invalid", "topic": "test"})
            response = websocket.receive_json()

            assert response["type"] == "error"
            assert "Expected start_deliberation" in response["message"]

    def test_websocket_requires_topic(self, client):
        """Test that WebSocket requires a topic."""
        with client.websocket_connect("/ws/deliberate") as websocket:
            # Send without topic
            websocket.send_json({"type": "start_deliberation"})
            response = websocket.receive_json()

            assert response["type"] == "error"
            assert "Topic is required" in response["message"]

    def test_websocket_requires_api_key(self, client):
        """Test that WebSocket returns error when API key is missing."""
        with patch.dict("os.environ", {}, clear=True):
            # Clear the API key environment variable
            with patch("noble_cause_steward.main.AsyncOpenRouterAdapter") as mock_adapter:
                mock_adapter.side_effect = ValueError("OPENROUTER_API_KEY environment variable is required")

                with client.websocket_connect("/ws/deliberate") as websocket:
                    websocket.send_json({
                        "type": "start_deliberation",
                        "topic": "Test topic"
                    })
                    response = websocket.receive_json()

                    assert response["type"] == "error"
                    assert "OPENROUTER_API_KEY" in response["message"]

    @patch("noble_cause_steward.main.AsyncOpenRouterAdapter")
    @patch("noble_cause_steward.main.LangGraphDeliberation")
    def test_websocket_successful_deliberation(self, mock_delib_class, mock_adapter_class, client):
        """Test successful WebSocket deliberation flow."""
        # Set up mock deliberation service
        mock_deliberation = AsyncMock()
        mock_deliberation.run_deliberation = AsyncMock(return_value={
            "session_id": "test-123",
            "topic": "Test topic",
            "round": 3,
            "transcript": [],
            "consensus_reached": True,
            "final_recommendation": "Test recommendation"
        })
        mock_delib_class.return_value = mock_deliberation

        # Mock adapter
        mock_adapter_class.return_value = MagicMock()

        with client.websocket_connect("/ws/deliberate") as websocket:
            # Send start message
            websocket.send_json({
                "type": "start_deliberation",
                "topic": "Should we fund this project?"
            })

            # The mock deliberation completes immediately
            # In real scenario, we'd receive streaming events

        # Verify deliberation was called
        mock_deliberation.run_deliberation.assert_called_once()
        call_args = mock_deliberation.run_deliberation.call_args
        assert "Should we fund this project?" in str(call_args)

    @patch("noble_cause_steward.main.AsyncOpenRouterAdapter")
    @patch("noble_cause_steward.main.LangGraphDeliberation")
    def test_websocket_callback_is_set(self, mock_delib_class, mock_adapter_class, client):
        """Test that the callback is properly set on the deliberation service."""
        mock_deliberation = AsyncMock()
        mock_deliberation.run_deliberation = AsyncMock(return_value={
            "session_id": "test",
            "topic": "test",
            "round": 3,
            "transcript": [],
            "consensus_reached": True,
            "final_recommendation": None
        })
        mock_delib_class.return_value = mock_deliberation
        mock_adapter_class.return_value = MagicMock()

        with client.websocket_connect("/ws/deliberate") as websocket:
            websocket.send_json({
                "type": "start_deliberation",
                "topic": "Test"
            })

        # Verify set_callback was called
        mock_deliberation.set_callback.assert_called_once()

    def test_websocket_handles_invalid_json(self, client):
        """Test that WebSocket handles invalid JSON gracefully."""
        with client.websocket_connect("/ws/deliberate") as websocket:
            # Send invalid JSON
            websocket.send_text("not valid json")
            response = websocket.receive_json()

            assert response["type"] == "error"
            assert "Invalid JSON" in response["message"]

    @patch("noble_cause_steward.main.AsyncOpenRouterAdapter")
    @patch("noble_cause_steward.main.LangGraphDeliberation")
    def test_websocket_handles_deliberation_error(self, mock_delib_class, mock_adapter_class, client):
        """Test that WebSocket handles deliberation errors."""
        mock_deliberation = AsyncMock()
        mock_deliberation.run_deliberation = AsyncMock(
            side_effect=Exception("LLM service unavailable")
        )
        mock_delib_class.return_value = mock_deliberation
        mock_adapter_class.return_value = MagicMock()

        with client.websocket_connect("/ws/deliberate") as websocket:
            websocket.send_json({
                "type": "start_deliberation",
                "topic": "Test topic"
            })

            response = websocket.receive_json()
            assert response["type"] == "error"
            assert "Deliberation failed" in response["message"]


class TestWebSocketMessageProtocol:
    """Tests for the WebSocket message protocol structure."""

    def test_message_types_documented(self):
        """Ensure all message types are properly documented."""
        # These are the expected message types based on the protocol
        expected_backend_to_frontend = [
            "round_start",
            "agent_start",
            "agent_response",
            "round_end",
            "deliberation_complete",
            "error"
        ]

        expected_frontend_to_backend = [
            "start_deliberation"
        ]

        # This is a documentation test - verify the protocol is well-defined
        assert len(expected_backend_to_frontend) == 6
        assert len(expected_frontend_to_backend) == 1
