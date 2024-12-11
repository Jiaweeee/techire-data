from backend.app.services.es.client import ESClient
from backend.app.core.config import settings

def delete_index():
    """删除 Elasticsearch 索引"""
    es_client = ESClient()
    
    try:
        # 检查索引是否存在
        print(f"Checking if index '{settings.ES_JOB_INDEX}' exists...")
        
        # 获取别名指向的实际索引
        if es_client.client.indices.exists_alias(name=settings.ES_JOB_INDEX):
            # 获取所有指向该别名的索引
            aliases = es_client.client.indices.get_alias(name=settings.ES_JOB_INDEX)
            for index_name in aliases:
                print(f"Deleting index '{index_name}'...")
                es_client.client.indices.delete(index=index_name)
                print(f"Index '{index_name}' deleted successfully!")
        else:
            # 如果不是别名，直接删除索引
            print(f"Deleting index '{settings.ES_JOB_INDEX}'...")
            es_client.delete_index(settings.ES_JOB_INDEX)
            print("Index deleted successfully!")
        
    except Exception as e:
        print(f"Error during index deletion: {str(e)}")
        raise

if __name__ == "__main__":
    delete_index() 