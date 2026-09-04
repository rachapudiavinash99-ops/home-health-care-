from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.crud import crud_care_request, crud_patient
from app.schemas.care_request import CareRequestCreate, CareRequestResponse
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=CareRequestResponse)
async def create_request(
    *,
    db: AsyncSession = Depends(deps.get_db),
    request_in: CareRequestCreate,
    current_user: User = Depends(deps.role_required(["PATIENT"]))
) -> Any:
    patient = await crud_patient.get_patient_by_user_id(db, user_id=current_user.id)
    if not patient:
        raise HTTPException(status_code=400, detail="Complete patient profile first")
    
    care_req = await crud_care_request.create_care_request(db, request_in=request_in, patient_id=patient.id)
    return care_req

@router.get("/me", response_model=List[CareRequestResponse])
async def read_my_requests(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["PATIENT"]))
) -> Any:
    patient = await crud_patient.get_patient_by_user_id(db, user_id=current_user.id)
    if not patient:
        return []
    requests = await crud_care_request.get_patient_requests(db, patient_id=patient.id)
    return requests

@router.get("/", response_model=List[CareRequestResponse])
async def read_all_requests(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["ADMIN"]))
) -> Any:
    requests = await crud_care_request.get_all_requests(db)
    return requests
