"""empty message

Revision ID: 34c0f5c7a19b
Revises: fb48aaae1109
Create Date: 2021-10-10 15:27:32.227008

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34c0f5c7a19b'
down_revision = 'fb48aaae1109'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bank_account', sa.Column('bank_branch_name', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bank_account', 'bank_branch_name')
    # ### end Alembic commands ###