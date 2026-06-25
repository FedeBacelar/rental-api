"""seed security

Revision ID: 0005_seed_security
Revises: 0004_seed_catalogs
Create Date: 2026-06-07
"""

from alembic import op
import sqlalchemy as sa


revision = "0005_seed_security"
down_revision = "0004_seed_catalogs"
branch_labels = None
depends_on = None


# Password de desarrollo para usuarios seedeados: 1234
DEFAULT_PASSWORD_HASH = "$2b$12$.y1SmZCTQ517I.FE6zaItOhpZSFOcQ1A.ozhFs1TRw1fud77grsyG"


roles_table = sa.table(
    "roles",
    sa.column("id", sa.Integer()),
    sa.column("code", sa.String()),
    sa.column("name", sa.String()),
    sa.column("is_active", sa.Boolean()),
)

permissions_table = sa.table(
    "permissions",
    sa.column("id", sa.Integer()),
    sa.column("code", sa.String()),
    sa.column("name", sa.String()),
    sa.column("is_active", sa.Boolean()),
)

role_permissions_table = sa.table(
    "role_permissions",
    sa.column("id", sa.Integer()),
    sa.column("role_id", sa.Integer()),
    sa.column("permission_id", sa.Integer()),
)

users_table = sa.table(
    "users",
    sa.column("id", sa.Integer()),
    sa.column("role_id", sa.Integer()),
    sa.column("status_id", sa.Integer()),
    sa.column("username", sa.String()),
    sa.column("email", sa.String()),
    sa.column("password_hash", sa.String()),
    sa.column("first_name", sa.String()),
    sa.column("last_name", sa.String()),
    sa.column("is_active", sa.Boolean()),
)


def upgrade() -> None:
    # The original seed had MANAGER/STAFF. Security now starts with one operator role.
    op.execute("DELETE FROM roles WHERE code IN ('MANAGER', 'STAFF')")

    op.bulk_insert(
        roles_table,
        [
            {"id": 2, "code": "OPERATOR", "name": "Operador", "is_active": True},
        ],
    )

    op.bulk_insert(
        permissions_table,
        [
            {"id": 1, "code": "users:manage", "name": "Administrar usuarios", "is_active": True},
            {"id": 2, "code": "roles:manage", "name": "Administrar roles y permisos", "is_active": True},
            {"id": 3, "code": "catalogs:read", "name": "Consultar catalogos", "is_active": True},
            {"id": 4, "code": "customers:read", "name": "Consultar clientes", "is_active": True},
            {"id": 5, "code": "customers:manage", "name": "Administrar clientes", "is_active": True},
            {"id": 6, "code": "inventory:read", "name": "Consultar inventario", "is_active": True},
            {"id": 7, "code": "inventory:manage", "name": "Administrar inventario", "is_active": True},
            {"id": 8, "code": "rentals:read", "name": "Consultar rentas", "is_active": True},
            {"id": 9, "code": "rentals:manage", "name": "Administrar rentas", "is_active": True},
        ],
    )

    op.bulk_insert(
        role_permissions_table,
        [
            {"id": 1, "role_id": 1, "permission_id": 1},
            {"id": 2, "role_id": 1, "permission_id": 2},
            {"id": 3, "role_id": 1, "permission_id": 3},
            {"id": 4, "role_id": 1, "permission_id": 4},
            {"id": 5, "role_id": 1, "permission_id": 5},
            {"id": 6, "role_id": 1, "permission_id": 6},
            {"id": 7, "role_id": 1, "permission_id": 7},
            {"id": 8, "role_id": 1, "permission_id": 8},
            {"id": 9, "role_id": 1, "permission_id": 9},
            {"id": 10, "role_id": 2, "permission_id": 3},
            {"id": 11, "role_id": 2, "permission_id": 4},
            {"id": 12, "role_id": 2, "permission_id": 5},
            {"id": 13, "role_id": 2, "permission_id": 6},
            {"id": 14, "role_id": 2, "permission_id": 7},
            {"id": 15, "role_id": 2, "permission_id": 8},
            {"id": 16, "role_id": 2, "permission_id": 9},
            {"id": 17, "role_id": 4, "permission_id": 3},
            {"id": 18, "role_id": 4, "permission_id": 6},
        ],
    )

    op.bulk_insert(
        users_table,
        [
            {
                "id": 1,
                "role_id": 1,
                "status_id": 1,
                "username": "admin",
                "email": "admin@rentalapi.local",
                "password_hash": DEFAULT_PASSWORD_HASH,
                "first_name": "Admin",
                "last_name": "Sistema",
                "is_active": True,
            },
            {
                "id": 2,
                "role_id": 2,
                "status_id": 1,
                "username": "operator",
                "email": "operator@rentalapi.local",
                "password_hash": DEFAULT_PASSWORD_HASH,
                "first_name": "Operador",
                "last_name": "Sucursal",
                "is_active": True,
            },
            {
                "id": 3,
                "role_id": 4,
                "status_id": 1,
                "username": "readonly",
                "email": "readonly@rentalapi.local",
                "password_hash": DEFAULT_PASSWORD_HASH,
                "first_name": "Solo",
                "last_name": "Lectura",
                "is_active": True,
            },
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM users WHERE username IN ('admin', 'operator', 'readonly')")
    op.execute("DELETE FROM role_permissions WHERE role_id IN (1, 2, 4)")
    op.execute("DELETE FROM permissions WHERE code IN ('users:manage', 'roles:manage', 'catalogs:read', 'customers:read', 'customers:manage', 'inventory:read', 'inventory:manage', 'rentals:read', 'rentals:manage')")
    op.execute("DELETE FROM roles WHERE code = 'OPERATOR'")
    op.bulk_insert(
        roles_table,
        [
            {"id": 2, "code": "MANAGER", "name": "Encargado", "is_active": True},
            {"id": 3, "code": "STAFF", "name": "Empleado", "is_active": True},
        ],
    )
