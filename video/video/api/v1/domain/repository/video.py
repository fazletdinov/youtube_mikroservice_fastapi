from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import Result, delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from video.database.models.video import Video
from video.api.v1.schemas.video import CreateVideoSchema, UpdateVideoSchema

from .base_crud import CrudBase


class VideoDAL(CrudBase):
    def __init__(self, session: AsyncSession) -> None:
        self.db_session = session

    @override
    async def create(self, video_body: CreateVideoSchema):
        try:
            video = Video(
                title=video_body.title,
                description=video_body.description,
                file=video_body.file,
                image=video_body.image,
            )
            self.db_session.add(video)
            await self.db_session.commit()
            await self.db_session.refresh(video)
            return video
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка SQLAlchemyError при создании video",
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Неизвестная ошибка при создании video",
            )

    @override
    async def get(self, video_id):
        try:
            query = select(Video).where(Video.id == video_id)
            res: Result = await self.db_session.execute(query)  # type: ignore
            video = res.scalar()
            return video
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка SQLAlchemyError при получении video",
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Неизвестная ошибка при получении video",
            )

    @override
    async def update(self, video_id: int, update_body_video: UpdateVideoSchema):
        try:
            stmt = (
                update(Video).where(Video.id == video_id).values(**update_body_video.model_dump()).returning(Video.id)
            )
            res: Result = await self.db_session.execute(stmt)
            await self.db_session.commit()
            video = await self.db_session.get(Video, res.scalar())
            return video
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка SQLAlchemyError при обновлении video",
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Неизвестная ошибка при обновлении video",
            )

    @override
    async def delete(self, video_id: int) -> Any:
        try:
            stmt = delete(Video).where(Video.id == video_id).returning(Video.id)
            res: Result = await self.db_session.execute(stmt)
            await self.db_session.commit()
            return res.scalar()
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка SQLAlchemyError при удалении video",
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Неизвестная ошибка при удалении video",
            )

    async def get_list(self):
        try:
            query = select(Video)
            res: Result = await self.db_session.execute(query)  # type: ignore
            videos = res.scalars().all()
            return videos

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка SQLAlchemyError при получении списка video",
            )

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Неизвестная ошибка при получении списка video",
            )
