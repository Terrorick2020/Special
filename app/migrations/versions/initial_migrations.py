"""initial migration

Revision ID: 123456789abc
Revises: 
Create Date: 2023-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '123456789abc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('domain', sa.String(), nullable=False),
        sa.Column('subdomains_count', sa.Integer(), nullable=False),
        sa.Column('pages_found', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('content_file_path', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_results_domain'), 'results', ['domain'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_results_domain'), table_name='results')
    op.drop_table('results')