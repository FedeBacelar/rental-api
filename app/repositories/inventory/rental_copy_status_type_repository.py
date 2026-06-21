from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory.rental_copy_status_type import RentalCopyStatusType


class RentalCopyStatusTypeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, status_id: int) -> Optional[RentalCopyStatusType]:
        return self.db.scalar(select(RentalCopyStatusType).where(RentalCopyStatusType.id == status_id))

    def get_by_code(self, code: str) -> Optional[RentalCopyStatusType]:
        return self.db.scalar(select(RentalCopyStatusType).where(RentalCopyStatusType.code == code))

    def list_active(self) -> list[RentalCopyStatusType]:
        return list(self.db.scalars(select(RentalCopyStatusType).where(RentalCopyStatusType.is_active.is_(True)).order_by(RentalCopyStatusType.name.asc())).all())



