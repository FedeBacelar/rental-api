from pydantic import BaseModel, Field


class RentalCopyCreateRequest(BaseModel):
    rental_item_id: int = Field(gt=0)
    copy_number: int = Field(gt=0)
    internal_code: str = Field(min_length=1, max_length=80)


class RentalCopyResponse(BaseModel):
    id: int
    rental_item_id: int
    status_id: int
    copy_number: int
    internal_code: str
    is_active: bool
