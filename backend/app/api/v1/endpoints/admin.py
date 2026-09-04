from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.crud import crud_admin
from app.schemas.admin import DashboardStatsResponse
from app.models.user import User

router = APIRouter()

@router.get("/dashboard", response_model=DashboardStatsResponse)
async def get_admin_dashboard(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["ADMIN"]))
) -> Any:
    stats = await crud_admin.get_dashboard_stats(db)
    return stats
