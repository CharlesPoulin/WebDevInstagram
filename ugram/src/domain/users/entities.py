"""User domain entities with rich business logic and validation."""

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Self
from uuid import UUID, uuid4

from ..time_provider import ITimeProvider


@dataclass
class User:
    """User aggregate root containing identity and profile information.

    This entity represents a user in the system with all their profile data.
    It enforces business rules and invariants through validation methods.
    """

    id: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    registration_date: datetime
    phone_number: str | None = None
    profile_photo_url: str | None = None

    # Email validation regex (simplified)
    _EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    # Phone number validation (international format, simplified)
    _PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")

    def __post_init__(self) -> None:
        """Validate invariants after initialization."""
        self._validate_username()
        self._validate_email()
        if self.phone_number:
            self._validate_phone_number()

    @classmethod
    def create_new(
        cls,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        time_provider: ITimeProvider,
        phone_number: str | None = None,
        profile_photo_url: str | None = None,
    ) -> Self:
        """Factory method to create a new user with generated ID and registration date.

        Args:
            username: Unique username
            email: User's email address
            first_name: User's first name
            last_name: User's last name
            time_provider: Provider for current time (injected dependency)
            phone_number: Optional phone number
            profile_photo_url: Optional profile photo URL

        Returns:
            New User instance with generated ID and current registration date
        """
        return cls(
            id=uuid4(),
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            profile_photo_url=profile_photo_url,
            registration_date=time_provider.now(),
        )

    def update_profile(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        phone_number: str | None = None,
    ) -> None:
        """Update user profile fields with validation.

        Args:
            first_name: New first name
            last_name: New last name
            email: New email address
            phone_number: New phone number (can be None to remove)

        Raises:
            ValueError: If any validation fails
        """
        if first_name is not None:
            self.first_name = first_name

        if last_name is not None:
            self.last_name = last_name

        if email is not None:
            self.email = email
            self._validate_email()

        if phone_number is not None:
            self.phone_number = phone_number
            self._validate_phone_number()

    def update_profile_photo(self, photo_url: str | None) -> None:
        """Update profile photo URL."""
        self.profile_photo_url = photo_url

    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"

    def _validate_username(self) -> None:
        """Validate username follows business rules."""
        if not self.username:
            raise ValueError("Username cannot be empty")
        if len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if len(self.username) > 50:
            raise ValueError("Username must not exceed 50 characters")
        if not re.match(r"^[a-zA-Z0-9_]+$", self.username):
            raise ValueError("Username can only contain letters, numbers, and underscores")

    def _validate_email(self) -> None:
        """Validate email format."""
        if not self.email:
            raise ValueError("Email cannot be empty")
        if not self._EMAIL_REGEX.match(self.email):
            raise ValueError("Invalid email format")
        if len(self.email) > 100:
            raise ValueError("Email must not exceed 100 characters")

    def _validate_phone_number(self) -> None:
        """Validate phone number format if provided."""
        if self.phone_number and not self._PHONE_REGEX.match(self.phone_number):
            raise ValueError("Invalid phone number format. Use international format (e.g., +15551234567)")
