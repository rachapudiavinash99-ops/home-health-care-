from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.crud import crud_vitals_meds, crud_patient
from app.schemas.vitals_meds import (
    VitalSignCreate, VitalSignResponse,
    MedicationCreate, MedicationResponse, MedicationUpdate
)
from app.models.user import User

router = APIRouter()

@router.post("/vitals", response_model=VitalSignResponse)
async def create_vital_sign(
    *,
    db: AsyncSession = Depends(deps.get_db),
    vital_in: VitalSignCreate,
    current_user: User = Depends(deps.role_required(["CAREGIVER", "NURSE", "DOCTOR", "ADMIN"]))
) -> Any:
    vital = await crud_vitals_meds.create_vital_sign(db, vital_in=vital_in)
    return vital

@router.get("/vitals/patient/{patient_id}", response_model=List[VitalSignResponse])
async def read_vitals(
    patient_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["CAREGIVER", "NURSE", "DOCTOR", "ADMIN", "PATIENT"]))
) -> Any:
    vitals = await crud_vitals_meds.get_patient_vitals(db, patient_id=patient_id)
    return vitals

@router.post("/medications", response_model=MedicationResponse)
async def create_medication(
    *,
    db: AsyncSession = Depends(deps.get_db),
    med_in: MedicationCreate,
    current_user: User = Depends(deps.role_required(["DOCTOR"]))
) -> Any:
    med = await crud_vitals_meds.create_medication(db, med_in=med_in, doctor_id=current_user.id)
    return med

@router.get("/medications/patient/{patient_id}", response_model=List[MedicationResponse])
async def read_medications(
    patient_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["CAREGIVER", "NURSE", "DOCTOR", "ADMIN", "PATIENT"]))
) -> Any:
    meds = await crud_vitals_meds.get_patient_medications(db, patient_id=patient_id)
    return meds

@router.put("/medications/{med_id}/status", response_model=MedicationResponse)
async def update_med_status(
    *,
    db: AsyncSession = Depends(deps.get_db),
    med_id: int,
    status_in: MedicationUpdate,
    current_user: User = Depends(deps.role_required(["DOCTOR", "ADMIN"]))
) -> Any:
    med = await crud_vitals_meds.update_medication_status(db, med_id=med_id, status_in=status_in)
    if not med:
        raise HTTPException(status_code=404, detail="Medication not found")
    return med
