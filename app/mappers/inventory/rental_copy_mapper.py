from app.dto.inventory import RentalCopyResponse
from app.models.inventory.rental_copy import RentalCopy


def rental_copy_to_rental_copy_response(
    rental_copy: RentalCopy,
) -> RentalCopyResponse:
    return RentalCopyResponse(
        id=rental_copy.id,
        rental_item_id=rental_copy.rental_item_id,
        status_id=rental_copy.status_id,
        copy_number=rental_copy.copy_number,
        inventory_code=rental_copy.internal_code,
        is_active=rental_copy.is_active,
    )


def rental_copies_to_rental_copy_responses(
    rental_copies: list[RentalCopy],
) -> list[RentalCopyResponse]:
    return [
        rental_copy_to_rental_copy_response(rental_copy)
        for rental_copy in rental_copies
    ]
