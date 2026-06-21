from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.rental.rental_detail_status_type import RentalDetailStatusType


class RentalDetailStatusTypeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, status_id: int) -> Optional[RentalDetailStatusType]:
        return self.db.scalar(select(RentalDetailStatusType).where(RentalDetailStatusType.id == status_id))

    def get_by_code(self, code: str) -> Optional[RentalDetailStatusType]:
        return self.db.scalar(select(RentalDetailStatusType).where(RentalDetailStatusType.code == code))

    def list_active(self) -> list[RentalDetailStatusType]:
        return list(self.db.scalars(select(RentalDetailStatusType).where(RentalDetailStatusType.is_active.is_(True)).order_by(RentalDetailStatusType.name.asc())).all())



