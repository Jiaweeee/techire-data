from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.app.services.es.client import ESClient
from backend.app.api.deps import get_db
from data_storage.crud import CompanyCRUD

router = APIRouter()

class StatsResponse(BaseModel):
    total_jobs: int
    total_companies: int

@router.get("/summary", response_model=StatsResponse)
async def get_stats_summary(db: Session = Depends(get_db)):
    """
    获取系统统计数据
    - total_jobs: Elasticsearch 中已索引的职位数量
    - total_companies: 数据库中的公司数量
    """
    # 获取 ES 中的职位数量
    es_client = ESClient()
    es_stats = es_client.search({
        "track_total_hits": True,
        "size": 0,
        "query": {
            "match_all": {}
        }
    })
    total_jobs = es_stats.get("hits", {}).get("total", {}).get("value", 0)

    # 获取数据库中的公司数量
    company_crud = CompanyCRUD()
    total_companies = company_crud.count_total()

    return StatsResponse(
        total_jobs=total_jobs,
        total_companies=total_companies
    )
