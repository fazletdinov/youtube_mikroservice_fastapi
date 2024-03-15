from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

import jwt
from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError

from users.core.config import settings
from users.api.v1.schemas.token import (
    AccessTokenPayload,
    RefreshTokenPayload,
    TokenPayloadsBase,
    TokenType,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def __verify_token(token: str, token_type: TokenType, algorithm: str) -> str:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="could not validate credentials",
            headers={"WWW-Authenticate:": "Bearer"},
        )
    try:
        if token_type == TokenType.access.value:
            payload_model = AccessTokenPayload
        else:
            payload_model = RefreshTokenPayload
        public_key = settings.token.public_key_path.read_text()
        payload = jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
        token_data = payload_model(**payload)
        if token_data.exp < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


async def verify_access_token(
    access_token: Annotated[str, Depends(oauth2_scheme)],
    access_type=TokenType.access.value,
    algorithm=settings.token.algorithm,
) -> str:
    token: str = await __verify_token(access_token, access_type, algorithm)
    return token


async def verify_refresh_token(
    refresh_token: Annotated[str, Cookie(None, include_in_schema=False)],
    refresh_type=TokenType.refresh.value,
    algorithm=settings.token.algorithm,
):
    token: str = await __verify_token(refresh_token, refresh_type, algorithm)
    return token


class TokenManagerBase(metaclass=ABCMeta):
    @abstractmethod
    async def generate_access_token(self, *args: Any, **kwargs: Any) -> str:
        """Генерирует access токен"""

    @abstractmethod
    async def generate_refresh_token(self, *args: Any, **kwargs: Any) -> str:
        """Генерирует refresh токен"""

    @abstractmethod
    async def get_data_from_access_token(self, *args: Any, **kwargs: Any):
        """Получение данных из access токен"""

    @abstractmethod
    async def get_data_from_refresh_token(self, *args: Any, **kwargs: Any):
        """Получение данных из refresh токен"""


class TokenManager(TokenManagerBase):
    @staticmethod
    async def __generate_token(
        data: dict[str, Any],
        private_key: str,
        algorithm: str,
        expire_delta: int,
        payload_model: TokenPayloadsBase,
    ) -> str:
        expires_delta = datetime.utcnow() + timedelta(minutes=expire_delta)
        token_payload = payload_model(
            sub=data.get("sub"),
            email=data.get("email"),
            role=data.get("role"),
            exp=expires_delta,
        )
        encode_jwt = jwt.encode(payload=token_payload.model_dump(), key=private_key, algorithm=algorithm)
        return encode_jwt

    async def generate_access_token(self, data: dict[str, Any]) -> str:
        return await TokenManager.__generate_token(
            data,
            private_key=settings.token.private_key_path.read_text(),
            algorithm=settings.token.algorithm,
            expire_delta=settings.token.access_expire,
            payload_model=AccessTokenPayload,
        )

    async def generate_refresh_token(self, data: dict[str, Any]) -> str:
        return await TokenManager.__generate_token(
            data,
            private_key=settings.token.private_key_path.read_text(),
            algorithm=settings.token.algorithm,
            expire_delta=settings.token.refresh_expire,
            payload_model=RefreshTokenPayload,
        )

    @staticmethod
    async def __get_data_from_token(
        token: str, public_key: str, algorithm: str, payload_model: TokenPayloadsBase
    ) -> TokenPayloadsBase:
        try:
            payload = jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
            return payload_model(**payload)
        except PyJWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")

    async def get_data_from_access_token(self, access_token: str) -> AccessTokenPayload:
        return await TokenManager.__get_data_from_token(
            access_token,
            public_key=settings.token.public_key_path.read_text(),
            algorithm=settings.token.algorithm,
            payload_model=AccessTokenPayload,
        )

    async def get_data_from_refresh_token(self, refresh_token: str) -> RefreshTokenPayload:
        return await TokenManager.__get_data_from_token(
            refresh_token,
            public_key=settings.token.public_key_path.read_text(),
            algorithm=settings.token.algorithm,
            payload_model=RefreshTokenPayload,
        )


async def get_token_manager() -> TokenManager:
    return TokenManager()
