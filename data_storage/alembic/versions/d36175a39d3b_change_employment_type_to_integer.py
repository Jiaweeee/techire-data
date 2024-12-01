"""change_employment_type_to_integer

Revision ID: d36175a39d3b
Revises: 670d2b258f7d
Create Date: 2024-12-01 20:38:22.368745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'd36175a39d3b'
down_revision: Union[str, None] = '670d2b258f7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. 添加临时列
    op.add_column('jobs', sa.Column('temp_type', sa.Integer(), nullable=True))
    
    # 2. 更新临时列的值
    op.execute("""
        UPDATE jobs 
        SET temp_type = CASE normalized_employment_type
            WHEN 'full_time' THEN 1
            WHEN 'part_time' THEN 2
            WHEN 'contract' THEN 3
            WHEN 'internship' THEN 4
            WHEN 'temporary' THEN 5
            WHEN 'remote' THEN 6
            WHEN 'hybrid' THEN 7
            WHEN 'on_site' THEN 8
            ELSE NULL
        END
    """)
    
    # 3. 删除原列
    op.drop_column('jobs', 'normalized_employment_type')
    
    # 4. 重命名临时列
    op.alter_column('jobs', 'temp_type',
                    new_column_name='normalized_employment_type',
                    existing_type=sa.Integer(),
                    existing_nullable=True)

def downgrade() -> None:
    # 1. 添加临时列
    op.add_column('jobs', sa.Column('temp_type', mysql.VARCHAR(32), nullable=True))
    
    # 2. 更新临时列的值
    op.execute("""
        UPDATE jobs 
        SET temp_type = CASE normalized_employment_type
            WHEN 1 THEN 'full_time'
            WHEN 2 THEN 'part_time'
            WHEN 3 THEN 'contract'
            WHEN 4 THEN 'internship'
            WHEN 5 THEN 'temporary'
            WHEN 6 THEN 'remote'
            WHEN 7 THEN 'hybrid'
            WHEN 8 THEN 'on_site'
            ELSE NULL
        END
    """)
    
    # 3. 删除原列
    op.drop_column('jobs', 'normalized_employment_type')
    
    # 4. 重命名临时列
    op.alter_column('jobs', 'temp_type',
                    new_column_name='normalized_employment_type',
                    existing_type=mysql.VARCHAR(32),
                    existing_nullable=True)
