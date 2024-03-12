from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .comment import Comment


class Video(Base):
    __tablename__ = "video"

    title: Mapped[str] = mapped_column(String(length=50))
    description: Mapped[str] = mapped_column(String(length=500))
    file: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, server_default=func.now()
    )
    image: Mapped[str]
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="video", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"Video - ({self.id}, {self.title})"
