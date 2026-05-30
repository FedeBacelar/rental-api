from enum import Enum


class RoleCode(str, Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    STAFF = "STAFF"
    READ_ONLY = "READ_ONLY"
