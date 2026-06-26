from app.dto.inventory import MovieResponse
from app.models.inventory.movie_detail import MovieDetail
from app.models.inventory.rental_item import RentalItem


def movie_to_movie_response(
    rental_item: RentalItem,
    movie_detail: MovieDetail,
    genre_code: str | None = None,
    genre_name: str | None = None,
) -> MovieResponse:
    return MovieResponse(
        id=rental_item.id,
        genre_id=rental_item.genre_id,
        genre_code=genre_code,
        genre_name=genre_name,
        title=rental_item.title,
        description=rental_item.description,
        age_rating=rental_item.age_rating,
        base_daily_price=rental_item.base_daily_price,
        late_fee_per_day=rental_item.late_fee_per_day,
        replacement_cost=rental_item.replacement_cost,
        duration_minutes=movie_detail.duration_minutes,
        director=movie_detail.director,
        original_language=movie_detail.original_language,
        is_active=rental_item.is_active,
    )
