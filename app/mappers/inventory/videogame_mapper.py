from app.dto.inventory import VideogameResponse
from app.models.inventory.videogame_detail import VideogameDetail
from app.models.inventory.rental_item import RentalItem


def videogame_to_videogame_response(
        rental_item: RentalItem,
        videogame_detail: VideogameDetail,
) -> VideogameResponse:
    return VideogameResponse(
        id=rental_item.id,
        genre_id=rental_item.genre_id,
        title=rental_item.title,
        description=rental_item.description,
        age_rating=rental_item.age_rating,
        base_daily_price=rental_item.base_daily_price,
        late_fee_per_day=rental_item.late_fee_per_day,
        replacement_cost=rental_item.replacement_cost,
        platform_id=videogame_detail.platform_id,
        publisher=videogame_detail.publisher,
        multiplayer=videogame_detail.multiplayer,
    )