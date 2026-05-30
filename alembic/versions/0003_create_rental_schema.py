"""create rental schema

Revision ID: 0003_create_rental_schema
Revises: 0002_create_security_schema
Create Date: 2026-05-28
"""

from alembic import op
import sqlalchemy as sa


revision = "0003_create_rental_schema"
down_revision = "0002_create_security_schema"
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
    create_catalog_table("customer_status_types")
    create_catalog_table("rental_status_types")
    create_catalog_table("rental_detail_status_types")

    op.create_table(
        "customers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("status_id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("document_number", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("address", sa.String(length=200), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["status_id"], ["customer_status_types.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_customers_document_number", "customers", ["document_number"], unique=True)
    op.create_index("ix_customers_email", "customers", ["email"], unique=True)

    op.create_table(
        "rentals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("status_id", sa.Integer(), nullable=False),
        sa.Column("rental_date", sa.Date(), nullable=False),
        sa.Column("expected_return_date", sa.Date(), nullable=False),
        sa.Column("actual_return_date", sa.Date(), nullable=True),
        sa.Column("total_amount", sa.Numeric(10, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("late_fee_amount", sa.Numeric(10, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("final_amount", sa.Numeric(10, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"]),
        sa.ForeignKeyConstraint(["status_id"], ["rental_status_types.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "rental_details",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("rental_id", sa.Integer(), nullable=False),
        sa.Column("rental_copy_id", sa.Integer(), nullable=False),
        sa.Column("status_id", sa.Integer(), nullable=False),
        sa.Column("price_per_day", sa.Numeric(10, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("late_fee_per_day", sa.Numeric(10, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("replacement_cost", sa.Numeric(10, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("rental_days", sa.Integer(), nullable=False),
        sa.Column("late_days", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("subtotal", sa.Numeric(10, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("late_fee_amount", sa.Numeric(10, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("replacement_fee_amount", sa.Numeric(10, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("final_amount", sa.Numeric(10, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["rental_copy_id"], ["rental_copies.id"]),
        sa.ForeignKeyConstraint(["rental_id"], ["rentals.id"]),
        sa.ForeignKeyConstraint(["status_id"], ["rental_detail_status_types.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rental_details")
    op.drop_table("rentals")
    op.drop_index("ix_customers_email", table_name="customers")
    op.drop_index("ix_customers_document_number", table_name="customers")
    op.drop_table("customers")
    drop_catalog_table("rental_detail_status_types")
    drop_catalog_table("rental_status_types")
    drop_catalog_table("customer_status_types")
