from uuid import UUID

from .entities import Comment
from .repositories import ISocialRepository


class SocialService:
    def __init__(self, social_repo: ISocialRepository) -> None:
        self.social_repo = social_repo

    def post_comment(self, user_id: UUID, target_id: UUID, content: str) -> Comment:
        # Business logic for posting comment
        raise NotImplementedError
