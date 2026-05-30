from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, func

from app.db.base import Base


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("rental_status_types.id"), nullable=False)
    rental_date = Column(Date, nullable=False)
    expected_return_date = Column(Date, nullable=False)
    actual_return_date = Column(Date, nullable=True)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    late_fee_amount = Column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    final_amount = Column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
