from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.rental.rental_detail import RentalDetail


class RentalDetailRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict[str, Any]) -> RentalDetail:
        detail = RentalDetail(**data)
        self.db.add(detail)
        self.db.commit()
        self.db.refresh(detail)
        return detail

    def create_many(self, items: list[dict[str, Any]]) -> list[RentalDetail]:
        details = [RentalDetail(**item) for item in items]
        self.db.add_all(details)
        self.db.commit()
        for detail in details:
            self.db.refresh(detail)
        return details

    def get_by_id(self, detail_id: int) -> Optional[RentalDetail]:
        return self.db.scalar(select(RentalDetail).where(RentalDetail.id == detail_id))

    def list_by_rental_id(self, rental_id: int) -> list[RentalDetail]:
        return list(self.db.scalars(select(RentalDetail).where(RentalDetail.rental_id == rental_id).order_by(RentalDetail.id.asc())).all())

    def list_by_status_id(self, status_id: int) -> list[RentalDetail]:
        return list(self.db.scalars(select(RentalDetail).where(RentalDetail.status_id == status_id).order_by(RentalDetail.id.asc())).all())

    def update(self, detail: RentalDetail, data: dict[str, Any]) -> RentalDetail:
        for field, value in data.items():
            setattr(detail, field, value)
        self.db.commit()
        self.db.refresh(detail)
        return detail

    def update_status(self, detail: RentalDetail, status_id: int) -> RentalDetail:
        detail.status_id = status_id
        self.db.commit()
        self.db.refresh(detail)
        return detail



