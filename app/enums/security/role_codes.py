from enum import Enum


class RoleCode(str, Enum):
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"
    READ_ONLY = "READ_ONLY"
