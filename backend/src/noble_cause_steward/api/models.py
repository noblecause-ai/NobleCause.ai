"""Pydantic models for Noble Cause Steward API."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class MemoryIn(BaseModel):
    """Input model for creating a new memory."""
    text: str


class MemoryQueryIn(BaseModel):
    """Input model for querying memories."""
    query_text: str
    n_results: Optional[int] = 4


class MemoryOut(BaseModel):
    """Output model for memory query results."""
    text: str
    metadata: Dict[str, Any]
    distance: float


class MemoryCreateResponse(BaseModel):
    """Response model for memory creation."""
    id: str


class MemoryQueryResponse(BaseModel):
    """Response model for memory queries."""
    results: List[MemoryOut]