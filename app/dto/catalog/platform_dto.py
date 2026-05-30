from pydantic import BaseModel


class PlatformResponse(BaseModel):
    id: int
    code: str
    name: str
    is_active: bool
