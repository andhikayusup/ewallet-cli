"""Unit tests for logout command handler."""
import unittest
from unittest.mock import MagicMock
from io import StringIO
import sys

from app.models import User, Session
from app.handlers.logout import cmd_logout
from app.repositories import InMemoryUserRepository, InMemorySessionRepository

class TestLogoutHandler(unittest.TestCase):
    """Test cases for the logout command handler."""
    
    def setUp(self):
        """Set up test environment before each test."""
        # Create a mock CLI object
        self.cli = MagicMock()
        self.cli.user_repository = InMemoryUserRepository()
        self.cli.session_repository = InMemorySessionRepository()
        
        # Create a test user
        self.test_user = User.create("test_user")
        self.cli.user_repository.save(self.test_user)
        
        # Setup stdout capture
        self.held_output = StringIO()
        self.old_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        """Clean up after each test."""
        # Restore stdout
        sys.stdout = self.old_stdout
        self.held_output.close()

    def test_successful_logout(self):
        """Test successful user logout."""
        # Given
        session = Session.create(self.test_user)
        self.cli.session_repository.save(session)
        
        # When
        cmd_logout(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn(f"User '{self.test_user.name}' logged out successfully", output)
        
        # Verify session was cleared
        self.assertIsNone(self.cli.session_repository._session)
    
    def test_logout_when_not_logged_in(self):
        """Test logout when no user is logged in."""
        # Given
        self.cli.session_repository.clear()  # Ensure no session exists
        
        # When
        cmd_logout(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn("Error: No user is currently logged in", output)

if __name__ == '__main__':
    unittest.main() 