from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Response, status
from pydantic import EmailStr, SecretStr

from users.core.config import settings
from users.permissins.user import CurrentUser
from users.schemas.token import TokenResponse
from users.schemas.user import CreateUserSchema, ResponseUserSchema, UpdateUserSchema
from users.services.user import AuthService, get_auth_service

auth_router = APIRouter(tags=["Auth"], prefix="/auth")


@auth_router.post("/", response_model=ResponseUserSchema)
async def register(
    user_body: CreateUserSchema, auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.register(user_body)


@auth_router.patch("/update", response_model=ResponseUserSchema)
async def update_user(
    user: CurrentUser,
    user_body: UpdateUserSchema,
    auth_service: AuthService = Depends(get_auth_service),
):
    user_dict: dict[str, str] = user_body.model_dump(exclude_none=True)
    if user_dict is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="нужно заполнить хотябы одно поле",
        )
    return await auth_service.update_user(user.id, user_body)


@auth_router.delete("/deactivate_user", response_model=int)
async def deactivate_user(
    user: CurrentUser, auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.deactivate_user(user.id)


@auth_router.get("/me", response_model=ResponseUserSchema)
async def me(user: CurrentUser):
    return user


@auth_router.post("/login", response_model=TokenResponse)
async def login(
    response: Response,
    username: Annotated[EmailStr, Form()],
    password: Annotated[SecretStr, Form()],
    auth_service: AuthService = Depends(get_auth_service),
):
    access_token, refresh_token = await auth_service.login(username, password)
    response.set_cookie(
        key=settings.token.refresh_cookie_name,
        value=refresh_token,
        httponly=True,
        expires=settings.token.refresh_expire,
    )
    return TokenResponse(access_token=access_token, token_type="bearer")
