"""Change is_leads to integer

Revision ID: dd854b0f3706
Revises: 72462d2a4f7c
Create Date: 2024-05-30 22:06:31.676818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd854b0f3706'
down_revision = '72462d2a4f7c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('leads', schema=None) as batch_op:
        batch_op.alter_column('is_leads',
               existing_type=sa.BOOLEAN(),
               type_=sa.Integer(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('leads', schema=None) as batch_op:
        batch_op.alter_column('is_leads',
               existing_type=sa.Integer(),
               type_=sa.BOOLEAN(),
               existing_nullable=True)

    # ### end Alembic commands ###
