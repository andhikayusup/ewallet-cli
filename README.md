# E-Wallet CLI Application

A simple interactive command-line e-wallet application that allows users to manage their digital wallet, perform transactions, and interact with other users.

## Features
- User registration and authentication
- Digital wallet management
- Money transfers between users
- Balance checking
- Secure session management

## Setup

### Virtual Environment
1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the virtual environment:
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. To deactivate when done:
```bash
deactivate
```

## Commands

### User Management
- `register <username>`: Create a new user account
  - Example: `register john`

- `login <username>`: Log in as a registered user
  - Example: `login john`

- `logout`: Log out the current user

### Wallet Operations
- `balance`: Check your current wallet balance

- `topup <amount>`: Add money to your wallet
  - Example: `topup 50000`
  - Amount must be a positive number

- `transfer <username> <amount>`: Send money to another user
  - Example: `transfer jane 25000`
  - Recipient must be a registered user
  - Cannot transfer to yourself
  - Must have sufficient balance

### System Commands
- `help`: Shows available commands and their descriptions
- `exit`: Quits the program

## Running the Application
Make sure your virtual environment is activated, then run:
```bash
python main.py
```

## Running Tests
With virtual environment activated:
```bash
python -m unittest discover tests
```

## Example Usage
```bash
# Register new users
> register john
User 'john' registered successfully!

# Login
> login john
User 'john' logged in successfully!

# Top up wallet
> topup 100000
Successfully topped up Rp100000.00
Current balance: Rp100000.00

# Check balance
> balance
Current balance for user 'john': Rp100000.00

# Transfer money
> transfer jane 50000
Successfully transferred Rp50000.00 to jane
Your new balance: Rp50000.00

# Logout
> logout
User 'john' logged out successfully

# Exit
> exit
Goodbye!
```