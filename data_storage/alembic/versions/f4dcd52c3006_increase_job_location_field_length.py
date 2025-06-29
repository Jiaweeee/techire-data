"""increase_job_location_field_length

Revision ID: f4dcd52c3006
Revises: c10276356e0f
Create Date: 2024-12-12 16:15:01.427884

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f4dcd52c3006'
down_revision: Union[str, None] = 'c10276356e0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('jobs', 'location',
               existing_type=mysql.VARCHAR(length=64),
               type_=sa.String(length=1024),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('jobs', 'location',
               existing_type=sa.String(length=1024),
               type_=mysql.VARCHAR(length=64),
               existing_nullable=True)
    # ### end Alembic commands ###
