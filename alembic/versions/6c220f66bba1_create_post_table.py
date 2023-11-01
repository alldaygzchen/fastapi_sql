"""create post table

Revision ID: 6c220f66bba1
Revises: 
Create Date: 2023-11-01 10:28:41.255567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c220f66bba1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False,primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False)
                )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
