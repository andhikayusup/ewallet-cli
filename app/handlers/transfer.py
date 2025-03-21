"""Handler for the transfer command."""
from decimal import Decimal, InvalidOperation
from app.utils import println

def cmd_transfer(cli) -> None:
    """Handle the transfer command.
    
    Usage: transfer <username> <amount>
    Example: transfer john 50000
    
    Transfers the specified amount from your wallet to another user's wallet.
    Both users must be registered and amount must be a positive number.
    """
    try:
        # Check if user is logged in
        current_session = cli.session_repository._session
        if not current_session:
            println("Error: You must be logged in to transfer money")
            println("Please login first using: login <username>")
            return
            
        # Get and validate recipient username and amount
        if len(cli.current_args) < 2:
            println("Error: Both recipient username and amount are required")
            println("Usage: transfer <username> <amount>")
            println("Example: transfer john 50000")
            return
            
        recipient_name = cli.current_args[0]
        
        # Check if trying to transfer to self
        if recipient_name.lower() == current_session.user.name.lower():
            println("Error: Cannot transfer money to yourself")
            return
            
        # Find recipient user
        recipient = cli.user_repository.find_by_name(recipient_name)
        if not recipient:
            println(f"Error: User '{recipient_name}' not found")
            println("Please check the username and try again")
            return
            
        # Parse and validate amount
        try:
            amount = Decimal(cli.current_args[1])
        except InvalidOperation:
            println("Error: Invalid amount format")
            println("Amount must be a number")
            return
            
        if amount <= 0:
            println("Error: Amount must be positive")
            return
            
        # Check if sender has sufficient balance
        sender = current_session.user
        if sender.wallet.balance < amount:
            println(f"Error: Insufficient balance")
            println(f"Your current balance: Rp{sender.wallet.balance:.2f}")
            println(f"Required amount: Rp{amount:.2f}")
            return
            
        # Perform the transfer
        sender.wallet.balance -= amount
        recipient.wallet.balance += amount
        
        # Save both users
        cli.user_repository.save(sender)
        cli.user_repository.save(recipient)
        
        # Show success message
        println(f"Successfully transferred Rp{amount:.2f} to {recipient.name}")
        println(f"Your new balance: Rp{sender.wallet.balance:.2f}")
        
    except IndexError:
        println("Error: Both recipient username and amount are required")
        println("Usage: transfer <username> <amount>")
        println("Example: transfer john 50000") 