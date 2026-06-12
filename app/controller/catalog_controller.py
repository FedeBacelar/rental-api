from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dto.catalog import (
    CustomerStatusResponse,
    GenreResponse,
    PlatformResponse,
    RentalCopyStatusResponse,
)
from app.services.catalog_service import CatalogService

router = APIRouter(prefix="/catalogs", tags=["catalogs"])


@router.get("/genres", response_model=list[GenreResponse])
def list_genres(db: Session = Depends(get_db)) -> list[GenreResponse]:
    service = CatalogService(db)
    genres = service.list_genres()

    if genres is None:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Issue 1.1 pending implementation",
        )

    return genres


@router.get("/platforms", response_model=list[PlatformResponse])
def list_platforms(db: Session = Depends(get_db)) -> list[PlatformResponse]:
    # La logica pendiente vive en CatalogService.list_platforms().
    service = CatalogService(db)
    platforms = service.list_platforms()

    if platforms is None:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Issue 1.2",
        )

    return platforms


@router.get("/rental-copy-statuses", response_model=list[RentalCopyStatusResponse])
def list_rental_copy_statuses(
    db: Session = Depends(get_db),
) -> list[RentalCopyStatusResponse]:
    # Issue 1.3: este endpoint ya esta conectado.
    # La logica pendiente vive en CatalogService.list_rental_copy_statuses().
    service = CatalogService(db)
    statuses = service.list_rental_copy_statuses()

    if statuses is None:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Issue 1.3 pending implementation",
        )

    return statuses


@router.get("/customer-statuses", response_model=list[CustomerStatusResponse])
def list_customer_statuses(
    db: Session = Depends(get_db),
) -> list[CustomerStatusResponse]:
    # Issue 1.4: este endpoint ya esta conectado.
    # La logica pendiente vive en CatalogService.list_customer_statuses().
    service = CatalogService(db)
    statuses = service.list_customer_statuses()

    if statuses is None:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Issue 1.4 pending implementation",
        )

    return statuses
