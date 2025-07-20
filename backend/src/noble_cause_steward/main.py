"""Main FastAPI application for Noble Cause Steward."""

from fastapi import FastAPI, HTTPException
from noble_cause_steward.api.models import (
    MemoryIn,
    MemoryQueryIn,
    MemoryCreateResponse,
    MemoryQueryResponse,
    MemoryOut
)
from noble_cause_steward.memory.chroma_provider import ChromaMemoryProvider

# Create FastAPI application instance
app = FastAPI()

# Initialize memory provider
memory_provider = ChromaMemoryProvider()


@app.get("/health")
def health_check():
    """Health check endpoint that returns the application status."""
    return {"status": "ok"}


@app.post("/memories", response_model=MemoryCreateResponse, status_code=201)
def add_memory(memory_data: MemoryIn):
    """Add a new memory to the collection."""
    try:
        memory_id = memory_provider.add_memory(memory_data.text)
        return MemoryCreateResponse(id=memory_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add memory: {str(e)}")


@app.post("/memories/query", response_model=MemoryQueryResponse)
def query_memories(query_data: MemoryQueryIn):
    """Query memories based on semantic similarity."""
    try:
        results = memory_provider.query_memories(
            query_data.query_text,
            query_data.n_results
        )
        
        # Convert results to MemoryOut format
        formatted_results = []
        for result in results:
            formatted_results.append(MemoryOut(
                text=result["document"],
                metadata=result["metadata"],
                distance=result["distance"]
            ))
        
        return MemoryQueryResponse(results=formatted_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query memories: {str(e)}")