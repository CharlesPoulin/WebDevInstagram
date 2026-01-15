"""SQLAlchemy ORM models for database persistence."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String  # type: ignore
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column  # type: ignore


class Base(DeclarativeBase):  # type: ignore[misc]
    """Base class for all ORM models."""

    pass


class UserORM(Base):
    """ORM model for users table.

    This is the infrastructure concern - mapping domain entities to database tables.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    profile_photo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    registration_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
