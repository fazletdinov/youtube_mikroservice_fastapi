from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from likes.api.v1.domain.services.reaction import ReactionService
from likes.api.v1.controller.reaction import ReactionController
from likes.database.session import db_helper


async def get_reaction_service(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
) -> ReactionService:
    return ReactionService(session)


async def get_reaction_controller(
    service: Annotated[ReactionService, Depends(get_reaction_service)],
) -> ReactionController:
    return ReactionController(service)
