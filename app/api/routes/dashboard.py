from fastapi import APIRouter

from app.repositories.dashboard_repository import DashboardRepository

router = APIRouter(prefix="/api", tags=["dashboard"])
repo = DashboardRepository()


@router.get("/dashboard/stats")
def get_dashboard_stats():
    return repo.get_stats()
