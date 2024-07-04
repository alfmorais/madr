"""include books relationship in novelist

Revision ID: d23448cba817
Revises: cccdd905eabf
Create Date: 2024-07-04 15:43:33.621882

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d23448cba817"
down_revision: Union[str, None] = "cccdd905eabf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("novelist", sa.Column("books", sa.Integer, sa.ForeignKey("book.id")))


def downgrade() -> None:
    op.drop_column("novelist", "books")
