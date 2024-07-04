"""create novelist table

Revision ID: d56b5b99cf1d
Revises: 1afb051e7b3a
Create Date: 2024-07-03 16:57:42.158698

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d56b5b99cf1d"
down_revision: Union[str, None] = "1afb051e7b3a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "novelist",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("novelist")
