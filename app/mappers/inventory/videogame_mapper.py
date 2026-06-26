from app.dto.inventory import VideogameResponse
from app.models.inventory.videogame_detail import VideogameDetail
from app.models.inventory.rental_item import RentalItem


def videogame_to_videogame_response(
        rental_item: RentalItem,
        videogame_detail: VideogameDetail,
        genre_code: str | None = None,
        genre_name: str | None = None,
        platform_code: str | None = None,
        platform_name: str | None = None,
) -> VideogameResponse:
    return VideogameResponse(
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
        platform_id=videogame_detail.platform_id,
        platform_code=platform_code,
        platform_name=platform_name,
        publisher=videogame_detail.publisher,
        multiplayer=videogame_detail.multiplayer,
        is_active=rental_item.is_active,
    )
