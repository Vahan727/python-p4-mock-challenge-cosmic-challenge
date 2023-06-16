"""relationbships

Revision ID: ca31e67ede8e
Revises: 
Create Date: 2023-06-15 21:34:23.310880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca31e67ede8e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('distance_from_earth', sa.String(), nullable=True),
    sa.Column('nearest_star', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_planets'))
    )
    op.create_table('scientists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('field_of_study', sa.String(), nullable=False),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_scientists')),
    sa.UniqueConstraint('name', name=op.f('uq_scientists_name'))
    )
    op.create_table('missions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('scientist_id', sa.Integer(), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['planet_id'], ['planets.id'], name=op.f('fk_missions_planet_id_planets')),
    sa.ForeignKeyConstraint(['scientist_id'], ['scientists.id'], name=op.f('fk_missions_scientist_id_scientists')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_missions')),
    sa.UniqueConstraint('name', 'scientist_id', 'planet_id', name=op.f('uq_missions_name'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('missions')
    op.drop_table('scientists')
    op.drop_table('planets')
    # ### end Alembic commands ###