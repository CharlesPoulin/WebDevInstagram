from uuid import UUID

from .entities import Image
from .repositories import IImageRepository


class ImageService:
    def __init__(self, image_repo: IImageRepository) -> None:
        self.image_repo = image_repo

    def upload_image(self, owner_id: UUID, url: str) -> Image:
        # Business logic for image upload would go here
        raise NotImplementedError
