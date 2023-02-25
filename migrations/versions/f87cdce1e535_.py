"""empty message

Revision ID: f87cdce1e535
Revises: 5b8423e68881
Create Date: 2023-02-25 16:44:25.216978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f87cdce1e535'
down_revision = '5b8423e68881'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_post')
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('mainImage', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('type', sa.Integer(), nullable=False))
        batch_op.drop_column('date_posted')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(length=60), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('notifications', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('notifications')
        batch_op.drop_column('created_at')
        batch_op.drop_column('image')

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_posted', sa.DATETIME(), nullable=False))
        batch_op.drop_column('type')
        batch_op.drop_column('mainImage')
        batch_op.drop_column('created_at')

    op.create_table('_alembic_tmp_post',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=False),
    sa.Column('mainImage', sa.VARCHAR(length=20), nullable=True),
    sa.Column('type', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
