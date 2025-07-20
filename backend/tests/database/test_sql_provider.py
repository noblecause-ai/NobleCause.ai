"""Tests for SQLProvider database operations."""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from noble_cause_steward.database.sql_models import Base, Recommendation


class TestSQLProvider:
    """Test class for SQLProvider database operations."""
    
    @pytest.fixture
    def in_memory_db(self):
        """Create an in-memory SQLite database for testing."""
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        yield session
        
        session.close()
    
    def test_database_connection(self, in_memory_db):
        """Test that a connection to a mock SQLite database can be established."""
        # This test will fail until SQLProvider is implemented
        from noble_cause_steward.database.sql_provider import SQLProvider
        
        # Create SQLProvider instance
        provider = SQLProvider(database_url='sqlite:///:memory:')
        
        # Assert that connection can be established
        assert provider.is_connected() is True
        
        # Clean up
        provider.close()
    
    def test_add_and_retrieve_recommendation(self, in_memory_db):
        """Test that a Recommendation can be written to and retrieved from database."""
        # This test will fail until SQLProvider is implemented
        from noble_cause_steward.database.sql_provider import SQLProvider
        
        # Create SQLProvider instance
        provider = SQLProvider(database_url='sqlite:///:memory:')
        
        # Create a test recommendation
        test_recommendation = {
            'title': 'Test Recommendation',
            'summary': 'This is a test recommendation for database operations.',
            'pillar': 'Environmental Stewardship'
        }
        
        # Add recommendation to database
        recommendation_id = provider.add_recommendation(
            title=test_recommendation['title'],
            summary=test_recommendation['summary'],
            pillar=test_recommendation['pillar']
        )
        
        # Assert that recommendation was added successfully
        assert recommendation_id is not None
        assert isinstance(recommendation_id, int)
        assert recommendation_id > 0
        
        # Retrieve the recommendation
        retrieved_recommendation = provider.get_recommendation(recommendation_id)
        
        # Assert that all fields match
        assert retrieved_recommendation is not None
        assert retrieved_recommendation['id'] == recommendation_id
        assert retrieved_recommendation['title'] == test_recommendation['title']
        assert retrieved_recommendation['summary'] == test_recommendation['summary']
        assert retrieved_recommendation['pillar'] == test_recommendation['pillar']
        assert 'created_at' in retrieved_recommendation
        assert retrieved_recommendation['created_at'] is not None
        
        # Verify created_at is a valid datetime string
        created_at = datetime.fromisoformat(retrieved_recommendation['created_at'])
        assert isinstance(created_at, datetime)
        
        # Clean up
        provider.close()
    
    def test_recommendation_model_creation(self, in_memory_db):
        """Test that Recommendation model can be created and saved directly."""
        # Create a recommendation instance
        recommendation = Recommendation(
            title='Direct Model Test',
            summary='Testing direct model creation and persistence.',
            pillar='Social Justice'
        )
        
        # Add to session and commit
        in_memory_db.add(recommendation)
        in_memory_db.commit()
        
        # Assert that ID was assigned
        assert recommendation.id is not None
        assert recommendation.id > 0
        
        # Query back from database
        retrieved = in_memory_db.query(Recommendation).filter_by(id=recommendation.id).first()
        
        # Assert all fields match
        assert retrieved is not None
        assert retrieved.title == 'Direct Model Test'
        assert retrieved.summary == 'Testing direct model creation and persistence.'
        assert retrieved.pillar == 'Social Justice'
        assert retrieved.created_at is not None
        assert isinstance(retrieved.created_at, datetime)
        
        # Test to_dict method
        recommendation_dict = retrieved.to_dict()
        assert recommendation_dict['id'] == retrieved.id
        assert recommendation_dict['title'] == retrieved.title
        assert recommendation_dict['summary'] == retrieved.summary
        assert recommendation_dict['pillar'] == retrieved.pillar
        assert recommendation_dict['created_at'] is not None