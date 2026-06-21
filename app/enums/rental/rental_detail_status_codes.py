from enum import Enum


class RentalDetailStatusCode(str, Enum):
    RENTED = "RENTED"
    OVERDUE = "OVERDUE"
    RETURNED = "RETURNED"
    CANCELLED = "CANCELLED"
    LOST = "LOST"
