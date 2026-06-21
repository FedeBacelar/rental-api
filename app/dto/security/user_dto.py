from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.enums.catalog import UserStatusCode
from app.enums.security import RoleCode


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    role_code: RoleCode


class UserRoleUpdateRequest(BaseModel):
    role_code: RoleCode


class UserStatusUpdateRequest(BaseModel):
    status_code: UserStatusCode


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role_code: str
    status_code: str
    created_at: datetime
    updated_at: datetime
