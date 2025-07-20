"""SQLProvider for managing structured data storage in a relational database."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from .sql_models import Base, Recommendation


class SQLProvider:
    """Manages structured data storage in a relational database using SQLAlchemy."""
    
    def __init__(self, database_url: str):
        """
        Initialize the SQLProvider with a database URL.
        
        Args:
            database_url: The database connection URL (e.g., 'sqlite:///:memory:')
        """
        self.database_url = database_url
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        
        # Create all tables based on the defined models
        Base.metadata.create_all(self.engine)
    
    def is_connected(self) -> bool:
        """
        Verify the database connection.
        
        Returns:
            bool: True if connected, False otherwise
        """
        try:
            # Test the connection by executing a simple query
            with self.engine.connect() as connection:
                connection.execute("SELECT 1")
            return True
        except SQLAlchemyError:
            return False
    
    def add_recommendation(self, title: str, summary: str, pillar: str) -> int:
        """
        Create a new Recommendation object and commit it to the database.
        
        Args:
            title: The recommendation title
            summary: The recommendation summary
            pillar: The pillar category
            
        Returns:
            int: The ID of the created recommendation
        """
        session = self.Session()
        try:
            recommendation = Recommendation(
                title=title,
                summary=summary,
                pillar=pillar
            )
            session.add(recommendation)
            session.commit()
            return recommendation.id
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_recommendation(self, recommendation_id: int) -> dict:
        """
        Retrieve a specific recommendation by its ID.
        
        Args:
            recommendation_id: The ID of the recommendation to retrieve
            
        Returns:
            dict: The recommendation data as a dictionary, or None if not found
        """
        session = self.Session()
        try:
            recommendation = session.query(Recommendation).filter_by(id=recommendation_id).first()
            if recommendation:
                return recommendation.to_dict()
            return None
        except SQLAlchemyError:
            raise
        finally:
            session.close()
    
    def close(self):
        """Close the database connection."""
        if hasattr(self, 'engine'):
            self.engine.dispose()