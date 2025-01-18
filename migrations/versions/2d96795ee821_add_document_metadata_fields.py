"""Add document metadata fields

Revision ID: 2d96795ee821
Revises: 
Create Date: 2025-01-18 15:57:52.758556

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '2d96795ee821'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('document', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('char_count', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('analysis_cost', sa.Integer(), nullable=True))
        batch_op.drop_column('analysis_summary')
        batch_op.drop_column('doc_metadata')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('document', schema=None) as batch_op:
        batch_op.add_column(sa.Column('doc_metadata', sqlite.JSON(), nullable=True))
        batch_op.add_column(sa.Column('analysis_summary', sa.TEXT(), nullable=True))
        batch_op.drop_column('analysis_cost')
        batch_op.drop_column('char_count')
        batch_op.drop_column('title')

    # ### end Alembic commands ###
