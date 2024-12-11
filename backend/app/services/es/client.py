from elasticsearch import Elasticsearch
from ...core.config import settings
from typing import Dict, Any, List

class ESClient:
    def __init__(self):
        self.client = Elasticsearch(
            settings.ES_HOSTS,
            basic_auth=(settings.ES_USERNAME, settings.ES_PASSWORD),
            request_timeout=settings.ES_TIMEOUT,
            max_retries=settings.ES_MAX_RETRIES,
            retry_on_timeout=settings.ES_RETRY_ON_TIMEOUT,
            connections_per_node=settings.ES_MAX_CONNECTIONS
        )
    
    def create_index(self, index_name: str, mapping: dict):
        """创建索引"""
        if not self.client.indices.exists(index=index_name):
            return self.client.indices.create(
                index=index_name,
                body=mapping
            )
    
    def search(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """执行搜索"""
        return self.client.search(
            index=settings.ES_JOB_INDEX,
            body=query
        )
    
    def index_document(self, doc_id: str, document: Dict[str, Any], index: str = None) -> Dict[str, Any]:
        """索引文档
        Args:
            doc_id: 文档ID
            document: 文档内容
            index: 可选的具体索引名称，如果不提供则使用别名指向的索引
        """
        if index is None:
            # 如果没有提供具体索引，则尝试获取别名指向的索引
            try:
                aliases = self.client.indices.get_alias(name=settings.ES_JOB_INDEX)
                index = list(aliases.keys())[0]
            except Exception:
                # 如果获取别名失败，使用别名作为索引名
                index = settings.ES_JOB_INDEX
        
        return self.client.index(
            index=index,
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
        return self.client.reindex(
            body={
                "source": {"index": source_index},
                "dest": {"index": target_index}
            },
            wait_for_completion=True
        )
    
    def create_alias(self, index: str, alias: str):
        """创建索引别名"""
        return self.client.indices.put_alias(
            index=index,
            name=alias
        )
    
    def delete_index(self, index: str):
        """删除索引"""
        if self.client.indices.exists(index=index):
            return self.client.indices.delete(index=index)
    
    def exists_document(self, doc_id: str) -> bool:
        """检查文档是否存在"""
        return self.client.exists(
            index=settings.ES_JOB_INDEX,
            id=doc_id
        )
    
    def update_document(self, doc_id: str, document: Dict[str, Any]) -> Dict[str, Any]:
        """更新文档"""
        actual_index = self.get_actual_index()
        
        return self.client.update(
            index=actual_index,
            id=doc_id,
            doc=document
        )
    
    def get_actual_index(self) -> str:
        """获取别名指向的实际索引名称"""
        aliases = self.client.indices.get_alias(name=settings.ES_JOB_INDEX)
        return list(aliases.keys())[0]
    