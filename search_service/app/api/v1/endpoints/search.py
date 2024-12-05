from fastapi import APIRouter, Depends
from ....schemas.search import SearchParams, SearchResponse
from ....services.search import SearchService
from ....services.es.client import ESClient
router = APIRouter()

@router.post("/jobs", response_model=SearchResponse)
async def search_jobs(params: SearchParams):
    search_service = SearchService()
    return search_service.search_jobs(params)

@router.post("/jobs/index", status_code=201)
async def index_job(job_data: dict):
    """索引单个职位数据"""
    es_client = ESClient()
    return es_client.index_document(job_data["id"], job_data)

@router.delete("/jobs/{job_id}")
async def delete_job(job_id: str):
    """删除职位索引"""
    es_client = ESClient()
    return es_client.delete_document(job_id) 