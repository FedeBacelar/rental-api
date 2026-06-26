from pydantic import BaseModel, ConfigDict, Field

class VideogameCreateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    genre_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=180)
    description: str | None = None
    age_rating: str | None = Field(default=None, max_length=20)
    base_daily_price: float = Field(ge=0)
    late_fee_per_day: float = Field(ge=0)
    replacement_cost: float = Field(ge=0)

    platform_id: int = Field(gt=0)
    publisher: str = Field(min_length=1, max_length=150)
    multiplayer: bool

class VideogameResponse(BaseModel):
    id: int
    genre_id: int
    genre_code: str | None = None
    genre_name: str | None = None
    title: str
    description: str | None = None
    age_rating: str | None = None
    base_daily_price: float
    late_fee_per_day: float
    replacement_cost: float

    platform_id: int
    platform_code: str | None = None
    platform_name: str | None = None
    publisher: str
    multiplayer: bool

    is_active: bool
