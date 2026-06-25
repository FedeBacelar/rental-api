from app.dto.catalog import GenreResponse
from app.models.catalog.genre import Genre


def genre_to_genre_response(genre: Genre) -> GenreResponse:
    # Convierte el modelo interno Genre al DTO que expone la API.
    return GenreResponse(
        id=genre.id,
        code=genre.code,
        name=genre.name,
        is_active=genre.is_active,
    )

def genres_to_genre_response(genres: list[Genre]) -> list[GenreResponse]:
    # Reutiliza el mapeo individual para mantener respuestas consistentes.
    return [genre_to_genre_response(genre) for genre in genres]
