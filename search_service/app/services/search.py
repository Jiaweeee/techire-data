from typing import Dict, Any, List, Optional
from datetime import datetime
from .es.client import ESClient
from ..schemas.search import SearchParams, SearchResult, SearchResponse, Company

class SearchService:
    def __init__(self):
        self.es_client = ESClient()
    
    def search_jobs(self, params: SearchParams) -> SearchResponse:
        # 构建查询
        query = self._build_query(params)
        
        # 执行搜索
        results = self.es_client.search(query)
        
        # 处理结果
        return self._process_results(results, params)
    
    def _build_query(self, params: SearchParams) -> Dict[str, Any]:
        query = {
            "query": {
                "bool": {
                    "must": [],
                    "should": [],
                    "filter": [
                        {"term": {"expired": False}}
                    ]
                }
            },
            "from": (params.page - 1) * params.per_page,
            "size": params.per_page,
            "sort": [
                "_score",
                {"posted_date": {"order": "desc"}}
            ]
        }
        
        # 添加文本搜索（带字段权重和模糊匹配）
        if params.q:
            # 主要匹配条件
            query["query"]["bool"]["must"].append({
                "multi_match": {
                    "query": params.q,
                    "fields": [
                        "title^3",
                        "skill_tags^2",
                        "company.name^1.5",
                        "full_description^1"
                    ],
                    "type": "best_fields",
                    "tie_breaker": 0.3,
                    "fuzziness": "AUTO",
                    "operator": "or"
                }
            })
            
            # 短语匹配提升分数
            query["query"]["bool"]["should"].extend([
                {
                    "match_phrase": {
                        "title": {
                            "query": params.q,
                            "boost": 2,
                            "slop": 1
                        }
                    }
                },
                {
                    "match_phrase": {
                        "skill_tags": {
                            "query": params.q,
                            "boost": 1.5
                        }
                    }
                }
            ])
            
            # 精确匹配提升分数
            query["query"]["bool"]["should"].extend([
                {
                    "term": {
                        "title.keyword": {
                            "value": params.q,
                            "boost": 4
                        }
                    }
                },
                {
                    "term": {
                        "skill_tags.keyword": {
                            "value": params.q,
                            "boost": 3
                        }
                    }
                }
            ])
        
        # 添加位置过滤
        if params.location:
            query["query"]["bool"]["filter"].append({
                "match": {"location": params.location}
            })
        
        # 添加工作类型过滤
        if params.employment_type:
            query["query"]["bool"]["filter"].append({
                "term": {"employment_type": params.employment_type}
            })
        
        # 添加远程工作过滤
        if params.is_remote is not None:
            query["query"]["bool"]["filter"].append({
                "term": {"is_remote": params.is_remote}
            })
        
        # 添加公司过滤
        if params.company_ids:
            query["query"]["bool"]["filter"].append({
                "terms": {"company.id": params.company_ids}
            })
        
        return query
    
    def _process_results(self, results: dict, params: SearchParams) -> SearchResponse:
        hits = results.get("hits", {})
        total = hits.get("total", {}).get("value", 0)
        
        search_results = []
        for hit in hits.get("hits", []):
            source = hit.get("_source", {})
            score = hit.get("_score", 0.0)  # 确保有默认分数
            
            # 确保 employment_type 是字符串
            employment_type = str(source.get("employment_type", "")) if source.get("employment_type") else None
            
            result = SearchResult(
                id=source.get("id"),
                title=source.get("title"),
                company=Company(
                    id=source.get("company", {}).get("id"),
                    name=source.get("company", {}).get("name")
                ),
                location=source.get("location"),
                employment_type=employment_type,
                posted_date=source.get("posted_date"),
                is_remote=source.get("is_remote", False),
                skill_tags=source.get("skill_tags", []),
                score=score
            )
            search_results.append(result)
        
        return SearchResponse(
            total=total,
            results=search_results,
            page=params.page,
            per_page=params.per_page
        ) 