"""Live integration tests for deliberation with real OpenRouter API.

These tests make real API calls to validate end-to-end integration.
They use the cheapest available models to minimize costs.

Run with: pytest tests/deliberation/test_live_deliberation.py -m live

WARNING: These tests incur real API costs (~$0.01-0.05 per run).
"""

import pytest
import os
from noble_cause_steward.llm.async_open_router_adapter import AsyncOpenRouterAdapter
from noble_cause_steward.deliberation.langgraph_deliberation import LangGraphDeliberation


@pytest.fixture
def require_api_key():
    """Ensure API key is available."""
    # Check multiple sources for API key
    api_key_env = os.getenv('OPENROUTER_API_KEY')
    api_key_dotenv = None
    
    # Try loading from .env file if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key_dotenv = os.getenv('OPENROUTER_API_KEY')
    except Exception:
        pass
    
    api_key = api_key_env or api_key_dotenv
    
    if not api_key:
        skip_reason = (
            "\n" + "="*70 + "\n"
            "SKIPPED: Live test requires OPENROUTER_API_KEY\n"
            "="*70 + "\n"
            f"Environment check: env={api_key_env is not None}, dotenv={api_key_dotenv is not None}\n"
            "\n"
            "To run live tests:\n"
            "  1. Set environment variable:\n"
            "     export OPENROUTER_API_KEY='your-key-here'\n"
            "\n"
            "  2. Or add to backend/.env file:\n"
            "     OPENROUTER_API_KEY=your-key-here\n"
            "\n"
            "  3. Then run:\n"
            "     poetry run pytest tests/deliberation/test_live_deliberation.py -m live -v\n"
            "="*70 + "\n"
        )
        pytest.skip(skip_reason)
    
    return api_key


@pytest.mark.asyncio
@pytest.mark.live
async def test_live_deliberation_with_cheapest_models(require_api_key):
    """Live test with cheapest models - validates real API integration.

    This test:
    1. Selects cheapest models from each provider
    2. Runs a single round of deliberation (not full 3-round)
    3. Validates that real API calls work end-to-end

    Cost estimate: ~$0.01-0.05 per run
    
    Run with: pytest tests/deliberation/test_live_deliberation.py -m live -v
    """
    # Create adapter
    llm_adapter = AsyncOpenRouterAdapter()

    # Create deliberation service with cheapest models
    deliberation = LangGraphDeliberation(
        llm_adapter=llm_adapter,
        agent_models=None,  # Will use dynamic selection
        use_cheapest_models=True  # Use cheapest models for testing
    )

    # Capture events
    events = []

    async def capture_event(event):
        events.append(event)

    deliberation.set_callback(capture_event)

    # Run a minimal deliberation (we'll manually execute one round)
    topic = "Should we test this system? (This is a test topic for live integration testing.)"

    # Create initial state
    from noble_cause_steward.deliberation.state import create_initial_state
    initial_state = create_initial_state("live-test-001", topic)

    # Ensure agent models are set (dynamic selection happens here)
    if deliberation.agent_models is None:
        from noble_cause_steward.deliberation.langgraph_deliberation import get_agent_models
        deliberation.agent_models = await get_agent_models(use_cheapest=True)

    # Execute only Round 1 (Propose) to minimize costs
    # This validates the API integration without running full deliberation
    try:
        state_after_round1 = await deliberation._execute_round(initial_state, 1)

        # Verify we got responses
        assert len(state_after_round1["transcript"]) > 0

        # Verify all agents responded (or at least attempted)
        assert len(state_after_round1["transcript"]) == len(deliberation.agent_models)

        # Verify events were emitted
        event_types = [e["type"] for e in events]
        assert "round_start" in event_types
        assert "agent_start" in event_types
        assert "agent_response" in event_types
        assert "round_end" in event_types

        # Log results for debugging
        print(f"\n=== Live Test Results ===")
        print(f"Topic: {topic}")
        print(f"Agents used: {[a['name'] for a in deliberation.agent_models]}")
        print(f"Responses received: {len(state_after_round1['transcript'])}")
        for response in state_after_round1["transcript"]:
            print(f"  - {response['agent_name']}: {len(response['content'])} chars")
            if response["content"].startswith("[Error:"):
                print(f"    ERROR: {response['content']}")

    except Exception as e:
        pytest.fail(f"Live deliberation failed: {type(e).__name__}: {e}")


@pytest.mark.asyncio
@pytest.mark.live
async def test_live_model_selection(require_api_key):
    """Test that model selection works with real API."""
    from noble_cause_steward.llm.model_selector import ModelSelector

    selector = ModelSelector()

    # Test best model selection
    best_models = await selector.select_best_models()
    assert len(best_models) >= 1
    assert all("model" in m for m in best_models)
    assert all("name" in m for m in best_models)

    print(f"\n=== Best Models Selected ===")
    for model in best_models:
        print(f"  - {model['name']}: {model['model']}")

    # Test cheapest model selection
    cheapest_models = await selector.select_cheapest_models()
    assert len(cheapest_models) >= 1
    assert all("model" in m for m in cheapest_models)

    print(f"\n=== Cheapest Models Selected ===")
    for model in cheapest_models:
        print(f"  - {model['name']}: {model['model']}")
