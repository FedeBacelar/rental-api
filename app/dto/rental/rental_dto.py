from datetime import date
from pydantic import BaseModel, Field


class RentalCustomerSummary(BaseModel):
    id: int
    full_name: str
    document_number: str


class RentalStatusSummary(BaseModel):
    code: str
    name: str


class RentalCreateRequest(BaseModel):
    customer_id: int = Field(gt=0)
    expected_return_date: date
    rental_copy_ids: list[int] = Field(min_length=1)


class RentalResponse(BaseModel):
    id: int
    customer_id: int
    customer: RentalCustomerSummary | None = None
    status_id: int
    status_code: str
    status_name: str | None = None
    status: RentalStatusSummary | None = None
    rental_date: date
    expected_return_date: date
    actual_return_date: date | None = None
    total_amount: float
    late_fee_amount: float = 0
    final_amount: float | None = None
    items_count: int | None = None
    pending_items_count: int | None = None

    model_config = {"from_attributes": True}
