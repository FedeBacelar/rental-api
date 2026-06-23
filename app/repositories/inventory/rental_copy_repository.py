from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory.rental_copy import RentalCopy


class RentalCopyRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict[str, Any]) -> RentalCopy:
        copy = RentalCopy(**data)
        self.db.add(copy)
        self.db.commit()
        self.db.refresh(copy)
        return copy

    def get_by_id(self, copy_id: int) -> Optional[RentalCopy]:
        return self.db.scalar(select(RentalCopy).where(RentalCopy.id == copy_id))

    def get_by_internal_code(self, internal_code: str) -> Optional[RentalCopy]:
        return self.db.scalar(select(RentalCopy).where(RentalCopy.internal_code == internal_code))

    def get_by_item_id_and_copy_number(
        self,
        item_id: int,
        copy_number: int,
    ) -> Optional[RentalCopy]:
        return self.db.scalar(
            select(RentalCopy).where(
                RentalCopy.rental_item_id == item_id,
                RentalCopy.copy_number == copy_number,
            )
        )

    def list_by_item_id(self, item_id: int) -> list[RentalCopy]:
        return list(self.db.scalars(select(RentalCopy).where(RentalCopy.rental_item_id == item_id).order_by(RentalCopy.copy_number.asc())).all())

    def list_by_status_id(self, status_id: int) -> list[RentalCopy]:
        return list(self.db.scalars(select(RentalCopy).where(RentalCopy.status_id == status_id).order_by(RentalCopy.id.asc())).all())

    def update_status(self, copy: RentalCopy, status_id: int) -> RentalCopy:
        copy.status_id = status_id
        self.db.commit()
        self.db.refresh(copy)
        return copy
