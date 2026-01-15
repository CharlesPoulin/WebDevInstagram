"""User domain service containing business logic and use cases."""

from uuid import UUID

from ..time_provider import ITimeProvider
from .entities import User
from .repositories import IUserRepository


class UserNotFoundError(Exception):
    """Raised when a user cannot be found."""

    pass


class UserAlreadyExistsError(Exception):
    """Raised when attempting to create a user that already exists."""

    pass


class UserService:
    """Domain service orchestrating user-related use cases.

    This service contains business logic that doesn't naturally fit
    within a single entity and coordinates repository operations.
    """

    def __init__(
        self, user_repo: IUserRepository, time_provider: ITimeProvider
    ) -> None:
        self.user_repo = user_repo
        self.time_provider = time_provider

    def get_user(self, user_id: UUID) -> User:
        """Get a user by ID.

        Args:
            user_id: The user's UUID

        Returns:
            The user

        Raises:
            UserNotFoundError: If user does not exist
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found")
        return user

    def get_user_by_username(self, username: str) -> User:
        """Get a user by username.

        Args:
            username: The username to search for

        Returns:
            The user

        Raises:
            UserNotFoundError: If user does not exist
        """
        user = self.user_repo.get_by_username(username)
        if not user:
            raise UserNotFoundError(f"User with username '{username}' not found")
        return user

    def create_user(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        phone_number: str | None = None,
        profile_photo_url: str | None = None,
    ) -> User:
        """Create a new user with validation.

        Args:
            username: Unique username
            email: User's email address
            first_name: User's first name
            last_name: User's last name
            phone_number: Optional phone number
            profile_photo_url: Optional profile photo URL

        Returns:
            The created user

        Raises:
            UserAlreadyExistsError: If username or email already exists
            ValueError: If validation fails
        """
        # Check uniqueness
        if self.user_repo.get_by_username(username):
            raise UserAlreadyExistsError(f"Username '{username}' already exists")

        if self.user_repo.get_by_email(email):
            raise UserAlreadyExistsError(f"Email '{email}' already exists")

        # Create user (validation happens in entity)
        user = User.create_new(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            time_provider=self.time_provider,
            phone_number=phone_number,
            profile_photo_url=profile_photo_url,
        )

        # Persist
        return self.user_repo.save(user)

    def update_user_profile(
        self,
        user_id: UUID,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        phone_number: str | None = None,
    ) -> User:
        """Update user profile information.

        Args:
            user_id: ID of the user to update
            first_name: New first name (optional)
            last_name: New last name (optional)
            email: New email (optional)
            phone_number: New phone number (optional)

        Returns:
            The updated user

        Raises:
            UserNotFoundError: If user does not exist
            UserAlreadyExistsError: If email is being changed to one that already exists
            ValueError: If validation fails
        """
        # Get existing user
        user = self.get_user(user_id)

        # Check email uniqueness if being changed
        if email and email != user.email:
            existing_user = self.user_repo.get_by_email(email)
            if existing_user and existing_user.id != user_id:
                raise UserAlreadyExistsError(f"Email '{email}' already in use")

        # Update profile (validation happens in entity)
        user.update_profile(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
        )

        # Persist changes
        return self.user_repo.update(user)

    def list_users(self, limit: int = 100, offset: int = 0) -> list[User]:
        """List all users with pagination.

        Args:
            limit: Maximum number of users to return (default 100, max 1000)
            offset: Number of users to skip (default 0)

        Returns:
            List of users

        Raises:
            ValueError: If limit or offset are invalid
        """
        if limit < 1 or limit > 1000:
            raise ValueError("Limit must be between 1 and 1000")
        if offset < 0:
            raise ValueError("Offset must be non-negative")

        return self.user_repo.list_all(limit=limit, offset=offset)

    def get_total_user_count(self) -> int:
        """Get total count of users.

        Returns:
            Total number of users
        """
        return self.user_repo.count()
