from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.api import deps
from app.crud import crud_visit, crud_appointment
from app.schemas.visit import VisitResponse, VisitCreate, VisitUpdate
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=VisitResponse)
async def create_visit_record(
    *,
    db: AsyncSession = Depends(deps.get_db),
    visit_in: VisitCreate,
    current_user: User = Depends(deps.role_required(["CAREGIVER"]))
) -> Any:
    # A real system would verify the caregiver owns the appointment
    appt = await crud_appointment.get_appointment(db, visit_in.appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
        
    visit = await crud_visit.get_visit_by_appointment(db, appointment_id=visit_in.appointment_id)
    if visit:
        raise HTTPException(status_code=400, detail="Visit record already exists for this appointment")
        
    visit = await crud_visit.create_visit(db, visit_in=visit_in)
    return visit

@router.put("/{appointment_id}/complete", response_model=VisitResponse)
async def complete_visit_record(
    *,
    db: AsyncSession = Depends(deps.get_db),
    appointment_id: int,
    visit_in: VisitUpdate,
    current_user: User = Depends(deps.role_required(["CAREGIVER"]))
) -> Any:
    visit = await crud_visit.get_visit_by_appointment(db, appointment_id=appointment_id)
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
        
    visit = await crud_visit.update_visit(db, db_visit=visit, visit_in=visit_in)
    return visit
