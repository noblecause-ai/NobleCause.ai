"""Repository for persisting deliberation data to the database."""

import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc

from noble_cause_steward.database.sql_models import Deliberation, DeliberationResponse
from noble_cause_steward.deliberation.state import DeliberationState

logger = logging.getLogger(__name__)


class DeliberationRepository:
    """Repository for deliberation CRUD operations."""

    def __init__(self, db_session: Session):
        """Initialize the repository with a database session.

        Args:
            db_session: SQLAlchemy session for database operations.
        """
        self.db = db_session

    def save_deliberation(
        self,
        state: DeliberationState,
        agent_models: Optional[List[Dict[str, str]]] = None
    ) -> Deliberation:
        """Save a complete deliberation to the database.

        Args:
            state: The final deliberation state.
            agent_models: Optional list of agent model configurations.

        Returns:
            The created Deliberation model instance.
        """
        # Create the deliberation record
        deliberation = Deliberation(
            session_id=state["session_id"],
            topic=state["topic"],
            started_at=datetime.utcnow(),  # Will be overwritten if we track actual start
            completed_at=datetime.utcnow(),
            consensus_reached=state["consensus_reached"],
            final_recommendation=state["final_recommendation"],
            agent_models=agent_models
        )

        self.db.add(deliberation)
        self.db.flush()  # Get the ID assigned

        # Create response records
        for response in state["transcript"]:
            db_response = DeliberationResponse(
                deliberation_id=deliberation.id,
                agent_id=response["agent_id"],
                agent_name=response["agent_name"],
                round=response["round"],
                round_name=response["round_name"],
                content=response["content"],
                timestamp=datetime.fromisoformat(response["timestamp"].replace("Z", "+00:00"))
            )
            self.db.add(db_response)

        self.db.commit()
        logger.info(f"Saved deliberation {state['session_id']} with {len(state['transcript'])} responses")

        return deliberation

    def get_deliberation_by_session_id(self, session_id: str) -> Optional[Deliberation]:
        """Retrieve a deliberation by its session ID.

        Args:
            session_id: The unique session identifier.

        Returns:
            The Deliberation model instance, or None if not found.
        """
        return self.db.query(Deliberation).filter(
            Deliberation.session_id == session_id
        ).first()

    def get_deliberation_with_responses(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a deliberation with all its responses.

        Args:
            session_id: The unique session identifier.

        Returns:
            Dictionary representation with responses, or None if not found.
        """
        deliberation = self.get_deliberation_by_session_id(session_id)
        if deliberation:
            return deliberation.to_dict(include_responses=True)
        return None

    def list_deliberations(
        self,
        limit: int = 20,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """List deliberations with pagination, most recent first.

        Args:
            limit: Maximum number of deliberations to return.
            offset: Number of deliberations to skip.

        Returns:
            List of deliberation dictionaries (without responses).
        """
        deliberations = self.db.query(Deliberation).order_by(
            desc(Deliberation.completed_at)
        ).limit(limit).offset(offset).all()

        return [d.to_dict(include_responses=False) for d in deliberations]

    def count_deliberations(self) -> int:
        """Count total number of deliberations.

        Returns:
            Total count of deliberation records.
        """
        return self.db.query(Deliberation).count()

    def delete_deliberation(self, session_id: str) -> bool:
        """Delete a deliberation and all its responses.

        Args:
            session_id: The unique session identifier.

        Returns:
            True if deleted, False if not found.
        """
        deliberation = self.get_deliberation_by_session_id(session_id)
        if deliberation:
            self.db.delete(deliberation)
            self.db.commit()
            logger.info(f"Deleted deliberation {session_id}")
            return True
        return False
