from app.dto.catalog import (
    CustomerStatusResponse,
    GenreResponse,
    PlatformResponse,
    RentalCopyStatusResponse,
)
from app.dto.auth import AuthenticatedUserResponse, LoginRequest, LoginResponse
from app.dto.customer import CustomerCreateRequest, CustomerResponse
from app.dto.inventory import (
    MovieCreateRequest,
    MovieResponse,
    RentalCopyCreateRequest,
    RentalCopyResponse,
    RentalItemResponse,
    VideogameCreateRequest,
    VideogameResponse,
)
from app.dto.rental import (
    RentalCreateRequest,
    RentalDetailResponse,
    RentalResponse,
    ReturnRentalItemRequest,
)

__all__ = [
    "AuthenticatedUserResponse",
    "CustomerCreateRequest",
    "CustomerResponse",
    "CustomerStatusResponse",
    "GenreResponse",
    "LoginRequest",
    "LoginResponse",
    "MovieCreateRequest",
    "MovieResponse",
    "PlatformResponse",
    "RentalCopyCreateRequest",
    "RentalCopyResponse",
    "RentalCopyStatusResponse",
    "RentalCreateRequest",
    "RentalDetailResponse",
    "RentalItemResponse",
    "RentalResponse",
    "ReturnRentalItemRequest",
    "VideogameCreateRequest",
    "VideogameResponse",
]
