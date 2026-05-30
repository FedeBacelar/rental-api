from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.security.role import Role


class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, role_id: int) -> Optional[Role]:
        return self.db.scalar(select(Role).where(Role.id == role_id))

    def get_by_code(self, code: str) -> Optional[Role]:
        return self.db.scalar(select(Role).where(Role.code == code))

    def list_active(self) -> list[Role]:
        return list(self.db.scalars(select(Role).where(Role.is_active.is_(True)).order_by(Role.name.asc())).all())



