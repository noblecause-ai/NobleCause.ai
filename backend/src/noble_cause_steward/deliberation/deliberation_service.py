"""DeliberationService for managing multi-agent conversations.

This module provides the DeliberationService class that orchestrates
conversations between multiple AI agents in the Gremium.
"""

import os
from typing import List, Dict, Any
from noble_cause_steward.llm.open_router_adapter import OpenRouterAdapter


class DeliberationService:
    """Service for managing multi-agent deliberations."""
    
    def __init__(self, open_router_adapter: OpenRouterAdapter, member_models: List[str]):
        """Initialize the DeliberationService.
        
        Args:
            open_router_adapter: The LLM adapter for making API calls.
            member_models: List of model identifiers for Gremium members.
        """
        self.open_router_adapter = open_router_adapter
        self.member_models = member_models
    
    def run_deliberation(self, topic: str, initial_prompt: str) -> Dict[str, Any]:
        """Run a deliberation session with all Gremium members.
        
        Args:
            topic: The topic for deliberation.
            initial_prompt: The initial prompt to start the conversation.
            
        Returns:
            A structured transcript object containing responses from all members.
        """
        # Load the Gremium system prompt
        # Get the path relative to the project root (go up from backend/src/noble_cause_steward/deliberation)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(current_dir, "..", "..", "..", "..")
        prompt_path = os.path.join(project_root, "prompts", "gremium_prompt.md")
        with open(prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = f.read()
        
        # Initialize responses list
        responses = []
        
        # Loop through each member model and get their response
        for model in self.member_models:
            response = self.open_router_adapter.generate_completion_with_system(
                system_prompt=system_prompt,
                user_prompt=initial_prompt,
                model=model
            )
            
            responses.append({
                "model": model,
                "content": response
            })
        
        # Assemble and return the final transcript
        return {
            "topic": topic,
            "initial_prompt": initial_prompt,
            "responses": responses
        }