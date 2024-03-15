from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Role(str, Enum):
    USER = "user"
    MODERATOR = "moderator"


class User(Base):
    email: Mapped[str] = mapped_column(String(length=100), unique=True)
    password: Mapped[bytes]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    role: Mapped[Role] = mapped_column(default=Role.USER)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), server_default=func.now())

    def __repr__(self) -> str:
        return f"User - ({self.id}, {self.email})"
