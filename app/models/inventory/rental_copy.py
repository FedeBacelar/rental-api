from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, UniqueConstraint, func

from app.db.base import Base


class RentalCopy(Base):
    __tablename__ = "rental_copies"
    __table_args__ = (
        UniqueConstraint("rental_item_id", "copy_number", name="uq_rental_copies_item_copy_number"),
    )

    id = Column(Integer, primary_key=True)
    rental_item_id = Column(Integer, ForeignKey("rental_items.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("rental_copy_status_types.id"), nullable=False)
    copy_number = Column(Integer, nullable=False)
    internal_code = Column(String(80), nullable=False, unique=True, index=True)
    is_active = Column(Boolean, nullable=False, default=True, server_default="1")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
