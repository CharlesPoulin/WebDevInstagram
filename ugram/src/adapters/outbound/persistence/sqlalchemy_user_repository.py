from uuid import UUID

from sqlalchemy.orm import Session  # type: ignore

from ....domain.users.entities import User
from ....domain.users.repositories import IUserRepository


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, user_id: UUID) -> User | None:
        # implementation using sqlalchemy
        raise NotImplementedError

    def get_by_username(self, username: str) -> User | None:
        raise NotImplementedError

    def save(self, user: User) -> User:
        raise NotImplementedError
