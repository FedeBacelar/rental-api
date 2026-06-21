from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class AuthenticatedUserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    permissions: list[str]


class LoginResponse(BaseModel):
    user: AuthenticatedUserResponse
