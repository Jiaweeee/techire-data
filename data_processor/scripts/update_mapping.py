from backend.app.services.es.client import ESClient
from data_processor.elasticsearch.mappings import JOB_MAPPING
from backend.app.core.config import settings
from datetime import datetime

def update_mapping():
    """更新索引 mapping"""
    es_client = ESClient()
    new_index = None
    
    try:
        # 1. 检查别名是否存在
        if not es_client.client.indices.exists_alias(name=settings.ES_JOB_INDEX):
            raise ValueError(f"Alias {settings.ES_JOB_INDEX} does not exist. Please run init_es first.")
            
        # 2. 获取当前别名指向的索引
        aliases = es_client.client.indices.get_alias(name=settings.ES_JOB_INDEX)
        old_indices = list(aliases.keys())
        if not old_indices:
            raise ValueError("No indices found for the alias")
        old_index = old_indices[0]
        
        # 3. 生成新的索引名（使用时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_index = f"{settings.ES_JOB_INDEX}_{timestamp}"
        
        # 4. 创建新索引
        print(f"Creating new index: {new_index}")
        es_client.create_index(new_index, JOB_MAPPING)
        
        # 5. 重新索引数据
        print(f"Reindexing data from {old_index} to {new_index}...")
        es_client.reindex(old_index, new_index)
        
        # 6. 删除旧索引（在更新别名之前）
        print(f"Deleting old index: {old_index}")
        es_client.delete_index(old_index)
        
        # 7. 创建新的别名
        print(f"Creating alias {settings.ES_JOB_INDEX} for index {new_index}")
        es_client.create_alias(new_index, settings.ES_JOB_INDEX)
        
        print("Mapping update completed successfully!")
        
    except Exception as e:
        print(f"Error during mapping update: {str(e)}")
        # 清理失败的新索引
        if new_index:
            print(f"Cleaning up failed index: {new_index}")
            es_client.delete_index(new_index)
        raise

if __name__ == "__main__":
    update_mapping()