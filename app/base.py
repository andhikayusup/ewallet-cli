"""Base CLI implementation."""

from typing import Callable, Dict

from .registry import CommandRegistry

class CLI:
    def __init__(self):
        self.commands: Dict[str, dict] = {}
        self.running = True
        
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

    def handle_command(self, command: str) -> None:
        """Process a command string and execute the appropriate handler."""
        command = command.strip().lower()
        
        if command in self.commands:
            self.commands[command]["handler"]()
        else:
            print(f"Unknown command: {command}")
            self.commands["help"]["handler"]()

    def run(self) -> None:
        """Main CLI loop."""
        print("Welcome to the E-Wallet CLI!")
        print("Type 'help' for available commands.")
        
        while self.running:
            try:
                command = input("\n> ")
                self.handle_command(command)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break 