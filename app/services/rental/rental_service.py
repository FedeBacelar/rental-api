from sqlalchemy.orm import Session


class RentalService:
    def __init__(self, db: Session):
        self.db = db
