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
    first_name: str
    last_name: str
    document_number: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    is_active: bool
