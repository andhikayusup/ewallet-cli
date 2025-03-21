"""Unit tests for Session model."""
import unittest
from datetime import datetime
from uuid import UUID

from app.models import User, Session

class TestSession(unittest.TestCase):
    """Test cases for the Session model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_user = User.create("test_user")
    
    def test_session_creation(self):
        """Test session creation with factory method."""
        # Given
        expected_user = self.test_user
        
        # When
        actual = Session.create(expected_user)
        
        # Then
        self.assertIsInstance(actual.id, UUID)
        self.assertIsInstance(actual.created_at, datetime)
        self.assertEqual(actual.user, expected_user)

if __name__ == '__main__':
    unittest.main() 