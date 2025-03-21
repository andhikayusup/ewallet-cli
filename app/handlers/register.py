"""Handler for the register command."""
from app.models.user import User
from app.utils import println

def cmd_register(cli) -> None:
    """Handle the register command.
    
    Usage: register <username>
    Example: register john
    """
    try:
        # Get the username from the command arguments
        username = cli.current_args[0]
        
        # Check if user already exists
        existing_user = cli.user_repository.find_by_name(username)
        if existing_user:
            println(f"Error: User '{username}' already exists")
            return
            
        # Create and save the new user
        user = User.create(username)
        cli.user_repository.save(user)
        
        println(f"User '{username}' registered successfully!")
        println(f"User ID: {user.id}")
        println(f"Initial wallet balance: {user.wallet.balance}")
        
    except IndexError:
        println("Error: Username required")
        println("Usage: register <username>")
        println("Example: register john") 