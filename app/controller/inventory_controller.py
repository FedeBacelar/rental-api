from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.dto.inventory.movie_dto import MovieCreateRequest, MovieResponse
from app.dto.inventory.videogame_dto import VideogameCreateRequest, VideogameResponse
from app.dto.inventory.rental_item_dto import RentalItemResponse

from app.services.inventory_service import InventoryService


router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.post("/movies", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(
    request: MovieCreateRequest,
    db: Session = Depends(get_db),
) -> MovieResponse:
    service = InventoryService(db)

    return service.create_movie(request)

@router.post("/videogames", response_model=VideogameResponse, status_code=status.HTTP_201_CREATED)
def create_videogame(
    request: VideogameCreateRequest,
    db:Session = Depends(get_db),
) -> VideogameResponse:
    service = InventoryService(db)

    return service.create_videogame(request)

@router.get("/items", response_model=list [RentalItemResponse])
def list_rental_items(
    db: Session = Depends(get_db)
) -> list[RentalItemResponse]:
    service = InventoryService(db)

    return service.list_rental_items()