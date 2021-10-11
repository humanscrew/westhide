"""empty message

Revision ID: 68ce4c0ddcba
Revises: 3b2706f7eb3e
Create Date: 2021-10-10 13:34:46.128118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68ce4c0ddcba'
down_revision = '3b2706f7eb3e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('finance_account_tree',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('finance_account_closure_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tree_id', sa.Integer(), nullable=False),
    sa.Column('ancestor_id', sa.Integer(), nullable=False),
    sa.Column('descendant_id', sa.Integer(), nullable=False),
    sa.Column('distance', sa.Integer(), nullable=False),
    sa.Column('depth', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ancestor_id'], ['finance_account.id'], ),
    sa.ForeignKeyConstraint(['descendant_id'], ['finance_account.id'], ),
    sa.ForeignKeyConstraint(['tree_id'], ['finance_account_tree.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('finance_account_closure_table')
    op.drop_table('finance_account_tree')
    # ### end Alembic commands ###