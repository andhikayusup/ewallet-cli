"""Handler for the help command."""

def cmd_help(cli) -> None:
    """Display help message with available commands."""
    print("\nAvailable commands:")
    # Sort commands alphabetically for better readability
    for name, cmd in sorted(cli.commands.items()):
        print(f"  {name:<10} - {cmd['description']}")
    print() 