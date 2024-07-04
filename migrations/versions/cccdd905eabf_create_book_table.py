"""create book table

Revision ID: cccdd905eabf
Revises: d56b5b99cf1d
Create Date: 2024-07-04 14:11:39.194801

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cccdd905eabf"
down_revision: Union[str, None] = "d56b5b99cf1d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "book",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String, unique=True, nullable=False),
        sa.Column("year", sa.Integer, nullable=False),
        sa.Column(
            "novelist_id", sa.Integer, sa.ForeignKey("novelist.id"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("book")
