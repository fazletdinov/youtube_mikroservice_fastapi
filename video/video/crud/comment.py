from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import Result, Row, delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from video.database.models.comment import Comment
from video.schemas.comment import CreateCommentSchema, UpdateCommentSchema

from .base_crud import CrudBase


class CommentDAL(CrudBase):
    def __init__(self, session: AsyncSession) -> None:
        self.db_session = session

    @override
    async def create(
        self, user_id: int, video_id: int, body_comment: CreateCommentSchema
    ) -> Row[tuple[Comment]] | None | Exception:
        try:
            new_comment = Comment(
                user_id=user_id, video_id=video_id, text=body_comment.text
            )
            self.db_session.add(new_comment)
            await self.db_session.commit()
            await self.db_session.refresh(new_comment)
            return await self.get(new_comment.id, new_comment.video_id)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка SQLAlchemyError при создании comment",
            )

    @override
    async def get(
        self, comment_id: int, video_id: int
    ) -> Row[tuple[Comment]] | None | Exception:
        try:
            query = select(Comment).where(
                Comment.id == comment_id, Comment.video_id == video_id
            )
            res: Result = await self.db_session.execute(query)
            comment: Row[tuple[Comment]] = res.fetchone()
            return comment
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка SQLAlchemyError при получении comment",
            )

    @override
    async def update(
        self,
        comment_id: int,
        user_id: int,
        video_id: int,
        body_comment: UpdateCommentSchema,
    ) -> Row[tuple[Comment]] | None | Exception:
        try:
            stmt = (
                update(Comment)
                .where(
                    Comment.id == comment_id,
                    Comment.user_id == user_id,
                    Comment.video_id == video_id,
                )
                .values(**body_comment.model_dump())
                .returning(Comment.id)
            )
            res: Result = await self.db_session.execute(stmt)
            updated_comment_id = res.scalar()
            return await self.get(updated_comment_id, video_id)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка SQLAlchemyError при обновлении comment",
            )

    @override
    async def delete(
        self, comment_id: int, user_id: int, video_id: int
    ) -> int | None | Exception:
        try:
            stmt = (
                delete(Comment)
                .where(
                    Comment.id == comment_id,
                    Comment.user_id == user_id,
                    Comment.video_id == video_id,
                )
                .returning(Comment.id)
            )
            res: Result = await self.db_session.execute(stmt)
            deleted_comment_id = res.scalar()
            return deleted_comment_id
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка SQLAlchemyError при удалении comment",
            )

    async def get_comments(
        self, video_id: int
    ) -> Sequence[Row[tuple[Comment]]] | None | Exception:
        try:
            query = select(Comment).where(Comment.video_id == video_id)
            res: Result = await self.db_session.execute(query)
            return res.scalars().all()
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка SQLAlchemyError",
            )
