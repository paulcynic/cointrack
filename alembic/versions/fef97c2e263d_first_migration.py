"""First migration

Revision ID: fef97c2e263d
Revises: 
Create Date: 2022-01-10 21:51:15.989799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fef97c2e263d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_coin_id'), 'coin', ['id'], unique=False)
    op.create_table('currency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=4), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('label')
    )
    op.create_index(op.f('ix_currency_id'), 'currency', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('hashed_password', sa.String(length=128), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=True)
    op.create_table('coinprice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('coin_name', sa.String(length=128), nullable=False),
    sa.Column('currency_label', sa.String(length=4), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('current_datetime', sa.DateTime(), nullable=True),
    sa.Column('submitter_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['coin_name'], ['coin.name'], ),
    sa.ForeignKeyConstraint(['currency_label'], ['currency.label'], ),
    sa.ForeignKeyConstraint(['submitter_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_coinprice_id'), 'coinprice', ['id'], unique=False)
    op.create_index(op.f('ix_coinprice_submitter_id'), 'coinprice', ['submitter_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_coinprice_submitter_id'), table_name='coinprice')
    op.drop_index(op.f('ix_coinprice_id'), table_name='coinprice')
    op.drop_table('coinprice')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_currency_id'), table_name='currency')
    op.drop_table('currency')
    op.drop_index(op.f('ix_coin_id'), table_name='coin')
    op.drop_table('coin')
    # ### end Alembic commands ###