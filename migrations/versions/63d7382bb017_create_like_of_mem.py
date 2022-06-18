"""create like of mem

Revision ID: 63d7382bb017
Revises: 3c1db43a1f7e
Create Date: 2022-06-19 08:19:20.015937

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '63d7382bb017'
down_revision = '3c1db43a1f7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('likeofmem',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('mem_id', sa.Integer(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['mem_id'], ['mem.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('mem_id', 'user_id', name='_mem_user_uc')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likeofmem')
    # ### end Alembic commands ###