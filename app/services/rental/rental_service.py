from datetime import date, datetime
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dto.rental.rental_detail_dto import (
    RentalDetailCopySummary,
    RentalDetailItemSummary,
    RentalDetailResponse,
    RentalDetailStatusSummary,
)
from app.dto.rental.rental_dto import (
    RentalCreateRequest,
    RentalCustomerSummary,
    RentalResponse,
    RentalStatusSummary,
)
from app.dto.rental.rental_return_dto import ReturnRentalItemRequest
from app.enums.customer import CustomerStatusCode
from app.enums.inventory import RentalCopyStatusCode
from app.enums.rental import RentalDetailStatusCode, RentalStatusCode
from app.models.rental.rental import Rental
from app.models.rental.rental_detail import RentalDetail
from app.repositories.customer.customer_repository import CustomerRepository
from app.repositories.customer.customer_status_type_repository import CustomerStatusTypeRepository
from app.repositories.inventory.rental_copy_repository import RentalCopyRepository
from app.repositories.inventory.rental_copy_status_type_repository import RentalCopyStatusTypeRepository
from app.repositories.inventory.rental_item_repository import RentalItemRepository
from app.repositories.inventory.rental_item_type_repository import RentalItemTypeRepository
from app.repositories.rental.rental_detail_repository import RentalDetailRepository
from app.repositories.rental.rental_detail_status_type_repository import RentalDetailStatusTypeRepository
from app.repositories.rental.rental_repository import RentalRepository
from app.repositories.rental.rental_status_type_repository import RentalStatusTypeRepository


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
        partially_returned_status = rental_status_repo.get_by_code(RentalStatusCode.PARTIALLY_RETURNED.value)
        overdue_rental_status = rental_status_repo.get_by_code(RentalStatusCode.OVERDUE.value)
        partially_overdue_status = rental_status_repo.get_by_code(RentalStatusCode.PARTIALLY_OVERDUE.value)
        rented_detail_status = detail_status_repo.get_by_code(RentalDetailStatusCode.RENTED.value)
        overdue_detail_status = detail_status_repo.get_by_code(RentalDetailStatusCode.OVERDUE.value)

        required_statuses = [
            open_rental_status,
            partially_returned_status,
            overdue_rental_status,
            partially_overdue_status,
            rented_detail_status,
            overdue_detail_status,
        ]
        if any(status is None for status in required_statuses):
            raise RuntimeError("Faltan estados base para marcar rentas vencidas")

        overdue_rentals = rental_repo.list_overdue_by_status_ids(
            status_ids=[open_rental_status.id, partially_returned_status.id],
            today=today,
        )

        updated_details_count = 0
        for rental in overdue_rentals:
            if rental.status_id == partially_returned_status.id:
                rental.status_id = partially_overdue_status.id
            else:
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
        return self._build_rental_response(rental)

    def get_rental(self, rental_id: int) -> RentalResponse:
        rental_repo = RentalRepository(self.db)

        # Buscar la renta por id
        rental = rental_repo.get_by_id(rental_id)
        if rental is None:
            raise HTTPException(status_code=404, detail="La renta no existe")

        return self._build_rental_response(rental)

    def list_rentals(
        self,
        customer_id: int | None = None,
        status_code: str | None = None,
        overdue: bool = False,
    ) -> list[RentalResponse]:
        customer_repo = CustomerRepository(self.db)
        rental_repo = RentalRepository(self.db)
        rental_status_repo = RentalStatusTypeRepository(self.db)

        if customer_id is not None and customer_repo.get_by_id(customer_id) is None:
            raise HTTPException(status_code=404, detail="El cliente no existe")

        status_id = None
        if status_code is not None:
            status = rental_status_repo.get_by_code(status_code)
            if status is None:
                raise HTTPException(status_code=400, detail="El estado de renta no existe")
            status_id = status.id

        overdue_status_ids = None
        if overdue:
            overdue_codes = [
                RentalStatusCode.OPEN.value,
                RentalStatusCode.OVERDUE.value,
                RentalStatusCode.PARTIALLY_RETURNED.value,
                RentalStatusCode.PARTIALLY_OVERDUE.value,
            ]
            statuses = [
                rental_status_repo.get_by_code(code)
                for code in overdue_codes
            ]
            overdue_status_ids = [
                status.id
                for status in statuses
                if status is not None
            ]

        rentals = rental_repo.list_filtered(
            customer_id=customer_id,
            status_id=status_id,
            overdue_status_ids=overdue_status_ids,
            today=date.today() if overdue else None,
        )
        return [self._build_rental_response(rental) for rental in rentals]

    def list_rentals_by_customer(self, customer_id: int) -> list[RentalResponse]:
        customer_repo = CustomerRepository(self.db)
        rental_repo = RentalRepository(self.db)

        customer = customer_repo.get_by_id(customer_id)
        if customer is None:
            raise HTTPException(status_code=404, detail="El cliente no existe")

        rentals = rental_repo.list_by_customer_id(customer_id)
        return [self._build_rental_response(rental) for rental in rentals]

    def list_rental_details(self, rental_id: int) -> list[RentalDetailResponse]:
        rental_repo = RentalRepository(self.db)
        detail_repo = RentalDetailRepository(self.db)

        rental = rental_repo.get_by_id(rental_id)
        if rental is None:
            raise HTTPException(status_code=404, detail="La renta no existe")

        details = detail_repo.list_by_rental_id(rental_id)
        return [self._build_rental_detail_response(detail) for detail in details]

    def return_rental_item(
        self,
        rental_detail_id: int,
        request: ReturnRentalItemRequest,
    ) -> RentalDetailResponse:
        return_date = request.actual_return_date or date.today()

        detail_repo = RentalDetailRepository(self.db)
        rental_repo = RentalRepository(self.db)
        copy_repo = RentalCopyRepository(self.db)
        detail_status_repo = RentalDetailStatusTypeRepository(self.db)
        rental_status_repo = RentalStatusTypeRepository(self.db)
        copy_status_repo = RentalCopyStatusTypeRepository(self.db)

        rented_detail_status = detail_status_repo.get_by_code(RentalDetailStatusCode.RENTED.value)
        overdue_detail_status = detail_status_repo.get_by_code(RentalDetailStatusCode.OVERDUE.value)
        returned_detail_status = detail_status_repo.get_by_code(RentalDetailStatusCode.RETURNED.value)
        lost_detail_status = detail_status_repo.get_by_code(RentalDetailStatusCode.LOST.value)

        rented_copy_status = copy_status_repo.get_by_code(RentalCopyStatusCode.RENTED.value)
        final_copy_status = copy_status_repo.get_by_code(request.copy_status_code)

        closed_rental_status = rental_status_repo.get_by_code(RentalStatusCode.CLOSED.value)
        partially_returned_status = rental_status_repo.get_by_code(RentalStatusCode.PARTIALLY_RETURNED.value)
        partially_overdue_status = rental_status_repo.get_by_code(RentalStatusCode.PARTIALLY_OVERDUE.value)

        required_statuses = [
            rented_detail_status,
            overdue_detail_status,
            returned_detail_status,
            lost_detail_status,
            rented_copy_status,
            final_copy_status,
            closed_rental_status,
            partially_returned_status,
            partially_overdue_status,
        ]
        if any(status is None for status in required_statuses):
            raise HTTPException(status_code=500, detail="Faltan estados base para devolver la copia")

        detail = detail_repo.get_by_id(rental_detail_id)
        if detail is None:
            raise HTTPException(status_code=404, detail="El detalle de renta no existe")
        if detail.status_id not in {rented_detail_status.id, overdue_detail_status.id}:
            raise HTTPException(status_code=400, detail="El detalle de renta ya fue resuelto")

        rental = rental_repo.get_by_id(detail.rental_id)
        if rental is None:
            raise HTTPException(status_code=404, detail="La renta asociada no existe")
        if return_date < rental.rental_date:
            raise HTTPException(status_code=400, detail="La fecha de devolucion no puede ser anterior a la renta")

        copy = copy_repo.get_by_id(detail.rental_copy_id)
        if copy is None:
            raise HTTPException(status_code=404, detail="La copia asociada no existe")
        if copy.status_id != rented_copy_status.id:
            raise HTTPException(status_code=400, detail="La copia no esta alquilada")

        late_days = max((return_date - rental.expected_return_date).days, 0)
        late_fee_amount = Decimal(detail.late_fee_per_day) * late_days
        replacement_fee_amount = Decimal("0")
        final_detail_status_id = returned_detail_status.id

        if request.copy_status_code == RentalCopyStatusCode.LOST.value:
            replacement_fee_amount = Decimal(detail.replacement_cost)
            final_detail_status_id = lost_detail_status.id

        detail.status_id = final_detail_status_id
        detail.late_days = late_days
        detail.late_fee_amount = late_fee_amount
        detail.replacement_fee_amount = replacement_fee_amount
        detail.final_amount = Decimal(detail.subtotal) + late_fee_amount + replacement_fee_amount
        detail.resolved_at = datetime.now()
        detail.notes = request.notes

        copy.status_id = final_copy_status.id

        rental_details = detail_repo.list_by_rental_id(rental.id)
        has_pending_details = any(
            item.status_id in {rented_detail_status.id, overdue_detail_status.id}
            for item in rental_details
        )
        has_overdue_pending_details = any(
            item.status_id == overdue_detail_status.id
            for item in rental_details
        )

        if has_pending_details:
            if has_overdue_pending_details:
                rental.status_id = partially_overdue_status.id
            else:
                rental.status_id = partially_returned_status.id
        else:
            rental.status_id = closed_rental_status.id
            rental.actual_return_date = return_date

        rental.late_fee_amount = sum(Decimal(item.late_fee_amount) for item in rental_details)
        rental.final_amount = sum(Decimal(item.final_amount) for item in rental_details)

        try:
            self.db.commit()
            self.db.refresh(detail)
        except Exception:
            self.db.rollback()
            raise

        return self._build_rental_detail_response(detail)

    def _build_rental_response(self, rental: Rental) -> RentalResponse:
        customer = CustomerRepository(self.db).get_by_id(rental.customer_id)
        status = RentalStatusTypeRepository(self.db).get_by_id(rental.status_id)
        if status is None:
            raise HTTPException(status_code=500, detail="El estado de la renta no existe")

        details = RentalDetailRepository(self.db).list_by_rental_id(rental.id)
        detail_status_repo = RentalDetailStatusTypeRepository(self.db)
        rented_status = detail_status_repo.get_by_code(RentalDetailStatusCode.RENTED.value)
        overdue_status = detail_status_repo.get_by_code(RentalDetailStatusCode.OVERDUE.value)
        pending_status_ids = {
            item.id
            for item in [rented_status, overdue_status]
            if item is not None
        }

        customer_summary = None
        if customer is not None:
            customer_summary = RentalCustomerSummary(
                id=customer.id,
                full_name=f"{customer.first_name} {customer.last_name}",
                document_number=customer.document_number,
            )

        status_summary = RentalStatusSummary(
            code=status.code,
            name=status.name,
        )

        return RentalResponse(
            id=rental.id,
            customer_id=rental.customer_id,
            customer=customer_summary,
            status_id=rental.status_id,
            status_code=status.code,
            status_name=status.name,
            status=status_summary,
            rental_date=rental.rental_date,
            expected_return_date=rental.expected_return_date,
            actual_return_date=rental.actual_return_date,
            total_amount=rental.total_amount,
            late_fee_amount=rental.late_fee_amount,
            final_amount=rental.final_amount,
            items_count=len(details),
            pending_items_count=sum(
                1 for detail in details if detail.status_id in pending_status_ids
            ),
        )

    def _build_rental_detail_response(self, detail: RentalDetail) -> RentalDetailResponse:
        copy = RentalCopyRepository(self.db).get_by_id(detail.rental_copy_id)
        item = RentalItemRepository(self.db).get_by_id(copy.rental_item_id) if copy else None
        item_type = RentalItemTypeRepository(self.db).get_by_id(item.item_type_id) if item else None
        copy_status = RentalCopyStatusTypeRepository(self.db).get_by_id(copy.status_id) if copy else None
        detail_status = RentalDetailStatusTypeRepository(self.db).get_by_id(detail.status_id)
        if detail_status is None:
            raise HTTPException(status_code=500, detail="El estado del detalle no existe")

        copy_summary = None
        if copy is not None:
            copy_summary = RentalDetailCopySummary(
                id=copy.id,
                copy_number=copy.copy_number,
                inventory_code=copy.internal_code,
                status_code=copy_status.code if copy_status else None,
            )

        item_summary = None
        if item is not None and item_type is not None:
            item_summary = RentalDetailItemSummary(
                id=item.id,
                type_code=item_type.code,
                title=item.title,
            )

        status_summary = RentalDetailStatusSummary(
            code=detail_status.code,
            name=detail_status.name,
        )

        return RentalDetailResponse(
            id=detail.id,
            rental_id=detail.rental_id,
            rental_copy_id=detail.rental_copy_id,
            rental_copy=copy_summary,
            item=item_summary,
            status_id=detail.status_id,
            status_code=detail_status.code,
            status_name=detail_status.name,
            status=status_summary,
            price_per_day=detail.price_per_day,
            late_fee_per_day=detail.late_fee_per_day,
            replacement_cost=detail.replacement_cost,
            rental_days=detail.rental_days,
            late_days=detail.late_days,
            subtotal=detail.subtotal,
            late_fee_amount=detail.late_fee_amount,
            replacement_fee_amount=detail.replacement_fee_amount,
            final_amount=detail.final_amount,
            resolved_at=detail.resolved_at,
            notes=detail.notes,
        )
