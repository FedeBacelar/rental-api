from pydantic import BaseModel


class CustomerStatusResponse(BaseModel):
    id: int
    code: str
    name: str
    is_active: bool
