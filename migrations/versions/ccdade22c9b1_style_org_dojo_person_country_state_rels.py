"""style/org/dojo/person/country/state rels

Revision ID: ccdade22c9b1
Revises: 39b354802da1
Create Date: 2020-04-23 01:51:21.272121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccdade22c9b1'
down_revision = '39b354802da1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'dojo', 'org', ['org_id'], ['id'])
    op.create_foreign_key(None, 'person', 'style', ['style_id'], ['id'])
    op.create_foreign_key(None, 'state', 'country', ['country_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'state', type_='foreignkey')
    op.drop_constraint(None, 'person', type_='foreignkey')
    op.drop_constraint(None, 'dojo', type_='foreignkey')
    # ### end Alembic commands ###
