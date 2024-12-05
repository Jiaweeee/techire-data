from search_service.app.services.es.client import ESClient
from search_service.app.core.config import settings

def delete_index():
    """删除 Elasticsearch 索引"""
    es_client = ESClient()
    
    try:
        # 检查索引是否存在
        print(f"Checking if index '{settings.ES_JOB_INDEX}' exists...")
        
        # 删除索引
        print(f"Deleting index '{settings.ES_JOB_INDEX}'...")
        es_client.delete_index(settings.ES_JOB_INDEX)
        print("Index deleted successfully!")
        
    except Exception as e:
        print(f"Error during index deletion: {str(e)}")
        raise

if __name__ == "__main__":
    delete_index() 