"""empty message

Revision ID: 17e69a7e9898
Revises: None
Create Date: 2013-06-30 16:25:19.987725

"""

# revision identifiers, used by Alembic.
revision = '17e69a7e9898'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.Unicode(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('events')
