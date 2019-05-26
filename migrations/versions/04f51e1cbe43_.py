"""empty message

Revision ID: 04f51e1cbe43
Revises: b0c728edc9f8
Create Date: 2019-05-26 20:47:29.254532

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '04f51e1cbe43'
down_revision = 'b0c728edc9f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('username', sa.String(length=25), nullable=False),
    sa.Column('first_name', sa.String(length=25), nullable=False),
    sa.Column('last_name', sa.String(length=25), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=25), autoincrement=False, nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=25), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.Column('username', sa.VARCHAR(length=25), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('id', name='user_id_key'),
    sa.UniqueConstraint('username', name='user_username_key')
    )
    op.drop_table('account')
    # ### end Alembic commands ###
