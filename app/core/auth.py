from dataclasses import dataclass

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.enums.catalog import UserStatusCode
from app.enums.security import PermissionCode
from app.models.security.user import User
from app.repositories.catalog.user_status_type_repository import UserStatusTypeRepository
from app.repositories.security.role_repository import RoleRepository
from app.repositories.security.user_repository import UserRepository
from app.services.token_service import TokenService


@dataclass(frozen=True)
class AuthenticatedUser:
    id: int
    username: str
    role: str
    permissions: list[str]


def get_current_user(
    access_token: str | None = Cookie(default=None),
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

    permissions = _get_permissions(payload)

    return AuthenticatedUser(
        id=user.id,
        username=user.username,
        role=role.code,
        permissions=permissions,
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
