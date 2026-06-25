from datetime import datetime

from pydantic import BaseModel


class RentalDetailResponse(BaseModel):
    id: int
    rental_id: int
    rental_copy_id: int
    status_id: int
    status_code: str
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
