"""remove_normalized_employment_type_field

Revision ID: 3aaf4c2fb5a7
Revises: d36175a39d3b
Create Date: 2024-12-01 20:55:42.183857

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '3aaf4c2fb5a7'
down_revision: Union[str, None] = 'd36175a39d3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade() -> None:
    # 先检查 employment_type 列是否存在，如果存在则删除
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('jobs')]
    if 'employment_type' in columns:
        op.drop_column('jobs', 'employment_type')
        
    # Rename normalized_employment_type to employment_type
    op.alter_column('jobs', 'normalized_employment_type',
                    existing_type=sa.Integer(),
                    new_column_name='employment_type')

def downgrade() -> None:
    # Add back the original employment_type column
    op.add_column('jobs', sa.Column('employment_type', sa.String(64), nullable=True))
    # Rename employment_type back to normalized_employment_type
    op.alter_column('jobs', 'employment_type',
                    existing_type=sa.Integer(),
                    new_column_name='normalized_employment_type')
