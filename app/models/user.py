"""User and wallet related models."""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4

@dataclass
class Wallet:
    """Represents a user's wallet."""
    balance: Decimal = Decimal('0')

@dataclass
class User:
    """Represents a user in the system."""
    id: UUID
    name: str
    wallet: Wallet

    @classmethod
    def create(cls, name: str) -> 'User':
        """Create a new user with a generated ID and empty wallet."""
        return cls(
            id=uuid4(),
            name=name,
            wallet=Wallet()
        ) 