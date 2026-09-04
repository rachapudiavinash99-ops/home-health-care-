from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from sqlalchemy.future import select

from app.api import deps
from app.crud import crud_appointment, crud_patient
from app.schemas.appointment import AppointmentResponse, AppointmentCreate, AppointmentUpdateStatus
from app.models.user import User, Caregiver
from app.models.care_request import CareRequest, CareRequestStatus
from app.models.appointment import Appointment, AppointmentState

router = APIRouter()

@router.post("/", response_model=AppointmentResponse)
async def create_appointment(
    *,
    db: AsyncSession = Depends(deps.get_db),
    appt_in: AppointmentCreate,
    current_user: User = Depends(deps.role_required(["ADMIN", "DOCTOR", "CAREGIVER", "PATIENT"]))
) -> Any:
    patient_id = appt_in.patient_id
    if current_user.role.value == "PATIENT":
        patient = await crud_patient.get_patient_by_user_id(db, user_id=current_user.id)
        if not patient:
            raise HTTPException(status_code=400, detail="Patient profile not found for current user")
        patient_id = patient.id
    elif not patient_id:
        p_res = await db.execute(select(User).where(User.role == "PATIENT"))
        first_p = p_res.scalars().first()
        patient_id = first_p.id if first_p else 1

    # Caregiver resolution
    caregiver_id = appt_in.caregiver_id
    if not caregiver_id:
        cg_res = await db.execute(select(Caregiver))
        first_cg = cg_res.scalars().first()
        caregiver_id = first_cg.id if first_cg else 1

    # Scheduled date & times
    scheduled_dt = appt_in.scheduled_date or datetime.now()
    if appt_in.scheduled_start:
        try:
            scheduled_dt = datetime.fromisoformat(appt_in.scheduled_start.replace("Z", "+00:00"))
        except Exception:
            pass

    start_time_str = appt_in.start_time or scheduled_dt.strftime("%I:%M %p")
    end_time_str = appt_in.end_time or (scheduled_dt + timedelta(hours=1)).strftime("%I:%M %p")

    # Auto-create linked CareRequest if not provided
    care_request_id = appt_in.care_request_id
    if not care_request_id:
        care_req = CareRequest(
            patient_id=patient_id,
            service_id=appt_in.service_id,
            preferred_date=scheduled_dt,
            preferred_start_time=start_time_str,
            duration_hours=1,
            medical_requirements=appt_in.notes or "Scheduled Home Healthcare Visit",
            special_instructions="Booked via CareFleet Patient Portal",
            status=CareRequestStatus.APPROVED
        )
        db.add(care_req)
        await db.commit()
        await db.refresh(care_req)
        care_request_id = care_req.id

    db_appt = Appointment(
        care_request_id=care_request_id,
        patient_id=patient_id,
        caregiver_id=caregiver_id,
        service_id=appt_in.service_id,
        scheduled_date=scheduled_dt,
        start_time=start_time_str,
        end_time=end_time_str,
        status=AppointmentState.CONFIRMED,
        notes=appt_in.notes or "Direct patient booking"
    )
    db.add(db_appt)
    await db.commit()
    await db.refresh(db_appt)
    return db_appt

@router.get("/", response_model=List[AppointmentResponse])
async def read_all_appointments(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["ADMIN", "DOCTOR", "CAREGIVER", "NURSE", "PATIENT"]))
) -> Any:
    if current_user.role.value == "PATIENT":
        patient = await crud_patient.get_patient_by_user_id(db, user_id=current_user.id)
        if not patient:
            return []
        return await crud_appointment.get_patient_appointments(db, patient_id=patient.id)
    return await crud_appointment.get_all_appointments(db)

@router.get("/me", response_model=List[AppointmentResponse])
async def read_my_appointments(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["PATIENT"]))
) -> Any:
    patient = await crud_patient.get_patient_by_user_id(db, user_id=current_user.id)
    if not patient:
        return []
    return await crud_appointment.get_patient_appointments(db, patient_id=patient.id)

@router.patch("/{appt_id}/status", response_model=AppointmentResponse)
@router.put("/{appt_id}/status", response_model=AppointmentResponse)
async def update_status(
    *,
    db: AsyncSession = Depends(deps.get_db),
    appt_id: int,
    status_in: AppointmentUpdateStatus,
    current_user: User = Depends(deps.role_required(["ADMIN", "CAREGIVER", "DOCTOR", "PATIENT"]))
) -> Any:
    appt = await crud_appointment.get_appointment(db, appt_id=appt_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appt = await crud_appointment.update_appointment_status(db, db_appt=appt, status_in=status_in)
    return appt
