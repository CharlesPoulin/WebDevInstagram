"""User profile API endpoints.

This module provides RESTful endpoints for user profile management.
"""

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


def _user_to_response(user: User) -> UserProfileResponse:
    """Convert domain User entity to response DTO."""
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
    description=("Create a new user with profile information. Username and email must be unique."),
)
def create_user(
    request: CreateUserRequest,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserProfileResponse:
    """Create a new user.

    Args:
        request: User creation request data
        service: Injected user service

    Returns:
        Created user profile

    Raises:
        HTTPException: 409 if username or email already exists, 400 for errors
    """
    try:
        user = service.create_user(
            username=request.username,
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            phone_number=request.phone_number,
            profile_photo_url=request.profile_photo_url,
        )
        return _user_to_response(user)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.get(
    "",
    response_model=UserListResponse,
    summary="List all users",
    description=("Get a paginated list of all users. Default limit is 20, maximum is 100."),
)
def list_users(
    service: Annotated[UserService, Depends(get_user_service)],
    limit: int = Query(20, ge=1, le=100, description="Number of users to return"),
    offset: int = Query(0, ge=0, description="Number of users to skip"),
) -> UserListResponse:
    """List all users with pagination.

    Args:
        limit: Maximum number of users to return (1-100)
        offset: Number of users to skip
        service: Injected user service

    Returns:
        Paginated list of users with total count
    """
    users = service.list_users(limit=limit, offset=offset)
    total = service.get_total_user_count()

    return UserListResponse(
        users=[_user_to_response(user) for user in users],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{user_id}",
    response_model=UserProfileResponse,
    summary="Get user by ID",
    description="Retrieve detailed profile information for a specific user.",
)
def get_user(
    user_id: UUID,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserProfileResponse:
    """Get a user's profile by their ID.

    Args:
        user_id: UUID of the user
        service: Injected user service

    Returns:
        User profile information

    Raises:
        HTTPException: 404 if user not found
    """
    try:
        user = service.get_user(user_id)
        return _user_to_response(user)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.put(
    "/{user_id}",
    response_model=UserProfileResponse,
    summary="Update user profile",
    description=("Update profile information for a user. Only provided fields will be updated."),
)
def update_user_profile(
    user_id: UUID,
    request: UpdateUserProfileRequest,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserProfileResponse:
    """Update a user's profile.

    Args:
        user_id: UUID of the user to update
        request: Profile update request data
        service: Injected user service

    Returns:
        Updated user profile

    Raises:
        HTTPException: 404 if user not found, 409 if email already in use,
                      400 for validation errors
    """
    try:
        user = service.update_user_profile(
            user_id=user_id,
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            phone_number=request.phone_number,
        )
        return _user_to_response(user)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
