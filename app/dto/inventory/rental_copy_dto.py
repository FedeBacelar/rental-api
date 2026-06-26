from pydantic import AliasChoices, BaseModel, Field


class RentalCopyCreateRequest(BaseModel):
    rental_item_id: int = Field(gt=0)
    copy_number: int = Field(gt=0)
    inventory_code: str = Field(
        min_length=1,
        max_length=80,
        validation_alias=AliasChoices("inventory_code", "internal_code"),
    )


class RentalCopyResponse(BaseModel):
    id: int
    rental_item_id: int
    item_title: str | None = None
    item_type_code: str | None = None
    status_id: int
    status_code: str | None = None
    status_name: str | None = None
    copy_number: int
    inventory_code: str
    is_active: bool
