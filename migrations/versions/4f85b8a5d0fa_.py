"""empty message

Revision ID: 4f85b8a5d0fa
Revises: ac816cc0de84
Create Date: 2023-06-24 10:11:53.372859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f85b8a5d0fa'
down_revision = 'ac816cc0de84'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('film', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('film', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'genre', ['id_genre'], ['id'])

    # ### end Alembic commands ###
