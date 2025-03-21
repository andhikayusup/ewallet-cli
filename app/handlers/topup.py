"""Handler for the topup command."""
from decimal import Decimal, InvalidOperation
from app.utils import println

def cmd_topup(cli) -> None:
    """Handle the topup command.
    
    Usage: topup <amount>
    Example: topup 50000
    
    Adds the specified amount to the user's wallet balance.
    Amount must be a positive number.
    """
    try:
        # Check if user is logged in
        current_session = cli.session_repository._session
        if not current_session:
            println("Error: You must be logged in to top up your wallet")
            println("Please login first using: login <username>")
            return
            
        # Get and validate amount
        if not cli.current_args:
            println("Error: Amount required")
            println("Usage: topup <amount>")
            println("Example: topup 50000")
            return
            
        try:
            amount = Decimal(cli.current_args[0])
        except InvalidOperation:
            println("Error: Invalid amount format")
            println("Amount must be a number")
            return
            
        if amount <= 0:
            println("Error: Amount must be positive")
            return
            
        # Update wallet balance
        user = current_session.user
        user.wallet.balance += amount
        cli.user_repository.save(user)  # Save the updated user data
        
        # Show success message
        println(f"Successfully topped up Rp{amount:.2f}")
        println(f"Current balance: Rp{user.wallet.balance:.2f}")
        
    except IndexError:
        println("Error: Amount required")
        println("Usage: topup <amount>")
        println("Example: topup 50000") 