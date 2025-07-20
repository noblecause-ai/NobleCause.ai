"""SQLAlchemy models for Noble Cause Steward database."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

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