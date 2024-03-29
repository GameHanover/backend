"""empty message

Revision ID: 21c8191cb0ba
Revises: 
Create Date: 2022-07-11 20:52:27.798709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21c8191cb0ba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('address1', sa.String(length=100), nullable=True),
    sa.Column('address2', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('state', sa.String(length=50), nullable=True),
    sa.Column('zip_code', sa.String(length=15), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('field',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('person',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.Column('phone_nbr', sa.String(), nullable=True),
    sa.Column('table_type', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('coach',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['person.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('game',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('game_dt', sa.Date(), nullable=True),
    sa.Column('field_id', sa.Integer(), nullable=True),
    sa.Column('coach_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['coach_id'], ['coach.id'], ),
    sa.ForeignKeyConstraint(['field_id'], ['field.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('game')
    op.drop_table('coach')
    op.drop_table('person')
    op.drop_table('field')
    op.drop_table('address')
    # ### end Alembic commands ###
