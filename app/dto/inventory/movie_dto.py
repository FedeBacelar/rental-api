from pydantic import BaseModel, ConfigDict, Field

class MovieCreateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    genre_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=180)
    description:  str | None = None
    age_rating: str | None = Field(default=None, max_length=20)
    base_daily_price: float = Field(ge=0)
    late_fee_per_day: float = Field(ge=0)
    replacement_cost: float = Field(ge=0)

    duration_minutes: int = Field(gt=0)
    director: str = Field(min_length=1, max_length=150)
    original_language: str = Field(min_length=1, max_length=80)

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
