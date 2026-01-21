from abc import ABC, abstractmethod
from uuid import UUID

from .entities import Comment, Reaction


class ISocialRepository(ABC):
    @abstractmethod
    def add_reaction(self, reaction: Reaction) -> Reaction:
        pass

    @abstractmethod
    def add_comment(self, comment: Comment) -> Comment:
        pass

    @abstractmethod
    def get_comments_for_target(self, target_id: UUID) -> list[Comment]:
        pass
