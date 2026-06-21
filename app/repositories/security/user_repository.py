from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums.security import UserStatusCode
from app.models.security.user_status_type import UserStatusType
from app.models.security.role import Role
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
        statement = (
            select(User)
            .join(UserStatusType, UserStatusType.id == User.status_id)
            .where(UserStatusType.code == UserStatusCode.ACTIVE.value)
            .order_by(User.username.asc())
        )

        return list(self.db.scalars(statement).all())

    def list_with_role_and_status(self) -> list[tuple[User, str, str]]:
        statement = (
            select(User, Role.code, UserStatusType.code)
            .join(Role, Role.id == User.role_id)
            .join(UserStatusType, UserStatusType.id == User.status_id)
            .order_by(User.username.asc())
        )

        return [
            (user, role_code, status_code)
            for user, role_code, status_code in self.db.execute(statement).all()
        ]

    def update(self, user: User, data: dict[str, Any]) -> User:
        for field, value in data.items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user



