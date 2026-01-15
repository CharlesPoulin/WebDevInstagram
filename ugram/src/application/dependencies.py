"""Dependency injection container for FastAPI.

This module wires together infrastructure adapters and domain services,
following the dependency inversion principle.
"""

from fastapi import Depends
from sqlalchemy.orm import Session  # type: ignore
from collections.abc import Generator

from ..adapters.outbound.persistence.database import get_db
from ..adapters.outbound.persistence.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from ..adapters.outbound.time_provider import SystemTimeProvider
from ..domain.time_provider import ITimeProvider
from ..domain.images.services import ImageService
from ..domain.social.services import SocialService
from ..domain.users.services import UserService


def get_time_provider() -> ITimeProvider:
    """Dependency provider for TimeProvider.

    Returns:
        SystemTimeProvider instance for production use
    """
    return SystemTimeProvider()


def get_user_service(
    db: Session = Depends(get_db),
    time_provider: ITimeProvider = Depends(get_time_provider),
) -> UserService:
    """Dependency provider for UserService.

    Args:
        db: Database session injected by FastAPI
        time_provider: Time provider injected by FastAPI

    Returns:
        Configured UserService with repository and time provider
    """
    user_repo = SQLAlchemyUserRepository(db)
    return UserService(user_repo, time_provider)


def get_image_service() -> ImageService:
    """Dependency provider for ImageService."""
    raise NotImplementedError


def get_social_service() -> SocialService:
    """Dependency provider for SocialService."""
    raise NotImplementedError
