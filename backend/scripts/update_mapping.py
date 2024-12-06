from app.services.es.client import ESClient
from app.services.es.mappings import JOB_MAPPING
from app.core.config import settings
from datetime import datetime

def update_mapping():
    """更新索引 mapping"""
    es_client = ESClient()
    
    # 1. 生成新的索引名（使用时间戳）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_index = f"{settings.ES_JOB_INDEX}_{timestamp}"
    old_index = settings.ES_JOB_INDEX
    
    try:
        # 2. 创建新索引
        print(f"Creating new index: {new_index}")
        es_client.create_index(new_index, JOB_MAPPING)
        
        # 3. 重新索引数据
        print("Reindexing data...")
        es_client.reindex(old_index, new_index)
        
        # 4. 更新别名
        print("Updating alias...")
        es_client.update_alias(old_index, new_index, settings.ES_JOB_INDEX)
        
        # 5. 删除旧索引
        print("Deleting old index...")
        es_client.delete_index(old_index)
        
        print("Mapping update completed successfully!")
        
    except Exception as e:
        print(f"Error during mapping update: {str(e)}")
        # 清理失败的新索引
        es_client.delete_index(new_index)
        raise

if __name__ == "__main__":
    update_mapping()