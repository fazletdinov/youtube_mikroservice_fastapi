from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Comment(Base):
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc), server_default=func.now()
    )
    user_id: Mapped[UUID]
    video_id: Mapped[UUID]

    def __repr__(self) -> str:
        return f"Comment - ({self.id})"
