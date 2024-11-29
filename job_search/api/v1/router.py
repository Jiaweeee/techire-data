from fastapi import APIRouter
from .endpoints import jobs, companies

api_router = APIRouter()

# Include job routes
api_router.include_router(
    jobs.router,
    prefix="/jobs",
    tags=["jobs"]
)

# Include company routes
api_router.include_router(
    companies.router,
    prefix="/companies",
    tags=["companies"]
) 