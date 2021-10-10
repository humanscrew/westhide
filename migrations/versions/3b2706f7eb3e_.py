"""empty message

Revision ID: 3b2706f7eb3e
Revises: 261ce284e86b
Create Date: 2021-10-10 13:24:27.228642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b2706f7eb3e'
down_revision = '261ce284e86b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auxiliary_account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=80), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('finance_account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=80), nullable=False),
    sa.Column('caption', sa.String(length=80), nullable=True),
    sa.Column('direction', sa.String(length=1), nullable=True, comment='1=credit;0=debit'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('map_finance_account2auxiliary_account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('finance_account_id', sa.Integer(), nullable=True),
    sa.Column('auxiliary_account_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['auxiliary_account_id'], ['auxiliary_account.id'], ),
    sa.ForeignKeyConstraint(['finance_account_id'], ['finance_account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('map_finance_account2auxiliary_account')
    op.drop_table('finance_account')
    op.drop_table('auxiliary_account')
    # ### end Alembic commands ###
