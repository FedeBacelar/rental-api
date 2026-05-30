from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text, func

from app.db.base import Base


class RentalItem(Base):
    __tablename__ = "rental_items"

    id = Column(Integer, primary_key=True)
    item_type_id = Column(Integer, ForeignKey("rental_item_types.id"), nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    title = Column(String(180), nullable=False, index=True)
    description = Column(Text, nullable=True)
    age_rating = Column(String(20), nullable=True)
    base_daily_price = Column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    late_fee_per_day = Column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    replacement_cost = Column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    is_active = Column(Boolean, nullable=False, default=True, server_default="1")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
