from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from comment.api.v1.domain.repository.comment import CommentDAL
from comment.api.v1.schemas.comment import CommentSchemaRequest, CommentSchemaUpdate, CommentSchemaResponse


class CommentService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_comment(
        self, user_uuid: UUID, video_uuid: UUID, body: CommentSchemaRequest
    ) -> CommentSchemaResponse:
        comment_crud = CommentDAL(self.session)
        comment = await comment_crud.create(user_uuid, video_uuid, body)
        return CommentSchemaResponse.model_validate(comment)

    async def update_comment(
        self, user_uuid: UUID, video_uuid: UUID, comment_uuid: UUID, body: CommentSchemaUpdate
    ) -> CommentSchemaResponse:
        comment_crud = CommentDAL(self.session)
        comment = await comment_crud.update(user_uuid, video_uuid, comment_uuid, body)
        return CommentSchemaResponse.model_validate(comment)

    async def delete_comment(self, user_uuid: UUID, video_uuid: UUID, comment_uuid: UUID) -> UUID:
        comment_crud = CommentDAL(self.session)
        comment_id = await comment_crud.delete(user_uuid, video_uuid, comment_uuid)
        return comment_id

    async def get_comment(self, user_uuid: UUID, video_uuid: UUID, comment_uuid: UUID) -> CommentSchemaResponse:
        comment_crud = CommentDAL(self.session)
        comment = await comment_crud.get(user_uuid, video_uuid, comment_uuid)
        return CommentSchemaResponse.model_validate(comment)

    async def get_comments_from_video(
        self,
        video_uuid: UUID,
    ) -> list[CommentSchemaResponse]:
        comment_crud = CommentDAL(self.session)
        comments = await comment_crud.get_comments_from_video(video_uuid)
        return [CommentSchemaResponse.model_validate(comment) for comment in comments]

    async def get_comments_from_users(self, user_uuid: UUID) -> list[CommentSchemaResponse]:
        comment_crud = CommentDAL(self.session)
        comments = await comment_crud.get_comments_from_users(user_uuid)
        return [CommentSchemaResponse.model_validate(comment) for comment in comments]
