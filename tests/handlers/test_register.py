"""Unit tests for register command handler."""
import unittest
from unittest.mock import MagicMock
from io import StringIO
import sys

from app.handlers.register import cmd_register
from app.repositories import InMemoryUserRepository

class TestRegisterHandler(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        # Create a mock CLI object
        self.cli = MagicMock()
        self.cli.user_repository = InMemoryUserRepository()
        
        # Setup stdout capture
        self.held_output = StringIO()
        self.old_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        """Clean up after each test."""
        # Restore stdout
        sys.stdout = self.old_stdout
        self.held_output.close()

    def test_successful_registration(self):
        """Test successful user registration."""
        # Setup command arguments
        self.cli.current_args = ["new_user"]
        
        # Execute command
        cmd_register(self.cli)
        output = self.held_output.getvalue()
        
        # Verify success message
        self.assertIn("User 'new_user' registered successfully!", output)
        self.assertIn("User ID:", output)
        self.assertIn("Initial wallet balance: 0", output)
        
        # Verify user was saved
        user = self.cli.user_repository.find_by_name("new_user")
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "new_user")
        
    def test_duplicate_username(self):
        """Test registration with existing username."""
        # Register first user
        self.cli.current_args = ["test_user"]
        cmd_register(self.cli)
        self.held_output.truncate(0)
        self.held_output.seek(0)
        
        # Try to register same username again
        cmd_register(self.cli)
        output = self.held_output.getvalue()
        
        # Verify error message
        self.assertIn("Error: User 'test_user' already exists", output)
        
    def test_missing_username(self):
        """Test registration without username."""
        # Setup empty arguments
        self.cli.current_args = []
        
        # Execute command
        cmd_register(self.cli)
        output = self.held_output.getvalue()
        
        # Verify error message
        self.assertIn("Error: Username required", output)
        self.assertIn("Usage: register <username>", output)
        self.assertIn("Example: register john", output)

if __name__ == '__main__':
    unittest.main() 