from pydantic import BaseModel
from decimal import Decimal


class RentalItemResponse(BaseModel):
    id: int
    item_type_id: int
    genre_id: int
    title: str
    description: str | None = None
    age_rating: str | None = None
    base_daily_price: Decimal
    late_fee_per_day: Decimal
    replacement_cost: Decimal
    is_active: bool
