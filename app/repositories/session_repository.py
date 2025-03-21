"""Session repository for managing user sessions."""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.models.session import Session
from app.models.user import User

class SessionRepository(ABC):
    """Abstract base class for session repositories."""
    
    @abstractmethod
    def save(self, session: Session) -> None:
        """Save a session."""
        pass
    
    @abstractmethod
    def find_by_user_name(self, username: str) -> Optional[Session]:
        """Find a session by username."""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all sessions."""
        pass

class InMemorySessionRepository(SessionRepository):
    """In-memory implementation of the session repository."""
    
    def __init__(self):
        self._session: Optional[Session] = None
    
    def save(self, session: Session) -> None:
        """Save a session, replacing any existing one."""
        self._session = session
    
    def find_by_user_name(self, username: str) -> Optional[Session]:
        """Find a session by username."""
        if self._session and self._session.user.name.lower() == username.lower():
            return self._session
        return None
    
    def clear(self) -> None:
        """Clear all sessions."""
        self._session = None 