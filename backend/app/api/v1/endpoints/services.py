from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.crud import crud_service
from app.schemas.service import ServiceResponse, ServiceCreate
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[ServiceResponse])
async def read_services(
    db: AsyncSession = Depends(deps.get_db),
    active_only: bool = True
) -> Any:
    services = await crud_service.get_all_services(db, active_only=active_only)
    return services

@router.post("/", response_model=ServiceResponse)
async def create_service(
    *,
    db: AsyncSession = Depends(deps.get_db),
    service_in: ServiceCreate,
    current_user: User = Depends(deps.role_required(["ADMIN"]))
) -> Any:
    service = await crud_service.create_service(db, service_in=service_in)
    return service
