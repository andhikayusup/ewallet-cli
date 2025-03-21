"""Unit tests for UserRepository implementations."""
import unittest
from uuid import uuid4

from app.models import User
from app.repositories import InMemoryUserRepository

class TestInMemoryUserRepository(unittest.TestCase):
    """Test cases for the in-memory user repository implementation."""
    
    def setUp(self):
        """Set up a fresh repository for each test."""
        self.repo = InMemoryUserRepository()
        self.test_user = User.create("test_user")
    
    def test_save_and_find_by_id(self):
        """Test saving a user and finding them by ID."""
        # Given
        expected = self.test_user
        
        # When
        self.repo.save(expected)
        actual = self.repo.find_by_id(expected.id)
        
        # Then
        self.assertEqual(expected, actual)
    
    def test_find_by_nonexistent_id(self):
        """Test that finding a nonexistent user ID returns None."""
        # Given
        nonexistent_id = uuid4()
        
        # When
        actual = self.repo.find_by_id(nonexistent_id)
        
        # Then
        self.assertIsNone(actual)
    
    def test_save_and_find_by_name(self):
        """Test saving a user and finding them by name."""
        # Given
        expected = self.test_user
        
        # When
        self.repo.save(expected)
        actual = self.repo.find_by_name(expected.name)
        
        # Then
        self.assertEqual(expected, actual)
    
    def test_find_by_nonexistent_name(self):
        """Test that finding a nonexistent username returns None."""
        # Given
        nonexistent_name = "nonexistent_user"
        
        # When
        actual = self.repo.find_by_name(nonexistent_name)
        
        # Then
        self.assertIsNone(actual)
    
    def test_case_insensitive_name_search(self):
        """Test that name search is case insensitive."""
        # Given
        expected = self.test_user
        self.repo.save(expected)
        test_cases = ["TEST_USER", "test_user", "Test_User"]
        
        # When/Then
        for variant in test_cases:
            with self.subTest(variant=variant):
                actual = self.repo.find_by_name(variant)
                self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main() 