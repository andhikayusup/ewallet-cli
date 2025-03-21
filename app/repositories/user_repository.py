"""User repository for data persistence."""
from abc import ABC, abstractmethod
from typing import Dict, Optional
from uuid import UUID

from app.models.user import User

class UserRepository(ABC):
    """Abstract base class for user repositories."""
    
    @abstractmethod
    def save(self, user: User) -> None:
        """Save a user to the repository."""
        pass
    
    @abstractmethod
    def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Find a user by their ID."""
        pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[User]:
        """Find a user by their name."""
        pass

class InMemoryUserRepository(UserRepository):
    """In-memory implementation of the user repository."""
    
    def __init__(self):
        self._users: Dict[UUID, User] = {}
        self._names: Dict[str, UUID] = {}
    
    def save(self, user: User) -> None:
        """Save a user to the in-memory storage."""
        self._users[user.id] = user
        self._names[user.name.lower()] = user.id
    
    def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Find a user by their ID."""
        return self._users.get(user_id)
    
    def find_by_name(self, name: str) -> Optional[User]:
        """Find a user by their name."""
        user_id = self._names.get(name.lower())
        if user_id:
            return self._users.get(user_id)
        return None 