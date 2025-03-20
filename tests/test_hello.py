"""Unit tests for hello command handler."""
import unittest
from unittest.mock import MagicMock
from io import StringIO
import sys

from app.handlers.hello import cmd_hello

class TestHelloHandler(unittest.TestCase):
    def setUp(self):
        # Create a mock CLI object
        self.cli = MagicMock()

        # Setup stdout capture
        self.held_output = StringIO()
        self.old_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.old_stdout
        self.held_output.close()

    def test_cmd_hello(self):
        """Test the hello command outputs the expected greeting."""
        expected_output = "hello"

        cmd_hello(self.cli)
        actual_output = self.held_output.getvalue().strip()

        self.assertEqual(actual_output, expected_output)

if __name__ == '__main__':
    unittest.main() 