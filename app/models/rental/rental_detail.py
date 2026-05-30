from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, Text, func

from app.db.base import Base


class RentalDetail(Base):
    __tablename__ = "rental_details"

    id = Column(Integer, primary_key=True)
    rental_id = Column(Integer, ForeignKey("rentals.id"), nullable=False)
    rental_copy_id = Column(Integer, ForeignKey("rental_copies.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("rental_detail_status_types.id"), nullable=False)
    price_per_day = Column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    late_fee_per_day = Column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    replacement_cost = Column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    rental_days = Column(Integer, nullable=False)
    late_days = Column(Integer, nullable=False, default=0, server_default="0")
    subtotal = Column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    late_fee_amount = Column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    replacement_fee_amount = Column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    final_amount = Column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    resolved_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
