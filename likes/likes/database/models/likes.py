import enum
import uuid

from uuid import uuid4

from sqlalchemy import SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from likes.database.models.base import Base  # noqa


class Reaction(Base):
    """Модель для представление сущности реакция"""

    class Type(enum.IntEnum):
        """Перечисление для типа реакции"""

        LIKE = 1
        DISLIKE = 2

    __tablename__ = "reaction"
    reaction_uuid: Mapped[uuid.UUID] = mapped_column(default=uuid4)
    idea_uuid: Mapped[uuid.UUID]
    user_uuid: Mapped[uuid.UUID]
    type_reaction: Mapped[Type] = mapped_column(SmallInteger)
