"""tech category added

Revision ID: 5a34b5ba14f5
Revises: c1df8d1ff2b1
Create Date: 2020-05-08 22:14:26.466120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a34b5ba14f5'
down_revision = 'c1df8d1ff2b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tech', sa.Column('category', sa.String(length=25), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tech', 'category')
    # ### end Alembic commands ###