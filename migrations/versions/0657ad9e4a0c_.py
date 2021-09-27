"""empty message

Revision ID: 0657ad9e4a0c
Revises: cb035a497b2f
Create Date: 2021-09-27 12:18:23.155977

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0657ad9e4a0c'
down_revision = 'cb035a497b2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('route', sa.Column('route_meta_id', sa.Integer(), nullable=True))
    op.drop_constraint('route_ibfk_1', 'route', type_='foreignkey')
    op.create_foreign_key(None, 'route', 'route_meta', ['route_meta_id'], ['id'])
    op.drop_column('route', 'meta_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('route', sa.Column('meta_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'route', type_='foreignkey')
    op.create_foreign_key('route_ibfk_1', 'route', 'route_meta', ['meta_id'], ['id'])
    op.drop_column('route', 'route_meta_id')
    # ### end Alembic commands ###
