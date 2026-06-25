from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import require_permission
from app.db.session import get_db

from app.dto.inventory import (
    MovieCreateRequest,
    MovieResponse,
    RentalCopyCreateRequest,
    RentalCopyResponse,
    RentalItemResponse,
    VideogameCreateRequest,
    VideogameResponse,
)

from app.enums.security import PermissionCode
from app.services.inventory.inventory_service import InventoryService


router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.post(
    "/movies",
    response_model=MovieResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission(PermissionCode.INVENTORY_MANAGE))],
)
def create_movie(
    request: MovieCreateRequest,
    db: Session = Depends(get_db),
) -> MovieResponse:
    service = InventoryService(db)

    return service.create_movie(request)


@router.post(
    "/videogames",
    response_model=VideogameResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission(PermissionCode.INVENTORY_MANAGE))],
)
def create_videogame(
    request: VideogameCreateRequest,
    db: Session = Depends(get_db),
) -> VideogameResponse:
    service = InventoryService(db)

    return service.create_videogame(request)


@router.post(
    "/copies",
    response_model=RentalCopyResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission(PermissionCode.INVENTORY_MANAGE))],
)
def create_rental_copy(
    request: RentalCopyCreateRequest,
    db: Session = Depends(get_db),
) -> RentalCopyResponse:
    service = InventoryService(db)

    return service.create_rental_copy(request)


@router.get(
    "/items",
    response_model=list[RentalItemResponse],
    dependencies=[Depends(require_permission(PermissionCode.INVENTORY_READ))],
)
def list_rental_items(
    db: Session = Depends(get_db),
) -> list[RentalItemResponse]:
    service = InventoryService(db)

    return service.list_rental_items()


@router.get(
    "/items/{item_id}",
    response_model=MovieResponse | VideogameResponse,
    dependencies=[Depends(require_permission(PermissionCode.INVENTORY_READ))],
)
def get_rental_item(
    item_id: int,
    db: Session = Depends(get_db),
) -> MovieResponse | VideogameResponse:
    service = InventoryService(db)

    return service.get_rental_item(item_id)


@router.get(
    "/items/{item_id}/copies",
    response_model=list[RentalCopyResponse],
    dependencies=[Depends(require_permission(PermissionCode.INVENTORY_READ))],
)
def list_rental_copies_by_item(
    item_id: int,
    db: Session = Depends(get_db),
) -> list[RentalCopyResponse]:
    service = InventoryService(db)

    return service.list_rental_copies_by_item(item_id)


@router.get(
    "/copies/available",
    response_model=list[RentalCopyResponse],
    dependencies=[Depends(require_permission(PermissionCode.INVENTORY_READ))],
)
def list_available_rental_copies(
    db: Session = Depends(get_db),
) -> list[RentalCopyResponse]:
    service = InventoryService(db)

    return service.list_available_rental_copies()


@router.get(
    "/copies/{copy_id}",
    response_model=RentalCopyResponse,
    dependencies=[Depends(require_permission(PermissionCode.INVENTORY_READ))],
)
def get_rental_copy(
    copy_id: int,
    db: Session = Depends(get_db),
) -> RentalCopyResponse:
    service = InventoryService(db)

    return service.get_rental_copy(copy_id)
