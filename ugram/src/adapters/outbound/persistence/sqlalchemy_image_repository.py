from uuid import UUID

from sqlalchemy.orm import Session  # type: ignore

from ....domain.images.entities import Image
from ....domain.images.repositories import IImageRepository


class SQLAlchemyImageRepository(IImageRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, image: Image) -> Image:
        raise NotImplementedError

    def get_by_id(self, image_id: UUID) -> Image | None:
        raise NotImplementedError

    def list_by_owner(self, owner_id: UUID) -> list[Image]:
        raise NotImplementedError
