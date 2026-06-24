from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dto.rental.rental_dto import RentalCreateRequest, RentalResponse
from app.enums.catalog.customer_status_codes import CustomerStatusCode
from app.enums.catalog.rental_copy_status_codes import RentalCopyStatusCode
from app.enums.catalog.rental_detail_status_codes import RentalDetailStatusCode
from app.enums.catalog.rental_status_codes import RentalStatusCode
from app.models.rental.rental import Rental
from app.models.rental.rental_detail import RentalDetail
from app.repositories.catalog.customer_status_type_repository import CustomerStatusTypeRepository
from app.repositories.catalog.rental_copy_status_type_repository import RentalCopyStatusTypeRepository
from app.repositories.catalog.rental_detail_status_type_repository import RentalDetailStatusTypeRepository
from app.repositories.catalog.rental_status_type_repository import RentalStatusTypeRepository
from app.repositories.inventory.rental_copy_repository import RentalCopyRepository
from app.repositories.inventory.rental_item_repository import RentalItemRepository
from app.repositories.rental.customer_repository import CustomerRepository


class RentalService:
    def __init__(self, db: Session):
        self.db = db

    def create_rental(self, request: RentalCreateRequest) -> RentalResponse:
        # --- Repositorios que vamos a usar ---
        customer_repo = CustomerRepository(self.db)
        copy_repo = RentalCopyRepository(self.db)
        item_repo = RentalItemRepository(self.db)
        customer_status_repo = CustomerStatusTypeRepository(self.db)
        copy_status_repo = RentalCopyStatusTypeRepository(self.db)
        rental_status_repo = RentalStatusTypeRepository(self.db)
        detail_status_repo = RentalDetailStatusTypeRepository(self.db)

        # --- Paso 1: traducir los codigos de estado (texto) a sus id (numero) ---
        active_customer_status = customer_status_repo.get_by_code(CustomerStatusCode.ACTIVE.value)
        available_status = copy_status_repo.get_by_code(RentalCopyStatusCode.AVAILABLE.value)
        rented_copy_status = copy_status_repo.get_by_code(RentalCopyStatusCode.RENTED.value)
        open_rental_status = rental_status_repo.get_by_code(RentalStatusCode.OPEN.value)
        rented_detail_status = detail_status_repo.get_by_code(RentalDetailStatusCode.RENTED.value)

        # --- Paso 2: validar el cliente ---
        customer = customer_repo.get_by_id(request.customer_id)
        if customer is None:
            raise HTTPException(status_code=404, detail="El cliente no existe")
        if customer.status_id != active_customer_status.id:
            raise HTTPException(status_code=400, detail="El cliente no esta activo")

        # --- Paso 3: validar que pidio al menos una copia ---
        if not request.rental_copy_ids:
            raise HTTPException(status_code=400, detail="Debe incluir al menos una copia")

        # --- Paso 4: calcular los dias de alquiler ---
        rental_date = date.today()
        rental_days = (request.expected_return_date - rental_date).days
        if rental_days <= 0:
            raise HTTPException(status_code=400, detail="La fecha de devolucion debe ser posterior a hoy")

        # --- Paso 5: validar cada copia y preparar los detalles (con snapshot de precios) ---
        copies_to_rent = []
        details_data = []
        for copy_id in request.rental_copy_ids:
            copy = copy_repo.get_by_id(copy_id)
            if copy is None:
                raise HTTPException(status_code=404, detail=f"La copia {copy_id} no existe")
            if copy.status_id != available_status.id:
                raise HTTPException(status_code=400, detail=f"La copia {copy_id} no esta disponible")

            item = item_repo.get_by_id(copy.rental_item_id)
            if item is None:
                raise HTTPException(status_code=404, detail=f"No se encontro el item de la copia {copy_id}")

            copies_to_rent.append(copy)
            details_data.append({
                "rental_copy_id": copy.id,
                "status_id": rented_detail_status.id,
                "price_per_day": item.base_daily_price,
                "late_fee_per_day": item.late_fee_per_day,
                "replacement_cost": item.replacement_cost,
                "rental_days": rental_days,
            })

        # --- Paso 6 al 8: crear todo en una sola transaccion (todo o nada) ---
        try:
            # Crear la renta (en borrador, sin commit todavia)
            rental = Rental(
                customer_id=customer.id,
                status_id=open_rental_status.id,
                rental_date=rental_date,
                expected_return_date=request.expected_return_date,
            )
            self.db.add(rental)
            self.db.flush()  # asigna el id de la renta sin confirmar aun

            # Crear los detalles, ya con el rental_id
            for data in details_data:
                detail = RentalDetail(rental_id=rental.id, **data)
                self.db.add(detail)

            # Marcar las copias como RENTED
            for copy in copies_to_rent:
                copy.status_id = rented_copy_status.id

            # Confirmar TODO de una vez
            self.db.commit()
            self.db.refresh(rental)
        except Exception:
            self.db.rollback()
            raise

        # --- Paso 9: devolver la renta creada ---
        return RentalResponse.model_validate(rental)
