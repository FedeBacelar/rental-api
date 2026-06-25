from app.dto.inventory import RentalItemResponse
from app.models.inventory.rental_item import RentalItem


def rental_item_to_rental_item_response(item: RentalItem) -> RentalItemResponse:
    return RentalItemResponse(
        id=item.id,
        item_type_id=item.item_type_id,
        genre_id=item.genre_id,
        title=item.title,
        description=item.description,
        age_rating=item.age_rating,
        base_daily_price=item.base_daily_price,
        late_fee_per_day=item.late_fee_per_day,
        replacement_cost=item.replacement_cost,
        is_active=item.is_active,
    )

def rental_items_to_rental_item_response(
        items: list[RentalItem],
) -> list[RentalItemResponse]:
    return[
        rental_item_to_rental_item_response(item)
        for item in items
    ]