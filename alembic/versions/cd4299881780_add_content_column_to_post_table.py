"""add content column to post table

Revision ID: cd4299881780
Revises: 6c220f66bba1
Create Date: 2023-11-01 10:38:50.715557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd4299881780'
down_revision: Union[str, None] = '6c220f66bba1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
