"""Centralized command registry."""

from .handlers import hello, help, exit, register, login

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
            "register",
            lambda: register.cmd_register(cli),
            "Register a new user (usage: register <username>)"
        )
        cli.register_command(
            "login",
            lambda: login.cmd_login(cli),
            "Login as a user (usage: login <username>)"
        )
        cli.register_command(
            "exit",
            lambda: exit.cmd_exit(cli),
            "Quit the program"
        )