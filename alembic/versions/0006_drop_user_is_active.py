"""drop user is_active

Revision ID: 0006_drop_user_is_active
Revises: 0005_seed_security
Create Date: 2026-06-07
"""

from alembic import op
import sqlalchemy as sa


revision = "0006_drop_user_is_active"
down_revision = "0005_seed_security"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("users", "is_active")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
    )
