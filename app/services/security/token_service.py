from datetime import datetime, timedelta, timezone
from hashlib import sha256
from uuid import uuid4

import jwt
from fastapi import Response
from jwt import InvalidTokenError

from app.core.config import settings


class TokenService:
    ACCESS_COOKIE_NAME = "access_token"
    REFRESH_COOKIE_NAME = "refresh_token"

    @staticmethod
    def utc_now() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def to_database_datetime(value: datetime) -> datetime:
        return value.astimezone(timezone.utc).replace(tzinfo=None)

    @staticmethod
    def hash_token(token: str) -> str:
        return sha256(token.encode("utf-8")).hexdigest()

    def create_access_token(self, user_id: int, username: str, role: str, permissions: list[str]) -> str:
        issued_at = self.utc_now()
        expires_at = issued_at + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        payload = {
            "sub": str(user_id),
            "username": username,
            "role": role,
            "permissions": permissions,
            "type": "access",
            "exp": expires_at,
            "iat": issued_at,
        }

        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    def create_refresh_token(self, user_id: int) -> str:
        issued_at = self.utc_now()
        expires_at = issued_at + timedelta(days=settings.refresh_token_expire_days)
        payload = {
            "sub": str(user_id),
            "jti": str(uuid4()),
            "type": "refresh",
            "exp": expires_at,
            "iat": issued_at,
        }

        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    def get_refresh_expiration(self) -> datetime:
        return self.to_database_datetime(
            self.utc_now() + timedelta(days=settings.refresh_token_expire_days)
        )

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        except InvalidTokenError as exc:
            raise ValueError("Invalid token") from exc

    def set_access_cookie(self, response: Response, access_token: str) -> None:
        response.set_cookie(
            key=self.ACCESS_COOKIE_NAME,
            value=access_token,
            httponly=True,
            secure=settings.auth_cookie_secure,
            samesite="lax",
            max_age=settings.access_token_expire_minutes * 60,
            path="/",
        )

    def set_auth_cookies(self, response: Response, access_token: str, refresh_token: str) -> None:
        self.set_access_cookie(response, access_token)
        response.set_cookie(
            key=self.REFRESH_COOKIE_NAME,
            value=refresh_token,
            httponly=True,
            secure=settings.auth_cookie_secure,
            samesite="lax",
            max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
            path="/auth",
        )

    def clear_auth_cookies(self, response: Response) -> None:
        response.delete_cookie(key=self.ACCESS_COOKIE_NAME, path="/")
        response.delete_cookie(key=self.REFRESH_COOKIE_NAME, path="/auth")
