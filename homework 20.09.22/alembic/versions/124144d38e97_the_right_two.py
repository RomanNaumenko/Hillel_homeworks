"""the_right_two

Revision ID: 124144d38e97
Revises: 0da34ed91639
Create Date: 2022-10-13 02:19:34.917430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '124144d38e97'
down_revision = '0da34ed91639'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transaction_queue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('transaction_id', sa.String(length=50), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction_queue')
    # ### end Alembic commands ###
