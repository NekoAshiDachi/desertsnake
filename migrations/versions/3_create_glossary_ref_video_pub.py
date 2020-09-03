"""create glossary, reference, video, publication - add data after

Revision ID: 3_create_glossary_ref_video_pub
Revises: 2_create_style_org_dojo_person
Create Date: 2020-04-23 01:39:05.648920

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3_create_glossary_ref_video_pub'
down_revision = '2_create_style_org_dojo_person'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('glossary',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('word', sa.String(50), nullable=True),
        sa.Column('translation', sa.String(50), nullable=True),
        sa.Column('kanji', sa.String(25), nullable=True),
        sa.Column('type', sa.String(25), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_date', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_date', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        mysql_default_charset='utf8',
        mysql_engine='InnoDB'
    )

    op.create_table('reference',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('glossary_id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(25), nullable=True),
        sa.Column('person_id', sa.Integer(), nullable=True),
        sa.Column('video_id', sa.Integer(), nullable=True),
        sa.Column('pub_id', sa.Integer(), nullable=True),
        sa.Column('text', sa.Text(), nullable=True),
        sa.Column('created_date', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_date', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        mysql_default_charset='utf8',
        mysql_engine='InnoDB'
    )

    op.create_table('video',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('style_id', sa.Integer(), nullable=True),
        sa.Column('org_id', sa.Integer(), nullable=True),
        sa.Column('performer_person_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('URL', sa.String(50), nullable=True),
        sa.Column('created_date', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_date', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        mysql_default_charset='utf8',
        mysql_engine='InnoDB'
    )

    op.create_table('publication',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('author_person_id', sa.Integer(), nullable=True),
        sa.Column('publisher', sa.String(25), nullable=True),
        sa.Column('format', sa.String(25), nullable=True),
        sa.Column('year', sa.Date(), nullable=True),
        sa.Column('store_link', sa.Text(), nullable=True),
        sa.Column('cover_link', sa.String(50), nullable=True),
        sa.Column('created_date', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_date', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        mysql_default_charset='utf8',
        mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('publication')
    op.drop_table('video')
    op.drop_table('reference')
    op.drop_table('glossary')
    # ### end Alembic commands ###