"""Base CLI implementation."""

from typing import Callable, Dict, List
from shlex import split

from .registry import CommandRegistry
from .utils import println
from .repositories.user_repository import UserRepository, InMemoryUserRepository

class CLI:
    def __init__(self):
        self.commands: Dict[str, dict] = {}
        self.running = True
        self.current_args: List[str] = []
        
        # Initialize repositories
        self.user_repository: UserRepository = InMemoryUserRepository()
        
        # Register all commands using the central registry
        CommandRegistry.register_all(self)

    def register_command(
        self,
        name: str,
        handler: Callable[[], None],
        description: str
    ) -> None:
        """Register a new command with the CLI.

        Args:
            name: The command name (what users will type)
            handler: The function that will handle the command
            description: A brief description of what the command does
        """
        self.commands[name.lower()] = {
            "handler": handler,
            "description": description
        }

    def handle_command(self, command_line: str) -> None:
        """Process a command string and execute the appropriate handler."""
        try:
            # Split the command line into command and arguments
            parts = split(command_line.strip())
            if not parts:
                return
                
            command = parts[0].lower()
            self.current_args = parts[1:]
            
            if command in self.commands:
                self.commands[command]["handler"]()
            else:
                println(f"Unknown command: {command}")
                self.commands["help"]["handler"]()
        finally:
            # Clear arguments after command execution
            self.current_args = []

    def run(self) -> None:
        """Main CLI loop."""
        println("Welcome to the E-Wallet CLI!")
        println("Type 'help' for available commands.")
        
        while self.running:
            try:
                command = input("\n> ")
                self.handle_command(command)
            except KeyboardInterrupt:
                println("\nGoodbye!")
                break
            except EOFError:
                println("\nGoodbye!")
                break 