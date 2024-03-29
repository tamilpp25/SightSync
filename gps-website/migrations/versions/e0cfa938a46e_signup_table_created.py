"""signup table created

Revision ID: e0cfa938a46e
Revises: 
Create Date: 2024-03-16 15:12:40.228361

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0cfa938a46e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('signup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.Column('GuardianName', sa.String(), nullable=True),
    sa.Column('UserName', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('signup')
    # ### end Alembic commands ###
