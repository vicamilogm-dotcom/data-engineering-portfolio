"""added users table

Revision ID: 2639a56e331b
Revises:
Create Date: 2026-01-15 01:50:00.769504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2639a56e331b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create table and keep reference for bulk_insert
    users = op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    # Insert seed users
    op.bulk_insert(
        users,
        [
            {"email": "oliver.giles@lewagon.org", "hashed_password": "notreally"},
            {"email": "bruno@lewagon.org", "hashed_password": "notreallyeither"},
        ],
    )

    # Indexes (si tus tests esperan index, los dejamos)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
