from typing import Annotated

from fastapi import APIRouter, Depends

from ....application.dependencies import get_image_service
from ....domain.images.services import ImageService

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/")
def upload_image(
    service: Annotated[ImageService, Depends(get_image_service)],
) -> None:
    # logic for image upload
    pass
