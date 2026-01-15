from abc import ABC, abstractmethod
from uuid import UUID

from .entities import User


class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: UUID) -> User | None:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass
