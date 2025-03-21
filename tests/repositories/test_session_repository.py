"""Unit tests for SessionRepository implementations."""
import unittest

from app.models import User, Session
from app.repositories import InMemorySessionRepository

class TestInMemorySessionRepository(unittest.TestCase):
    """Test cases for the in-memory session repository implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.repo = InMemorySessionRepository()
        self.test_user = User.create("test_user")
        self.test_session = Session.create(self.test_user)
    
    def test_save_and_find_session(self):
        """Test saving a session and finding it by username."""
        # Given
        expected = self.test_session
        
        # When
        self.repo.save(expected)
        actual = self.repo.find_by_user_name(self.test_user.name)
        
        # Then
        self.assertEqual(expected, actual)
    
    def test_find_nonexistent_session(self):
        """Test finding a session for a nonexistent user."""
        # Given
        nonexistent_username = "nonexistent"
        
        # When
        actual = self.repo.find_by_user_name(nonexistent_username)
        
        # Then
        self.assertIsNone(actual)
    
    def test_single_session_policy(self):
        """Test that saving a new session replaces the existing one."""
        # Given
        first_user = User.create("first_user")
        second_user = User.create("second_user")
        first_session = Session.create(first_user)
        second_session = Session.create(second_user)
        
        # When
        self.repo.save(first_session)
        self.repo.save(second_session)
        
        # Then
        self.assertIsNone(self.repo.find_by_user_name(first_user.name))
        self.assertEqual(second_session, self.repo.find_by_user_name(second_user.name))
    
    def test_clear_sessions(self):
        """Test clearing all sessions."""
        # Given
        self.repo.save(self.test_session)
        
        # When
        self.repo.clear()
        
        # Then
        self.assertIsNone(self.repo.find_by_user_name(self.test_user.name))
    
    def test_case_insensitive_username_search(self):
        """Test that username search is case insensitive."""
        # Given
        self.repo.save(self.test_session)
        test_cases = ["TEST_USER", "test_user", "Test_User"]
        
        # When/Then
        for variant in test_cases:
            with self.subTest(variant=variant):
                actual = self.repo.find_by_user_name(variant)
                self.assertEqual(self.test_session, actual)

if __name__ == '__main__':
    unittest.main() 