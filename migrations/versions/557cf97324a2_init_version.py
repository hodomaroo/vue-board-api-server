"""init-version

Revision ID: 557cf97324a2
Revises: 
Create Date: 2023-07-10 00:13:12.286057

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '557cf97324a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tokens', sa.Column('refresh_token', sa.Uuid(), nullable=True))
    op.add_column('tokens', sa.Column('token_expire_date', sa.DateTime(), nullable=True))
    op.add_column('tokens', sa.Column('refresh_token_expire_date', sa.DateTime(), nullable=True))
    op.drop_column('tokens', 'expireDate')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tokens', sa.Column('expireDate', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('tokens', 'refresh_token_expire_date')
    op.drop_column('tokens', 'token_expire_date')
    op.drop_column('tokens', 'refresh_token')
    # ### end Alembic commands ###
