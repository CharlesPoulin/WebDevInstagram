from uuid import UUID

from fastapi import APIRouter, Depends

from ....application.dependencies import get_user_service
from ....domain.users.entities import User
from ....domain.users.services import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}")
def get_user(user_id: UUID, service: UserService = Depends(get_user_service)) -> User:
    return service.get_user(user_id)
