"""adding column others to patients,users,departments,roles and doctors

Revision ID: 7034304955c9
Revises: cf474fdc0e62
Create Date: 2024-10-10 18:25:49.310822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7034304955c9'
down_revision = 'cf474fdc0e62'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('departments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('others', sa.String(length=255), nullable=True))

    with op.batch_alter_table('doctors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('others', sa.String(length=255), nullable=True))

    with op.batch_alter_table('patients', schema=None) as batch_op:
        batch_op.add_column(sa.Column('others', sa.String(length=255), nullable=True))

    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('others', sa.String(length=255), nullable=True))

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('others', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('others')

    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.drop_column('others')

    with op.batch_alter_table('patients', schema=None) as batch_op:
        batch_op.drop_column('others')

    with op.batch_alter_table('doctors', schema=None) as batch_op:
        batch_op.drop_column('others')

    with op.batch_alter_table('departments', schema=None) as batch_op:
        batch_op.drop_column('others')

    # ### end Alembic commands ###
