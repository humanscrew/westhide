"""empty message

Revision ID: 23b96ae47308
Revises: e580ac41c9b3
Create Date: 2021-10-05 17:14:45.648632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23b96ae47308'
down_revision = 'e580ac41c9b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company_group', sa.Column('desc', sa.String(length=80), nullable=True))
    op.add_column('company_group', sa.Column('icon', sa.String(length=80), nullable=True))
    op.add_column('company_group', sa.Column('address', sa.String(length=80), nullable=True))
    op.add_column('company_group', sa.Column('location', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('company_group', 'location')
    op.drop_column('company_group', 'address')
    op.drop_column('company_group', 'icon')
    op.drop_column('company_group', 'desc')
    # ### end Alembic commands ###
