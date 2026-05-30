from enum import Enum


class RentalCopyStatusCode(str, Enum):
    AVAILABLE = "AVAILABLE"
    RENTED = "RENTED"
    MAINTENANCE = "MAINTENANCE"
    DAMAGED = "DAMAGED"
    LOST = "LOST"
