from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dto.rental.rental_dto import RentalCreateRequest, RentalResponse
from app.services.rental_service import RentalService

router = APIRouter(prefix="/rentals", tags=["rentals"])


@router.post("/", response_model=RentalResponse, status_code=status.HTTP_201_CREATED)
def create_rental(
    request: RentalCreateRequest,
    db: Session = Depends(get_db),
) -> RentalResponse:
    service = RentalService(db)
    return service.create_rental(request)