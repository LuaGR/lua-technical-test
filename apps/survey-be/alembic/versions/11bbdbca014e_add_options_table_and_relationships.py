"""add options table and relationships

Revision ID: 11bbdbca014e
Revises: beb380bf832f
Create Date: 2025-07-15 23:49:15.783308

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11bbdbca014e'
down_revision: Union[str, Sequence[str], None] = 'beb380bf832f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('options',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_options_id'), 'options', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_options_id'), table_name='options')
    op.drop_table('options')
    # ### end Alembic commands ###
