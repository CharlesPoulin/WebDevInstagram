"""User API endpoints for profile management."""

from collections.abc import Generator
from contextlib import contextmanager
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ....application.dependencies import get_user_service
from ....application.dtos import (
    CreateUserRequest,
    UpdateUserProfileRequest,
    UserListResponse,
    UserProfileResponse,
)
from ....domain.users.entities import User
from ....domain.users.services import (
    UserAlreadyExistsError,
    UserNotFoundError,
    UserService,
)

router = APIRouter(prefix="/users", tags=["users"])

# Type alias for dependency injection
UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@contextmanager
def handle_user_exceptions() -> Generator[None]:
    """Map domain exceptions to appropriate HTTP responses."""
    try:
        yield
    except UserNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e)) from e
    except UserAlreadyExistsError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e)) from e
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e)) from e


def _to_response(user: User) -> UserProfileResponse:
    """Map domain entity to API response."""
    return UserProfileResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        profile_photo_url=user.profile_photo_url,
        registration_date=user.registration_date,
    )


@router.post(
    "",
    response_model=UserProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user. Username and email must be unique.",
)
def create_user(request: CreateUserRequest, service: UserServiceDep) -> UserProfileResponse:
    """Create user with the provided profile data."""
    with handle_user_exceptions():
        user = service.create_user(
            username=request.username,
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            phone_number=request.phone_number,
            profile_photo_url=request.profile_photo_url,
        )
        return _to_response(user)


@router.get(
    "",
    response_model=UserListResponse,
    summary="List all users",
    description="Paginated user list. Default limit: 20, max: 100.",
)
def list_users(
    service: UserServiceDep,
    limit: int = Query(20, ge=1, le=100, description="Max users to return"),
    offset: int = Query(0, ge=0, description="Users to skip"),
) -> UserListResponse:
    """Return paginated list of users."""
    users = service.list_users(limit=limit, offset=offset)
    return UserListResponse(
        users=[_to_response(u) for u in users],
        total=service.get_total_user_count(),
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{user_id}",
    response_model=UserProfileResponse,
    summary="Get user by ID",
    description="Retrieve profile for a specific user.",
)
def get_user(user_id: UUID, service: UserServiceDep) -> UserProfileResponse:
    """Fetch user by ID or raise 404."""
    with handle_user_exceptions():
        return _to_response(service.get_user(user_id))


@router.put(
    "/{user_id}",
    response_model=UserProfileResponse,
    summary="Update user profile",
    description="Partial update of user profile fields.",
)
def update_user_profile(
    user_id: UUID,
    request: UpdateUserProfileRequest,
    service: UserServiceDep,
) -> UserProfileResponse:
    """Update user profile with provided fields."""
    with handle_user_exceptions():
        user = service.update_user_profile(
            user_id=user_id,
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            phone_number=request.phone_number,
        )
        return _to_response(user)
