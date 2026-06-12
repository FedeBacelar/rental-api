from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dto.inventory.movie_dto import MovieCreateRequest, MovieResponse
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.post("/movies", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(
    request: MovieCreateRequest,
    db: Session = Depends(get_db),
) -> MovieResponse:
    service = InventoryService(db)

    return service.create_movie(request)

