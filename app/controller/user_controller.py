from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import require_permission
from app.db.session import get_db
from app.dto.security import (
    UserCreateRequest,
    UserResponse,
    UserRoleUpdateRequest,
    UserStatusUpdateRequest,
)
from app.enums.security import PermissionCode
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(require_permission(PermissionCode.USERS_MANAGE))],
)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    request: UserCreateRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
    return UserService(db).create_user(request)


@router.get("", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)) -> list[UserResponse]:
    return UserService(db).list_users()


@router.patch("/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    request: UserRoleUpdateRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
    return UserService(db).update_user_role(user_id, request)


@router.patch("/{user_id}/status", response_model=UserResponse)
def update_user_status(
    user_id: int,
    request: UserStatusUpdateRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
    return UserService(db).update_user_status(user_id, request)
