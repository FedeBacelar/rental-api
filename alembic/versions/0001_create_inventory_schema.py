"""create inventory schema

Revision ID: 0001_create_inventory_schema
Revises:
Create Date: 2026-05-28
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_create_inventory_schema"
down_revision = None
branch_labels = None
depends_on = None


def create_catalog_table(table_name: str) -> None:
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(f"ix_{table_name}_code", table_name, ["code"], unique=True)


def drop_catalog_table(table_name: str) -> None:
    op.drop_index(f"ix_{table_name}_code", table_name=table_name)
    op.drop_table(table_name)


def upgrade() -> None:
    create_catalog_table("rental_item_types")
    create_catalog_table("genres")
    create_catalog_table("platforms")
    create_catalog_table("rental_copy_status_types")

    op.create_table(
        "rental_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("item_type_id", sa.Integer(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("age_rating", sa.String(length=20), nullable=True),
        sa.Column("base_daily_price", sa.Numeric(10, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("late_fee_per_day", sa.Numeric(10, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("replacement_cost", sa.Numeric(10, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["genre_id"], ["genres.id"]),
        sa.ForeignKeyConstraint(["item_type_id"], ["rental_item_types.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_rental_items_title", "rental_items", ["title"], unique=False)

    op.create_table(
        "movie_details",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("rental_item_id", sa.Integer(), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("director", sa.String(length=150), nullable=False),
        sa.Column("original_language", sa.String(length=80), nullable=False),
        sa.ForeignKeyConstraint(["rental_item_id"], ["rental_items.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("rental_item_id"),
    )

    op.create_table(
        "videogame_details",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("rental_item_id", sa.Integer(), nullable=False),
        sa.Column("platform_id", sa.Integer(), nullable=False),
        sa.Column("publisher", sa.String(length=150), nullable=False),
        sa.Column("multiplayer", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.ForeignKeyConstraint(["platform_id"], ["platforms.id"]),
        sa.ForeignKeyConstraint(["rental_item_id"], ["rental_items.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("rental_item_id"),
    )

    op.create_table(
        "rental_copies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("rental_item_id", sa.Integer(), nullable=False),
        sa.Column("status_id", sa.Integer(), nullable=False),
        sa.Column("copy_number", sa.Integer(), nullable=False),
        sa.Column("internal_code", sa.String(length=80), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["rental_item_id"], ["rental_items.id"]),
        sa.ForeignKeyConstraint(["status_id"], ["rental_copy_status_types.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("rental_item_id", "copy_number", name="uq_rental_copies_item_copy_number"),
    )
    op.create_index("ix_rental_copies_internal_code", "rental_copies", ["internal_code"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_rental_copies_internal_code", table_name="rental_copies")
    op.drop_table("rental_copies")
    op.drop_table("videogame_details")
    op.drop_table("movie_details")
    op.drop_index("ix_rental_items_title", table_name="rental_items")
    op.drop_table("rental_items")
    drop_catalog_table("rental_copy_status_types")
    drop_catalog_table("platforms")
    drop_catalog_table("genres")
    drop_catalog_table("rental_item_types")
