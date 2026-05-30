from sqlalchemy import Column, ForeignKey, Integer, String

from app.db.base import Base


class MovieDetail(Base):
    __tablename__ = "movie_details"

    id = Column(Integer, primary_key=True)
    rental_item_id = Column(Integer, ForeignKey("rental_items.id"), nullable=False, unique=True)
    duration_minutes = Column(Integer, nullable=False)
    director = Column(String(150), nullable=False)
    original_language = Column(String(80), nullable=False)
