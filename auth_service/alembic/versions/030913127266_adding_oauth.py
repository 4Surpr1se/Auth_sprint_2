"""Adding oauth

Revision ID: 030913127266
Revises: 5247b31f993a
Create Date: 2024-09-21 19:02:12.206548

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '030913127266'
down_revision: Union[str, None] = '5247b31f993a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('oauth',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('provider', sa.String(), nullable=True),
    sa.Column('provider_user_id', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('provider_user_id')
    )
    op.create_index(op.f('ix_oauth_id'), 'oauth', ['id'], unique=True)
    op.create_table('user_oauth',
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('oauth_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['oauth_id'], ['oauth.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    op.drop_column('users', 'oauth_provider')
    op.drop_column('users', 'oauth_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('oauth_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('oauth_provider', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_table('user_oauth')
    op.drop_index(op.f('ix_oauth_id'), table_name='oauth')
    op.drop_table('oauth')
    # ### end Alembic commands ###