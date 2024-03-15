from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr


class TokenType(str, Enum):
    access = "access"
    refresh = "refresh"


class TokenPayloadsBase(BaseModel):
    sub: int
    email: EmailStr
    role: str
    exp: datetime

    model_config = ConfigDict(from_attributes=True, revalidate_instances="always")


class AccessTokenPayload(TokenPayloadsBase):
    pass


class RefreshTokenPayload(TokenPayloadsBase):
    pass


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
