from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Video(Base):
    title: Mapped[str] = mapped_column(String(length=50))
    description: Mapped[str] = mapped_column(String(length=500))
    file: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc), server_default=func.now()
    )
    image: Mapped[str]
    comments_id: Mapped[list[UUID]]

    def __repr__(self) -> str:
        return f"Video - ({self.id}, {self.title})"
