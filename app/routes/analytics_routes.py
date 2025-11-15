"""Analytics routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.analytics import DashboardStats
from app.controllers.analytics_controller import get_dashboard_stats
from app.utils.auth import require_admin
from app.models.user import User

router = APIRouter()


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_endpoint(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get analytics dashboard (admin only)."""
    stats = await get_dashboard_stats(db)
    return DashboardStats(**stats)
