"""Unit tests for balance command handler."""
import unittest
from unittest.mock import MagicMock
from io import StringIO
import sys
from decimal import Decimal

from app.models import User, Session
from app.handlers.balance import cmd_balance
from app.repositories import InMemoryUserRepository, InMemorySessionRepository

class TestBalanceHandler(unittest.TestCase):
    """Test cases for the balance command handler."""
    
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

    def test_balance_check_when_logged_in(self):
        """Test checking balance when user is logged in."""
        # Given
        session = Session.create(self.test_user)
        self.cli.session_repository.save(session)
        self.cli.current_args = ["test_user"]
        
        # When
        cmd_balance(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        
        self.assertIn(f"Current balance for user '{self.test_user.name}': Rp0.00", output)
    
    def test_balance_check_when_not_logged_in(self):
        """Test checking balance when user is not logged in."""
        # Given
        self.cli.current_args = []
        
        # When
        cmd_balance(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn("Error: You must be logged in to check your balance", output)
        self.assertIn("Please login first using: login <username>", output)

if __name__ == '__main__':
    unittest.main() 