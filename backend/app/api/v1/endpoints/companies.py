from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from data_storage.crud import CompanyCRUD
from backend.app.schemas import CompanyDetail, CompanyBrief

router = APIRouter()

@router.get("/list", response_model=List[CompanyDetail])
async def get_companies(
    page: Optional[int] = None,
    page_size: Optional[int] = None
):
    """
    获取所有公司列表
    """
    crud = CompanyCRUD()
    companies = crud.get_all(page=page, page_size=page_size)
    return companies

@router.get("/detail", response_model=CompanyDetail)
async def get_company_detail(
    company_id: str = Query(...)
):
    """
    获取单个公司详情
    """
    crud = CompanyCRUD()
    company = crud.get_by_id(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

# @router.get("/search", response_model=List[CompanyBrief])
# async def search_companies(
#     q: str = Query(..., description="搜索关键词"),
#     limit: Optional[int] = Query(10, description="返回结果数量限制", ge=1, le=50)
# ):
#     """
#     搜索公司
#     """
#     crud = CompanyCRUD()
#     companies = crud.search(name=q, limit=limit)
#     return companies 