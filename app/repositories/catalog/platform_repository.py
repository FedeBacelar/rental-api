from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.catalog.platform import Platform


class PlatformRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, platform_id: int) -> Optional[Platform]:
        return self.db.scalar(select(Platform).where(Platform.id == platform_id))

    def get_by_code(self, code: str) -> Optional[Platform]:
        return self.db.scalar(select(Platform).where(Platform.code == code))

    def list_active(self) -> list[Platform]:
        return list(self.db.scalars(select(Platform).where(Platform.is_active.is_(True)).order_by(Platform.name.asc())).all())



