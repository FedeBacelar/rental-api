from datetime import datetime

from pydantic import BaseModel


class RentalDetailCopySummary(BaseModel):
    id: int
    copy_number: int
    inventory_code: str
    status_code: str | None = None


class RentalDetailItemSummary(BaseModel):
    id: int
    type_code: str
    title: str


class RentalDetailStatusSummary(BaseModel):
    code: str
    name: str


class RentalDetailResponse(BaseModel):
    id: int
    rental_id: int
    rental_copy_id: int
    rental_copy: RentalDetailCopySummary | None = None
    item: RentalDetailItemSummary | None = None
    status_id: int
    status_code: str
    status_name: str | None = None
    status: RentalDetailStatusSummary | None = None
    price_per_day: float
    late_fee_per_day: float
    replacement_cost: float
    rental_days: int
    late_days: int
    subtotal: float
    late_fee_amount: float
    replacement_fee_amount: float
    final_amount: float
    resolved_at: datetime | None = None
    notes: str | None = None
