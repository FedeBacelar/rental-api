from pydantic import BaseModel


class RentalCopyStatusResponse(BaseModel):
    id: int
    code: str
    name: str
    is_active: bool
