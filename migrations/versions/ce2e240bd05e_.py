"""empty message

Revision ID: ce2e240bd05e
Revises: 0657ad9e4a0c
Create Date: 2021-09-28 02:12:08.126675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce2e240bd05e'
down_revision = '0657ad9e4a0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('map_user2route',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('route_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['route_id'], ['route.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('route_closure_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ancestor_id', sa.Integer(), nullable=False),
    sa.Column('descendant_id', sa.Integer(), nullable=False),
    sa.Column('depth', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ancestor_id'], ['route.id'], ),
    sa.ForeignKeyConstraint(['descendant_id'], ['route.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('route_closure_table')
    op.drop_table('map_user2route')
    # ### end Alembic commands ###
