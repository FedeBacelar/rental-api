from pydantic import BaseModel


class RentalItemResponse(BaseModel):
    id: int
    item_type_id: int
    item_type_code: str | None = None
    item_type_name: str | None = None
    genre_id: int
    genre_code: str | None = None
    genre_name: str | None = None
    title: str
    description: str | None = None
    age_rating: str | None = None
    base_daily_price: float
    late_fee_per_day: float
    replacement_cost: float
    is_active: bool
