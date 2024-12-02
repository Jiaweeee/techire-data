"""consolidate_posted_date_fields

Revision ID: 8a87b2220639
Revises: 3aaf4c2fb5a7
Create Date: 2024-12-02 11:02:01.770748

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '8a87b2220639'
down_revision: Union[str, None] = '3aaf4c2fb5a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create new posted_date column as DateTime
    op.add_column('jobs', sa.Column('new_posted_date', sa.DateTime(timezone=True), nullable=True))
    
    # Copy data from normalized_posted_date to new_posted_date
    op.execute("""
        UPDATE jobs 
        SET new_posted_date = normalized_posted_date
    """)
    
    # Drop old columns
    op.drop_column('jobs', 'posted_date')
    op.drop_column('jobs', 'normalized_posted_date')
    
    # Rename new column to posted_date
    op.alter_column('jobs', 'new_posted_date',
                    new_column_name='posted_date',
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=True)

def downgrade() -> None:
    # Add back the original columns
    op.add_column('jobs', sa.Column('posted_date', sa.String(64), nullable=True))
    op.add_column('jobs', sa.Column('normalized_posted_date', sa.DateTime(timezone=True), nullable=True))
    
    # Copy data back
    op.execute("""
        UPDATE jobs 
        SET normalized_posted_date = posted_date
    """)
    
    # Drop the consolidated column
    op.drop_column('jobs', 'posted_date')
