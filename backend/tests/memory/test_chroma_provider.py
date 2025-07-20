import pytest
from unittest.mock import Mock, patch, MagicMock
import chromadb
from chromadb.config import Settings
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Import the class we're testing
from noble_cause_steward.memory.chroma_provider import ChromaMemoryProvider


class TestChromaMemoryProvider:
    """Test cases for ChromaDB Memory Service."""
    
    @pytest.fixture
    def mock_chroma_client(self):
        """Create a mock ChromaDB client for testing."""
        mock_client = Mock()
        mock_collection = Mock()
        mock_client.create_collection.return_value = mock_collection
        mock_client.get_collection.return_value = mock_collection
        return mock_client
    
    @pytest.fixture
    def chroma_provider(self, mock_chroma_client):
        """Create a ChromaMemoryProvider instance with mocked client."""
        with patch('chromadb.Client', return_value=mock_chroma_client):
            provider = ChromaMemoryProvider(collection_name="test_collection")
        return provider
    
    def test_collection_creation(self, mock_chroma_client):
        """Test that a ChromaDB collection is successfully created."""
        # Arrange
        collection_name = "test_memories"
        expected_collection = Mock()
        mock_chroma_client.create_collection.return_value = expected_collection
        
        # Act & Assert
        with patch('chromadb.Client', return_value=mock_chroma_client):
            provider = ChromaMemoryProvider(collection_name=collection_name)
            
        # Assert that the collection was created with the correct name
        mock_chroma_client.create_collection.assert_called_once_with(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Assert that the provider has the collection reference
        assert provider.collection is not None
        assert provider.collection_name == collection_name
    
    def test_add_single_memory(self, chroma_provider, mock_chroma_client):
        """Test that a single text document is successfully added to a collection."""
        # Arrange
        test_text = "This is a test memory about artificial intelligence."
        test_metadata = {"source": "test", "timestamp": "2024-01-01T00:00:00Z"}
        
        # Get the mock collection from the client
        mock_collection = mock_chroma_client.create_collection.return_value
        
        # Act
        memory_id = chroma_provider.add_memory(
            text=test_text,
            metadata=test_metadata
        )
        
        # Assert
        assert memory_id is not None
        assert isinstance(memory_id, str)
        
        # Verify that the collection's add method was called with correct parameters
        mock_collection.add.assert_called_once()
        call_args = mock_collection.add.call_args
        
        # Check that documents, metadatas, and ids were provided
        assert "documents" in call_args.kwargs
        assert "metadatas" in call_args.kwargs
        assert "ids" in call_args.kwargs
        
        # Verify the content
        assert call_args.kwargs["documents"] == [test_text]
        assert call_args.kwargs["metadatas"] == [test_metadata]
        assert len(call_args.kwargs["ids"]) == 1
    
    def test_query_returns_relevant_memory(self, chroma_provider, mock_chroma_client):
        """Test that a query returns relevant documents based on semantic similarity."""
        # Arrange
        test_document = "Machine learning is a subset of artificial intelligence."
        test_metadata = {"source": "knowledge_base", "topic": "AI"}
        query_text = "What is machine learning?"
        
        # Mock the collection and its query response
        mock_collection = mock_chroma_client.create_collection.return_value
        mock_query_result = {
            "documents": [[test_document]],
            "metadatas": [[test_metadata]],
            "ids": [["memory_123"]],
            "distances": [[0.15]]  # Low distance indicates high similarity
        }
        mock_collection.query.return_value = mock_query_result
        
        # First add a memory to query against
        chroma_provider.add_memory(
            text=test_document,
            metadata=test_metadata
        )
        
        # Act - Query for relevant memories
        results = chroma_provider.query_memories(
            query_text=query_text,
            n_results=1
        )
        
        # Assert
        assert results is not None
        assert len(results) == 1
        
        # Verify the returned result contains the expected document
        result = results[0]
        assert result["document"] == test_document
        assert result["metadata"] == test_metadata
        assert result["id"] == "memory_123"
        assert "distance" in result
        assert result["distance"] == 0.15
        
        # Verify that the collection's query method was called correctly
        mock_collection.query.assert_called_once()
        query_call_args = mock_collection.query.call_args
        
        assert "query_texts" in query_call_args.kwargs
        assert query_call_args.kwargs["query_texts"] == [query_text]
        assert query_call_args.kwargs["n_results"] == 1