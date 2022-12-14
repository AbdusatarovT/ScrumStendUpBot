"""empty message

Revision ID: f85544ab974d
Revises: 84fde0ebfab6
Create Date: 2022-11-27 21:53:08.057922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f85544ab974d'
down_revision = '84fde0ebfab6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
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
