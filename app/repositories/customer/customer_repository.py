from typing import Any, Optional

from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.models.customer.customer import Customer


class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict[str, Any]) -> Customer:
        customer = Customer(**data)
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        return self.db.scalar(select(Customer).where(Customer.id == customer_id))

    def get_by_document_number(self, document_number: str) -> Optional[Customer]:
        return self.db.scalar(select(Customer).where(Customer.document_number == document_number))

    def search_customers(self, query: str) -> list[Customer]:
        return list(self.db.scalars(select(Customer).where(or_(Customer.first_name.ilike(f"%{query}%"),Customer.last_name.ilike(f"%{query}%"),Customer.email.ilike(f"%{query}%"),Customer.document_number.ilike(f"%{query}%"),)).order_by(Customer.last_name.asc(), Customer.first_name.asc())
        ).all())

    def list_active(self) -> list[Customer]:
        return list(self.db.scalars(select(Customer).where(Customer.is_active.is_(True)).order_by(Customer.last_name.asc(), Customer.first_name.asc())).all())

    def update(self, customer: Customer, data: dict[str, Any]) -> Customer:
        for field, value in data.items():
            setattr(customer, field, value)
        self.db.commit()
        self.db.refresh(customer)
        return customer



