from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    id: UUID
    username: str
    email: str


@dataclass
class UserProfile:
    user_id: UUID
    bio: str | None = None
    avatar_url: str | None = None
