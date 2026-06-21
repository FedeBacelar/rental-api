from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.rental.rental_status_type import RentalStatusType


class RentalStatusTypeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, status_id: int) -> Optional[RentalStatusType]:
        return self.db.scalar(select(RentalStatusType).where(RentalStatusType.id == status_id))

    def get_by_code(self, code: str) -> Optional[RentalStatusType]:
        return self.db.scalar(select(RentalStatusType).where(RentalStatusType.code == code))

    def list_active(self) -> list[RentalStatusType]:
        return list(self.db.scalars(select(RentalStatusType).where(RentalStatusType.is_active.is_(True)).order_by(RentalStatusType.name.asc())).all())



