from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.security.user_status_type import UserStatusType


class UserStatusTypeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, status_id: int) -> Optional[UserStatusType]:
        return self.db.scalar(select(UserStatusType).where(UserStatusType.id == status_id))

    def get_by_code(self, code: str) -> Optional[UserStatusType]:
        return self.db.scalar(select(UserStatusType).where(UserStatusType.code == code))

    def list_active(self) -> list[UserStatusType]:
        return list(self.db.scalars(select(UserStatusType).where(UserStatusType.is_active.is_(True)).order_by(UserStatusType.name.asc())).all())



