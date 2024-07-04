"""create users table

Revision ID: 1afb051e7b3a
Revises: 
Create Date: 2024-06-27 13:47:20.728270

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "1afb051e7b3a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("password", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )


def downgrade() -> None:
    op.drop_table("user")
