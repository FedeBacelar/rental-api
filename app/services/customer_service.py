from sqlalchemy.orm import Session

from app.dto.customer import CustomerCreateRequest, CustomerResponse


class CustomerService:
    def __init__(self, db: Session):
        self.db = db

    def create_customer(self, request: CustomerCreateRequest) -> CustomerResponse:
        # Issue 2.1: implementar este metodo.
        # Validar que no exista otro cliente con el mismo document_number.
        # Usar CustomerStatusTypeRepository para obtener el estado inicial del cliente.
        # Usar CustomerRepository para crear el cliente.
        # Convertir el resultado al DTO CustomerResponse con la estrategia que prefieras.
        pass

    def search_customers(self, query: str) -> list[CustomerResponse]:
        # Issue 2.2: implementar este metodo.
        # Buscar clientes existentes segun el criterio recibido.
        # Usar CustomerRepository y agregar metodos nuevos si hace falta.
        # Convertir el resultado al DTO CustomerResponse con la estrategia que prefieras.
        pass

    def list_active_customers(self) -> list[CustomerResponse]:
        # Issue 2.3: implementar este metodo.
        # Usar CustomerRepository para obtener clientes activos.
        # Convertir el resultado al DTO CustomerResponse con la estrategia que prefieras.
        # Devolver una lista de clientes para que el controller responda al endpoint.
        pass
