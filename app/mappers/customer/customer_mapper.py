from app.dto.customer import CustomerResponse
from app.models.customer.customer import Customer


def customer_to_customer_response(customer: Customer) -> CustomerResponse:
    # Convierte el modelo interno Customer al DTO que expone la API.
    return CustomerResponse(
        id=customer.id,
        status_id=customer.status_id,
        first_name=customer.first_name,
        last_name=customer.last_name,
        document_number=customer.document_number,
        email=customer.email,
        phone=customer.phone,
        address=customer.address,
        is_active=customer.is_active,
    )


def customers_to_customer_response(customers: list[Customer]) -> list[CustomerResponse]:
    # Reutiliza el mapeo individual para mantener respuestas consistentes.
    return [customer_to_customer_response(customer) for customer in customers]
