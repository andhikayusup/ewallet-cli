"""Unit tests for help command handler."""
import unittest
from unittest.mock import MagicMock
from io import StringIO
import sys

from app.handlers.help import cmd_help

class TestHelpHandler(unittest.TestCase):
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

    def test_cmd_help(self):
        """Test the help command displays available commands."""
        # Setup mock commands
        self.cli.commands = {
            'hello': {'description': 'Say hello'}
        }
        
        expected_output = "\nAvailable commands:\n  hello      - Say hello\n\n"
        
        cmd_help(self.cli)
        actual_output = self.held_output.getvalue()
        
        self.assertEqual(actual_output, expected_output)

if __name__ == '__main__':
    unittest.main() 