from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Image:
    id: UUID
    owner_id: UUID
    url: str
    created_at: datetime


@dataclass
class ImageMetadata:
    image_id: UUID
    width: int
    height: int
    format: str
