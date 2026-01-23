"""Main FastAPI application for Noble Cause Steward."""

from dotenv import load_dotenv
load_dotenv()

import asyncio
import json
import logging
from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from noble_cause_steward.api.models import (
    MemoryIn,
    MemoryQueryIn,
    MemoryCreateResponse,
    MemoryQueryResponse,
    MemoryOut,
    DeliberationRequest
)
from noble_cause_steward.memory.chroma_provider import ChromaMemoryProvider
from noble_cause_steward.research.research_manager import ResearchManager
from noble_cause_steward.research.web_adapter import WebAdapter
from noble_cause_steward.llm.open_router_adapter import OpenRouterAdapter
from noble_cause_steward.llm.async_open_router_adapter import AsyncOpenRouterAdapter
from noble_cause_steward.deliberation.deliberation_service import DeliberationService
from noble_cause_steward.deliberation.langgraph_deliberation import LangGraphDeliberation, AGENT_MODELS
from noble_cause_steward.deliberation.repository import DeliberationRepository
from noble_cause_steward.database.sql_models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

logger = logging.getLogger(__name__)

# Database setup (optional - only if DATABASE_URL is configured)
DATABASE_URL = os.getenv("DATABASE_URL")
db_engine = None
SessionLocal = None

if DATABASE_URL:
    try:
        db_engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
        # Create tables if they don't exist
        Base.metadata.create_all(bind=db_engine)
        logger.info("Database connection established")
    except Exception as e:
        logger.warning(f"Database connection failed: {e}. Persistence disabled.")

# Create FastAPI application instance
app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # SvelteKit dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize memory provider
memory_provider = ChromaMemoryProvider()

# Initialize research manager
def get_research_manager() -> ResearchManager:
    """Dependency to get ResearchManager instance."""
    web_adapter = WebAdapter()
    llm_adapter = OpenRouterAdapter()
    return ResearchManager(web_adapter, llm_adapter)


# Initialize deliberation service
def get_deliberation_service() -> DeliberationService:
    """Dependency to get DeliberationService instance."""
    llm_adapter = OpenRouterAdapter()
    # Default member models for the Gremium
    member_models = [
        "anthropic/claude-3.5-sonnet",
        "openai/gpt-4o",
        "google/gemini-pro-1.5"
    ]
    return DeliberationService(llm_adapter, member_models)


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


@app.get("/api/steward/status")
def get_steward_status(research_manager: ResearchManager = Depends(get_research_manager)):
    """Get the current status of the steward."""
    # Return live data from the research manager
    return research_manager.get_current_status()


@app.post("/api/deliberate")
async def deliberate(
    request: DeliberationRequest,
    deliberation_service: DeliberationService = Depends(get_deliberation_service)
):
    """Stream the results of a Gremium deliberation using Server-Sent Events.

    This endpoint is kept for backward compatibility. Consider using the
    WebSocket endpoint /ws/deliberate for better real-time experience.
    """

    async def event_generator():
        """Generate SSE events for the deliberation process."""
        try:
            # Run the deliberation in a thread pool to avoid blocking the event loop
            transcript = await asyncio.to_thread(
                deliberation_service.run_deliberation,
                request.topic,
                f"Please deliberate on the following topic: {request.topic}"
            )

            # Stream each response as an SSE event
            for response in transcript["responses"]:
                # Format as SSE message
                data = json.dumps(response)
                yield f"data: {data}\n\n"

                # Add a small delay to simulate the deliberation process
                await asyncio.sleep(1)

        except Exception as e:
            # Send error as SSE event
            error_data = json.dumps({"error": str(e)})
            yield f"data: {error_data}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.websocket("/ws/deliberate")
async def websocket_deliberate(websocket: WebSocket):
    """WebSocket endpoint for real-time 3-round deliberation.

    Protocol:
    - Frontend -> Backend: {"type": "start_deliberation", "topic": "..."}
    - Backend -> Frontend: {"type": "round_start", "round": 1|2|3, "round_name": "..."}
    - Backend -> Frontend: {"type": "agent_start", "agent_id": "...", "agent_name": "..."}
    - Backend -> Frontend: {"type": "agent_response", "agent_id": "...", "content": "...", ...}
    - Backend -> Frontend: {"type": "round_end", "round": 1|2|3}
    - Backend -> Frontend: {"type": "deliberation_complete", "session_id": "...", ...}
    - Backend -> Frontend: {"type": "error", "message": "..."}
    """
    await websocket.accept()
    logger.info("WebSocket connection accepted")

    try:
        # Wait for start message
        data = await websocket.receive_text()
        message = json.loads(data)

        if message.get("type") != "start_deliberation":
            await websocket.send_json({
                "type": "error",
                "message": "Expected start_deliberation message"
            })
            await websocket.close()
            return

        topic = message.get("topic")
        if not topic:
            await websocket.send_json({
                "type": "error",
                "message": "Topic is required"
            })
            await websocket.close()
            return

        logger.info(f"Starting WebSocket deliberation on topic: {topic[:50]}...")

        # Initialize the LangGraph deliberation service
        try:
            llm_adapter = AsyncOpenRouterAdapter()
        except ValueError as e:
            await websocket.send_json({
                "type": "error",
                "message": str(e)
            })
            await websocket.close()
            return

        # Use dynamic model selection (best models for production)
        # Models will be selected automatically on first deliberation
        deliberation = LangGraphDeliberation(llm_adapter, agent_models=None)

        # Set up callback to stream events to WebSocket
        async def send_event(event: dict):
            try:
                await websocket.send_json(event)
            except Exception as e:
                logger.error(f"Error sending WebSocket message: {e}")

        deliberation.set_callback(send_event)

        # Run the deliberation
        try:
            final_state = await deliberation.run_deliberation(topic)
            logger.info(f"Deliberation completed. Session: {final_state['session_id']}")

            # Save to database if configured
            if SessionLocal:
                try:
                    db = SessionLocal()
                    repo = DeliberationRepository(db)
                    repo.save_deliberation(final_state, AGENT_MODELS)
                    db.close()
                    logger.info(f"Saved deliberation {final_state['session_id']} to database")
                except Exception as db_error:
                    logger.error(f"Failed to save deliberation to database: {db_error}")

        except Exception as e:
            logger.error(f"Deliberation error: {e}")
            await websocket.send_json({
                "type": "error",
                "message": f"Deliberation failed: {str(e)}"
            })

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except json.JSONDecodeError:
        logger.error("Invalid JSON received")
        try:
            await websocket.send_json({
                "type": "error",
                "message": "Invalid JSON format"
            })
        except Exception:
            pass
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "message": f"Server error: {str(e)}"
            })
        except Exception:
            pass
    finally:
        try:
            await websocket.close()
        except Exception:
            pass


@app.get("/api/deliberations")
def list_deliberations(limit: int = 20, offset: int = 0):
    """List all deliberations with pagination.

    Args:
        limit: Maximum number of deliberations to return (default 20).
        offset: Number of deliberations to skip (default 0).

    Returns:
        List of deliberation summaries.
    """
    if not SessionLocal:
        raise HTTPException(
            status_code=503,
            detail="Database not configured. Set DATABASE_URL environment variable."
        )

    try:
        db = SessionLocal()
        repo = DeliberationRepository(db)
        deliberations = repo.list_deliberations(limit=limit, offset=offset)
        total = repo.count_deliberations()
        db.close()

        return {
            "deliberations": deliberations,
            "total": total,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list deliberations: {str(e)}")


@app.get("/api/deliberations/{session_id}")
def get_deliberation(session_id: str):
    """Get a single deliberation with all responses.

    Args:
        session_id: The unique session identifier.

    Returns:
        Complete deliberation with all responses.
    """
    if not SessionLocal:
        raise HTTPException(
            status_code=503,
            detail="Database not configured. Set DATABASE_URL environment variable."
        )

    try:
        db = SessionLocal()
        repo = DeliberationRepository(db)
        deliberation = repo.get_deliberation_with_responses(session_id)
        db.close()

        if not deliberation:
            raise HTTPException(status_code=404, detail="Deliberation not found")

        return deliberation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get deliberation: {str(e)}")