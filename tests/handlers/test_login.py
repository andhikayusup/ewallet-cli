"""Unit tests for login command handler."""
import unittest
from unittest.mock import MagicMock
from io import StringIO
import sys

from app.models import User
from app.handlers.login import cmd_login
from app.repositories import InMemoryUserRepository, InMemorySessionRepository

class TestLoginHandler(unittest.TestCase):
    """Test cases for the login command handler."""
    
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

    def test_successful_login(self):
        """Test successful user login."""
        # Given
        self.cli.current_args = ["test_user"]
        
        # When
        cmd_login(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn("User 'test_user' logged in successfully!", output)
        self.assertIn("Session ID:", output)
        
        # Verify session was created
        session = self.cli.session_repository.find_by_user_name("test_user")
        self.assertIsNotNone(session)
        self.assertEqual(session.user, self.test_user)
    
    def test_login_nonexistent_user(self):
        """Test login with non-existent username."""
        # Given
        self.cli.current_args = ["nonexistent"]
        
        # When
        cmd_login(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn("Error: User 'nonexistent' not found", output)
        self.assertIn("Please register first using: register <username>", output)
    
    def test_already_logged_in(self):
        """Test login when user is already logged in."""
        # Given
        self.cli.current_args = ["test_user"]
        
        # First login
        cmd_login(self.cli)
        self.held_output.truncate(0)
        self.held_output.seek(0)
        
        # When - try to login again
        cmd_login(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn("User 'test_user' is already logged in", output)
    
    def test_missing_username(self):
        """Test login without username."""
        # Given
        self.cli.current_args = []
        
        # When
        cmd_login(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn("Error: Username required", output)
        self.assertIn("Usage: login <username>", output)
        self.assertIn("Example: login john", output)
    
    def test_single_session_policy(self):
        """Test that logging in as a new user clears existing session."""
        # Given
        other_user = User.create("other_user")
        self.cli.user_repository.save(other_user)
        
        # First login
        self.cli.current_args = ["test_user"]
        cmd_login(self.cli)
        
        # When - login as other user
        self.cli.current_args = ["other_user"]
        cmd_login(self.cli)
        
        # Then
        self.assertIsNone(self.cli.session_repository.find_by_user_name("test_user"))
        self.assertIsNotNone(self.cli.session_repository.find_by_user_name("other_user"))

if __name__ == '__main__':
    unittest.main() 