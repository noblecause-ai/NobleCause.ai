"""Tests for the ResearchManager class."""

import pytest
from unittest.mock import Mock

from noble_cause_steward.research.research_manager import ResearchManager
from noble_cause_steward.research.constants import PRIMARY_RESEARCH_VENUES
from noble_cause_steward.llm.open_router_adapter import OpenRouterAdapter


class TestResearchManager:
    """Test cases for ResearchManager initialization and venue loading."""

    def test_research_manager_initialization(self):
        """Test that ResearchManager can be initialized with a mock WebAdapter."""
        # Arrange
        mock_web_adapter = Mock()
        
        # Act
        research_manager = ResearchManager(web_adapter=mock_web_adapter)
        
        # Assert
        assert research_manager is not None
        assert hasattr(research_manager, 'web_adapter')
        assert research_manager.web_adapter == mock_web_adapter

    def test_research_manager_loads_venues(self):
        """Test that ResearchManager correctly loads PRIMARY_RESEARCH_VENUES."""
        # Arrange
        mock_web_adapter = Mock()
        
        # Act
        research_manager = ResearchManager(web_adapter=mock_web_adapter)
        
        # Assert
        assert hasattr(research_manager, 'research_venues')
        assert research_manager.research_venues == PRIMARY_RESEARCH_VENUES
        assert isinstance(research_manager.research_venues, dict)
        assert len(research_manager.research_venues) > 0
        
        # Verify specific categories exist
        expected_categories = [
            "Dedicated Charity Evaluators",
            "Effective Altruism & Rationalist Hubs", 
            "Academic & Scientific Databases",
            "Major Philanthropic Foundations"
        ]
        for category in expected_categories:
            assert category in research_manager.research_venues
            assert isinstance(research_manager.research_venues[category], list)
            assert len(research_manager.research_venues[category]) > 0

    def test_scan_venues_calls_web_adapter_for_each_venue(self):
        """Test that scan_venues calls web_adapter.fetch() for each venue URL."""
        # Arrange
        mock_web_adapter = Mock()
        research_manager = ResearchManager(web_adapter=mock_web_adapter)
        
        # Calculate expected number of calls based on PRIMARY_RESEARCH_VENUES
        expected_call_count = sum(len(venues) for venues in PRIMARY_RESEARCH_VENUES.values())
        
        # Act
        research_manager.scan_venues()
        
        # Assert
        assert mock_web_adapter.fetch.call_count == expected_call_count
        
        # Verify that fetch was called with each URL from PRIMARY_RESEARCH_VENUES
        called_urls = [call[0][0] for call in mock_web_adapter.fetch.call_args_list]
        expected_urls = []
        for category_venues in PRIMARY_RESEARCH_VENUES.values():
            expected_urls.extend(category_venues)
        
        assert set(called_urls) == set(expected_urls)

    def test_scan_venues_handles_fetch_failures_gracefully(self):
        """Test that scan_venues handles fetch failures gracefully and returns successful content."""
        # Arrange
        mock_web_adapter = Mock()
        research_manager = ResearchManager(web_adapter=mock_web_adapter)
        
        # Configure mock to return mix of successful content and None for failures
        def mock_fetch_side_effect(url):
            if "givewell" in url or "80000hours" in url:
                return f"Content from {url}"
            return None  # Simulate fetch failure
        
        mock_web_adapter.fetch.side_effect = mock_fetch_side_effect
        
        # Act
        result = research_manager.scan_venues()
        
        # Assert
        # Method should complete without crashing
        assert result is not None
        
        # Should return content from successful fetches only
        successful_content = [content for content in result if content is not None]
        assert len(successful_content) == 2  # Only givewell and 80000hours should succeed
        
        # Verify content contains expected URLs
        assert any("givewell" in content for content in successful_content)
        assert any("80000hours" in content for content in successful_content)
        
        # Verify all URLs were still attempted
        expected_call_count = sum(len(venues) for venues in PRIMARY_RESEARCH_VENUES.values())
        assert mock_web_adapter.fetch.call_count == expected_call_count

    def test_extract_theory_of_change_successful(self):
        """Test that extract_theory_of_change successfully extracts Theory of Change from text."""
        # Arrange
        mock_web_adapter = Mock()
        mock_open_router_adapter = Mock()
        
        # Configure the mocked LLM to return a well-formed Theory of Change
        expected_theory_of_change = """
        Theory of Change:
        1. If we provide clean water access to rural communities
        2. Then health outcomes will improve and children can attend school regularly
        3. Leading to better educational outcomes and economic opportunities
        4. Ultimately resulting in poverty reduction and community development
        """
        mock_open_router_adapter.generate_completion.return_value = expected_theory_of_change
        
        research_manager = ResearchManager(
            web_adapter=mock_web_adapter,
            open_router_adapter=mock_open_router_adapter
        )
        
        input_text = """
        Our organization focuses on providing clean water solutions to underserved communities.
        We believe that access to clean water is fundamental to breaking the cycle of poverty.
        By installing water purification systems in rural villages, we aim to improve health
        outcomes, reduce waterborne diseases, and enable children to attend school instead
        of walking hours to fetch water.
        """
        
        # Act
        result = research_manager.extract_theory_of_change(input_text)
        
        # Assert
        # Verify the LLM was called with appropriate prompt
        mock_open_router_adapter.generate_completion.assert_called_once()
        call_args = mock_open_router_adapter.generate_completion.call_args[0][0]
        
        # Check that the prompt contains instructions for Theory of Change extraction
        assert "theory of change" in call_args.lower()
        assert "extract" in call_args.lower() or "identify" in call_args.lower()
        assert input_text in call_args
        
        # Verify the method returns the LLM response
        assert result == expected_theory_of_change

    def test_extract_theory_of_change_handles_llm_failure(self):
        """Test that extract_theory_of_change handles LLM failure gracefully."""
        # Arrange
        mock_web_adapter = Mock()
        mock_open_router_adapter = Mock()
        
        # Configure the mocked LLM to return None (simulating API failure)
        mock_open_router_adapter.generate_completion.return_value = None
        
        research_manager = ResearchManager(
            web_adapter=mock_web_adapter,
            open_router_adapter=mock_open_router_adapter
        )
        
        input_text = "Some project description text"
        
        # Act
        result = research_manager.extract_theory_of_change(input_text)
        
        # Assert
        # Verify the LLM was called
        mock_open_router_adapter.generate_completion.assert_called_once()
        
        # Verify the method handles failure gracefully by returning None
        assert result is None

    def test_seek_counterarguments_constructs_correct_search_queries(self):
        """Test that seek_counterarguments constructs correct search queries for critiques and risks."""
        # Arrange
        mock_web_adapter = Mock()
        mock_llm_adapter = Mock()
        research_manager = ResearchManager(
            web_adapter=mock_web_adapter,
            open_router_adapter=mock_llm_adapter
        )
        
        project_name = "Test Project"
        theory_of_change = "Test Theory"
        
        # Act
        research_manager.seek_counterarguments(
            project_name=project_name,
            theory_of_change=theory_of_change
        )
        
        # Assert
        # Verify that web_adapter.fetch was called with search URLs
        assert mock_web_adapter.fetch.call_count >= 2  # At least 2 search queries
        
        # Get all the URLs that were called
        called_urls = [call[0][0] for call in mock_web_adapter.fetch.call_args_list]
        
        # Verify that the URLs look like Google search queries
        google_search_urls = [url for url in called_urls if "google.com/search?q=" in url]
        assert len(google_search_urls) >= 2
        
        # Verify that search queries include expected patterns
        all_queries = " ".join(called_urls)
        assert "Test Project criticism" in all_queries
        assert "Test Theory risks" in all_queries

    def test_seek_counterarguments_summarizes_findings_with_llm(self):
        """Test that seek_counterarguments summarizes findings using LLM."""
        # Arrange
        mock_web_adapter = Mock()
        mock_llm_adapter = Mock()
        
        # Configure mock web adapter to return sample HTML content
        sample_html_content = """
        <html>
        <body>
        <div class="search-result">
        <h3>Criticism of Test Project</h3>
        <p>Some experts argue that Test Project may have unintended consequences...</p>
        </div>
        <div class="search-result">
        <h3>Risks in Test Theory</h3>
        <p>Research shows potential risks including resource allocation issues...</p>
        </div>
        </body>
        </html>
        """
        mock_web_adapter.fetch.return_value = sample_html_content
        
        # Configure mock LLM to return a summary
        expected_summary = """
        Summary of Critiques and Risks:
        1. Potential unintended consequences in project implementation
        2. Resource allocation concerns identified by experts
        3. Need for better risk mitigation strategies
        """
        mock_llm_adapter.generate_completion.return_value = expected_summary
        
        research_manager = ResearchManager(
            web_adapter=mock_web_adapter,
            open_router_adapter=mock_llm_adapter
        )
        
        project_name = "Test Project"
        theory_of_change = "Test Theory"
        
        # Act
        result = research_manager.seek_counterarguments(
            project_name=project_name,
            theory_of_change=theory_of_change
        )
        
        # Assert
        # Verify that generate_completion was called
        mock_llm_adapter.generate_completion.assert_called_once()
        
        # Verify that the prompt asks for summarizing critiques
        call_args = mock_llm_adapter.generate_completion.call_args[0][0]
        assert "summarize" in call_args.lower() or "summary" in call_args.lower()
        assert "critique" in call_args.lower() or "criticism" in call_args.lower()
        assert sample_html_content in call_args
        
        # Verify that the method returns the LLM summary
        assert result == expected_summary

    def test_conduct_research_cycle_full_workflow(self):
        """Test the complete research cycle workflow integration."""
        # Arrange
        mock_web_adapter = Mock()
        mock_llm_adapter = Mock()
        
        research_manager = ResearchManager(
            web_adapter=mock_web_adapter,
            open_router_adapter=mock_llm_adapter
        )
        
        # Mock return values for each step of the process
        sample_venue_html = [
            "<html><body><h1>GiveWell Research</h1><p>Effective charity analysis...</p></body></html>",
            "<html><body><h1>80000 Hours</h1><p>Career impact research...</p></body></html>",
            "<html><body><h1>Open Philanthropy</h1><p>Grant making insights...</p></body></html>"
        ]
        
        sample_theory_of_change = """
        Theory of Change for Clean Water Initiative:
        1. If we install water purification systems in rural communities
        2. Then waterborne diseases will decrease by 80%
        3. Leading to improved health outcomes and school attendance
        4. Ultimately resulting in economic development and poverty reduction
        """
        
        sample_counterarguments = """
        Summary of Critiques and Risks:
        1. High maintenance costs for water systems in remote areas
        2. Potential dependency on external technical support
        3. Risk of equipment failure without local repair capabilities
        4. Questions about long-term sustainability of interventions
        """
        
        expected_final_brief = """
        RESEARCH BRIEF: Clean Water Initiative
        
        THEORY OF CHANGE:
        Theory of Change for Clean Water Initiative:
        1. If we install water purification systems in rural communities
        2. Then waterborne diseases will decrease by 80%
        3. Leading to improved health outcomes and school attendance
        4. Ultimately resulting in economic development and poverty reduction
        
        COUNTERARGUMENTS & RISKS:
        Summary of Critiques and Risks:
        1. High maintenance costs for water systems in remote areas
        2. Potential dependency on external technical support
        3. Risk of equipment failure without local repair capabilities
        4. Questions about long-term sustainability of interventions
        
        RECOMMENDATION:
        Based on the analysis, this initiative shows promise but requires careful
        consideration of sustainability and maintenance challenges.
        """
        
        # Configure mocks to return sample data in sequence
        def mock_scan_venues():
            return sample_venue_html
        
        def mock_extract_theory_of_change(text):
            return sample_theory_of_change
        
        def mock_seek_counterarguments(project_name, theory_of_change):
            return sample_counterarguments
        
        # Mock the individual methods
        research_manager.scan_venues = Mock(side_effect=mock_scan_venues)
        research_manager.extract_theory_of_change = Mock(side_effect=mock_extract_theory_of_change)
        research_manager.seek_counterarguments = Mock(side_effect=mock_seek_counterarguments)
        
        # Configure LLM to return final synthesized brief
        mock_llm_adapter.generate_completion.return_value = expected_final_brief
        
        topic = "Clean Water Initiative"
        
        # Act
        result = research_manager.conduct_research_cycle(topic)
        
        # Assert
        # Verify that each step of the research cycle was called
        research_manager.scan_venues.assert_called_once()
        research_manager.extract_theory_of_change.assert_called_once()
        research_manager.seek_counterarguments.assert_called_once_with(topic, sample_theory_of_change)
        
        # Verify that the LLM was called for final synthesis
        mock_llm_adapter.generate_completion.assert_called_once()
        
        # Verify that the synthesis prompt contains all necessary components
        synthesis_call_args = mock_llm_adapter.generate_completion.call_args[0][0]
        assert "synthesize" in synthesis_call_args.lower() or "synthesis" in synthesis_call_args.lower()
        assert "research brief" in synthesis_call_args.lower()
        assert sample_theory_of_change in synthesis_call_args
        assert sample_counterarguments in synthesis_call_args
        assert topic in synthesis_call_args
        
        # Verify that the method returns the final synthesized brief
        assert result == expected_final_brief
        
        # Verify the extract_theory_of_change was called with venue content
        extract_call_args = research_manager.extract_theory_of_change.call_args[0][0]
        # Should contain concatenated venue HTML content
        assert any(html_content in extract_call_args for html_content in sample_venue_html)