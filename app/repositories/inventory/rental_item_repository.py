from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory.rental_item import RentalItem


class RentalItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict[str, Any]) -> RentalItem:
        item = RentalItem(**data)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_by_id(self, item_id: int) -> Optional[RentalItem]:
        return self.db.scalar(select(RentalItem).where(RentalItem.id == item_id))

    def list_active(self) -> list[RentalItem]:
        return list(self.db.scalars(select(RentalItem).where(RentalItem.is_active.is_(True)).order_by(RentalItem.title.asc())).all())

    def update(self, item: RentalItem, data: dict[str, Any]) -> RentalItem:
        for field, value in data.items():
            setattr(item, field, value)
        self.db.commit()
        self.db.refresh(item)
        return item



