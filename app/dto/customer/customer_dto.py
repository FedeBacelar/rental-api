from pydantic import BaseModel, EmailStr


class CustomerCreateRequest(BaseModel):
    first_name: str
    last_name: str
    document_number: str
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None


class CustomerResponse(BaseModel):
    id: int
    status_id: int
    status_code: str | None = None
    status_name: str | None = None
    first_name: str
    last_name: str
    full_name: str | None = None
    document_number: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    is_active: bool
