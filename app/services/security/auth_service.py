from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dto.auth import LoginRequest, LoginResponse
from app.enums.catalog import UserStatusCode
from app.mappers.auth import user_to_login_response
from app.models.security.user import User
from app.repositories.catalog.user_status_type_repository import UserStatusTypeRepository
from app.repositories.security.refresh_token_repository import RefreshTokenRepository
from app.repositories.security.role_repository import RoleRepository
from app.repositories.security.user_repository import UserRepository
from app.services.password_service import PasswordService
from app.services.token_service import TokenService


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def login(self, request: LoginRequest, response: Response) -> LoginResponse:
        user_repository = UserRepository(self.db)

        user = user_repository.get_by_username(request.username)

        if user is None or not PasswordService.verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        role, permission_codes = self._get_active_user_role_and_permissions(user)
        token_service = TokenService()
        access_token = token_service.create_access_token(
            user_id=user.id,
            username=user.username,
            role=role.code,
            permissions=permission_codes,
        )
        refresh_token = token_service.create_refresh_token(user_id=user.id)

        RefreshTokenRepository(self.db).create(
            {
                "user_id": user.id,
                "token_hash": token_service.hash_token(refresh_token),
                "expires_at": token_service.get_refresh_expiration(),
            }
        )
        token_service.set_auth_cookies(response, access_token, refresh_token)

        return user_to_login_response(
            user=user,
            role_code=role.code,
            permission_codes=permission_codes,
        )

    def refresh(self, refresh_token: str | None, response: Response) -> LoginResponse:
        if refresh_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is missing",
            )

        token_service = TokenService()
        payload = self._decode_refresh_token(refresh_token, token_service)
        token_hash = token_service.hash_token(refresh_token)
        now = token_service.to_database_datetime(token_service.utc_now())

        persisted_refresh_token = RefreshTokenRepository(self.db).get_active_by_hash(token_hash, now)
        if persisted_refresh_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is invalid",
            )

        user = UserRepository(self.db).get_by_id(self._get_user_id_from_payload(payload))
        if user is None or user.id != persisted_refresh_token.user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is invalid",
            )

        role, permission_codes = self._get_active_user_role_and_permissions(user)
        access_token = token_service.create_access_token(
            user_id=user.id,
            username=user.username,
            role=role.code,
            permissions=permission_codes,
        )
        token_service.set_access_cookie(response, access_token)

        return user_to_login_response(
            user=user,
            role_code=role.code,
            permission_codes=permission_codes,
        )

    def logout(self, refresh_token: str | None, response: Response) -> None:
        token_service = TokenService()

        if refresh_token is not None:
            token_hash = token_service.hash_token(refresh_token)
            revoked_at = token_service.to_database_datetime(token_service.utc_now())
            RefreshTokenRepository(self.db).revoke_by_hash(token_hash, revoked_at)

        token_service.clear_auth_cookies(response)

    def _decode_refresh_token(self, refresh_token: str, token_service: TokenService) -> dict:
        try:
            payload = token_service.decode_token(refresh_token)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is invalid",
            )

        if payload.get("type") != "refresh" or payload.get("sub") is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is invalid",
            )

        return payload

    def _get_user_id_from_payload(self, payload: dict) -> int:
        try:
            return int(payload["sub"])
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is invalid",
            )

    def _get_active_user_role_and_permissions(self, user: User):
        role_repository = RoleRepository(self.db)
        status_repository = UserStatusTypeRepository(self.db)

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

        return role, permission_codes
