"""Handler for the logout command."""
from app.utils import println

def cmd_logout(cli) -> None:
    """Handle the logout command.
    
    Usage: logout
    Logs out the current user by clearing their session.
    """
    # Check if user is logged in
    current_session = cli.session_repository._session
    if not current_session:
        println("Error: No user is currently logged in")
        return
        
    # Get username for message before clearing
    username = current_session.user.name
    
    # Clear the session
    cli.session_repository.clear()
    
    println(f"User '{username}' logged out successfully") 