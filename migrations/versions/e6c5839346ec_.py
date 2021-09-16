"""empty message

Revision ID: e6c5839346ec
Revises: 781a2de26e22
Create Date: 2021-09-13 18:37:46.222237

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e6c5839346ec'
down_revision = '781a2de26e22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cooperate_company', 'status',
               existing_type=mysql.VARCHAR(collation='utf8mb4_0900_as_cs', length=2),
               comment='1=on save;2=submitted;3=verified;4=to be modified;5=modified;6=abandon;',
               existing_comment='1=onsave;2=submitted;3=verified;4=to be modified;5=modified;6=abandon;',
               existing_nullable=True,
               existing_server_default=sa.text("'1'"))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cooperate_company', 'status',
               existing_type=mysql.VARCHAR(collation='utf8mb4_0900_as_cs', length=2),
               comment='1=onsave;2=submitted;3=verified;4=to be modified;5=modified;6=abandon;',
               existing_comment='1=on save;2=submitted;3=verified;4=to be modified;5=modified;6=abandon;',
               existing_nullable=True,
               existing_server_default=sa.text("'1'"))
    # ### end Alembic commands ###
