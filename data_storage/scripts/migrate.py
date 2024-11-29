import os
import sys
from alembic import command
from alembic.config import Config
from pathlib import Path
from data_storage.config import get_database_url

def run_migrations(message: str = None):
    """运行数据库迁移"""
    try:
        # 获取项目根目录
        project_root = Path(__file__).parent.parent.parent
        data_storage_dir = project_root / "data_storage"
        
        # 创建 Alembic 配置
        alembic_cfg = Config()
        alembic_cfg.set_main_option("script_location", str(data_storage_dir / "alembic"))
        
        # 设置数据库 URL
        alembic_cfg.set_main_option("sqlalchemy.url", get_database_url())
        
        if message:
            # 生成新的迁移脚本
            print(f"Generating new migration: {message}")
            command.revision(alembic_cfg, autogenerate=True, message=message)
            
        # 运行迁移
        print("Applying migrations...")
        command.upgrade(alembic_cfg, "head")
        
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # 如果提供了命令行参数，使用它作为迁移说明
    message = sys.argv[1] if len(sys.argv) > 1 else None
    run_migrations(message) 