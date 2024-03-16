from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from sqlalchemy import select, update, Result, delete

from likes.api.v1.schemas.reaction import ReactionSchemaRequest, ReactionSchemaUpdate
from likes.database.models.likes import Reaction


class ReactionDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_uuid: UUID, video_uuid: UUID, body: ReactionSchemaRequest) -> Reaction:
        try:
            reaction = Reaction(video_uuid=video_uuid, user_uuid=user_uuid, type_reaction=body.type_reaction)
            self.session.add(reaction)
            await self.session.commit()
            await self.session.refresh(reaction)
            return reaction
        except SQLAlchemyError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"ОшибкаSQLAlchemyError при создании Reaction {error}",
            )

    async def update(self, user_uuid: UUID, video_uuid: UUID, body: ReactionSchemaUpdate) -> Reaction:
        try:
            stmt = (
                update(Reaction)
                .where(Reaction.user_uuid == user_uuid, Reaction.video_uuid == video_uuid)
                .values(**body.model_dump())
                .returning(Reaction)
            )

            result: Result[Reaction] = await self.session.execute(stmt)
            await self.session.commit()
            reaction: Reaction = result.scalar()
            return reaction
        except SQLAlchemyError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка SQLAlchemyError при обновлении Reaction {error}",
            )

    async def get(self, video_id: UUID) -> list[Reaction]:
        try:
            query = select(Reaction).where(Reaction.video_uuid == video_id)
            result: Result[list[Reaction]] = await self.session.execute(query)
            return result.scalars()
        except SQLAlchemyError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка SQLAlchemyError при получении списка Reaction {error}",
            )

    async def delete(self, user_uuid: UUID, video_uuid: UUID) -> UUID:
        try:
            stmt = (
                delete(Reaction)
                .where(Reaction.user_uuid == user_uuid, Reaction.video_uuid == video_uuid)
                .returning(Reaction.id)
            )
            result: Result[UUID] = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar()
        except SQLAlchemyError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка SQLAlchemyError при удалении Reaction {error}",
            )
