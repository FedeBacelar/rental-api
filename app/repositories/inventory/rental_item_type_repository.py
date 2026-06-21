from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.catalog.rental_item_type import RentalItemType


class RentalItemTypeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, item_type_id: int) -> Optional[RentalItemType]:
        return self.db.scalar(select(RentalItemType).where(RentalItemType.id == item_type_id))

    def get_by_code(self, code: str) -> Optional[RentalItemType]:
        return self.db.scalar(select(RentalItemType).where(RentalItemType.code == code))

    def list_active(self) -> list[RentalItemType]:
        return list(self.db.scalars(select(RentalItemType).where(RentalItemType.is_active.is_(True)).order_by(RentalItemType.name.asc())).all())



