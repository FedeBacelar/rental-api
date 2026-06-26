from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dto.inventory import (
    MovieCreateRequest,
    MovieResponse,
    RentalCopyCreateRequest,
    RentalCopyResponse,
    RentalItemResponse,
    VideogameCreateRequest,
    VideogameResponse,
)
from app.enums.inventory import RentalCopyStatusCode, RentalItemTypeCode
from app.mappers.inventory import (
    movie_to_movie_response,
    videogame_to_videogame_response,
)
from app.repositories.catalog import (
    GenreRepository,
    PlatformRepository,
)
from app.repositories.inventory import (
    MovieDetailRepository,
    RentalCopyRepository,
    RentalCopyStatusTypeRepository,
    RentalItemRepository,
    RentalItemTypeRepository,
    VideogameDetailRepository,
)


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

        return movie_to_movie_response(
            rental_item,
            movie_detail,
            genre_code=genre.code,
            genre_name=genre.name,
        )


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
        
        return videogame_to_videogame_response(
            rental_item,
            videogame_detail,
            genre_code=genre.code,
            genre_name=genre.name,
            platform_code=platform.code,
            platform_name=platform.name,
        )
    
    def list_rental_items(self) -> list[RentalItemResponse]:
        item_repository = RentalItemRepository(self.db)
        items = item_repository.list_active()

        return [self._build_rental_item_response(item) for item in items]

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

            genre = GenreRepository(self.db).get_by_id(item.genre_id)

            return movie_to_movie_response(
                item,
                movie_detail,
                genre_code=genre.code if genre else None,
                genre_name=genre.name if genre else None,
            )

        if item_type.code == RentalItemTypeCode.VIDEOGAME.value:
            videogame_detail = videogame_repository.get_by_rental_item_id(item.id)

            if videogame_detail is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Videogame details were not found",
                )
            genre = GenreRepository(self.db).get_by_id(item.genre_id)
            platform = PlatformRepository(self.db).get_by_id(videogame_detail.platform_id)

            return videogame_to_videogame_response(
                item,
                videogame_detail,
                genre_code=genre.code if genre else None,
                genre_name=genre.name if genre else None,
                platform_code=platform.code if platform else None,
                platform_name=platform.name if platform else None,
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unsupported rental item type: {item_type.code}",
        )

    def create_rental_copy(
        self,
        request: RentalCopyCreateRequest,
    ) -> RentalCopyResponse:
        item_repository = RentalItemRepository(self.db)
        copy_repository = RentalCopyRepository(self.db)
        copy_status_repository = RentalCopyStatusTypeRepository(self.db)

        rental_item = item_repository.get_by_id(request.rental_item_id)

        if rental_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rental item was not found",
            )

        existing_copy_number = copy_repository.get_by_item_id_and_copy_number(
            request.rental_item_id,
            request.copy_number,
        )

        if existing_copy_number is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Copy number already exists for this rental item",
            )

        existing_internal_code = copy_repository.get_by_internal_code(request.inventory_code)

        if existing_internal_code is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Internal code already exists",
            )

        available_status = copy_status_repository.get_by_code(
            RentalCopyStatusCode.AVAILABLE.value
        )

        if available_status is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Rental copy status AVAILABLE was not found",
            )

        try:
            rental_copy = copy_repository.create(
                {
                    "rental_item_id": request.rental_item_id,
                    "status_id": available_status.id,
                    "copy_number": request.copy_number,
                    "internal_code": request.inventory_code,
                    "is_active": True,
                }
            )

        except IntegrityError as exc:
            self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Rental copy already exists",
            ) from exc

        return self._build_rental_copy_response(rental_copy)

    def get_rental_copy(self, copy_id: int) -> RentalCopyResponse:
        copy_repository = RentalCopyRepository(self.db)

        rental_copy = copy_repository.get_by_id(copy_id)

        if rental_copy is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rental copy was not found",
            )

        return self._build_rental_copy_response(rental_copy)

    def list_rental_copies_by_item(self, item_id: int) -> list[RentalCopyResponse]:
        item_repository = RentalItemRepository(self.db)
        copy_repository = RentalCopyRepository(self.db)

        rental_item = item_repository.get_by_id(item_id)

        if rental_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rental item was not found",
            )

        rental_copies = copy_repository.list_by_item_id(item_id)

        return [
            self._build_rental_copy_response(rental_copy)
            for rental_copy in rental_copies
        ]

    def list_available_rental_copies(self) -> list[RentalCopyResponse]:
        copy_repository = RentalCopyRepository(self.db)
        copy_status_repository = RentalCopyStatusTypeRepository(self.db)

        available_status = copy_status_repository.get_by_code(
            RentalCopyStatusCode.AVAILABLE.value
        )

        if available_status is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Rental copy status AVAILABLE was not found",
            )

        rental_copies = copy_repository.list_active_by_status_id(
            available_status.id
        )

        return [
            self._build_rental_copy_response(rental_copy)
            for rental_copy in rental_copies
        ]

    def _build_rental_item_response(self, item) -> RentalItemResponse:
        item_type = RentalItemTypeRepository(self.db).get_by_id(item.item_type_id)
        genre = GenreRepository(self.db).get_by_id(item.genre_id)

        return RentalItemResponse(
            id=item.id,
            item_type_id=item.item_type_id,
            item_type_code=item_type.code if item_type else None,
            item_type_name=item_type.name if item_type else None,
            genre_id=item.genre_id,
            genre_code=genre.code if genre else None,
            genre_name=genre.name if genre else None,
            title=item.title,
            description=item.description,
            age_rating=item.age_rating,
            base_daily_price=item.base_daily_price,
            late_fee_per_day=item.late_fee_per_day,
            replacement_cost=item.replacement_cost,
            is_active=item.is_active,
        )

    def _build_rental_copy_response(self, rental_copy) -> RentalCopyResponse:
        item_repository = RentalItemRepository(self.db)
        item_type_repository = RentalItemTypeRepository(self.db)
        copy_status_repository = RentalCopyStatusTypeRepository(self.db)

        item = item_repository.get_by_id(rental_copy.rental_item_id)
        item_type = item_type_repository.get_by_id(item.item_type_id) if item else None
        status = copy_status_repository.get_by_id(rental_copy.status_id)

        return RentalCopyResponse(
            id=rental_copy.id,
            rental_item_id=rental_copy.rental_item_id,
            item_title=item.title if item else None,
            item_type_code=item_type.code if item_type else None,
            status_id=rental_copy.status_id,
            status_code=status.code if status else None,
            status_name=status.name if status else None,
            copy_number=rental_copy.copy_number,
            inventory_code=rental_copy.internal_code,
            is_active=rental_copy.is_active,
        )
