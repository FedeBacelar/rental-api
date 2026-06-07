from datetime import datetime
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.security.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict[str, Any]) -> RefreshToken:
        refresh_token = RefreshToken(**data)
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)
        return refresh_token

    def get_active_by_hash(self, token_hash: str, now: datetime) -> Optional[RefreshToken]:
        statement = select(RefreshToken).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked_at.is_(None),
            RefreshToken.expires_at > now,
        )

        return self.db.scalar(statement)

    def revoke(self, refresh_token: RefreshToken, revoked_at: datetime) -> RefreshToken:
        refresh_token.revoked_at = revoked_at
        self.db.commit()
        self.db.refresh(refresh_token)
        return refresh_token

    def revoke_by_hash(self, token_hash: str, revoked_at: datetime) -> None:
        refresh_token = self.get_active_by_hash(token_hash, revoked_at)

        if refresh_token is None:
            return

        self.revoke(refresh_token, revoked_at)
