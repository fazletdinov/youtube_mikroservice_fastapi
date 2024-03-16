import enum
import uuid

from uuid import uuid4

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint

from likes.database.models.base import Base  # noqa


class Type(enum.IntEnum):
    """Перечисление для типа реакции"""

    LIKE = 1
    DISLIKE = 2


class Reaction(Base):
    """Модель для представление сущности реакция"""

    reaction_uuid: Mapped[uuid.UUID] = mapped_column(default=uuid4)
    video_uuid: Mapped[uuid.UUID]
    user_uuid: Mapped[uuid.UUID]
    type_reaction: Mapped[Type]
    UniqueConstraint("user_uuid", "video_uuid", name="unique_user_video")
