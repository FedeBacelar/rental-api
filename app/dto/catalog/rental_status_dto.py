from pydantic import BaseModel


class RentalStatusResponse(BaseModel):
    id: int
    code: str
    name: str
    is_active: bool
