from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dto.customer import CustomerCreateRequest, CustomerResponse
from app.services.customer_service import CustomerService


router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    request: CustomerCreateRequest,
    db: Session = Depends(get_db),
) -> CustomerResponse:
    service = CustomerService(db)

    return service.create_customer(request)


@router.get("/search", response_model=list[CustomerResponse])
def search_customers(
    query: str,
    db: Session = Depends(get_db),
) -> list[CustomerResponse]:
    service = CustomerService(db)
    customers = service.search_customers(query)

    return customers


@router.get("/active", response_model=list[CustomerResponse])
def list_active_customers(db: Session = Depends(get_db)) -> list[CustomerResponse]:
    service = CustomerService(db)

    return service.list_active_customers()
