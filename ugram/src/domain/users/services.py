from uuid import UUID

from .entities import User
from .repositories import IUserRepository


class UserService:
    def __init__(self, user_repo: IUserRepository) -> None:
        self.user_repo = user_repo

    def get_user(self, user_id: UUID) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user
