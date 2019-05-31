"""empty message

Revision ID: 507534808b1b
Revises: 131b18b0f82d
Create Date: 2019-05-31 18:15:43.814970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '507534808b1b'
down_revision = '131b18b0f82d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'account', ['id'])
    op.create_unique_constraint(None, 'project', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'project', type_='unique')
    op.drop_constraint(None, 'account', type_='unique')
    # ### end Alembic commands ###