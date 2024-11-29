from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ....schemas.job import CompanyBrief, CompanyDetail
from data_storage.crud import CompanyCRUD
from ....api.deps import get_db

router = APIRouter()

@router.get("/", response_model=List[CompanyBrief])
async def get_companies(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    获取所有公司列表
    """
    crud = CompanyCRUD()
    companies = crud.get_all()
    return companies[skip : skip + limit]

@router.get("/detail", response_model=CompanyDetail)
async def get_company_detail(
    company_id: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    获取单个公司详情
    """
    crud = CompanyCRUD()
    company = crud.get_by_id(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company 