"""Handler for the balance command."""
from app.utils import println

def cmd_balance(cli) -> None:
    """Handle the balance command.
    
    Usage: balance
    Shows the current wallet balance for the logged-in user.
    """
    # Check if user is logged in
    current_session = cli.session_repository._session
    
    if not current_session:
        println("Error: You must be logged in to check your balance")
        println("Please login first using: login <username>")
        return
        
    # Display balance
    user = current_session.user
    println(f"Current balance for user '{user.name}': Rp{user.wallet.balance:.2f}") 