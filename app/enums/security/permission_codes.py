from enum import Enum


class PermissionCode(str, Enum):
    USERS_MANAGE = "users:manage"
    ROLES_MANAGE = "roles:manage"
    CATALOGS_READ = "catalogs:read"
    CUSTOMERS_READ = "customers:read"
    CUSTOMERS_MANAGE = "customers:manage"
    INVENTORY_READ = "inventory:read"
    INVENTORY_MANAGE = "inventory:manage"
    RENTALS_READ = "rentals:read"
    RENTALS_MANAGE = "rentals:manage"
