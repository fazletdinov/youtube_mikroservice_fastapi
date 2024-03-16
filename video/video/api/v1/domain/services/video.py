import base64
import os
from abc import ABCMeta, abstractmethod
from typing import Any

from fastapi import Depends, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from video.api.v1.domain.repository.video import VideoDAL
from video.database.session import db_helper
from video.api.v1.schemas.video import CreateVideoSchema, UpdateVideoSchema
from video.api.v1.tasks.tasks import write_image, write_video


class VideoServiceBase(metaclass=ABCMeta):
    @abstractmethod
    async def create_video(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    async def get_video(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    async def update(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        pass


class VideoService(VideoServiceBase):
    def __init__(self, session: AsyncSession) -> None:
        self.db_session = session

    async def create_video(self, title: str, description: str, file: UploadFile, image: UploadFile) -> Any:
        video_crud = VideoDAL(self.db_session)
        username = "Idel"
        path_video = f"video/media/{username}/video"
        path_image = f"video/media/{username}/image"
        if not os.path.exists(path_video):
            os.makedirs(path_video)
        if not os.path.exists(path_image):
            os.makedirs(path_image)
        if file.content_type == "video/mp4" and image.content_type == "image/jpeg":
            video_raw_bytes = file.file.read()
            image_raw_bytes: bytes = image.file.read()
            video_base64: str = base64.b64encode(video_raw_bytes).decode()
            image_base64: str = base64.b64encode(image_raw_bytes).decode()
            write_video.delay(f"{path_video}/{title}.mp4", video_base64)
            write_image.delay(f"{path_image}/{title}.jpg", image_base64)
        else:
            raise HTTPException(
                status_code=status.HTTP_418_IM_A_TEAPOT,
                detail="Файл должен быть формата mp4, изображение формата jpg",
            )
        video_body = CreateVideoSchema(
            title=title,
            description=description,
            file=f"{path_video}/{title}.mp4",
            image=f"{path_image}/{title}.jpg",
        )
        return await video_crud.create(video_body)

    async def get_video(self, video_id: int) -> Any:
        video_crud = VideoDAL(self.db_session)
        video = await video_crud.get(video_id)
        if video is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="video not found")
        return video

    async def update(self, video_id: int, video_body: UpdateVideoSchema) -> Any:
        video_crud = VideoDAL(self.db_session)
        video = await video_crud.get(video_id)
        if video is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="video not found")
        return await video_crud.update(video_id, video_body)

    async def delete(self, video_id: int) -> Any:
        video_crud = VideoDAL(self.db_session)
        video = await video_crud.get(video_id)
        if video is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="video not found")
        return await video_crud.delete(video_id)


async def get_service_video(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> VideoService:
    return VideoService(session)
