from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.auth import require_permission
from app.db.session import get_db
from app.dto.rental.rental_detail_dto import RentalDetailResponse
from app.dto.rental.rental_dto import RentalCreateRequest, RentalResponse
from app.dto.rental.rental_return_dto import ReturnRentalItemRequest
from app.enums.security import PermissionCode
from app.services.rental.rental_service import RentalService

router = APIRouter(prefix="/rentals", tags=["rentals"])


@router.post(
    "",
    response_model=RentalResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission(PermissionCode.RENTALS_MANAGE))],
)
def create_rental(
    request: RentalCreateRequest,
    db: Session = Depends(get_db),
) -> RentalResponse:
    service = RentalService(db)
    return service.create_rental(request)


@router.get(
    "",
    response_model=list[RentalResponse],
    dependencies=[Depends(require_permission(PermissionCode.RENTALS_READ))],
)
def list_rentals(
    customer_id: int | None = Query(default=None, gt=0),
    status_code: str | None = None,
    overdue: bool = False,
    db: Session = Depends(get_db),
) -> list[RentalResponse]:
    service = RentalService(db)
    return service.list_rentals(
        customer_id=customer_id,
        status_code=status_code,
        overdue=overdue,
    )


@router.get(
    "/customer/{customer_id}",
    response_model=list[RentalResponse],
    dependencies=[Depends(require_permission(PermissionCode.RENTALS_READ))],
)
def list_rentals_by_customer(
    customer_id: int,
    db: Session = Depends(get_db),
) -> list[RentalResponse]:
    service = RentalService(db)
    return service.list_rentals_by_customer(customer_id)


@router.get(
    "/{rental_id}/details",
    response_model=list[RentalDetailResponse],
    dependencies=[Depends(require_permission(PermissionCode.RENTALS_READ))],
)
def list_rental_details(
    rental_id: int,
    db: Session = Depends(get_db),
) -> list[RentalDetailResponse]:
    service = RentalService(db)
    return service.list_rental_details(rental_id)


@router.get(
    "/{rental_id}",
    response_model=RentalResponse,
    dependencies=[Depends(require_permission(PermissionCode.RENTALS_READ))],
)
def get_rental(
    rental_id: int,
    db: Session = Depends(get_db),
) -> RentalResponse:
    service = RentalService(db)
    return service.get_rental(rental_id)


@router.post(
    "/details/{rental_detail_id}/return",
    response_model=RentalDetailResponse,
    dependencies=[Depends(require_permission(PermissionCode.RENTALS_MANAGE))],
)
def return_rental_item(
    rental_detail_id: int,
    request: ReturnRentalItemRequest,
    db: Session = Depends(get_db),
) -> RentalDetailResponse:
    service = RentalService(db)
    return service.return_rental_item(rental_detail_id, request)
