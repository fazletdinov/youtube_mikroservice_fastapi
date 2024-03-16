from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from likes.api.v1.depends.reaction import get_reaction_controller
from likes.api.v1.schemas.reaction import ReactionSchemaRequest, ReactionSchemaResponse, ReactionSchemaUpdate
from likes.api.v1.controller.reaction import ReactionController
from likes.core.config import settings

likes_router = APIRouter(tags=["Likes"], prefix=settings.app.API_V1_STR)


@likes_router.post("/reaction", response_model=ReactionSchemaResponse)
async def create_reaction(
    user_uuid: Annotated[UUID, Query()],
    video_uuid: Annotated[UUID, Query()],
    body: ReactionSchemaRequest,
    controller: Annotated[ReactionController, Depends(get_reaction_controller)],
) -> ReactionSchemaResponse:
    return await controller.view_create(user_uuid, video_uuid, body)


@likes_router.get("/reaction", response_model=ReactionSchemaResponse)
async def get_reactions(
    video_uuid: Annotated[UUID, Query()],
    body: ReactionSchemaRequest,
    controller: Annotated[ReactionController, Depends(get_reaction_controller)],
) -> ReactionSchemaResponse:
    return await controller.view_get_reaction_list(video_uuid, body)


@likes_router.put("/reaction", response_model=ReactionSchemaResponse)
async def update_reaction(
    user_uuid: Annotated[UUID, Query()],
    video_uuid: Annotated[UUID, Query()],
    body: ReactionSchemaUpdate,
    controller: Annotated[ReactionController, Depends(get_reaction_controller)],
) -> ReactionSchemaResponse:
    return await controller.view_update_reaction(user_uuid, video_uuid, body)


@likes_router.delete("/reaction")
async def delete_reaction(
    user_uuid: Annotated[UUID, Query()],
    video_uuid: Annotated[UUID, Query()],
    controller: Annotated[ReactionController, Depends(get_reaction_controller)],
) -> ReactionSchemaResponse:
    return await controller.view_delete_reaction(user_uuid, video_uuid)
