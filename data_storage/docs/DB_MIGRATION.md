# Database Migration Guide

This guide explains how to manage database migrations using Alembic with SQLAlchemy.

## Setup

1. Install Alembic:
```bash
pip install alembic
```

2. Initialize Alembic in project root:
```bash
alembic init alembic
```

3. Configure database URL in `alembic.ini`:
```ini
sqlalchemy.url = sqlite:///data_storage/file/database.db
```

4. Update `alembic/env.py` to import your models:
```python
from models import Base
target_metadata = Base.metadata
```

## Migration Commands

### Create a New Migration

After making changes to your SQLAlchemy models, create a new migration:
```bash
alembic revision --autogenerate -m "description of changes"
```

### Apply Migrations

To apply all pending migrations:
```bash
alembic upgrade head
```

### View Migration History

To see all migrations:
```bash
alembic history
```

### Rollback Migrations

To rollback to a specific version:
```bash
alembic downgrade <revision_id>
```

To rollback one step:
```bash
alembic downgrade -1
```

## Best Practices

1. Always backup your database before running migrations
2. Review auto-generated migration scripts before applying them
3. Test migrations in a development environment first
4. Create new migrations for each model change
5. Use meaningful descriptions in migration messages

## Example Workflow

1. Make changes to your models (e.g., add a new column)
2. Generate migration:
```bash
alembic revision --autogenerate -m "add new column x to table y"
```
3. Review the generated migration script in `alembic/versions/`
4. Apply the migration:
```bash
alembic upgrade head
```

## Troubleshooting

If you encounter issues:

1. Check if all models are properly imported in `env.py`
2. Verify database URL in `alembic.ini`
3. Ensure database user has proper permissions
4. Check alembic logs for detailed error messages