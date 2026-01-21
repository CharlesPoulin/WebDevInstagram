"""FastAPI dependency injection wiring.

Connects infrastructure adapters to domain services via dependency inversion.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session  # type: ignore

from ..adapters.outbound.persistence.database import get_db
from ..adapters.outbound.persistence.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from ..adapters.outbound.time_provider import SystemTimeProvider
from ..domain.images.services import ImageService
from ..domain.social.services import SocialService
from ..domain.time_provider import ITimeProvider
from ..domain.users.services import UserService

# Type alias for database session injection
DbSession = Annotated[Session, Depends(get_db)]


def get_time_provider() -> ITimeProvider:
    """Production time provider."""
    return SystemTimeProvider()


# Type alias for time provider injection (defined after get_time_provider)
TimeProviderDep = Annotated[ITimeProvider, Depends(get_time_provider)]


def get_user_service(db: DbSession, time_provider: TimeProviderDep) -> UserService:
    """Wire UserService with SQLAlchemy repository."""
    return UserService(SQLAlchemyUserRepository(db), time_provider)


def get_image_service() -> ImageService:
    """Placeholder - not yet implemented."""
    raise NotImplementedError


def get_social_service() -> SocialService:
    """Placeholder - not yet implemented."""
    raise NotImplementedError
