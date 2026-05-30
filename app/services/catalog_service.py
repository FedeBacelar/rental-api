from sqlalchemy.orm import Session

from app.dto.catalog import (
    CustomerStatusResponse,
    GenreResponse,
    PlatformResponse,
    RentalCopyStatusResponse,
)
from app.repositories.catalog.genre_repository import GenreRepository


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

        # Esta lista va a contener la respuesta que vamos a devolver por la API.
        # No devolvemos los objetos de la base directamente.
        genre_responses = []

        for genre in genres:
            # Convertimos cada Genre en un GenreResponse.
            # GenreResponse es el formato de respuesta que definimos para la API.
            genre_response = GenreResponse(
                id=genre.id,
                code=genre.code,
                name=genre.name,
                is_active=genre.is_active,
            )

            genre_responses.append(genre_response)

        return genre_responses

    def list_platforms(self) -> list[PlatformResponse]:
        # Issue 1.2: implementar este metodo.
        # Usar PlatformRepository para obtener las plataformas activas.
        # Convertir el resultado al DTO PlatformResponse con la estrategia que prefieras.
        # Devolver una lista de plataformas para que el controller responda al endpoint.
        pass

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
