from datetime import date
from decimal import Decimal

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
from app.repositories.rental.rental_detail_repository import RentalDetailRepository
from app.repositories.rental.rental_repository import RentalRepository


class RentalService:
    def __init__(self, db: Session):
        self.db = db

    def mark_overdue_rentals(self, today: date | None = None) -> dict[str, int]:
        today = today or date.today()

        rental_status_repo = RentalStatusTypeRepository(self.db)
        detail_status_repo = RentalDetailStatusTypeRepository(self.db)
        rental_repo = RentalRepository(self.db)
        detail_repo = RentalDetailRepository(self.db)

        open_rental_status = rental_status_repo.get_by_code(RentalStatusCode.OPEN.value)
        overdue_rental_status = rental_status_repo.get_by_code(RentalStatusCode.OVERDUE.value)
        rented_detail_status = detail_status_repo.get_by_code(RentalDetailStatusCode.RENTED.value)
        overdue_detail_status = detail_status_repo.get_by_code(RentalDetailStatusCode.OVERDUE.value)

        required_statuses = [
            open_rental_status,
            overdue_rental_status,
            rented_detail_status,
            overdue_detail_status,
        ]
        if any(status is None for status in required_statuses):
            raise RuntimeError("Faltan estados base para marcar rentas vencidas")

        overdue_rentals = rental_repo.list_open_overdue(
            open_status_id=open_rental_status.id,
            today=today,
        )

        updated_details_count = 0
        for rental in overdue_rentals:
            rental.status_id = overdue_rental_status.id

            details = detail_repo.list_by_rental_id_and_status_id(
                rental_id=rental.id,
                status_id=rented_detail_status.id,
            )

            for detail in details:
                detail.status_id = overdue_detail_status.id
                updated_details_count += 1

        self.db.commit()

        return {
            "updated_rentals": len(overdue_rentals),
            "updated_details": updated_details_count,
        }

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

        required_statuses = [
            active_customer_status,
            available_status,
            rented_copy_status,
            open_rental_status,
            rented_detail_status,
        ]
        if any(status is None for status in required_statuses):
            raise HTTPException(status_code=500, detail="Faltan estados base para crear la renta")

        # --- Paso 2: validar el cliente ---
        customer = customer_repo.get_by_id(request.customer_id)
        if customer is None:
            raise HTTPException(status_code=404, detail="El cliente no existe")
        if customer.status_id != active_customer_status.id:
            raise HTTPException(status_code=400, detail="El cliente no esta activo")

        # --- Paso 3: validar que pidio al menos una copia ---
        if not request.rental_copy_ids:
            raise HTTPException(status_code=400, detail="Debe incluir al menos una copia")
        if len(request.rental_copy_ids) != len(set(request.rental_copy_ids)):
            raise HTTPException(status_code=400, detail="No se puede incluir la misma copia mas de una vez")

        # --- Paso 4: calcular los dias de alquiler ---
        rental_date = date.today()
        rental_days = (request.expected_return_date - rental_date).days
        if rental_days <= 0:
            raise HTTPException(status_code=400, detail="La fecha de devolucion debe ser posterior a hoy")

        # --- Paso 5: validar cada copia y preparar los detalles (con snapshot de precios) ---
        copies_to_rent = []
        details_data = []
        total_amount = Decimal("0")
        for copy_id in request.rental_copy_ids:
            copy = copy_repo.get_by_id(copy_id)
            if copy is None:
                raise HTTPException(status_code=404, detail=f"La copia {copy_id} no existe")
            if not copy.is_active:
                raise HTTPException(status_code=400, detail=f"La copia {copy_id} no esta activa")
            if copy.status_id != available_status.id:
                raise HTTPException(status_code=400, detail=f"La copia {copy_id} no esta disponible")

            item = item_repo.get_by_id(copy.rental_item_id)
            if item is None:
                raise HTTPException(status_code=404, detail=f"No se encontro el item de la copia {copy_id}")
            if not item.is_active:
                raise HTTPException(status_code=400, detail=f"El item de la copia {copy_id} no esta activo")

            subtotal = Decimal(item.base_daily_price) * rental_days
            total_amount += subtotal

            copies_to_rent.append(copy)
            details_data.append({
                "rental_copy_id": copy.id,
                "status_id": rented_detail_status.id,
                "price_per_day": item.base_daily_price,
                "late_fee_per_day": item.late_fee_per_day,
                "replacement_cost": item.replacement_cost,
                "rental_days": rental_days,
                "subtotal": subtotal,
                "final_amount": subtotal,
            })

        # --- Paso 6 al 8: crear todo en una sola transaccion (todo o nada) ---
        try:
            # Crear la renta (en borrador, sin commit todavia)
            rental = Rental(
                customer_id=customer.id,
                status_id=open_rental_status.id,
                rental_date=rental_date,
                expected_return_date=request.expected_return_date,
                total_amount=total_amount,
                final_amount=total_amount,
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
        return RentalResponse(
            id=rental.id,
            customer_id=rental.customer_id,
            status_id=rental.status_id,
            status_code=open_rental_status.code,
            rental_date=rental.rental_date,
            expected_return_date=rental.expected_return_date,
            total_amount=rental.total_amount,
        )

    def get_rental(self, rental_id: int) -> RentalResponse:
        rental_repo = RentalRepository(self.db)
        rental_status_repo = RentalStatusTypeRepository(self.db)

        # Buscar la renta por id
        rental = rental_repo.get_by_id(rental_id)
        if rental is None:
            raise HTTPException(status_code=404, detail="La renta no existe")

        # Traducir el status_id (numero) a su status_code (texto)
        status = rental_status_repo.get_by_id(rental.status_id)
        if status is None:
            raise HTTPException(status_code=500, detail="El estado de la renta no existe")

        return RentalResponse(
            id=rental.id,
            customer_id=rental.customer_id,
            status_id=rental.status_id,
            status_code=status.code,
            rental_date=rental.rental_date,
            expected_return_date=rental.expected_return_date,
            total_amount=rental.total_amount,
        )
