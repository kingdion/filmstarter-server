"""empty message

Revision ID: 6bd16fb28ed5
Revises: 04f51e1cbe43
Create Date: 2019-05-26 20:50:02.427536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bd16fb28ed5'
down_revision = '04f51e1cbe43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'account', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'account', type_='unique')
    # ### end Alembic commands ###