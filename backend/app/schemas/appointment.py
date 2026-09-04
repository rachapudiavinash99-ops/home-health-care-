from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.appointment import AppointmentState

class AppointmentBase(BaseModel):
    scheduled_date: datetime
    start_time: str
    end_time: str
    notes: Optional[str] = None

class AppointmentCreate(BaseModel):
    scheduled_date: Optional[datetime] = None
    scheduled_start: Optional[str] = None
    scheduled_end: Optional[str] = None
    start_time: Optional[str] = "09:00 AM"
    end_time: Optional[str] = "10:00 AM"
    care_request_id: Optional[int] = None
    patient_id: Optional[int] = None
    service_id: int
    caregiver_id: Optional[int] = None
    notes: Optional[str] = None

class AppointmentUpdateStatus(BaseModel):
    status: AppointmentState

class AppointmentResponse(AppointmentBase):
    id: int
    care_request_id: Optional[int] = None
    patient_id: int
    service_id: int
    caregiver_id: Optional[int] = None
    status: AppointmentState
    
    class Config:
        from_attributes = True
