from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Response

from app.core.config import settings


class TokenService:
    ACCESS_COOKIE_NAME = "access_token"
    REFRESH_COOKIE_NAME = "refresh_token"

    def create_access_token(self, user_id: int, username: str, role: str, permissions: list[str]) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        payload = {
            "sub": str(user_id),
            "username": username,
            "role": role,
            "permissions": permissions,
            "type": "access",
            "exp": expires_at,
            "iat": datetime.now(timezone.utc),
        }

        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    def create_refresh_token(self, user_id: int) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": expires_at,
            "iat": datetime.now(timezone.utc),
        }

        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    def set_auth_cookies(self, response: Response, access_token: str, refresh_token: str) -> None:
        response.set_cookie(
            key=self.ACCESS_COOKIE_NAME,
            value=access_token,
            httponly=True,
            secure=settings.auth_cookie_secure,
            samesite="lax",
            max_age=settings.access_token_expire_minutes * 60,
            path="/",
        )
        response.set_cookie(
            key=self.REFRESH_COOKIE_NAME,
            value=refresh_token,
            httponly=True,
            secure=settings.auth_cookie_secure,
            samesite="lax",
            max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
            path="/auth",
        )
