from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.care_request import CareRequestStatus

class CareRequestBase(BaseModel):
    service_id: int
    preferred_date: datetime
    preferred_start_time: str
    duration_hours: int
    medical_requirements: Optional[str] = None
    special_instructions: Optional[str] = None

class CareRequestCreate(CareRequestBase):
    pass

class CareRequestUpdate(BaseModel):
    status: CareRequestStatus

class CareRequestResponse(CareRequestBase):
    id: int
    patient_id: int
    status: CareRequestStatus
    
    class Config:
        from_attributes = True
