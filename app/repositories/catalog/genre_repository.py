from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.catalog.genre import Genre


class GenreRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, genre_id: int) -> Optional[Genre]:
        return self.db.scalar(select(Genre).where(Genre.id == genre_id))

    def get_by_code(self, code: str) -> Optional[Genre]:
        return self.db.scalar(select(Genre).where(Genre.code == code))

    def list_active(self) -> list[Genre]:
        return list(self.db.scalars(select(Genre).where(Genre.is_active.is_(True)).order_by(Genre.name.asc())).all())



