from abc import ABCMeta, abstractmethod

import bcrypt
from fastapi import Depends, HTTPException, status
from pydantic import EmailStr, SecretStr
from sqlalchemy.ext.asyncio import AsyncSession

from users.api.v1.domain.repository.user import UserDAL
from users.database.models.user import User
from users.database.session import db_helper
from users.api.v1.schemas.user import CreateUserSchema, ResponseUserSchema, UpdateUserSchema
from users.api.v1.domain.services.auth_token import TokenManager, get_token_manager


class HashManagerBase(metaclass=ABCMeta):
    """Хэширование и проверка пороля"""

    @abstractmethod
    def hash_password(self, password: str) -> bytes:
        """Хеширование пароля"""

    @abstractmethod
    def verify_password(self, new_password: str, hash_password: bytes) -> bool:
        """Проверка пароля"""


class AuthServiceBase(metaclass=ABCMeta):
    """Service для управления пользователем"""

    @abstractmethod
    async def register(self, user_create_body: CreateUserSchema) -> ResponseUserSchema:
        """создание пользователя"""

    @abstractmethod
    async def update_user(self, user_id: int, user_update_body: UpdateUserSchema) -> ResponseUserSchema:
        """изменение данных пользователя"""

    @abstractmethod
    async def deactivate_user(self, user_id: int) -> int:
        """дэактивация пользователя"""

    @abstractmethod
    async def get_user(self, user_id: int) -> ResponseUserSchema:
        """получение user по id"""


class AuthService(AuthServiceBase, HashManagerBase):
    def __init__(self, session: AsyncSession, token_manager: TokenManager) -> None:
        self.session = session
        self.token_manager = token_manager

    def hash_password(self, password: str) -> bytes:
        salt: bytes = bcrypt.gensalt()
        pwd_hash_bytes: bytes = bcrypt.hashpw(password.encode(), salt)
        return pwd_hash_bytes

    def verify_password(self, new_password: str, hash_password: bytes) -> bool:
        return bcrypt.checkpw(new_password.encode(), hash_password)

    async def register(self, user_create_body: CreateUserSchema) -> ResponseUserSchema:
        user_crud = UserDAL(self.session)
        email_is_exists = await user_crud.get_by_email(user_create_body.email)
        if email_is_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь уже сущществует",
            )
        new_user = await user_crud.create(
            email=user_create_body.email,
            hash_password=self.hash_password(user_create_body.password.get_secret_value()),
        )
        return ResponseUserSchema.model_validate(new_user)

    async def update_user(self, user_id: int, user_update_body: UpdateUserSchema) -> ResponseUserSchema:
        user_crud = UserDAL(self.session)
        updated_user = await user_crud.update(user_id, user_update_body)
        return ResponseUserSchema.model_validate(updated_user)

    async def deactivate_user(self, user_id: int) -> int:
        user_crud = UserDAL(self.session)
        deactivated_user = await user_crud.delete(user_id)
        return deactivated_user

    async def get_user(self, user_id: int) -> ResponseUserSchema:
        user_crud = UserDAL(self.session)
        user = await user_crud.get(user_id)
        return ResponseUserSchema.model_validate(user)

    async def get_user_list(self, offset: int, limit: int) -> list[ResponseUserSchema]:
        user_crud = UserDAL(self.session)
        user_list = await user_crud.get_list(offset, limit)
        return [ResponseUserSchema.model_validate(user) for user in user_list]

    async def _generate_tokens(self, user: User) -> tuple[str, str]:
        token_payload = {"sub": user.id, "email": user.email, "role": user.role}
        access_token = await self.token_manager.generate_access_token(token_payload)
        refresh_token = await self.token_manager.generate_refresh_token(token_payload)
        return access_token, refresh_token

    async def login(self, email: EmailStr, password: SecretStr) -> tuple[str, str]:
        user_crud = UserDAL(self.session)
        user = await user_crud.get_by_email(email)
        if not user or not self.verify_password(new_password=password.get_secret_value(), hash_password=user.password):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="invalid email or password",
            )
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not active")
        return await self._generate_tokens(user)

    async def get_by_email(self, email: EmailStr) -> User:
        user_dal = UserDAL(self.session)
        user = await user_dal.get_by_email(email)
        return user

    async def get_by_email_full_info(self, email: EmailStr) -> ResponseUserSchema:
        user_dal = UserDAL(self.session)
        user = await user_dal.get_by_email_full_info(email)
        return ResponseUserSchema.model_validate(user)


async def get_auth_service(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    token_manager: TokenManager = Depends(get_token_manager),
) -> AuthService:
    return AuthService(session, token_manager)
