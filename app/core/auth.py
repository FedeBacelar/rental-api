from dataclasses import dataclass

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyCookie
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.enums.security import PermissionCode, UserStatusCode
from app.models.security.user import User
from app.repositories.security.role_repository import RoleRepository
from app.repositories.security.user_repository import UserRepository
from app.repositories.security.user_status_type_repository import UserStatusTypeRepository
from app.services.security.token_service import TokenService


access_token_cookie = APIKeyCookie(
    name=TokenService.ACCESS_COOKIE_NAME,
    scheme_name="AccessTokenCookie",
    description="Cookie HttpOnly generada por POST /auth/login.",
    auto_error=False,
)

refresh_token_cookie = APIKeyCookie(
    name=TokenService.REFRESH_COOKIE_NAME,
    scheme_name="RefreshTokenCookie",
    description="Cookie HttpOnly usada por refresh y logout.",
    auto_error=False,
)


@dataclass(frozen=True)
class AuthenticatedUser:
    id: int
    username: str
    role: str
    permissions: list[str]


def get_current_user(
    access_token: str | None = Security(access_token_cookie),
    db: Session = Depends(get_db),
) -> AuthenticatedUser:
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication is required",
        )

    payload = _decode_access_token(access_token)
    user = _get_active_user(db, payload)
    role = RoleRepository(db).get_by_id(user.role_id)

    if role is None or not role.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User role is inactive",
        )

    token_permissions = _get_permissions(payload)
    current_permissions = RoleRepository(db).list_permission_codes(role.id)

    if payload.get("role") != role.code or set(token_permissions) != set(current_permissions):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is outdated",
        )

    return AuthenticatedUser(
        id=user.id,
        username=user.username,
        role=role.code,
        permissions=current_permissions,
    )


def require_permission(permission: PermissionCode | str):
    required_permission = permission.value if isinstance(permission, PermissionCode) else permission

    def dependency(current_user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
        if required_permission not in current_user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission is required",
            )

        return current_user

    return dependency


def _decode_access_token(access_token: str) -> dict:
    token_service = TokenService()

    try:
        payload = token_service.decode_token(access_token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is invalid",
        )

    if payload.get("type") != "access" or payload.get("sub") is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is invalid",
        )

    return payload


def _get_active_user(db: Session, payload: dict) -> User:
    user_id = _get_user_id(payload)
    user = UserRepository(db).get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is invalid",
        )

    active_status = UserStatusTypeRepository(db).get_by_code(UserStatusCode.ACTIVE.value)
    if active_status is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Initial user status ACTIVE was not found",
        )

    if user.status_id != active_status.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )

    return user


def _get_user_id(payload: dict) -> int:
    try:
        return int(payload["sub"])
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is invalid",
        )


def _get_permissions(payload: dict) -> list[str]:
    permissions = payload.get("permissions")

    if not isinstance(permissions, list) or not all(isinstance(item, str) for item in permissions):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is invalid",
        )

    return permissions
