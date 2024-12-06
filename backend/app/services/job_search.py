from typing import Dict, Any
from .es.client import ESClient
from ..schemas import JobSearchParams, JobBrief, JobSearchResponse, SalaryRange, JobDetail, CompanyBrief
class JobSearchService:
    def __init__(self):
        self.es_client = ESClient()
    
    def search_jobs(self, params: JobSearchParams) -> JobSearchResponse:
        # 构建查询
        query = self._build_query(params)
        
        # 执行搜索
        results = self.es_client.search(query)
        
        # 处理结果
        return self._process_results(results, params)

    def _build_query(self, params: JobSearchParams) -> Dict[str, Any]:
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
                        "summary^1.2",
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
                        "summary": {
                            "query": params.q,
                            "boost": 1.5,
                            "slop": 2
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
    
    def _process_results(self, results: dict, params: JobSearchParams) -> JobSearchResponse:
        hits = results.get("hits", {})
        total = hits.get("total", {}).get("value", 0)
        
        search_results = []
        for hit in hits.get("hits", []):
            source = hit.get("_source", {})
            score = hit.get("_score", 0.0)
            
            # 获取薪资范围
            salary_range = source.get("salary_range", {})
            if salary_range:
                salary_range = SalaryRange(
                    min=salary_range.get("min"),
                    max=salary_range.get("max"),
                    fixed=salary_range.get("fixed"),
                    currency=salary_range.get("currency")
                )
            
            # 构建公司信息
            company = source.get("company", {})
            if company:
                company = CompanyBrief(
                    id=company.get("id"),
                    name=company.get("name"),
                    icon_url=company.get("icon_url")
                )
            
            result = JobBrief(
                id=source.get("id"),
                title=source.get("title"),
                company=company,
                location=source.get("location"),
                employment_type=source.get("employment_type"),
                posted_date=source.get("posted_date"),
                is_remote=source.get("is_remote", False),
                url=source.get("url"),
                skill_tags=source.get("skill_tags", []),
                summary=source.get("summary"),
                salary_range=salary_range,
                experience_level=source.get("experience_level"),
                score=score
            )
            search_results.append(result)
        
        return JobSearchResponse(
            total=total,
            results=search_results,
            page=params.page,
            per_page=params.per_page
        )

    def get_job_detail(self, job_id: str) -> JobDetail:
        # 构建查询
        query = {
            "query": {
                "term": {
                    "_id": job_id
                }
            }
        }
        
        # 执行搜索
        result = self.es_client.search(query)
        
        # 处理结果
        hits = result.get("hits", {}).get("hits", [])
        if not hits:
            raise ValueError(f"Job with id {job_id} not found")
            
        source = hits[0].get("_source", {})
        
        # 构建公司信息
        company = source.get("company", {})
        if company:
            company = CompanyBrief(
                id=company.get("id"),
                name=company.get("name"),
                icon_url=company.get("icon_url")
            )
        
        # 构建薪资范围
        salary_range = source.get("salary_range", {})
        if salary_range:
            salary_range = SalaryRange(
                min=salary_range.get("min"),
                max=salary_range.get("max"),
                fixed=salary_range.get("fixed"),
                currency=salary_range.get("currency")
            )
        
        # 返回职位详情
        return JobDetail(
            id=source.get("id"),
            title=source.get("title"),
            company=company,
            location=source.get("location"),
            employment_type=source.get("employment_type"),
            posted_date=source.get("posted_date"),
            is_remote=source.get("is_remote", False),
            url=source.get("url"),
            skill_tags=source.get("skill_tags", []),
            summary=source.get("summary"),
            salary_range=salary_range,
            experience_level=source.get("experience_level"),
            full_description=source.get("full_description"),
        ) 