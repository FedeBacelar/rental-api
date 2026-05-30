from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory.videogame_detail import VideogameDetail


class VideogameDetailRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict[str, Any]) -> VideogameDetail:
        detail = VideogameDetail(**data)
        self.db.add(detail)
        self.db.commit()
        self.db.refresh(detail)
        return detail

    def get_by_id(self, detail_id: int) -> Optional[VideogameDetail]:
        return self.db.scalar(select(VideogameDetail).where(VideogameDetail.id == detail_id))

    def get_by_rental_item_id(self, rental_item_id: int) -> Optional[VideogameDetail]:
        return self.db.scalar(select(VideogameDetail).where(VideogameDetail.rental_item_id == rental_item_id))



