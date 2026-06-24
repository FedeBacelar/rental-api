from pydantic import BaseModel


class RentalItemResponse(BaseModel):
    id: int
    item_type_id: int
    genre_id: int
    title: str
    description: str | None = None
    age_rating: str | None = None
    base_daily_price: float
    late_fee_per_day: float
    replacement_cost: float
    is_active: bool
