from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer.customer_status_type import CustomerStatusType


class CustomerStatusTypeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, status_id: int) -> Optional[CustomerStatusType]:
        return self.db.scalar(select(CustomerStatusType).where(CustomerStatusType.id == status_id))

    def get_by_code(self, code: str) -> Optional[CustomerStatusType]:
        return self.db.scalar(select(CustomerStatusType).where(CustomerStatusType.code == code))

    def list_active(self) -> list[CustomerStatusType]:
        return list(self.db.scalars(select(CustomerStatusType).where(CustomerStatusType.is_active.is_(True)).order_by(CustomerStatusType.name.asc())).all())



