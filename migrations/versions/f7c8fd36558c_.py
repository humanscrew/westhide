"""empty message

Revision ID: f7c8fd36558c
Revises: ed2299374398
Create Date: 2021-09-26 15:34:53.942718

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f7c8fd36558c'
down_revision = 'ed2299374398'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'real_name',
               existing_type=mysql.VARCHAR(collation='utf8mb4_0900_as_cs', length=80),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'real_name',
               existing_type=mysql.VARCHAR(collation='utf8mb4_0900_as_cs', length=80),
               nullable=False)
    # ### end Alembic commands ###
