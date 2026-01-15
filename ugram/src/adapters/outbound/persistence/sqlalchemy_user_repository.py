"""SQLAlchemy implementation of User repository."""

from uuid import UUID

from sqlalchemy import select  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from ....domain.users.entities import User
from ....domain.users.repositories import IUserRepository
from .models import UserORM


class SQLAlchemyUserRepository(IUserRepository):
    """Concrete implementation of IUserRepository using SQLAlchemy.

    This adapter translates between domain entities and database models.
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, user_id: UUID) -> User | None:
        """Get user by ID from database."""
        stmt = select(UserORM).where(UserORM.id == user_id)
        user_orm = self.session.scalars(stmt).first()
        return self._to_entity(user_orm) if user_orm else None

    def get_by_username(self, username: str) -> User | None:
        """Get user by username from database."""
        stmt = select(UserORM).where(UserORM.username == username)
        user_orm = self.session.scalars(stmt).first()
        return self._to_entity(user_orm) if user_orm else None

    def get_by_email(self, email: str) -> User | None:
        """Get user by email from database."""
        stmt = select(UserORM).where(UserORM.email == email)
        user_orm = self.session.scalars(stmt).first()
        return self._to_entity(user_orm) if user_orm else None

    def save(self, user: User) -> User:
        """Save new user to database."""
        user_orm = self._to_orm(user)
        self.session.add(user_orm)
        self.session.flush()  # Flush to get generated fields
        return self._to_entity(user_orm)

    def update(self, user: User) -> User:
        """Update existing user in database."""
        stmt = select(UserORM).where(UserORM.id == user.id)
        user_orm = self.session.scalars(stmt).first()

        if not user_orm:
            raise ValueError(f"User with ID {user.id} not found")

        # Update fields
        user_orm.username = user.username
        user_orm.email = user.email
        user_orm.first_name = user.first_name
        user_orm.last_name = user.last_name
        user_orm.phone_number = user.phone_number
        user_orm.profile_photo_url = user.profile_photo_url
        # Note: registration_date should not be updated

        self.session.flush()
        return self._to_entity(user_orm)

    def list_all(self, limit: int = 100, offset: int = 0) -> list[User]:
        """List all users with pagination."""
        stmt = select(UserORM).limit(limit).offset(offset).order_by(UserORM.username)
        user_orms = self.session.scalars(stmt).all()
        return [self._to_entity(orm) for orm in user_orms]

    def count(self) -> int:
        """Get total count of users."""
        from sqlalchemy import func

        stmt = select(func.count()).select_from(UserORM)
        return self.session.scalar(stmt) or 0

    def _to_entity(self, orm: UserORM) -> User:
        """Convert ORM model to domain entity.

        This is the anti-corruption layer preventing database concerns
        from leaking into the domain.
        """
        return User(
            id=orm.id,
            username=orm.username,
            email=orm.email,
            first_name=orm.first_name,
            last_name=orm.last_name,
            phone_number=orm.phone_number,
            profile_photo_url=orm.profile_photo_url,
            registration_date=orm.registration_date,
        )

    def _to_orm(self, entity: User) -> UserORM:
        """Convert domain entity to ORM model."""
        return UserORM(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            first_name=entity.first_name,
            last_name=entity.last_name,
            phone_number=entity.phone_number,
            profile_photo_url=entity.profile_photo_url,
            registration_date=entity.registration_date,
        )
