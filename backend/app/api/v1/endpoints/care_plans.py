from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.crud import crud_care_plan, crud_patient
from app.schemas.care_plan import CarePlanResponse, CarePlanCreate, CarePlanUpdate
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=CarePlanResponse)
async def create_care_plan(
    *,
    db: AsyncSession = Depends(deps.get_db),
    cp_in: CarePlanCreate,
    current_user: User = Depends(deps.role_required(["DOCTOR", "ADMIN"]))
) -> Any:
    cp = await crud_care_plan.create_care_plan(db, cp_in=cp_in, doctor_id=current_user.id)
    return cp

@router.get("/", response_model=List[CarePlanResponse])
async def read_all_care_plans(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["DOCTOR", "ADMIN", "CAREGIVER", "NURSE"]))
) -> Any:
    cps = await crud_care_plan.get_all_care_plans(db)
    return cps

@router.get("/patient/{patient_id}", response_model=List[CarePlanResponse])
async def read_patient_care_plans(
    patient_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["DOCTOR", "ADMIN", "CAREGIVER", "PATIENT"]))
) -> Any:
    # Basic RBAC check - if PATIENT, verify it's their own plans.
    if current_user.role.value == "PATIENT":
        patient = await crud_patient.get_patient_by_user_id(db, current_user.id)
        if not patient or patient.id != patient_id:
            raise HTTPException(status_code=403, detail="Not authorized to view these records")
            
    cps = await crud_care_plan.get_patient_care_plans(db, patient_id=patient_id)
    return cps

@router.put("/{cp_id}/status", response_model=CarePlanResponse)
async def update_status(
    *,
    db: AsyncSession = Depends(deps.get_db),
    cp_id: int,
    status_in: CarePlanUpdate,
    current_user: User = Depends(deps.role_required(["DOCTOR", "ADMIN"]))
) -> Any:
    cp = await crud_care_plan.get_care_plan(db, cp_id=cp_id)
    if not cp:
        raise HTTPException(status_code=404, detail="Care plan not found")
        
    cp = await crud_care_plan.update_care_plan_status(db, db_cp=cp, status_in=status_in)
    return cp
