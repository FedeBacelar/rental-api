from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.security.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict[str, Any]) -> User:
        user = User(**data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.scalar(select(User).where(User.id == user_id))

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.scalar(select(User).where(User.username == username))

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.scalar(select(User).where(User.email == email))

    def list_active(self) -> list[User]:
        return list(self.db.scalars(select(User).where(User.is_active.is_(True)).order_by(User.username.asc())).all())

    def update(self, user: User, data: dict[str, Any]) -> User:
        for field, value in data.items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user



