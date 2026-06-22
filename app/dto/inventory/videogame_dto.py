from pydantic import BaseModel

class VideogameCreateRequest(BaseModel):
    genre_id: int 
    title: str
    description: str | None = None
    age_rating: str | None = None
    base_daily_price: float
    late_fee_per_day: float
    replacement_cost: float

    platform_id: int
    publisher: str
    multiplayer: bool

class VideogameResponse(BaseModel):
    id: int
    genre_id: int
    title: str
    description: str | None = None
    age_rating: str | None = None
    base_daily_price: float
    late_fee_per_day: float
    replacement_cost: float

    platform_id: int
    publisher: str
    multiplayer: bool

    is_active: bool
