from sqlalchemy.orm import Session

from app.dto.catalog import (
    CustomerStatusResponse,
    GenreResponse,
    PlatformResponse,
    RentalCopyStatusResponse,
)
from app.mappers.catalog import genres_to_genre_response
from app.repositories.catalog.genre_repository import GenreRepository
from app.repositories.catalog.platform_repository import PlatformRepository


class CatalogService:
    def __init__(self, db: Session):
        self.db = db

    def list_genres(self) -> list[GenreResponse]:
        # Issue 1.1: implementar este metodo.
        # Usar GenreRepository para obtener los generos activos.
        # Convertir el resultado al DTO GenreResponse con la estrategia que prefieras.
        # Devolver una lista de generos para que el controller responda al endpoint.

        # El repository concentra las consultas a la base de datos.
        # Asi el service no necesita saber como se buscan los datos en MySQL.
        genre_repository = GenreRepository(self.db)

        # genres es una lista de objetos Genre.
        # Cada objeto Genre representa una fila de la tabla genres.
        genres = genre_repository.list_active()

        return genres_to_genre_response(genres)

    def list_platforms(self) -> list[PlatformResponse]:
        # Issue 1.2: implementar este metodo.
        # Usar PlatformRepository para obtener las plataformas activas.
        # Convertir el resultado al DTO PlatformResponse con la estrategia que prefieras.
        # Devolver una lista de plataformas para que el controller responda al endpoint.
        repository = PlatformRepository(self.db)

        platforms = repository.list_active()

        return [
            PlatformResponse(
                id=platform.id,
                code=platform.code,
                name=platform.name,
                is_active=platform.is_active,
            )
            for platform in platforms
        ]

    def list_rental_copy_statuses(self) -> list[RentalCopyStatusResponse]:
        # Issue 1.3: implementar este metodo.
        # Usar RentalCopyStatusTypeRepository para obtener los estados de copia activos.
        # Convertir el resultado al DTO RentalCopyStatusResponse con la estrategia que prefieras.
        # Devolver una lista de estados para que el controller responda al endpoint.
        repository = RentalCopyStatusTypeRepository(self.db)

        statuses = repository.list_active()

        return [
            RentalCopyStatusResponse(
            id=status.id,
            code=status.code,
            name=status.name,
            is_active=status.is_active,
            )
            for status in statuses
        ]

    def list_customer_statuses(self) -> list[CustomerStatusResponse]:
        # Issue 1.4: implementar este metodo.
        # Usar CustomerStatusTypeRepository para obtener los estados de cliente activos.
        # Convertir el resultado al DTO CustomerStatusResponse con la estrategia que prefieras.
        # Devolver una lista de estados para que el controller responda al endpoint.
        pass
