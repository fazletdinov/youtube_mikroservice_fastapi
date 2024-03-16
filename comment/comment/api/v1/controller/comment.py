from uuid import UUID

from comment.api.v1.domain.services.comment import CommentService
from comment.api.v1.schemas.comment import CommentSchemaRequest, CommentSchemaResponse, CommentSchemaUpdate


class CommentController:
    def __init__(self, service: CommentService) -> None:
        self.service = service

    async def view_create_comment(
        self, user_uuid: UUID, video_uuid: UUID, body: CommentSchemaRequest
    ) -> CommentSchemaResponse:
        return await self.service.create_comment(user_uuid, video_uuid, body)

    async def view_update_comment(
        self, user_uuid: UUID, video_uuid: UUID, comment_uuid: UUID, body: CommentSchemaUpdate
    ) -> CommentSchemaResponse:
        return await self.service.update_comment(user_uuid, video_uuid, comment_uuid, body)

    async def view_delete_comment(self, user_uuid: UUID, video_uuid: UUID, comment_uuid: UUID) -> UUID:
        return await self.service.delete_comment(user_uuid, video_uuid, comment_uuid)

    async def view_get_comment(self, user_uuid: UUID, video_uuid: UUID, comment_uuid: UUID) -> UUID:
        return await self.service.get_comment(user_uuid, video_uuid, comment_uuid)

    async def view_get_comments_from_video(self, video_uuid: UUID) -> CommentSchemaResponse:
        return await self.service.get_comments_from_video(video_uuid)

    async def view_get_comments_from_users(self, users_uuid: UUID) -> CommentSchemaResponse:
        return await self.service.get_comments_from_users(users_uuid)
