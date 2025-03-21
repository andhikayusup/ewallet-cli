"""Session model for user authentication."""
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from .user import User

@dataclass
class Session:
    """Represents a user session."""
    id: UUID
    user: User
    created_at: datetime

    @classmethod
    def create(cls, user: User) -> 'Session':
        """Create a new session for a user."""
        return cls(
            id=uuid4(),
            user=user,
            created_at=datetime.now()
        ) 