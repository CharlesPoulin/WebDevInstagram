import uuid

from sqlalchemy import String  # type: ignore
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column  # type: ignore


class Base(DeclarativeBase):  # type: ignore[misc]
    pass


class UserORM(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
