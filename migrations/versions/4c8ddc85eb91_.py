"""empty message

Revision ID: 4c8ddc85eb91
Revises: 195b23552dc4
Create Date: 2023-06-17 09:10:18.880353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c8ddc85eb91'
down_revision = '195b23552dc4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('film')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('film',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('id_poster', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['id_poster'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###