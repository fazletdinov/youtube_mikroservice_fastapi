from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from comment.api.v1.domain.services.comment import CommentService
from comment.api.v1.controller.comment import CommentController
from comment.database.session import db_helper


async def get_comment_service(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
) -> CommentService:
    return CommentService(session)


async def get_comment_controller(service: Annotated[CommentService, Depends(get_comment_service)]) -> CommentController:
    return CommentController(service)
