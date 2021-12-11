"""Add gigs

Revision ID: 256e1068c521
Revises: e6bd3297e2c8
Create Date: 2021-12-10 20:43:28.985652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '256e1068c521'
down_revision = 'e6bd3297e2c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gigs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('payment', sa.Float(), nullable=True),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('employer_id', sa.Integer(), nullable=True),
    sa.Column('slug', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['employer_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_gigs_employer_id'), 'gigs', ['employer_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_gigs_employer_id'), table_name='gigs')
    op.drop_table('gigs')
    # ### end Alembic commands ###
