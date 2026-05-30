from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.db.base import Base


class VideogameDetail(Base):
    __tablename__ = "videogame_details"

    id = Column(Integer, primary_key=True)
    rental_item_id = Column(Integer, ForeignKey("rental_items.id"), nullable=False, unique=True)
    platform_id = Column(Integer, ForeignKey("platforms.id"), nullable=False)
    publisher = Column(String(150), nullable=False)
    multiplayer = Column(Boolean, nullable=False, default=False, server_default="0")
