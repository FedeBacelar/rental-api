from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ReturnRentalItemRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    copy_status_code: Literal["AVAILABLE", "DAMAGED", "LOST"] = "AVAILABLE"
    actual_return_date: date | None = None
    notes: str | None = Field(default=None, max_length=500)
