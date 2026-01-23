"""ChromaDB Memory Provider for Noble Cause Steward."""

import uuid
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings


class ChromaMemoryProvider:
    """ChromaDB-based memory provider for storing and retrieving memories."""
    
    def __init__(self, collection_name: str = "memories"):
        """
        Initialize the ChromaDB memory provider.
        
        Args:
            collection_name: Name of the ChromaDB collection to use
        """
        self.collection_name = collection_name
        self.client = chromadb.Client()
        
        # Get or create the collection with cosine similarity
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_memory(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a memory (text document) to the collection.
        
        Args:
            text: The text content to store
            metadata: Optional metadata associated with the memory
            
        Returns:
            str: The unique ID of the stored memory
        """
        if metadata is None:
            metadata = {}
            
        # Generate a unique ID for this memory
        memory_id = str(uuid.uuid4())
        
        # Add the document to the collection
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[memory_id]
        )
        
        return memory_id
    
    def query_memories(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Query the collection for relevant memories based on semantic similarity.
        
        Args:
            query_text: The text to search for
            n_results: Maximum number of results to return
            
        Returns:
            List of dictionaries containing document, metadata, id, and distance
        """
        # Query the collection
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        # Format the results into a list of dictionaries
        formatted_results = []
        
        # ChromaDB returns results in nested lists, so we need to flatten them
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        ids = results.get("ids", [[]])[0]
        distances = results.get("distances", [[]])[0]
        
        for i in range(len(documents)):
            formatted_results.append({
                "document": documents[i],
                "metadata": metadatas[i] if i < len(metadatas) else {},
                "id": ids[i] if i < len(ids) else "",
                "distance": distances[i] if i < len(distances) else 0.0
            })
        
        return formatted_results