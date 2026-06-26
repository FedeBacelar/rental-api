from pydantic import BaseModel


class RentalDetailStatusResponse(BaseModel):
    id: int
    code: str
    name: str
    is_active: bool
