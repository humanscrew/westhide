"""empty message

Revision ID: 2aaeb4f2cd14
Revises: 6cdac8bbb0bc
Create Date: 2021-09-26 10:56:41.173814

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2aaeb4f2cd14'
down_revision = '6cdac8bbb0bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permit_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('value', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('map_user2permit_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('permit_code_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['permit_code_id'], ['permit_code.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('user_code', table_name='user')
    op.drop_column('user', 'user_code')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('user_code', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.create_index('user_code', 'user', ['user_code'], unique=False)
    op.drop_table('map_user2permit_code')
    op.drop_table('permit_code')
    # ### end Alembic commands ###
