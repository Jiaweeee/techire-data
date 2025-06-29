"""add_is_salary_estimated_field_to_job_analysis_table

Revision ID: 422860784587
Revises: f4dcd52c3006
Create Date: 2024-12-16 16:32:11.224225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '422860784587'
down_revision: Union[str, None] = 'f4dcd52c3006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job_analyses', sa.Column('is_salary_estimated', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('job_analyses', 'is_salary_estimated')
    # ### end Alembic commands ###
