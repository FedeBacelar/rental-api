from pydantic import BaseModel

class MovieCreateRequest(BaseModel):
    genre_id: int 
    title: str 
    description:  str | None = None
    age_rating: str | None = None 
    base_daily_price: float
    late_fee_per_day: float
    replacement_cost: float

    duration_minutes: int
    director: str
    original_language: str

class MovieResponse(BaseModel):
    id: int 
    genre_id: int
    title: str
    description: str | None = None
    age_rating: str | None = None
    base_daily_price: float
    late_fee_per_day: float
    replacement_cost: float
    
    duration_minutes: int
    director: str
    original_language: str 
    
    is_active: bool