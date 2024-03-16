from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from likes.api.v1.schemas.reaction import ReactionSchemaRequest, ReactionSchemaResponse, ReactionSchemaUpdate
from likes.api.v1.domain.repository.reaction import ReactionDAL


class ReactionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_reaction(
        self, user_uuid: UUID, video_uuid: UUID, body: ReactionSchemaRequest
    ) -> ReactionSchemaResponse:
        reaction_crud = ReactionDAL(self.session)
        reaction = await reaction_crud.create(user_uuid, video_uuid, body)
        return ReactionSchemaResponse.model_validate(reaction)

    async def get_reaction_list(self, video_uuid: UUID) -> list[ReactionSchemaResponse]:
        reaction_crud = ReactionDAL(self.session)
        reaction_list = await reaction_crud.get(video_uuid)
        return [ReactionSchemaResponse.model_validate(reaction) for reaction in reaction_list]

    async def update_reaction(
        self, user_uuid: UUID, video_uuid: UUID, body: ReactionSchemaUpdate
    ) -> ReactionSchemaResponse:
        reaction_crud = ReactionDAL(self.session)
        reaction = await reaction_crud.update(user_uuid, video_uuid, body)
        return ReactionSchemaResponse.model_validate(reaction)

    async def delete_reaction(self, user_uuid: UUID, video_uuid: UUID) -> UUID:
        reaction_crud = ReactionDAL(self.session)
        reaction_uuid = await reaction_crud.delete(user_uuid, video_uuid)
        return reaction_uuid
