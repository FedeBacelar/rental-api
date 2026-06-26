from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import require_permission
from app.db.session import get_db
from app.dto.catalog import (
    CustomerStatusResponse,
    GenreResponse,
    PlatformResponse,
    RentalDetailStatusResponse,
    RentalCopyStatusResponse,
    RentalStatusResponse,
)
from app.enums.security import PermissionCode
from app.services.catalog.catalog_service import CatalogService

router = APIRouter(
    prefix="/catalogs",
    tags=["catalogs"],
    dependencies=[Depends(require_permission(PermissionCode.CATALOGS_READ))],
)


@router.get("/genres", response_model=list[GenreResponse])
def list_genres(db: Session = Depends(get_db)) -> list[GenreResponse]:
    service = CatalogService(db)
    return service.list_genres()


@router.get("/platforms", response_model=list[PlatformResponse])
def list_platforms(db: Session = Depends(get_db)) -> list[PlatformResponse]:
    service = CatalogService(db)
    return service.list_platforms()


@router.get("/rental-copy-statuses", response_model=list[RentalCopyStatusResponse])
def list_rental_copy_statuses(
    db: Session = Depends(get_db),
) -> list[RentalCopyStatusResponse]:
    service = CatalogService(db)
    return service.list_rental_copy_statuses()


@router.get("/customer-statuses", response_model=list[CustomerStatusResponse])
def list_customer_statuses(
    db: Session = Depends(get_db),
) -> list[CustomerStatusResponse]:
    service = CatalogService(db)

    return service.list_customer_statuses()


@router.get("/rental-statuses", response_model=list[RentalStatusResponse])
def list_rental_statuses(
    db: Session = Depends(get_db),
) -> list[RentalStatusResponse]:
    service = CatalogService(db)
    return service.list_rental_statuses()


@router.get("/rental-detail-statuses", response_model=list[RentalDetailStatusResponse])
def list_rental_detail_statuses(
    db: Session = Depends(get_db),
) -> list[RentalDetailStatusResponse]:
    service = CatalogService(db)
    return service.list_rental_detail_statuses()
