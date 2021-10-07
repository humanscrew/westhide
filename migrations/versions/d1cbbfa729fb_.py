"""empty message

Revision ID: d1cbbfa729fb
Revises: 1d68ce4f3a3d
Create Date: 2021-10-06 22:01:06.281043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1cbbfa729fb'
down_revision = '1d68ce4f3a3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ticket_laiu8_client', sa.Column('sales', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ticket_laiu8_client', 'sales')
    # ### end Alembic commands ###
