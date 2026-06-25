from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.dto.customer import CustomerCreateRequest, CustomerResponse
from app.mappers.customer import (
    customer_to_customer_response,
    customers_to_customer_response,
)
from app.repositories.catalog.customer_status_type_repository import CustomerStatusTypeRepository
from app.repositories.rental.customer_repository import CustomerRepository


class CustomerService:
    def __init__(self, db: Session):
        self.db = db

    def create_customer(self, request: CustomerCreateRequest) -> CustomerResponse:
        customer_repository = CustomerRepository(self.db)
        status_repository = CustomerStatusTypeRepository(self.db)

        existing_customer = customer_repository.get_by_document_number(
            request.document_number
        )

        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A customer with this document number already exists",
            )

        active_status = status_repository.get_by_code("ACTIVE")

        if active_status is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Initial customer status ACTIVE was not found",
            )

        customer_data = {
            "status_id": active_status.id,
            "first_name": request.first_name,
            "last_name": request.last_name,
            "document_number": request.document_number,
            "email": request.email,
            "phone": request.phone,
            "address": request.address,
            "is_active": True,
        }

        customer = customer_repository.create(customer_data)

        return customer_to_customer_response(customer)

    def search_customers(self, query: str) -> list[CustomerResponse]:
        customer_repository = CustomerRepository(self.db)
        customers = customer_repository.search_customers(query)

        return customers_to_customer_response(customers)

    def list_active_customers(self) -> list[CustomerResponse]:
        customer_repository = CustomerRepository(self.db)
        customers = customer_repository.list_active()

        return customers_to_customer_response(customers)
    
    