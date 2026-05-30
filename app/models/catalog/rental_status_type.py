from sqlalchemy import Boolean, Column, Integer, String

from app.db.base import Base


class RentalStatusType(Base):
    __tablename__ = "rental_status_types"

    id = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True, server_default="1")
