from fastapi import APIRouter, Depends

from ....application.dependencies import get_social_service
from ....domain.social.services import SocialService

router = APIRouter(prefix="/social", tags=["social"])


@router.post("/comment")
def post_comment(service: SocialService = Depends(get_social_service)) -> None:
    # logic for posting comment
    pass
