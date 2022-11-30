"""empty message

Revision ID: d556f4f2c626
Revises: 8669a89131be
Create Date: 2022-11-22 15:44:24.738845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd556f4f2c626'
down_revision = '8669a89131be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.VARCHAR(length=65), autoincrement=False, nullable=False))
    # ### end Alembic commands ###