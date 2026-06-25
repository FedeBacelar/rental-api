from datetime import date
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.rental import Rental


class RentalRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict[str, Any]) -> Rental:
        rental = Rental(**data)
        self.db.add(rental)
        self.db.commit()
        self.db.refresh(rental)
        return rental

    def get_by_id(self, rental_id: int) -> Optional[Rental]:
        return self.db.scalar(select(Rental).where(Rental.id == rental_id))

    def list_by_customer_id(self, customer_id: int) -> list[Rental]:
        return list(
            self.db.scalars(
                select(Rental)
                .where(Rental.customer_id == customer_id)
                .order_by(Rental.rental_date.desc())
            ).all()
        )

    def list_by_status_id(self, status_id: int) -> list[Rental]:
        return list(
            self.db.scalars(
                select(Rental)
                .where(Rental.status_id == status_id)
                .order_by(Rental.rental_date.desc())
            ).all()
        )

    def list_overdue_by_status_ids(
        self,
        status_ids: list[int],
        today: date,
    ) -> list[Rental]:
        return list(
            self.db.scalars(
                select(Rental).where(
                    Rental.status_id.in_(status_ids),
                    Rental.expected_return_date < today,
                )
            ).all()
        )

    def update(self, rental: Rental, data: dict[str, Any]) -> Rental:
        for field, value in data.items():
            setattr(rental, field, value)
        self.db.commit()
        self.db.refresh(rental)
        return rental

    def update_status(self, rental: Rental, status_id: int) -> Rental:
        rental.status_id = status_id
        self.db.commit()
        self.db.refresh(rental)
        return rental
