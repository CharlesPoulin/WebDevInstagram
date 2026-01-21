from abc import ABC, abstractmethod
from uuid import UUID

from .entities import Image


class IImageRepository(ABC):
    @abstractmethod
    def save(self, image: Image) -> Image:
        pass

    @abstractmethod
    def get_by_id(self, image_id: UUID) -> Image | None:
        pass

    @abstractmethod
    def list_by_owner(self, owner_id: UUID) -> list[Image]:
        pass
