"""State schema for structured deliberation.

This module defines TypedDicts for the 3-round deliberation system:
Propose -> Critique -> Synthesize
"""

from typing import TypedDict, List, Optional
from datetime import datetime


class AgentResponse(TypedDict):
    """A single response from an agent during deliberation."""
    agent_id: str
    agent_name: str
    round: int
    round_name: str
    content: str
    timestamp: str


class DeliberationState(TypedDict):
    """State object for tracking deliberation progress."""
    session_id: str
    topic: str
    round: int
    transcript: List[AgentResponse]
    consensus_reached: bool
    final_recommendation: Optional[str]


# Round prompts for each phase of deliberation
ROUND_PROMPTS = {
    1: {
        "name": "Propose",
        "system_suffix": """

## Current Phase: PROPOSE (Round 1 of 3)

In this phase, you are presenting your initial analysis and recommendations on the topic.

Your task:
1. Analyze the topic from your unique perspective
2. Identify key considerations, opportunities, and risks
3. Propose specific actions or recommendations
4. Support your proposals with evidence-based reasoning

Be substantive and specific. Your proposals will be critiqued by other members in the next round.""",
        "user_prefix": "Please provide your initial analysis and proposals on the following topic:\n\n"
    },
    2: {
        "name": "Critique",
        "system_suffix": """

## Current Phase: CRITIQUE (Round 2 of 3)

In this phase, you are reviewing and critiquing the proposals from Round 1.

Your task:
1. Identify strengths and weaknesses in the proposals
2. Point out potential risks, blind spots, or unintended consequences
3. Challenge assumptions with evidence-based counterarguments
4. Suggest improvements or alternatives where appropriate

Be rigorous but constructive. Your critiques will inform the final synthesis.""",
        "user_prefix": "Based on the proposals from Round 1, please provide your critique:\n\n## Previous Proposals:\n"
    },
    3: {
        "name": "Synthesize",
        "system_suffix": """

## Current Phase: SYNTHESIZE (Round 3 of 3)

In this phase, you are synthesizing the proposals and critiques into a final recommendation.

Your task:
1. Identify areas of agreement and disagreement
2. Weigh the evidence and arguments presented
3. Formulate a coherent final recommendation
4. Acknowledge remaining uncertainties or areas for further investigation

Aim for a balanced synthesis that addresses the critiques raised.""",
        "user_prefix": "Based on the proposals and critiques from previous rounds, please provide your synthesis:\n\n## Deliberation Transcript:\n"
    }
}


def create_initial_state(session_id: str, topic: str) -> DeliberationState:
    """Create a new deliberation state.

    Args:
        session_id: Unique identifier for this deliberation session.
        topic: The topic being deliberated.

    Returns:
        A new DeliberationState initialized for Round 1.
    """
    return DeliberationState(
        session_id=session_id,
        topic=topic,
        round=1,
        transcript=[],
        consensus_reached=False,
        final_recommendation=None
    )


def format_transcript_for_prompt(transcript: List[AgentResponse], include_rounds: Optional[List[int]] = None) -> str:
    """Format the transcript for inclusion in a prompt.

    Args:
        transcript: List of agent responses.
        include_rounds: Optional list of round numbers to include. If None, includes all.

    Returns:
        Formatted string representation of the transcript.
    """
    if not transcript:
        return "(No previous responses)"

    lines = []
    for response in transcript:
        if include_rounds is None or response["round"] in include_rounds:
            lines.append(f"### {response['agent_name']} ({response['round_name']}):")
            lines.append(response["content"])
            lines.append("")

    return "\n".join(lines) if lines else "(No relevant responses)"
