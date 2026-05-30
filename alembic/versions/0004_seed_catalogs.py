"""seed catalogs

Revision ID: 0004_seed_catalogs
Revises: 0003_create_rental_schema
Create Date: 2026-05-28
"""

from alembic import op
import sqlalchemy as sa


revision = "0004_seed_catalogs"
down_revision = "0003_create_rental_schema"
branch_labels = None
depends_on = None


def catalog_table(name: str) -> sa.Table:
    return sa.table(
        name,
        sa.column("id", sa.Integer()),
        sa.column("code", sa.String()),
        sa.column("name", sa.String()),
        sa.column("is_active", sa.Boolean()),
    )


roles_table = sa.table(
    "roles",
    sa.column("id", sa.Integer()),
    sa.column("code", sa.String()),
    sa.column("name", sa.String()),
    sa.column("is_active", sa.Boolean()),
)


def upgrade() -> None:
    op.bulk_insert(
        catalog_table("rental_item_types"),
        [
            {"id": 1, "code": "MOVIE", "name": "Pelicula", "is_active": True},
            {"id": 2, "code": "VIDEOGAME", "name": "Videojuego", "is_active": True},
        ],
    )

    op.bulk_insert(
        catalog_table("genres"),
        [
            {"id": 1, "code": "ACTION", "name": "Accion", "is_active": True},
            {"id": 2, "code": "ADVENTURE", "name": "Aventura", "is_active": True},
            {"id": 3, "code": "COMEDY", "name": "Comedia", "is_active": True},
            {"id": 4, "code": "DRAMA", "name": "Drama", "is_active": True},
            {"id": 5, "code": "HORROR", "name": "Terror", "is_active": True},
            {"id": 6, "code": "RPG", "name": "RPG", "is_active": True},
            {"id": 7, "code": "SPORTS", "name": "Deportes", "is_active": True},
        ],
    )

    op.bulk_insert(
        catalog_table("platforms"),
        [
            {"id": 1, "code": "PC", "name": "PC", "is_active": True},
            {"id": 2, "code": "PLAYSTATION", "name": "PlayStation", "is_active": True},
            {"id": 3, "code": "XBOX", "name": "Xbox", "is_active": True},
            {"id": 4, "code": "NINTENDO", "name": "Nintendo", "is_active": True},
        ],
    )

    op.bulk_insert(
        catalog_table("rental_copy_status_types"),
        [
            {"id": 1, "code": "AVAILABLE", "name": "Disponible", "is_active": True},
            {"id": 2, "code": "RENTED", "name": "Alquilada", "is_active": True},
            {"id": 3, "code": "MAINTENANCE", "name": "Mantenimiento", "is_active": True},
            {"id": 4, "code": "DAMAGED", "name": "Danada", "is_active": True},
            {"id": 5, "code": "LOST", "name": "Perdida", "is_active": True},
        ],
    )

    op.bulk_insert(
        catalog_table("customer_status_types"),
        [
            {"id": 1, "code": "ACTIVE", "name": "Activo", "is_active": True},
            {"id": 2, "code": "INACTIVE", "name": "Inactivo", "is_active": True},
            {"id": 3, "code": "BLOCKED", "name": "Bloqueado", "is_active": True},
        ],
    )

    op.bulk_insert(
        catalog_table("rental_status_types"),
        [
            {"id": 1, "code": "OPEN", "name": "Abierta", "is_active": True},
            {"id": 2, "code": "PARTIALLY_RETURNED", "name": "Parcialmente devuelta", "is_active": True},
            {"id": 3, "code": "OVERDUE", "name": "Vencida", "is_active": True},
            {"id": 4, "code": "PARTIALLY_OVERDUE", "name": "Parcialmente vencida", "is_active": True},
            {"id": 5, "code": "CLOSED", "name": "Cerrada", "is_active": True},
            {"id": 6, "code": "CANCELLED", "name": "Cancelada", "is_active": True},
        ],
    )

    op.bulk_insert(
        catalog_table("rental_detail_status_types"),
        [
            {"id": 1, "code": "RENTED", "name": "Alquilado", "is_active": True},
            {"id": 2, "code": "OVERDUE", "name": "Vencido", "is_active": True},
            {"id": 3, "code": "RETURNED", "name": "Devuelto", "is_active": True},
            {"id": 4, "code": "CANCELLED", "name": "Cancelado", "is_active": True},
            {"id": 5, "code": "LOST", "name": "Perdido", "is_active": True},
        ],
    )

    op.bulk_insert(
        catalog_table("user_status_types"),
        [
            {"id": 1, "code": "ACTIVE", "name": "Activo", "is_active": True},
            {"id": 2, "code": "INACTIVE", "name": "Inactivo", "is_active": True},
            {"id": 3, "code": "BLOCKED", "name": "Bloqueado", "is_active": True},
        ],
    )

    op.bulk_insert(
        roles_table,
        [
            {"id": 1, "code": "ADMIN", "name": "Administrador", "is_active": True},
            {"id": 2, "code": "MANAGER", "name": "Encargado", "is_active": True},
            {"id": 3, "code": "STAFF", "name": "Empleado", "is_active": True},
            {"id": 4, "code": "READ_ONLY", "name": "Solo lectura", "is_active": True},
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM roles WHERE code IN ('ADMIN', 'MANAGER', 'STAFF', 'READ_ONLY')")
    op.execute("DELETE FROM user_status_types WHERE code IN ('ACTIVE', 'INACTIVE', 'BLOCKED')")
    op.execute("DELETE FROM rental_detail_status_types WHERE code IN ('RENTED', 'OVERDUE', 'RETURNED', 'CANCELLED', 'LOST')")
    op.execute("DELETE FROM rental_status_types WHERE code IN ('OPEN', 'PARTIALLY_RETURNED', 'OVERDUE', 'PARTIALLY_OVERDUE', 'CLOSED', 'CANCELLED')")
    op.execute("DELETE FROM customer_status_types WHERE code IN ('ACTIVE', 'INACTIVE', 'BLOCKED')")
    op.execute("DELETE FROM rental_copy_status_types WHERE code IN ('AVAILABLE', 'RENTED', 'MAINTENANCE', 'DAMAGED', 'LOST')")
    op.execute("DELETE FROM platforms WHERE code IN ('PC', 'PLAYSTATION', 'XBOX', 'NINTENDO')")
    op.execute("DELETE FROM genres WHERE code IN ('ACTION', 'ADVENTURE', 'COMEDY', 'DRAMA', 'HORROR', 'RPG', 'SPORTS')")
    op.execute("DELETE FROM rental_item_types WHERE code IN ('MOVIE', 'VIDEOGAME')")
