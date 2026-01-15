"""SQLAlchemy implementation of the User repository."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import InstrumentedAttribute

from ....domain.users.entities import User
from ....domain.users.repositories import IUserRepository
from .models import UserORM


class SQLAlchemyUserRepository(IUserRepository):
    """SQLAlchemy adapter for user persistence."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, user_id: UUID) -> User | None:
        return self._get_one_by(UserORM.id, user_id)

    def get_by_username(self, username: str) -> User | None:
        return self._get_one_by(UserORM.username, username)

    def get_by_email(self, email: str) -> User | None:
        return self._get_one_by(UserORM.email, email)

    def save(self, user: User) -> User:
        orm = self._to_orm(user)
        self._session.add(orm)
        self._session.flush()
        return self._to_entity(orm)

    def update(self, user: User) -> User:
        orm = self._session.scalars(select(UserORM).where(UserORM.id == user.id)).first()

        if not orm:
            raise ValueError(f"User with ID {user.id} not found")

        orm.username = user.username
        orm.email = user.email
        orm.first_name = user.first_name
        orm.last_name = user.last_name
        orm.phone_number = user.phone_number
        orm.profile_photo_url = user.profile_photo_url
        # registration_date is immutable

        self._session.flush()
        return self._to_entity(orm)

    def list_all(self, limit: int = 100, offset: int = 0) -> list[User]:
        stmt = select(UserORM).order_by(UserORM.username).limit(limit).offset(offset)
        return [self._to_entity(orm) for orm in self._session.scalars(stmt)]

    def count(self) -> int:
        return self._session.scalar(select(func.count()).select_from(UserORM)) or 0

    # --- Private helpers ---

    def _get_one_by[T](self, column: InstrumentedAttribute[T], value: T) -> User | None:
        """Fetch single user by column match."""
        orm = self._session.scalars(select(UserORM).where(column == value)).first()
        return self._to_entity(orm) if orm else None

    def _to_entity(self, orm: UserORM) -> User:
        """Map ORM to domain entity (anti-corruption layer)."""
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
        """Map domain entity to ORM."""
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
