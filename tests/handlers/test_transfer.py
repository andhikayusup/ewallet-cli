"""Unit tests for transfer command handler."""
import unittest
from unittest.mock import MagicMock
from io import StringIO
import sys
from decimal import Decimal

from app.models import User, Session
from app.handlers.transfer import cmd_transfer
from app.repositories import InMemoryUserRepository, InMemorySessionRepository

class TestTransferHandler(unittest.TestCase):
    """Test cases for the transfer command handler."""
    
    def setUp(self):
        """Set up test environment before each test."""
        # Create a mock CLI object
        self.cli = MagicMock()
        self.cli.user_repository = InMemoryUserRepository()
        self.cli.session_repository = InMemorySessionRepository()
        
        # Create sender user with initial balance
        self.sender = User.create("sender")
        self.sender.wallet.balance = Decimal("100000")  # Initial balance 100k
        self.cli.user_repository.save(self.sender)
        
        # Create recipient user
        self.recipient = User.create("recipient")
        self.cli.user_repository.save(self.recipient)
        
        # Create and save sender's session
        self.session = Session.create(self.sender)
        self.cli.session_repository.save(self.session)
        
        # Setup stdout capture
        self.held_output = StringIO()
        self.old_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        """Clean up after each test."""
        # Restore stdout
        sys.stdout = self.old_stdout
        self.held_output.close()

    def test_successful_transfer(self):
        """Test successful money transfer."""
        # Given
        amount = Decimal("50000")
        self.cli.current_args = ["recipient", str(amount)]
        initial_sender_balance = self.sender.wallet.balance
        initial_recipient_balance = self.recipient.wallet.balance
        
        # When
        cmd_transfer(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn(f"Successfully transferred Rp{amount:.2f} to {self.recipient.name}", output)
        self.assertIn(f"Your new balance: Rp{initial_sender_balance - amount:.2f}", output)
        
        # Verify balances were updated
        updated_sender = self.cli.user_repository.find_by_name("sender")
        updated_recipient = self.cli.user_repository.find_by_name("recipient")
        self.assertEqual(updated_sender.wallet.balance, initial_sender_balance - amount)
        self.assertEqual(updated_recipient.wallet.balance, initial_recipient_balance + amount)
    
    def test_transfer_when_not_logged_in(self):
        """Test transfer when user is not logged in."""
        # Given
        self.cli.session_repository.clear()  # Clear session
        self.cli.current_args = ["recipient", "50000"]
        
        # When
        cmd_transfer(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn("Error: You must be logged in to transfer money", output)
        self.assertIn("Please login first using: login <username>", output)
    
    def test_transfer_to_nonexistent_user(self):
        """Test transfer to non-existent user."""
        # Given
        self.cli.current_args = ["nonexistent", "50000"]
        
        # When
        cmd_transfer(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn("Error: User 'nonexistent' not found", output)
        self.assertIn("Please check the username and try again", output)
    
    def test_transfer_to_self(self):
        """Test transfer to self."""
        # Given
        self.cli.current_args = ["sender", "50000"]  # Same as logged in user
        
        # When
        cmd_transfer(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn("Error: Cannot transfer money to yourself", output)
    
    def test_transfer_with_invalid_amount(self):
        """Test transfer with invalid amount format."""
        # Given
        self.cli.current_args = ["recipient", "invalid"]
        
        # When
        cmd_transfer(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn("Error: Invalid amount format", output)
        self.assertIn("Amount must be a number", output)
    
    def test_transfer_with_negative_amount(self):
        """Test transfer with negative amount."""
        # Given
        self.cli.current_args = ["recipient", "-50000"]
        
        # When
        cmd_transfer(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn("Error: Amount must be positive", output)
    
    def test_transfer_with_insufficient_balance(self):
        """Test transfer with insufficient balance."""
        # Given
        amount = self.sender.wallet.balance + Decimal("1")  # One more than available
        self.cli.current_args = ["recipient", str(amount)]
        
        # When
        cmd_transfer(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn("Error: Insufficient balance", output)
        self.assertIn(f"Your current balance: Rp{self.sender.wallet.balance:.2f}", output)
        self.assertIn(f"Required amount: Rp{amount:.2f}", output)
    
    def test_transfer_without_arguments(self):
        """Test transfer without providing arguments."""
        # Given
        self.cli.current_args = []
        
        # When
        cmd_transfer(self.cli)
        output = self.held_output.getvalue()
        
        # Then
        self.assertIn("Error: Both recipient username and amount are required", output)
        self.assertIn("Usage: transfer <username> <amount>", output)
        self.assertIn("Example: transfer john 50000", output)

if __name__ == '__main__':
    unittest.main() 