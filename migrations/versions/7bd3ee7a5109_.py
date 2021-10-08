"""empty message

Revision ID: 7bd3ee7a5109
Revises: 8be873b397f4
Create Date: 2021-10-02 11:39:03.963330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bd3ee7a5109'
down_revision = '8be873b397f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'ticket_laiu8', ['ticket_no'])
    op.create_foreign_key(None, 'ticket_laiu8_refund', 'ticket_laiu8', ['ticket_no'], ['ticket_no'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ticket_laiu8_refund', type_='foreignkey')
    op.drop_constraint(None, 'ticket_laiu8', type_='unique')
    # ### end Alembic commands ###