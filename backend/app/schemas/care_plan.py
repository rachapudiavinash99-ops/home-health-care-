from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.models.care_plan import CarePlanStatus

class CarePlanBase(BaseModel):
    patient_id: int
    diagnosis: str
    goals: Optional[str] = None
    instructions: Optional[str] = None
    required_services: Optional[str] = None
    frequency: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    follow_up_date: Optional[date] = None

class CarePlanCreate(CarePlanBase):
    pass

class CarePlanUpdate(BaseModel):
    status: CarePlanStatus

class CarePlanResponse(CarePlanBase):
    id: int
    doctor_id: int
    status: CarePlanStatus
    
    class Config:
        from_attributes = True
