"""User domain service containing business logic and use cases."""

from uuid import UUID

from ..time_provider import ITimeProvider
from .entities import User
from .repositories import IUserRepository


class UserNotFoundError(Exception):
    """User lookup failed."""


class UserAlreadyExistsError(Exception):
    """Username or email already taken."""


class UserService:
    """Orchestrates user-related use cases and enforces business rules."""

    def __init__(self, user_repo: IUserRepository, time_provider: ITimeProvider) -> None:
        self._repo = user_repo
        self._time = time_provider

    def get_user(self, user_id: UUID) -> User:
        """Fetch user by ID or raise UserNotFoundError."""
        user = self._repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found")
        return user

    def get_user_by_username(self, username: str) -> User:
        """Fetch user by username or raise UserNotFoundError."""
        user = self._repo.get_by_username(username)
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
        """Create user after validating uniqueness constraints."""
        if self._repo.get_by_username(username):
            raise UserAlreadyExistsError(f"Username '{username}' already exists")
        if self._repo.get_by_email(email):
            raise UserAlreadyExistsError(f"Email '{email}' already exists")

        user = User.create_new(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            time_provider=self._time,
            phone_number=phone_number,
            profile_photo_url=profile_photo_url,
        )
        return self._repo.save(user)

    def update_user_profile(
        self,
        user_id: UUID,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        phone_number: str | None = None,
    ) -> User:
        """Partial update of profile fields with email uniqueness check."""
        user = self.get_user(user_id)

        if email and email != user.email:
            existing = self._repo.get_by_email(email)
            if existing and existing.id != user_id:
                raise UserAlreadyExistsError(f"Email '{email}' already in use")

        user.update_profile(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
        )
        return self._repo.update(user)

    def list_users(self, limit: int = 100, offset: int = 0) -> list[User]:
        """Paginated user list. Limit: 1-1000."""
        if not 1 <= limit <= 1000:
            raise ValueError("Limit must be between 1 and 1000")
        if offset < 0:
            raise ValueError("Offset must be non-negative")
        return self._repo.list_all(limit=limit, offset=offset)

    def get_total_user_count(self) -> int:
        """Total user count for pagination metadata."""
        return self._repo.count()
