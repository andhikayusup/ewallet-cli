"""Handler for the login command."""
from app.models.session import Session
from app.utils import println

def cmd_login(cli) -> None:
    """Handle the login command.
    
    Usage: login <username>
    Example: login john
    """
    try:
        # Get the username from the command arguments
        username = cli.current_args[0]
        
        # Check if user exists
        user = cli.user_repository.find_by_name(username)
        if not user:
            println(f"Error: User '{username}' not found")
            println("Please register first using: register <username>")
            return
            
        # Check if user is already logged in
        existing_session = cli.session_repository.find_by_user_name(username)
        if existing_session:
            println(f"User '{username}' is already logged in")
            return
            
        # Create and save new session
        session = Session.create(user)
        cli.session_repository.clear()  # Clear any other sessions
        cli.session_repository.save(session)
        
        println(f"User '{username}' logged in successfully!")
        println(f"Session ID: {session.id}")
        
    except IndexError:
        println("Error: Username required")
        println("Usage: login <username>")
        println("Example: login john") 