from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dto.auth import LoginRequest, LoginResponse
from app.enums.catalog import UserStatusCode
from app.mappers.auth import user_to_login_response
from app.repositories.catalog.user_status_type_repository import UserStatusTypeRepository
from app.repositories.security.role_repository import RoleRepository
from app.repositories.security.user_repository import UserRepository
from app.services.password_service import PasswordService
from app.services.token_service import TokenService


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def login(self, request: LoginRequest, response: Response) -> LoginResponse:
        user_repository = UserRepository(self.db)
        role_repository = RoleRepository(self.db)
        status_repository = UserStatusTypeRepository(self.db)

        user = user_repository.get_by_username(request.username)

        if user is None or not PasswordService.verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        active_status = status_repository.get_by_code(UserStatusCode.ACTIVE.value)
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

        role = role_repository.get_by_id(user.role_id)
        if role is None or not role.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User role is inactive",
            )

        permission_codes = role_repository.list_permission_codes(role.id)
        token_service = TokenService()
        access_token = token_service.create_access_token(
            user_id=user.id,
            username=user.username,
            role=role.code,
            permissions=permission_codes,
        )
        refresh_token = token_service.create_refresh_token(user_id=user.id)
        token_service.set_auth_cookies(response, access_token, refresh_token)

        return user_to_login_response(
            user=user,
            role_code=role.code,
            permission_codes=permission_codes,
        )
