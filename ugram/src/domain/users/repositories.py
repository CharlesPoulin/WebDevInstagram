"""User repository port (interface) for persistence operations."""

from abc import ABC, abstractmethod
from uuid import UUID

from .entities import User


class IUserRepository(ABC):
    """Repository interface defining persistence operations for User aggregate.

    This is a port in hexagonal architecture - the infrastructure layer
    will provide the concrete implementation (adapter).
    """

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> User | None:
        """Retrieve a user by their unique identifier.

        Args:
            user_id: The user's UUID

        Returns:
            User if found, None otherwise
        """
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        """Retrieve a user by their username.

        Args:
            username: The user's username

        Returns:
            User if found, None otherwise
        """
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address.

        Args:
            email: The user's email

        Returns:
            User if found, None otherwise
        """
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        """Persist a new user to the repository.

        Args:
            user: The user to save

        Returns:
            The saved user with any generated fields populated
        """
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Update an existing user in the repository.

        Args:
            user: The user with updated fields

        Returns:
            The updated user

        Raises:
            ValueError: If user does not exist
        """
        pass

    @abstractmethod
    def list_all(self, limit: int = 100, offset: int = 0) -> list[User]:
        """List all users with pagination.

        Args:
            limit: Maximum number of users to return (default 100)
            offset: Number of users to skip (default 0)

        Returns:
            List of users
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """Get total count of users.

        Returns:
            Total number of users in the repository
        """
        pass
