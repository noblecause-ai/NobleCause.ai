"""Tests for main FastAPI application."""

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient


class TestMainApplication:
    """Test class for main FastAPI application endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI application."""
        # This will fail until main.py and the FastAPI app are created
        from noble_cause_steward.main import app
        return TestClient(app)
    
    def test_health_check_returns_ok(self, client):
        """Test that the health check endpoint returns status ok."""
        # Make GET request to health endpoint
        response = client.get("/health")
        
        # Assert response status code is 200
        assert response.status_code == 200
        
        # Assert response JSON is {"status": "ok"}
        assert response.json() == {"status": "ok"}
    
    @patch('noble_cause_steward.main.memory_provider')
    def test_add_memory_endpoint(self, mock_memory_provider, client):
        """Test that the add memory endpoint calls the provider correctly."""
        # Mock the memory provider's add_memory method
        mock_memory_provider.add_memory.return_value = "test-memory-id"
        
        # Prepare test payload
        payload = {"text": "This is a test memory"}
        
        # Make POST request to memories endpoint
        response = client.post("/memories", json=payload)
        
        # Assert response status code is 201
        assert response.status_code == 201
        
        # Assert the memory provider's add_memory method was called with correct text
        mock_memory_provider.add_memory.assert_called_once_with("This is a test memory")
        
        # Assert response contains the memory ID
        assert response.json() == {"id": "test-memory-id"}
    
    @patch('noble_cause_steward.main.memory_provider')
    def test_query_memory_endpoint(self, mock_memory_provider, client):
        """Test that the query memory endpoint calls the provider correctly."""
        # Mock the memory provider's query_memories method with ChromaDB format
        mock_results = [
            {
                "document": "Found memory 1",
                "metadata": {"source": "test"},
                "distance": 0.1,
                "id": "test-id-1"
            },
            {
                "document": "Found memory 2",
                "metadata": {"source": "test"},
                "distance": 0.2,
                "id": "test-id-2"
            }
        ]
        mock_memory_provider.query_memories.return_value = mock_results
        
        # Prepare test payload
        payload = {"query_text": "test query", "n_results": 2}
        
        # Make POST request to memories/query endpoint
        response = client.post("/memories/query", json=payload)
        
        # Assert response status code is 200
        assert response.status_code == 200
        
        # Assert the memory provider's query_memories method was called correctly
        mock_memory_provider.query_memories.assert_called_once_with("test query", 2)
        
        # Assert response matches expected format (converted to API format)
        expected_response = {
            "results": [
                {
                    "text": "Found memory 1",
                    "metadata": {"source": "test"},
                    "distance": 0.1
                },
                {
                    "text": "Found memory 2",
                    "metadata": {"source": "test"},
                    "distance": 0.2
                }
            ]
        }
        assert response.json() == expected_response
    
    @patch('noble_cause_steward.main.memory_provider')
    def test_query_memory_endpoint_default_n_results(self, mock_memory_provider, client):
        """Test that the query memory endpoint uses default n_results when not provided."""
        # Mock the memory provider's query_memories method
        mock_results = []
        mock_memory_provider.query_memories.return_value = mock_results
        
        # Prepare test payload without n_results
        payload = {"query_text": "test query"}
        
        # Make POST request to memories/query endpoint
        response = client.post("/memories/query", json=payload)
        
        # Assert response status code is 200
        assert response.status_code == 200
        
        # Assert the memory provider's query_memories method was called with default n_results=4
        mock_memory_provider.query_memories.assert_called_once_with("test query", 4)
    
    def test_get_steward_status(self, client):
        """Test that the steward status endpoint returns the expected status using mocked ResearchManager."""
        # Create a mock ResearchManager instance
        mock_research_manager = Mock()
        
        # Set up the mock to return the expected status
        mock_research_manager.get_current_status.return_value = {
            "status": "researching",
            "inner_monologue": "Analyzing data from GiveWell..."
        }
        
        # Override the dependency in the FastAPI app
        from noble_cause_steward.main import app, get_research_manager
        app.dependency_overrides[get_research_manager] = lambda: mock_research_manager
        
        # Make GET request to steward status endpoint
        response = client.get("/api/steward/status")
        
        # Assert response status code is 200
        assert response.status_code == 200
        
        # Assert response JSON matches expected structure from mocked data
        expected_response = {
            "status": "researching",
            "inner_monologue": "Analyzing data from GiveWell..."
        }
        assert response.json() == expected_response
        
        # Verify that get_current_status was called
        mock_research_manager.get_current_status.assert_called_once()
        
        # Clean up dependency overrides
        app.dependency_overrides.clear()
    
    def test_deliberate_endpoint_streams_events(self, client):
        """Test that the deliberate endpoint streams SSE events correctly."""
        # Prepare test payload
        payload = {"topic": "Test Topic"}
        
        # Make POST request to deliberate endpoint
        response = client.post("/api/deliberate", json=payload)
        
        # Assert response status code is 200
        assert response.status_code == 200
        
        # Assert response Content-Type header is correct for SSE
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
        
        # Iterate through streaming response content and validate SSE format
        lines = list(response.iter_lines())
        
        # Assert that we received some lines
        assert len(lines) > 0
        
        # Assert that lines are formatted as valid SSE messages (start with "data:")
        for line in lines:
            if line.strip():  # Skip empty lines
                # Decode bytes to string for comparison
                line_str = line.decode('utf-8') if isinstance(line, bytes) else line
                assert line_str.startswith("data:"), f"Line should start with 'data:' but got: {line_str}"