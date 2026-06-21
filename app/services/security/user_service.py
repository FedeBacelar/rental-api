from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.dto.security import (
    UserCreateRequest,
    UserResponse,
    UserRoleUpdateRequest,
    UserStatusUpdateRequest,
)
from app.enums.security import UserStatusCode
from app.mappers.security import user_to_user_response, users_to_user_response
from app.models.security.role import Role
from app.models.security.user import User
from app.models.security.user_status_type import UserStatusType
from app.repositories.security.role_repository import RoleRepository
from app.repositories.security.user_repository import UserRepository
from app.repositories.security.user_status_type_repository import UserStatusTypeRepository
from app.services.security.password_service import PasswordService


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, request: UserCreateRequest) -> UserResponse:
        user_repository = UserRepository(self.db)

        if user_repository.get_by_username(request.username) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this username already exists",
            )

        if user_repository.get_by_email(str(request.email)) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists",
            )

        role = self._get_active_role(request.role_code.value)
        active_status = self._get_active_status(UserStatusCode.ACTIVE.value)
        user = user_repository.create(
            {
                "role_id": role.id,
                "status_id": active_status.id,
                "username": request.username,
                "email": str(request.email),
                "password_hash": PasswordService.hash_password(request.password),
                "first_name": request.first_name,
                "last_name": request.last_name,
            }
        )

        return user_to_user_response(user, role.code, active_status.code)

    def list_users(self) -> list[UserResponse]:
        users = UserRepository(self.db).list_with_role_and_status()

        return users_to_user_response(users)

    def update_user_role(
        self,
        user_id: int,
        request: UserRoleUpdateRequest,
    ) -> UserResponse:
        user = self._get_user(user_id)
        role = self._get_active_role(request.role_code.value)
        user = UserRepository(self.db).update(user, {"role_id": role.id})
        user_status = self._get_status_by_id(user.status_id)

        return user_to_user_response(user, role.code, user_status.code)

    def update_user_status(
        self,
        user_id: int,
        request: UserStatusUpdateRequest,
    ) -> UserResponse:
        user = self._get_user(user_id)
        user_status = self._get_active_status(request.status_code.value)
        user = UserRepository(self.db).update(user, {"status_id": user_status.id})
        role = self._get_role_by_id(user.role_id)

        return user_to_user_response(user, role.code, user_status.code)

    def _get_user(self, user_id: int) -> User:
        user = UserRepository(self.db).get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User was not found",
            )

        return user

    def _get_active_role(self, role_code: str) -> Role:
        role = RoleRepository(self.db).get_by_code(role_code)
        if role is None or not role.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role is invalid or inactive",
            )

        return role

    def _get_role_by_id(self, role_id: int) -> Role:
        role = RoleRepository(self.db).get_by_id(role_id)
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User role was not found",
            )

        return role

    def _get_active_status(self, status_code: str) -> UserStatusType:
        user_status = UserStatusTypeRepository(self.db).get_by_code(status_code)
        if user_status is None or not user_status.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User status is invalid or inactive",
            )

        return user_status

    def _get_status_by_id(self, status_id: int) -> UserStatusType:
        user_status = UserStatusTypeRepository(self.db).get_by_id(status_id)
        if user_status is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User status was not found",
            )

        return user_status
