"""Unit tests for topup command handler."""
import unittest
from unittest.mock import MagicMock
from io import StringIO
import sys
from decimal import Decimal

from app.models import User, Session
from app.handlers.topup import cmd_topup
from app.repositories import InMemoryUserRepository, InMemorySessionRepository

class TestTopupHandler(unittest.TestCase):
    """Test cases for the topup command handler."""
    
    def setUp(self):
        """Set up test environment before each test."""
        # Create a mock CLI object
        self.cli = MagicMock()
        self.cli.user_repository = InMemoryUserRepository()
        self.cli.session_repository = InMemorySessionRepository()
        
        # Create a test user
        self.test_user = User.create("test_user")
        self.cli.user_repository.save(self.test_user)
        
        # Create and save test session
        self.test_session = Session.create(self.test_user)
        self.cli.session_repository.save(self.test_session)
        
        # Setup stdout capture
        self.held_output = StringIO()
        self.old_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        """Clean up after each test."""
        # Restore stdout
        sys.stdout = self.old_stdout
        self.held_output.close()

    def test_successful_topup(self):
        """Test successful wallet top up."""
        # Given
        initial_balance = self.test_user.wallet.balance
        amount = Decimal("50000")
        self.cli.current_args = [str(amount)]
        
        # When
        cmd_topup(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn(f"Successfully topped up Rp{amount:.2f}", output)
        self.assertIn(f"Current balance: Rp{amount:.2f}", output)
        
        # Verify balance was updated
        updated_user = self.cli.user_repository.find_by_name("test_user")
        self.assertEqual(updated_user.wallet.balance, initial_balance + amount)
    
    def test_topup_when_not_logged_in(self):
        """Test top up when user is not logged in."""
        # Given
        self.cli.session_repository.clear()  # Clear session
        self.cli.current_args = ["50000"]
        
        # When
        cmd_topup(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn("Error: You must be logged in to top up your wallet", output)
        self.assertIn("Please login first using: login <username>", output)
    
    def test_topup_with_invalid_amount(self):
        """Test top up with invalid amount format."""
        # Given
        self.cli.current_args = ["invalid"]
        
        # When
        cmd_topup(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn("Error: Invalid amount format", output)
        self.assertIn("Amount must be a number", output)
    
    def test_topup_with_negative_amount(self):
        """Test top up with negative amount."""
        # Given
        self.cli.current_args = ["-50000"]
        
        # When
        cmd_topup(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn("Error: Amount must be positive", output)
    
    def test_topup_without_amount(self):
        """Test top up without providing amount."""
        # Given
        self.cli.current_args = []
        
        # When
        cmd_topup(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn("Error: Amount required", output)
        self.assertIn("Usage: topup <amount>", output)
        self.assertIn("Example: topup 50000", output)

if __name__ == '__main__':
    unittest.main() 