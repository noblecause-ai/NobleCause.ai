"""Tests for DeliberationService."""

import unittest
from unittest.mock import Mock, patch

from noble_cause_steward.deliberation.deliberation_service import DeliberationService
from noble_cause_steward.llm.open_router_adapter import OpenRouterAdapter


class TestDeliberationService(unittest.TestCase):
    """Test cases for DeliberationService."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_adapter = Mock(spec=OpenRouterAdapter)
        self.member_models = [
            "openai/gpt-4o",
            "google/gemini-pro", 
            "anthropic/claude-3-opus",
            "mistralai/mistral-large"
        ]

    def test_service_initialization(self):
        """Test that the DeliberationService can be initialized."""
        # This test will fail until the constructor is implemented
        service = DeliberationService(
            open_router_adapter=self.mock_adapter,
            member_models=self.member_models
        )
        
        # Assert that the service stores the adapter and member models
        self.assertEqual(service.open_router_adapter, self.mock_adapter)
        self.assertEqual(service.member_models, self.member_models)

    def test_run_deliberation_calls_llm_for_each_member(self):
        """Test that run_deliberation calls the LLM adapter for each member."""
        # Initialize service
        service = DeliberationService(
            open_router_adapter=self.mock_adapter,
            member_models=self.member_models
        )
        
        # Configure mock to return a response
        self.mock_adapter.generate_completion_with_system.return_value = "Test response"
        
        # Call run_deliberation
        topic = "Climate change solutions"
        initial_prompt = "What are the most effective approaches to combat climate change?"
        
        service.run_deliberation(topic, initial_prompt)
        
        # Assert that generate_completion_with_system was called exactly 4 times
        self.assertEqual(self.mock_adapter.generate_completion_with_system.call_count, 4)
        
        # Verify that each call used a different member model
        call_args_list = self.mock_adapter.generate_completion_with_system.call_args_list
        used_models = [call[1]['model'] for call in call_args_list]  # Extract model from kwargs
        self.assertEqual(set(used_models), set(self.member_models))

    def test_run_deliberation_assembles_transcript(self):
        """Test that run_deliberation returns a structured transcript."""
        # Initialize service
        service = DeliberationService(
            open_router_adapter=self.mock_adapter,
            member_models=self.member_models
        )
        
        # Configure mock to return distinct responses for each member
        responses = [
            "Response from GPT-4",
            "Response from Gemini",
            "Response from Claude",
            "Response from Mistral"
        ]
        self.mock_adapter.generate_completion_with_system.side_effect = responses
        
        # Call run_deliberation
        topic = "AI ethics"
        initial_prompt = "What ethical considerations should guide AI development?"
        
        result = service.run_deliberation(topic, initial_prompt)
        
        # Assert that the result is a structured transcript
        self.assertIsInstance(result, dict)
        self.assertIn('topic', result)
        self.assertIn('initial_prompt', result)
        self.assertIn('responses', result)
        
        # Assert that the transcript contains the topic and initial prompt
        self.assertEqual(result['topic'], topic)
        self.assertEqual(result['initial_prompt'], initial_prompt)
        
        # Assert that responses contains entries for all members
        self.assertEqual(len(result['responses']), 4)
        
        # Assert that each response contains the model and content
        for i, response_entry in enumerate(result['responses']):
            self.assertIn('model', response_entry)
            self.assertIn('content', response_entry)
            self.assertEqual(response_entry['model'], self.member_models[i])
            self.assertEqual(response_entry['content'], responses[i])


if __name__ == '__main__':
    unittest.main()