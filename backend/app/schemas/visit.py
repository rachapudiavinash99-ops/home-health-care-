from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VisitBase(BaseModel):
    services_provided: Optional[str] = None
    patient_condition: Optional[str] = None
    notes: Optional[str] = None
    follow_up_recommendation: Optional[str] = None

class VisitCreate(VisitBase):
    appointment_id: int

class VisitUpdate(VisitBase):
    departure_time: datetime

class VisitResponse(VisitBase):
    id: int
    appointment_id: int
    arrival_time: datetime
    departure_time: Optional[datetime] = None
    
    class Config:
        from_attributes = True
