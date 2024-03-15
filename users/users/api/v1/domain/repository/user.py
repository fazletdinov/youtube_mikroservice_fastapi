from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import Result, Row, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from users.database.models.user import User
from users.api.v1.schemas.user import UpdateUserSchema

from .base_crud import CrudBase


class UserDAL(CrudBase):
    def __init__(self, session: AsyncSession) -> None:
        self.db_session = session

    @override
    async def create(self, email: str, hash_password: bytes) -> Row[tuple[User]] | Exception:
        try:
            new_user = User(email=email, password=hash_password)
            self.db_session.add(new_user)
            await self.db_session.commit()
            await self.db_session.refresh(new_user)
            return await self.get(new_user.id)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка SQLAlchemyError при добавлении user",
            )

    @override
    async def get(self, user_id: int) -> Row[tuple[User, int, int]] | None | Exception:
        try:
            query = select(User).where(User.id == user_id, User.is_active == True)

            res: Result = await self.db_session.execute(query)
            user_row: Row[tuple[User, int, int]] = res.fetchone()
            if user_row is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
            return user_row
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка SQLAlchemyError при получении user",
            )

    @override
    async def update(self, user_id: int, body_user: UpdateUserSchema) -> Row[tuple[User]] | None | Exception:
        try:
            stmt = update(User).where(User.id == user_id).values(**body_user.model_dump()).returning(User.id)
            res: Result = await self.db_session.execute(stmt)
            await self.db_session.commit()
            updated_user_id = res.scalar()
            return await self.get(updated_user_id)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка SQLAlchemyError при обновлении user",
            )

    @override
    async def delete(self, user_id: int) -> int:
        try:
            stmt = (
                update(User)
                .where(User.id == user_id, User.is_active == True)
                .values(is_active=False)
                .returning(User.id)
            )
            res: Result = await self.db_session.execute(stmt)
            await self.db_session.commit()
            deleted_user_id = res.scalar()
            return deleted_user_id
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка SQLAlchemyError при удалении user",
            )

    async def get_list(self, offset: int, limit: int) -> Sequence[Row[tuple[User, int, int]]] | None:
        try:
            query = select(User).where(User.is_active == True).limit(limit).offset(offset)

            res: Result = await self.db_session.execute(query)
            return res.all()
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка SQLAlchemyError при получении списка user",
            )

    async def get_by_email(self, email: str) -> User | None | Exception:
        try:
            query = select(User).where(User.email == email, User.is_active == True)  # type: ignore[E702]
            res: Result = await self.db_session.execute(query)
            user_row: User | None = res.scalar()
            return user_row
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="ошибка SQLAlchemyError при получении user по email",
            )

    async def get_by_email_full_info(self, email: str) -> Row[tuple[User, int, int]] | None | Exception:
        try:
            query = select(User).where(User.email == email, User.is_active == True)

            res: Result = await self.db_session.execute(query)
            user_row: Row[tuple[User, int, int]] = res.fetchone()
            if user_row is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
            return user_row
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка SQLAlchemyError при получении user",
            )
