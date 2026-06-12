from sqlalchemy.orm import Session

from app.dto.catalog import (
    CustomerStatusResponse,
    GenreResponse,
    PlatformResponse,
    RentalCopyStatusResponse,
)
from app.mappers.catalog import (
    genres_to_genre_response, 
    platforms_to_platform_response,
)
from app.repositories.catalog.genre_repository import GenreRepository
from app.repositories.catalog.platform_repository import PlatformRepository


class CatalogService:
    def __init__(self, db: Session):
        self.db = db

    def list_genres(self) -> list[GenreResponse]:
    
        # Convertir el resultado al DTO GenreResponse con la estrategia que prefieras.
        # Devolver una lista de generos para que el controller responda al endpoint.

        # El repository concentra las consultas a la base de datos.
        # Asi el service no necesita saber como se buscan los datos en MySQL.
        genre_repository = GenreRepository(self.db)
        genres = genre_repository.list_active()

        return genres_to_genre_response(genres)

    def list_platforms(self) -> list[PlatformResponse]:
        platform_repository = PlatformRepository(self.db)
        platforms = platform_repository.list_active()

        return platforms_to_platform_response(platforms)

    def list_rental_copy_statuses(self) -> list[RentalCopyStatusResponse]:
        # Issue 1.3: implementar este metodo.
        # Usar RentalCopyStatusTypeRepository para obtener los estados de copia activos.
        # Convertir el resultado al DTO RentalCopyStatusResponse con la estrategia que prefieras.
        # Devolver una lista de estados para que el controller responda al endpoint.
        pass

    def list_customer_statuses(self) -> list[CustomerStatusResponse]:
        # Issue 1.4: implementar este metodo.
        # Usar CustomerStatusTypeRepository para obtener los estados de cliente activos.
        # Convertir el resultado al DTO CustomerStatusResponse con la estrategia que prefieras.
        # Devolver una lista de estados para que el controller responda al endpoint.
        pass
