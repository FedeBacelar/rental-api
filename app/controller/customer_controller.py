from fastapi import APIRouter, Depends, HTTPException, status
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
    # Issue 2.1: este endpoint ya esta conectado.
    # La logica pendiente vive en CustomerService.create_customer().
    service = CustomerService(db)
    customer = service.create_customer(request)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Issue 2.1 pending implementation",
        )

    return customer


@router.get("/search", response_model=list[CustomerResponse])
def search_customers(
    query: str,
    db: Session = Depends(get_db),
) -> list[CustomerResponse]:
    # Issue 2.2: este endpoint ya esta conectado.
    # La logica pendiente vive en CustomerService.search_customers().
    service = CustomerService(db)
    customers = service.search_customers(query)

    if customers is None:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Issue 2.2 pending implementation",
        )

    return customers


@router.get("/active", response_model=list[CustomerResponse])
def list_active_customers(db: Session = Depends(get_db)) -> list[CustomerResponse]:
    # Issue 2.3: este endpoint ya esta conectado.
    # La logica pendiente vive en CustomerService.list_active_customers().
    service = CustomerService(db)
    customers = service.list_active_customers()

    if customers is None:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Issue 2.3 pending implementation",
        )

    return customers
