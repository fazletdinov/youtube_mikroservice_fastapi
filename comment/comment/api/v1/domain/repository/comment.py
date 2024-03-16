from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, delete, Result
from fastapi import HTTPException, status

from comment.api.v1.schemas.comment import CommentSchemaRequest, CommentSchemaUpdate
from comment.database.models.comment import Comment


class CommentDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_uuid: UUID, video_uuid: UUID, body: CommentSchemaRequest) -> Comment:
        try:
            comment = Comment(user_uuid=user_uuid, video_uuid=video_uuid, text=body.text)
            self.session.add(comment)
            await self.session.commit()
            await self.session.refresh(comment)
            return comment
        except SQLAlchemyError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка SQLAlchemyError при создании Comment {error}",
            )

    async def update(self, user_uuid: UUID, video_uuid: UUID, comment_uuid: UUID, body: CommentSchemaUpdate) -> Comment:
        try:
            stmt = (
                update(Comment)
                .where(Comment.user_id == user_uuid, Comment.video_id == video_uuid, Comment.id == comment_uuid)
                .values(**body.model_dump())
                .returning(Comment)
            )

            result: Result[Comment] = await self.session.execute(stmt)
            await self.session.commit()
            comment = result.scalar()
            return comment
        except SQLAlchemyError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка SQLAlchemyError при обновлении Comment {error}",
            )

    async def delete(self, user_uuid: UUID, video_uuid: UUID, comment_uuid: UUID) -> UUID:
        try:
            stmt = (
                delete(Comment)
                .where(Comment.id == comment_uuid, Comment.user_id == user_uuid, Comment.video_id == video_uuid)
                .returning(Comment.id)
            )
            result: Result[UUID] = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar()
        except SQLAlchemyError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка SQLAlchemyError при удалении Comment {error}",
            )

    async def get_comments_from_video(self, video_uuid: UUID) -> list[Comment]:
        try:
            query = select(Comment).where(Comment.video_id == video_uuid)
            result: Result[list[Comment]] = await self.session.execute(query)
            return result.scalars()
        except SQLAlchemyError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка SQLAlchemyError при получении списка Comment {error}",
            )

    async def get_comments_from_users(self, user_uuid: UUID) -> list[Comment]:
        try:
            query = select(Comment).where(Comment.user_id == user_uuid)
            result: Result[list[Comment]] = await self.session.execute(query)
            return result.scalars()
        except SQLAlchemyError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка SQLAlchemyError при получении списка Comment {error}",
            )

    async def get(self, user_uuid: UUID, video_uuid: UUID, comment_uuid: UUID) -> Comment:
        try:
            query = select(Comment).where(
                Comment.id == comment_uuid, Comment.user_id == user_uuid, Comment.video_id == video_uuid
            )
            result: Result[Comment] = await self.session.execute(query)
            return result.scalars()
        except SQLAlchemyError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка SQLAlchemyError при получении Comment {error}",
            )
