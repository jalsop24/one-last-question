"""newsletter model

Revision ID: 16e1056981ef
Revises: 98553475af0f
Create Date: 2024-04-24 21:11:46.463895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16e1056981ef'
down_revision: Union[str, None] = '98553475af0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_newsletter',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('newsletter_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['newsletter_id'], ['newsletters.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'newsletter_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_newsletter')
    # ### end Alembic commands ###
