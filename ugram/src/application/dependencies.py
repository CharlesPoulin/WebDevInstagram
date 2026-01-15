from ..domain.images.services import ImageService
from ..domain.social.services import SocialService
from ..domain.users.services import UserService

# In a real app, you'd initialize repositories here and inject them


def get_user_service() -> UserService:
    # Use cases for injection
    raise NotImplementedError


def get_image_service() -> ImageService:
    raise NotImplementedError


def get_social_service() -> SocialService:
    raise NotImplementedError
