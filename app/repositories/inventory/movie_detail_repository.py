from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory.movie_detail import MovieDetail


class MovieDetailRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict[str, Any]) -> MovieDetail:
        detail = MovieDetail(**data)
        self.db.add(detail)
        self.db.commit()
        self.db.refresh(detail)
        return detail

    def get_by_id(self, detail_id: int) -> Optional[MovieDetail]:
        return self.db.scalar(select(MovieDetail).where(MovieDetail.id == detail_id))

    def get_by_rental_item_id(self, rental_item_id: int) -> Optional[MovieDetail]:
        return self.db.scalar(select(MovieDetail).where(MovieDetail.rental_item_id == rental_item_id))

    def create_pending(self, data: dict[str, Any]) -> MovieDetail:
        detail = MovieDetail(**data)
        self.db.add(detail)
        self.db.flush()
        return detail