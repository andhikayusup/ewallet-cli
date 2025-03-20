"""Unit tests for exit command handler."""
import unittest
from unittest.mock import MagicMock
from io import StringIO
import sys

from app.handlers.exit import cmd_exit

class TestExitHandler(unittest.TestCase):
    def setUp(self):
        # Create a mock CLI object
        self.cli = MagicMock()
        self.cli.running = True

        # Setup stdout capture
        self.held_output = StringIO()
        self.old_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.old_stdout
        self.held_output.close()

    def test_cmd_exit(self):
        """Test the exit command stops the CLI."""

        # Verify CLI is running before exit
        self.assertTrue(self.cli.running)
        
        # Execute exit command
        cmd_exit(self.cli)
        
        # Verify CLI is no longer running
        self.assertFalse(self.cli.running)

if __name__ == '__main__':
    unittest.main()