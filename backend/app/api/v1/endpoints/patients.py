from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.crud import crud_patient
from app.schemas.patient import PatientResponse, PatientCreate, PatientUpdate
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[PatientResponse])
async def read_all_patients(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["ADMIN", "DOCTOR", "CAREGIVER", "NURSE"]))
) -> Any:
    patients = await crud_patient.get_all_patients(db)
    return patients

@router.get("/{patient_id}", response_model=PatientResponse)
async def read_patient_by_id(
    patient_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["ADMIN", "DOCTOR", "CAREGIVER", "NURSE", "PATIENT"]))
) -> Any:
    patient = await crud_patient.get_patient_by_id(db, patient_id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.get("/me", response_model=PatientResponse)
async def read_patient_me(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["PATIENT"]))
) -> Any:
    patient = await crud_patient.get_patient_by_user_id(db, user_id=current_user.id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    return patient

@router.post("/me", response_model=PatientResponse)
async def create_patient_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    patient_in: PatientCreate,
    current_user: User = Depends(deps.role_required(["PATIENT"]))
) -> Any:
    patient = await crud_patient.get_patient_by_user_id(db, user_id=current_user.id)
    if patient:
        raise HTTPException(status_code=400, detail="Profile already exists")
    patient = await crud_patient.create_patient(db, patient_in=patient_in, user_id=current_user.id)
    return patient

@router.put("/me", response_model=PatientResponse)
async def update_patient_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    patient_in: PatientUpdate,
    current_user: User = Depends(deps.role_required(["PATIENT"]))
) -> Any:
    patient = await crud_patient.get_patient_by_user_id(db, user_id=current_user.id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    patient = await crud_patient.update_patient(db, db_patient=patient, patient_in=patient_in)
    return patient
