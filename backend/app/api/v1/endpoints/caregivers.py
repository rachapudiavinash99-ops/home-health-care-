from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.crud import crud_caregiver
from app.schemas.caregiver import CaregiverResponse, CaregiverCreate, CaregiverUpdate
from app.schemas.appointment import AppointmentResponse
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[CaregiverResponse])
async def read_all_caregivers(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["ADMIN", "DOCTOR", "CAREGIVER", "NURSE", "PATIENT"]))
) -> Any:
    cgs = await crud_caregiver.get_all_caregivers(db)
    return cgs

@router.get("/me", response_model=CaregiverResponse)
async def read_caregiver_me(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["CAREGIVER"]))
) -> Any:
    cg = await crud_caregiver.get_caregiver_by_user_id(db, user_id=current_user.id)
    if not cg:
        raise HTTPException(status_code=404, detail="Profile not found")
    return cg

@router.post("/me", response_model=CaregiverResponse)
async def create_caregiver_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    cg_in: CaregiverCreate,
    current_user: User = Depends(deps.role_required(["CAREGIVER"]))
) -> Any:
    cg = await crud_caregiver.get_caregiver_by_user_id(db, user_id=current_user.id)
    if cg:
        raise HTTPException(status_code=400, detail="Profile already exists")
    cg = await crud_caregiver.create_caregiver(db, caregiver_in=cg_in, user_id=current_user.id)
    return cg

@router.get("/appointments", response_model=List[AppointmentResponse])
async def read_my_appointments(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["CAREGIVER"]))
) -> Any:
    cg = await crud_caregiver.get_caregiver_by_user_id(db, user_id=current_user.id)
    if not cg:
        return []
    appts = await crud_caregiver.get_caregiver_appointments(db, caregiver_id=cg.id)
    return appts
