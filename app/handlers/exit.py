"""System command handlers."""

def cmd_exit(cli) -> None:
    """Handle the exit command."""
    cli.running = False
    print("Goodbye!") 