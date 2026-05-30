from pydantic import BaseModel


class GenreResponse(BaseModel):
    id: int
    code: str
    name: str
    is_active: bool
