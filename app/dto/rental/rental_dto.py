from datetime import date
from pydantic import BaseModel


class RentalCreateRequest(BaseModel):
    customer_id: int
    expected_return_date: date
    rental_copy_ids: list[int]


class RentalResponse(BaseModel):
    id: int
    customer_id: int
    status_id: int
    rental_date: date
    expected_return_date: date
    total_amount: float

    model_config = {"from_attributes": True}
    
