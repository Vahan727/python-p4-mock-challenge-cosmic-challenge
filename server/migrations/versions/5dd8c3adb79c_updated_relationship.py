"""updated relationship

Revision ID: 5dd8c3adb79c
Revises: ca31e67ede8e
Create Date: 2023-06-18 18:25:20.135082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5dd8c3adb79c'
down_revision = 'ca31e67ede8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('missions', schema=None) as batch_op:
        batch_op.drop_constraint('fk_missions_planet_id_planets', type_='foreignkey')
        batch_op.drop_constraint('fk_missions_scientist_id_scientists', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_missions_planet_id_planets'), 'planets', ['planet_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(batch_op.f('fk_missions_scientist_id_scientists'), 'scientists', ['scientist_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('missions', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_missions_scientist_id_scientists'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_missions_planet_id_planets'), type_='foreignkey')
        batch_op.create_foreign_key('fk_missions_scientist_id_scientists', 'scientists', ['scientist_id'], ['id'])
        batch_op.create_foreign_key('fk_missions_planet_id_planets', 'planets', ['planet_id'], ['id'])

    # ### end Alembic commands ###