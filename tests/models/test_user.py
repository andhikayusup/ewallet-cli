"""Unit tests for User and Wallet models."""
import unittest
from decimal import Decimal
from uuid import UUID

from app.models import User, Wallet

class TestWallet(unittest.TestCase):
    """Test cases for the Wallet model."""
    
    def test_wallet_initialization(self):
        """Test that a new wallet starts with zero balance."""
        # Given
        expected = Wallet(balance=Decimal('0'))
        
        # When
        actual = Wallet()
        
        # Then
        self.assertEqual(expected, actual)

class TestUser(unittest.TestCase):
    """Test cases for the User model."""
    
    def test_user_creation(self):
        """Test user creation with factory method."""
        # Given
        name = "test_user"
        
        # When
        actual = User.create(name)
        
        # Then
        self.assertIsInstance(actual.id, UUID)  # Can't predict the UUID
        expected = User(
            id=actual.id,  # Use the generated ID for comparison
            name=name,
            wallet=Wallet()
        )
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main() 