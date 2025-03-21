"""Repositories package for the application."""

from .user_repository import UserRepository, InMemoryUserRepository

__all__ = ['UserRepository', 'InMemoryUserRepository'] 