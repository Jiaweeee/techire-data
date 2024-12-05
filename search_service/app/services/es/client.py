from elasticsearch import Elasticsearch
from ...core.config import settings
from typing import Dict, Any, List

class ESClient:
    def __init__(self):
        self.client = Elasticsearch(
            settings.ES_HOSTS,
            basic_auth=(settings.ES_USERNAME, settings.ES_PASSWORD),
            timeout=settings.ES_TIMEOUT
        )
    
    def create_index(self, index_name: str, mapping: dict):
        """创建索引"""
        if not self.client.indices.exists(index=index_name):
            return self.client.indices.create(index=index_name, body=mapping)
    
    def search(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """执行搜索"""
        return self.client.search(
            index=settings.ES_JOB_INDEX,
            body=query
        )
    
    def index_document(self, doc_id: str, document: Dict[str, Any]) -> Dict[str, Any]:
        """索引文档"""
        return self.client.index(
            index=settings.ES_JOB_INDEX,
            id=doc_id,
            document=document
        )
    
    def bulk_index(self, actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量索引"""
        return self.client.bulk(body=actions)
    
    def delete_document(self, doc_id: str) -> Dict[str, Any]:
        """删除文档"""
        return self.client.delete(
            index=settings.ES_JOB_INDEX,
            id=doc_id
        )
    
    def reindex(self, source_index: str, target_index: str):
        """重新索引数据"""
        return self.client.reindex({
            "source": {"index": source_index},
            "dest": {"index": target_index}
        }, wait_for_completion=True)
    
    def create_alias(self, index: str, alias: str):
        """创建索引别名"""
        return self.client.indices.put_alias(index=index, name=alias)
    
    def update_alias(self, old_index: str, new_index: str, alias: str):
        """更新索引别名"""
        return self.client.indices.update_aliases({
            "actions": [
                {"remove": {"index": old_index, "alias": alias}},
                {"add": {"index": new_index, "alias": alias}}
            ]
        })
    
    def delete_index(self, index: str):
        """删除索引"""
        if self.client.indices.exists(index=index):
            return self.client.indices.delete(index=index) 