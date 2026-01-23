"""Tests for the LangGraph-based deliberation service."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from noble_cause_steward.deliberation.state import (
    DeliberationState,
    AgentResponse,
    ROUND_PROMPTS,
    create_initial_state,
    format_transcript_for_prompt
)
from noble_cause_steward.deliberation.langgraph_deliberation import (
    LangGraphDeliberation,
    AGENT_MODELS
)


class TestDeliberationState:
    """Tests for the state schema and utilities."""

    def test_create_initial_state(self):
        """Test creating a new deliberation state."""
        state = create_initial_state("test-session-123", "Should we fund malaria nets?")

        assert state["session_id"] == "test-session-123"
        assert state["topic"] == "Should we fund malaria nets?"
        assert state["round"] == 1
        assert state["transcript"] == []
        assert state["consensus_reached"] is False
        assert state["final_recommendation"] is None

    def test_round_prompts_structure(self):
        """Test that round prompts are properly defined."""
        assert 1 in ROUND_PROMPTS
        assert 2 in ROUND_PROMPTS
        assert 3 in ROUND_PROMPTS

        for round_num, config in ROUND_PROMPTS.items():
            assert "name" in config
            assert "system_suffix" in config
            assert "user_prefix" in config

        assert ROUND_PROMPTS[1]["name"] == "Propose"
        assert ROUND_PROMPTS[2]["name"] == "Critique"
        assert ROUND_PROMPTS[3]["name"] == "Synthesize"

    def test_format_transcript_empty(self):
        """Test formatting an empty transcript."""
        result = format_transcript_for_prompt([])
        assert result == "(No previous responses)"

    def test_format_transcript_with_responses(self):
        """Test formatting a transcript with responses."""
        responses = [
            AgentResponse(
                agent_id="claude",
                agent_name="Claude",
                round=1,
                round_name="Propose",
                content="This is my proposal.",
                timestamp="2024-01-01T00:00:00"
            ),
            AgentResponse(
                agent_id="gpt4",
                agent_name="GPT-4",
                round=1,
                round_name="Propose",
                content="Here is my analysis.",
                timestamp="2024-01-01T00:01:00"
            )
        ]

        result = format_transcript_for_prompt(responses)

        assert "### Claude (Propose):" in result
        assert "This is my proposal." in result
        assert "### GPT-4 (Propose):" in result
        assert "Here is my analysis." in result

    def test_format_transcript_filter_rounds(self):
        """Test formatting with round filtering."""
        responses = [
            AgentResponse(
                agent_id="claude",
                agent_name="Claude",
                round=1,
                round_name="Propose",
                content="Round 1 content",
                timestamp="2024-01-01T00:00:00"
            ),
            AgentResponse(
                agent_id="claude",
                agent_name="Claude",
                round=2,
                round_name="Critique",
                content="Round 2 content",
                timestamp="2024-01-01T00:01:00"
            )
        ]

        result = format_transcript_for_prompt(responses, include_rounds=[1])

        assert "Round 1 content" in result
        assert "Round 2 content" not in result


class TestLangGraphDeliberation:
    """Tests for the LangGraph deliberation service."""

    @pytest.fixture
    def mock_llm_adapter(self):
        """Create a mock LLM adapter."""
        adapter = AsyncMock()
        adapter.generate_completion_with_system = AsyncMock(
            return_value="This is a mock response from the AI."
        )
        return adapter

    @pytest.fixture
    def deliberation_service(self, mock_llm_adapter):
        """Create a deliberation service with mock dependencies."""
        # Use a simple test prompt instead of loading from file
        with patch("builtins.open", MagicMock(return_value=MagicMock(
            __enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value="Test system prompt"))),
            __exit__=MagicMock(return_value=False)
        ))):
            service = LangGraphDeliberation(
                llm_adapter=mock_llm_adapter,
                agent_models=[
                    {"id": "test-agent", "model": "test/model", "name": "TestAgent"}
                ]
            )
        return service

    def test_initialization(self, deliberation_service):
        """Test service initialization."""
        assert deliberation_service.llm_adapter is not None
        assert deliberation_service.agent_models is not None
        assert len(deliberation_service.agent_models) == 1
        assert deliberation_service.agent_models[0]["name"] == "TestAgent"

    def test_default_agent_models(self):
        """Test that default agent models are properly configured."""
        assert len(AGENT_MODELS) == 3

        agent_names = [a["name"] for a in AGENT_MODELS]
        assert "Claude" in agent_names
        assert "GPT-4" in agent_names
        assert "Gemini" in agent_names

    @pytest.mark.asyncio
    async def test_execute_round(self, deliberation_service, mock_llm_adapter):
        """Test executing a single round."""
        state = create_initial_state("test-123", "Test topic")

        # Execute round 1
        new_state = await deliberation_service._execute_round(state, 1)

        # Verify LLM was called
        mock_llm_adapter.generate_completion_with_system.assert_called()

        # Verify state was updated
        assert len(new_state["transcript"]) == 1
        assert new_state["transcript"][0]["round"] == 1
        assert new_state["transcript"][0]["round_name"] == "Propose"

    @pytest.mark.asyncio
    async def test_callback_events(self, deliberation_service, mock_llm_adapter):
        """Test that callback events are emitted correctly."""
        events = []

        async def capture_callback(event):
            events.append(event)

        deliberation_service.set_callback(capture_callback)

        state = create_initial_state("test-123", "Test topic")
        await deliberation_service._execute_round(state, 1)

        # Check events
        event_types = [e["type"] for e in events]
        assert "round_start" in event_types
        assert "agent_start" in event_types
        assert "agent_response" in event_types
        assert "round_end" in event_types

    @pytest.mark.asyncio
    async def test_full_deliberation_flow(self, deliberation_service, mock_llm_adapter):
        """Test running a complete deliberation."""
        # Capture events
        events = []

        async def capture_callback(event):
            events.append(event)

        deliberation_service.set_callback(capture_callback)

        # Run deliberation
        final_state = await deliberation_service.run_deliberation(
            topic="Should we invest in AI safety research?",
            session_id="test-deliberation-001"
        )

        # Verify final state
        assert final_state["session_id"] == "test-deliberation-001"
        assert final_state["topic"] == "Should we invest in AI safety research?"

        # Should have 3 responses (1 per round, 1 agent)
        assert len(final_state["transcript"]) == 3

        # Verify rounds
        rounds = [r["round"] for r in final_state["transcript"]]
        assert rounds == [1, 2, 3]

        # Check for deliberation_complete event
        complete_events = [e for e in events if e["type"] == "deliberation_complete"]
        assert len(complete_events) == 1
        assert complete_events[0]["session_id"] == "test-deliberation-001"

    @pytest.mark.asyncio
    async def test_handles_llm_errors_gracefully(self, mock_llm_adapter):
        """Test that LLM errors are handled gracefully."""
        # Set up mock to return None (simulating error)
        mock_llm_adapter.generate_completion_with_system = AsyncMock(return_value=None)

        with patch("builtins.open", MagicMock(return_value=MagicMock(
            __enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value="Test prompt"))),
            __exit__=MagicMock(return_value=False)
        ))):
            service = LangGraphDeliberation(
                llm_adapter=mock_llm_adapter,
                agent_models=[{"id": "test", "model": "test/model", "name": "Test"}]
            )

        state = create_initial_state("test", "topic")
        new_state = await service._execute_round(state, 1)

        # Should have an error message in the response
        assert len(new_state["transcript"]) == 1
        assert "[Error:" in new_state["transcript"][0]["content"]

    @pytest.mark.asyncio
    async def test_session_id_generation(self, deliberation_service):
        """Test that session ID is generated if not provided."""
        final_state = await deliberation_service.run_deliberation(
            topic="Test topic"
            # No session_id provided
        )

        assert final_state["session_id"] is not None
        assert len(final_state["session_id"]) > 0

    @pytest.mark.asyncio
    async def test_finalize_node_consensus(self, deliberation_service, mock_llm_adapter):
        """Test that finalize node correctly determines consensus."""
        # Create state with synthesis responses
        state = DeliberationState(
            session_id="test",
            topic="Test",
            round=3,
            transcript=[
                AgentResponse(
                    agent_id="test",
                    agent_name="Test",
                    round=3,
                    round_name="Synthesize",
                    content="Valid synthesis response",
                    timestamp="2024-01-01T00:00:00"
                )
            ],
            consensus_reached=False,
            final_recommendation=None
        )

        final_state = await deliberation_service._finalize_node(state)

        assert final_state["consensus_reached"] is True
        assert final_state["final_recommendation"] is not None
