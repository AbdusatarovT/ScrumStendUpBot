"""empty message

Revision ID: 91c13ca65efd
Revises: 527ec02b990f
Create Date: 2022-11-28 11:42:32.603103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91c13ca65efd'
down_revision = '527ec02b990f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tg_id', sa.Integer(), nullable=True),
    sa.Column('yesterday_task', sa.Text(), nullable=True),
    sa.Column('today_task', sa.Text(), nullable=True),
    sa.Column('problem', sa.Text(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    # ### end Alembic commands ###
