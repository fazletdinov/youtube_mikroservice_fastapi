from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, Depends

from comment.core.config import settings
from comment.api.v1.controller.comment import CommentController
from comment.api.v1.depends.comment import get_comment_controller
from comment.api.v1.schemas.comment import CommentSchemaRequest, CommentSchemaResponse, CommentSchemaUpdate


comment_router = APIRouter(tags=["Comment"], prefix=settings.app.API_V1_STR)


@comment_router.post("/comment", response_model=CommentSchemaResponse)
async def create_comment(
    user_uuid: Annotated[UUID, Query()],
    video_uuid: Annotated[UUID, Query()],
    body: CommentSchemaRequest,
    controller: Annotated[CommentController, Depends(get_comment_controller)],
) -> CommentSchemaResponse:
    return await controller.view_create_comment(user_uuid, video_uuid, body)


@comment_router.patch("/comment", response_model=CommentSchemaResponse)
async def update_comment(
    user_uuid: Annotated[UUID, Query()],
    video_uuid: Annotated[UUID, Query()],
    comment_uuid: Annotated[UUID, Query()],
    body: CommentSchemaUpdate,
    controller: Annotated[CommentController, Depends(get_comment_controller)],
) -> CommentSchemaResponse:
    return await controller.view_update_comment(user_uuid, video_uuid, comment_uuid, body)


@comment_router.delete("/comment")
async def delete_comment(
    user_uuid: Annotated[UUID, Query()],
    video_uuid: Annotated[UUID, Query()],
    comment_uuid: Annotated[UUID, Query()],
    controller: Annotated[CommentController, Depends(get_comment_controller)],
) -> CommentSchemaResponse:
    return await controller.view_delete_comment(user_uuid, video_uuid, comment_uuid)


@comment_router.get("/comment/{comment_uuid}", response_model=CommentSchemaResponse)
async def get_comment(
    user_uuid: Annotated[UUID, Query()],
    video_uuid: Annotated[UUID, Query()],
    comment_uuid: UUID,
    controller: Annotated[CommentController, Depends(get_comment_controller)],
) -> CommentSchemaResponse:
    return await controller.view_get_comment(user_uuid, video_uuid, comment_uuid)


@comment_router.get("/comment", response_model=list[CommentSchemaResponse])
async def get_comments_video(
    video_uuid: Annotated[UUID, Query()], controller: Annotated[CommentController, Depends(get_comment_controller)]
) -> CommentSchemaResponse:
    return await controller.view_get_comments_from_video(video_uuid)


@comment_router.get("/comment", response_model=list[CommentSchemaResponse])
async def get_comments_users(
    user_uuid: Annotated[UUID, Query()], controller: Annotated[CommentController, Depends(get_comment_controller)]
) -> CommentSchemaResponse:
    return await controller.view_get_comments_from_users(user_uuid)
