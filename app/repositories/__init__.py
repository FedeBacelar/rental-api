from app.repositories.catalog import (
    CustomerStatusTypeRepository,
    GenreRepository,
    PlatformRepository,
    RentalCopyStatusTypeRepository,
    RentalDetailStatusTypeRepository,
    RentalItemTypeRepository,
    RentalStatusTypeRepository,
    UserStatusTypeRepository,
)
from app.repositories.inventory import (
    MovieDetailRepository,
    RentalCopyRepository,
    RentalItemRepository,
    VideogameDetailRepository,
)
from app.repositories.rental import (
    CustomerRepository,
    RentalDetailRepository,
    RentalRepository,
)
from app.repositories.security import (
    RoleRepository,
    UserRepository,
)

__all__ = [
    "CustomerRepository",
    "CustomerStatusTypeRepository",
    "GenreRepository",
    "MovieDetailRepository",
    "PlatformRepository",
    "RentalCopyRepository",
    "RentalCopyStatusTypeRepository",
    "RentalDetailRepository",
    "RentalDetailStatusTypeRepository",
    "RentalItemRepository",
    "RentalItemTypeRepository",
    "RentalRepository",
    "RentalStatusTypeRepository",
    "RoleRepository",
    "UserRepository",
    "UserStatusTypeRepository",
    "VideogameDetailRepository",
]



