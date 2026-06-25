from datetime import date
from pydantic import BaseModel, Field


class RentalCreateRequest(BaseModel):
    customer_id: int = Field(gt=0)
    expected_return_date: date
    rental_copy_ids: list[int] = Field(min_length=1)


class RentalResponse(BaseModel):
    id: int
    customer_id: int
    status_id: int
    status_code: str
    rental_date: date
    expected_return_date: date
    total_amount: float

    model_config = {"from_attributes": True}
