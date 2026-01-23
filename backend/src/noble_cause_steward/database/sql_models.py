"""SQLAlchemy models for Noble Cause Steward database."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Recommendation(Base):
    """SQLAlchemy model for storing recommendations."""
    
    __tablename__ = 'recommendations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=False)
    pillar = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Recommendation(id={self.id}, title='{self.title}', pillar='{self.pillar}')>"
    
    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'pillar': self.pillar,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Deliberation(Base):
    """SQLAlchemy model for storing deliberation sessions."""

    __tablename__ = 'deliberations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(36), unique=True, nullable=False, index=True)
    topic = Column(Text, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    consensus_reached = Column(Boolean, default=False, nullable=False)
    final_recommendation = Column(Text, nullable=True)
    agent_models = Column(JSON, nullable=True)  # Store list of agent model configs

    # Relationship to responses
    responses = relationship("DeliberationResponse", back_populates="deliberation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Deliberation(session_id='{self.session_id}', topic='{self.topic[:50]}...')>"

    def to_dict(self, include_responses: bool = False):
        """Convert the model instance to a dictionary.

        Args:
            include_responses: If True, include all response objects.
        """
        data = {
            'id': self.id,
            'session_id': self.session_id,
            'topic': self.topic,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'consensus_reached': self.consensus_reached,
            'final_recommendation': self.final_recommendation,
            'agent_models': self.agent_models
        }
        if include_responses:
            data['responses'] = [r.to_dict() for r in self.responses]
        return data


class DeliberationResponse(Base):
    """SQLAlchemy model for storing individual agent responses in a deliberation."""

    __tablename__ = 'deliberation_responses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    deliberation_id = Column(Integer, ForeignKey('deliberations.id'), nullable=False, index=True)
    agent_id = Column(String(50), nullable=False)
    agent_name = Column(String(100), nullable=False)
    round = Column(Integer, nullable=False)
    round_name = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    # Relationship to deliberation
    deliberation = relationship("Deliberation", back_populates="responses")

    def __repr__(self):
        return f"<DeliberationResponse(agent='{self.agent_name}', round={self.round})>"

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'id': self.id,
            'deliberation_id': self.deliberation_id,
            'agent_id': self.agent_id,
            'agent_name': self.agent_name,
            'round': self.round,
            'round_name': self.round_name,
            'content': self.content,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }