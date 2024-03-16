from asyncio import current_task
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from comment.core.config import settings


@dataclass
class DDHelper:
    url: str
    echo: bool

    def __post_init__(self):
        self.engine = create_async_engine(url=self.url, echo=self.echo)
        self.factory_session = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autoflush=False,
        )

    async def scoped_session_dependency(self):
        scoped_factory = async_scoped_session(
            self.factory_session,
            scopefunc=current_task,
        )
        try:
            async with scoped_factory() as session:
                yield session
        finally:
            await scoped_factory.remove()


db_helper = DDHelper(
    url=settings.db.async_url,
    echo=settings.db.echo,
)
