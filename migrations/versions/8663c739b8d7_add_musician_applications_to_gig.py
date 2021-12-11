"""Add musician applications to gig

Revision ID: 8663c739b8d7
Revises: 2bf843bdd622
Create Date: 2021-12-11 12:58:07.777871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8663c739b8d7'
down_revision = '2bf843bdd622'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('applications',
    sa.Column('gig_id', sa.Integer(), nullable=True),
    sa.Column('musician_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['gig_id'], ['gigs.id'], ),
    sa.ForeignKeyConstraint(['musician_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('applications')
    # ### end Alembic commands ###
