from uuid import UUID

from likes.api.v1.schemas.reaction import ReactionSchemaRequest, ReactionSchemaResponse, ReactionSchemaUpdate
from likes.api.v1.domain.services.reaction import ReactionService


class ReactionController:
    def __init__(self, service: ReactionService) -> None:
        self.service = service

    async def view_create(
        self, user_uuid: UUID, video_uuid: UUID, body: ReactionSchemaRequest
    ) -> ReactionSchemaResponse:
        return await self.service.create_reaction(user_uuid, video_uuid, body)

    async def view_get_reaction_list(self, video_uuid: UUID) -> list[ReactionSchemaResponse]:
        return await self.service.get_reaction_list(video_uuid)

    async def view_update_reaction(
        self, user_uuid: UUID, video_uuid: UUID, body: ReactionSchemaUpdate
    ) -> ReactionSchemaResponse:
        return await self.service.update_reaction(user_uuid, video_uuid, body)

    async def view_delete_reaction(self, user_uuid: UUID, video_uuid: UUID) -> UUID:
        return await self.service.delete_reaction(user_uuid, video_uuid)
