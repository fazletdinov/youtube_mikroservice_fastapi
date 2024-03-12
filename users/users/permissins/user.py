from typing import Annotated

from fastapi import Depends, HTTPException, status

from users.database.models.user import Role, User
from users.services.auth_token import (
    TokenManager,
    get_token_manager,
    verify_access_token,
)
from users.services.user import AuthService, get_auth_service


async def get_current_user(
    access_token: Annotated[str, Depends(verify_access_token)],
    token_manager: Annotated[TokenManager, Depends(get_token_manager)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    token_data = await token_manager.get_data_from_access_token(access_token)
    user = await auth_service.get_by_email(token_data.email)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


async def get_current_active_user(current_user: CurrentUser) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


async def get_current_user_role_moderator(current_user: CurrentUser) -> User:
    if current_user.role == Role.MODERATOR:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="permission denied"
    )


async def get_current_user_role_admin(current_user: CurrentUser) -> User:
    if current_user.is_superuser:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="permission denied"
    )


async def get_current_user_role_admin_and_moderator(current_user: CurrentUser) -> User:
    if current_user.is_superuser and current_user.role == Role.MODERATOR:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="permission denied"
    )
