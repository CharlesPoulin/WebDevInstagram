"""API request/response DTOs for HTTP boundary."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserProfileResponse(BaseModel):
    """User profile data returned by API."""

    id: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    phone_number: str | None
    profile_photo_url: str | None
    registration_date: datetime

    model_config = ConfigDict(
        from_attributes=True,  # Allow creating from ORM models
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "johndoe",
                "email": "[email protected]",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+15551234567",
                "profile_photo_url": "https://example.com/photos/john.jpg",
                "registration_date": "2026-01-14T10:30:00Z",
            }
        },
    )


class UpdateUserProfileRequest(BaseModel):
    """Partial update - only provided fields are changed."""

    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None
    phone_number: str | None = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v: str | None) -> str | None:
        """Validate phone number format."""
        if v and not v.startswith("+"):
            # Optionally auto-format to international format
            pass
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "[email protected]",
                "phone_number": "+15551234567",
            }
        }
    )


class CreateUserRequest(BaseModel):
    """Request DTO for creating a new user."""

    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone_number: str | None = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")
    profile_photo_url: str | None = Field(None, max_length=500)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "[email protected]",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+15551234567",
            }
        }
    )


class UserListResponse(BaseModel):
    """Response DTO for paginated list of users."""

    users: list[UserProfileResponse]
    total: int
    limit: int
    offset: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "users": [],
                "total": 100,
                "limit": 20,
                "offset": 0,
            }
        }
    )
