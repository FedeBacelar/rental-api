from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.dto.inventory import MovieCreateRequest, MovieResponse
from app.dto.inventory.rental_item_dto import RentalItemResponse
from app.repositories.inventory import RentalItemRepository

from app.enums import RentalItemTypeCode

from app.mappers.inventory import (
    movie_to_movie_response,
    videogame_to_videogame_response,
    rental_items_to_rental_item_response
)

from app.dto.inventory.videogame_dto import VideogameCreateRequest, VideogameResponse

from app.repositories.inventory.videogame_detail_repository import VideogameDetailRepository
from app.repositories.inventory.movie_detail_repository import MovieDetailRepository
from app.repositories.inventory.rental_item_repository import RentalItemRepository

from app.repositories.catalog.rental_item_type_repository import RentalItemTypeRepository
from app.repositories.catalog.genre_repository import GenreRepository
from app.repositories.catalog.platform_repository import PlatformRepository


class InventoryService:
    def __init__(self, db: Session):
        self.db = db

    def create_movie(self, request: MovieCreateRequest) -> MovieResponse:
        rental_item_repository = RentalItemRepository(self.db)
        movie_detail_repository = MovieDetailRepository(self.db)
        genre_repository = GenreRepository(self.db)
        rental_item_type_repository = RentalItemTypeRepository(self.db)

        movie_type = rental_item_type_repository.get_by_code("MOVIE")

        if movie_type is None: 
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Rental item type MOVIE was not found",
            )
        
        genre = genre_repository.get_by_id(request.genre_id)

        if genre is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Genre was not found",
            )
        
        try:
            rental_item = rental_item_repository.create_pending(
                {
                    "item_type_id": movie_type.id,
                    "genre_id": request.genre_id,
                    "title": request.title,
                    "description": request.description,
                    "age_rating": request.age_rating,
                    "base_daily_price": request.base_daily_price,
                    "late_fee_per_day": request.late_fee_per_day,
                    "replacement_cost": request.replacement_cost,
                    "is_active": True,
                }
            )

            movie_detail = movie_detail_repository.create_pending(
                {
                    "rental_item_id": rental_item.id,
                    "duration_minutes": request.duration_minutes,
                    "director": request.director,
                    "original_language": request.original_language,
                }
            )

            self.db.commit()

            self.db.refresh(rental_item)
            self.db.refresh(movie_detail)

        except Exception:
            self.db.rollback()
            raise

        return movie_to_movie_response(rental_item, movie_detail)


    def create_videogame(self, request: VideogameCreateRequest) -> VideogameResponse:
        rental_item_repository = RentalItemRepository(self.db)
        videogame_detail_repository = VideogameDetailRepository(self.db)
        rental_item_type_repository = RentalItemTypeRepository(self.db)
        genre_repository = GenreRepository(self.db)
        platform_repository = PlatformRepository(self.db)

        item_type = rental_item_type_repository.get_by_code("VIDEOGAME")

        genre = genre_repository.get_by_id(request.genre_id)

        if genre is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Genre was not found",
            )
        
        platform = platform_repository.get_by_id(request.platform_id)

        if platform is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Platform was not found",
            )

        if item_type is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Rental item type VIDEOGAME was not found",
            )
        
        try:  
            rental_item = rental_item_repository.create_pending(
                {
                    "item_type_id": item_type.id,
                    "genre_id": request.genre_id,
                    "title": request.title,
                    "description": request.description,
                    "age_rating": request.age_rating,
                    "base_daily_price": request.base_daily_price,
                    "late_fee_per_day": request.late_fee_per_day,
                    "replacement_cost": request.replacement_cost,
                    "is_active": True,
                }
            )

            videogame_detail = videogame_detail_repository.create_pending(
                {
                    "rental_item_id": rental_item.id,
                    "platform_id": request.platform_id,
                    "publisher": request.publisher,
                    "multiplayer": request.multiplayer,
                }
            )

            self.db.commit()
            self.db.refresh(rental_item)
            self.db.refresh(videogame_detail)

        except Exception:
            self.db.rollback()
            raise
        
        return videogame_to_videogame_response(rental_item, videogame_detail)
    
    def list_rental_items(self) -> list[RentalItemResponse]:
        item_repository = RentalItemRepository(self.db)
        items = item_repository.list_active()

        return rental_items_to_rental_item_response(items)

    def get_rental_item(self, item_id: int) -> MovieResponse | VideogameResponse:
        item_repository = RentalItemRepository(self.db)
        item_type_repository = RentalItemTypeRepository(self.db)
        movie_repository = MovieDetailRepository(self.db)
        videogame_repository = VideogameDetailRepository(self.db)

        item = item_repository.get_by_id(item_id)

        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rental item was not found",
            )

        item_type = item_type_repository.get_by_id(item.item_type_id)

        if item_type is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Rental item type was not found",
            )

        if item_type.code == RentalItemTypeCode.MOVIE.value:
            movie_detail = movie_repository.get_by_rental_item_id(item.id)

            if movie_detail is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Movie details were not found",
                )

            return movie_to_movie_response(item, movie_detail)

        if item_type.code == RentalItemTypeCode.VIDEOGAME.value:
            videogame_detail = videogame_repository.get_by_rental_item_id(item.id)

            if videogame_detail is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Videogame details were not found",
                )
            return videogame_to_videogame_response(item, videogame_detail)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unsupported rental item type: {item_type.code}",
        )
