"""Centralized command registry."""

from .handlers import hello, help, exit

class CommandRegistry:
    """Central registry for all CLI commands."""
    
    @classmethod
    def register_all(cls, cli) -> None:
        """Register all available commands with the CLI.
        
        This is the single source of truth for command registration.
        All new commands should be registered here.
        """
        cli.register_command(
            "hello",
            lambda: hello.cmd_hello(cli),
            "Get a hello response"
        )
        cli.register_command(
            "help",
            lambda: help.cmd_help(cli),
            "Show this help message"
        )
        cli.register_command(
            "exit",
            lambda: exit.cmd_exit(cli),
            "Quit the program"
        )