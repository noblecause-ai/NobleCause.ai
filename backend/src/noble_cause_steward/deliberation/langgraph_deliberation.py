"""LangGraph-based Deliberation Service.

This module provides a structured 3-round deliberation system using LangGraph
for state management and orchestration.
"""

import os
import uuid
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable, Awaitable
from langgraph.graph import StateGraph, END

from noble_cause_steward.deliberation.state import (
    DeliberationState,
    AgentResponse,
    ROUND_PROMPTS,
    create_initial_state,
    format_transcript_for_prompt
)
from noble_cause_steward.llm.async_open_router_adapter import AsyncOpenRouterAdapter
from noble_cause_steward.llm.model_selector import ModelSelector, DEFAULT_MODELS

logger = logging.getLogger(__name__)


# Agent configuration with friendly names (fallback if dynamic selection fails)
AGENT_MODELS = DEFAULT_MODELS


async def get_agent_models(use_cheapest: bool = False) -> List[Dict[str, str]]:
    """Get agent models, either dynamically selected or from defaults.

    Args:
        use_cheapest: If True, select cheapest models (for testing).
                     If False, select best models (for production).

    Returns:
        List of agent model configurations.
    """
    # Check for environment override first
    override = os.getenv('AGENT_MODELS_OVERRIDE')
    if override:
        try:
            import json
            models = json.loads(override)
            logger.info(f"Using model override from AGENT_MODELS_OVERRIDE: {len(models)} models")
            return models
        except json.JSONDecodeError as e:
            logger.warning(f"Invalid AGENT_MODELS_OVERRIDE JSON: {e}, using dynamic selection")

    # Try dynamic selection
    try:
        selector = ModelSelector()
        if use_cheapest:
            models = await selector.select_cheapest_models()
        else:
            models = await selector.select_best_models()
        logger.info(f"Selected {len(models)} models dynamically")
        return models
    except Exception as e:
        logger.warning(f"Dynamic model selection failed: {e}, using defaults")
        return AGENT_MODELS


# Callback type for state updates
StateCallback = Callable[[Dict[str, Any]], Awaitable[None]]


class LangGraphDeliberation:
    """Orchestrates multi-agent deliberation using LangGraph."""

    def __init__(
        self,
        llm_adapter: AsyncOpenRouterAdapter,
        agent_models: Optional[List[Dict[str, str]]] = None,
        gremium_prompt_path: Optional[str] = None,
        use_cheapest_models: bool = False
    ):
        """Initialize the LangGraph deliberation service.

        Args:
            llm_adapter: Async adapter for LLM API calls.
            agent_models: Optional list of agent configurations. 
                         If None, will use dynamic selection (best or cheapest).
            gremium_prompt_path: Optional path to the gremium prompt file.
            use_cheapest_models: If True and agent_models is None, use cheapest models.
        """
        self.llm_adapter = llm_adapter
        # If agent_models provided, use them; otherwise will be set async
        self.agent_models = agent_models
        self.use_cheapest_models = use_cheapest_models
        self.callback: Optional[StateCallback] = None

        # Load the base system prompt
        if gremium_prompt_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.join(current_dir, "..", "..", "..", "..")
            gremium_prompt_path = os.path.join(project_root, "prompts", "gremium_prompt.md")

        try:
            with open(gremium_prompt_path, 'r', encoding='utf-8') as f:
                self.base_system_prompt = f.read()
        except FileNotFoundError:
            logger.warning(f"Gremium prompt not found at {gremium_prompt_path}, using default")
            self.base_system_prompt = "You are a member of an AI deliberation council."

        # Note: agent_models will be set in run_deliberation if not provided
        # Build the LangGraph workflow
        self.graph = self._build_graph()

    def set_callback(self, callback: StateCallback):
        """Set the callback for state updates.

        Args:
            callback: Async function to call with state updates.
        """
        self.callback = callback

    async def _emit(self, event_type: str, data: Dict[str, Any]):
        """Emit an event through the callback if set.

        Args:
            event_type: Type of event (e.g., 'round_start', 'agent_response').
            data: Event data to send.
        """
        if self.callback:
            await self.callback({"type": event_type, **data})

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph state machine for deliberation.

        Returns:
            Compiled StateGraph ready for execution.
        """
        # Define the graph with DeliberationState
        workflow = StateGraph(DeliberationState)

        # Add nodes for each round
        workflow.add_node("propose", self._propose_node)
        workflow.add_node("critique", self._critique_node)
        workflow.add_node("synthesize", self._synthesize_node)
        workflow.add_node("finalize", self._finalize_node)

        # Define edges
        workflow.set_entry_point("propose")
        workflow.add_edge("propose", "critique")
        workflow.add_edge("critique", "synthesize")
        workflow.add_edge("synthesize", "finalize")
        workflow.add_edge("finalize", END)

        return workflow.compile()

    async def _execute_round(self, state: DeliberationState, round_num: int) -> DeliberationState:
        """Execute a single round of deliberation with all agents.

        Args:
            state: Current deliberation state.
            round_num: The round number (1, 2, or 3).

        Returns:
            Updated state with new responses.
        """
        round_config = ROUND_PROMPTS[round_num]
        round_name = round_config["name"]

        # Emit round start event
        await self._emit("round_start", {
            "round": round_num,
            "round_name": round_name
        })

        # Build the system prompt for this round
        system_prompt = self.base_system_prompt + round_config["system_suffix"]

        # Build the user prompt based on round
        if round_num == 1:
            user_prompt = round_config["user_prefix"] + state["topic"]
        elif round_num == 2:
            # Include only Round 1 responses
            transcript_text = format_transcript_for_prompt(state["transcript"], include_rounds=[1])
            user_prompt = round_config["user_prefix"] + transcript_text + f"\n\n## Topic: {state['topic']}"
        else:
            # Include all previous responses
            transcript_text = format_transcript_for_prompt(state["transcript"])
            user_prompt = round_config["user_prefix"] + transcript_text + f"\n\n## Topic: {state['topic']}"

        # Collect responses from all agents
        new_responses = []

        for agent in self.agent_models:
            agent_id = agent["id"]
            agent_name = agent["name"]
            model = agent["model"]

            # Emit agent start event
            await self._emit("agent_start", {
                "agent_id": agent_id,
                "agent_name": agent_name,
                "round": round_num,
                "round_name": round_name
            })

            logger.info(f"Round {round_num} ({round_name}): Getting response from {agent_name}")

            try:
                content = await self.llm_adapter.generate_completion_with_system(
                    system_message=system_prompt,
                    user_message=user_prompt,
                    model=model
                )

                if content is None:
                    content = f"[Error: Failed to get response from {agent_name}]"
                    logger.error(f"Failed to get response from {agent_name} in round {round_num}")

            except Exception as e:
                content = f"[Error: {type(e).__name__}: {str(e)}]"
                logger.error(f"Exception getting response from {agent_name}: {e}")

            response = AgentResponse(
                agent_id=agent_id,
                agent_name=agent_name,
                round=round_num,
                round_name=round_name,
                content=content,
                timestamp=datetime.utcnow().isoformat()
            )

            new_responses.append(response)

            # Emit agent response event
            await self._emit("agent_response", dict(response))

        # Emit round end event
        await self._emit("round_end", {"round": round_num})

        # Update state with new responses
        return DeliberationState(
            session_id=state["session_id"],
            topic=state["topic"],
            round=round_num,
            transcript=state["transcript"] + new_responses,
            consensus_reached=state["consensus_reached"],
            final_recommendation=state["final_recommendation"]
        )

    async def _propose_node(self, state: DeliberationState) -> DeliberationState:
        """Execute Round 1: Propose."""
        return await self._execute_round(state, 1)

    async def _critique_node(self, state: DeliberationState) -> DeliberationState:
        """Execute Round 2: Critique."""
        return await self._execute_round(state, 2)

    async def _synthesize_node(self, state: DeliberationState) -> DeliberationState:
        """Execute Round 3: Synthesize."""
        return await self._execute_round(state, 3)

    async def _finalize_node(self, state: DeliberationState) -> DeliberationState:
        """Finalize the deliberation by generating a consensus summary.

        This node analyzes all synthesis responses and determines if consensus
        was reached, then generates a final recommendation.
        """
        # Get synthesis responses
        synthesis_responses = [
            r for r in state["transcript"]
            if r["round"] == 3
        ]

        # Simple consensus check: all agents provided valid responses
        consensus_reached = all(
            not r["content"].startswith("[Error:")
            for r in synthesis_responses
        )

        # Generate final recommendation by combining synthesis responses
        if synthesis_responses:
            final_parts = []
            for r in synthesis_responses:
                if not r["content"].startswith("[Error:"):
                    final_parts.append(f"**{r['agent_name']}**: {r['content'][:500]}...")

            final_recommendation = "\n\n".join(final_parts) if final_parts else None
        else:
            final_recommendation = None

        # Emit deliberation complete event
        await self._emit("deliberation_complete", {
            "session_id": state["session_id"],
            "consensus_reached": consensus_reached,
            "final_recommendation": final_recommendation
        })

        return DeliberationState(
            session_id=state["session_id"],
            topic=state["topic"],
            round=3,
            transcript=state["transcript"],
            consensus_reached=consensus_reached,
            final_recommendation=final_recommendation
        )

    async def run_deliberation(self, topic: str, session_id: Optional[str] = None) -> DeliberationState:
        """Run a complete 3-round deliberation on the given topic.

        Args:
            topic: The topic to deliberate on.
            session_id: Optional session ID. Generated if not provided.

        Returns:
            Final deliberation state with all responses and recommendations.
        """
        if session_id is None:
            session_id = str(uuid.uuid4())

        # Set agent models if not already set (dynamic selection)
        if self.agent_models is None:
            self.agent_models = await get_agent_models(use_cheapest=self.use_cheapest_models)
            logger.info(f"Using {len(self.agent_models)} agents: {[a['name'] for a in self.agent_models]}")

        logger.info(f"Starting deliberation {session_id} on topic: {topic[:50]}...")

        # Create initial state
        initial_state = create_initial_state(session_id, topic)

        # Run the graph
        final_state = await self.graph.ainvoke(initial_state)

        logger.info(f"Deliberation {session_id} complete. Consensus: {final_state['consensus_reached']}")

        return final_state
