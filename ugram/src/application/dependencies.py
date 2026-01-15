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
from ..domain.images.services import ImageService
from ..domain.social.services import SocialService
from ..domain.users.services import UserService


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependency provider for UserService.

    Args:
        db: Database session injected by FastAPI

    Returns:
        Configured UserService with repository
    """
    user_repo = SQLAlchemyUserRepository(db)
    return UserService(user_repo)


def get_image_service() -> ImageService:
    """Dependency provider for ImageService."""
    raise NotImplementedError


def get_social_service() -> SocialService:
    """Dependency provider for SocialService."""
    raise NotImplementedError
