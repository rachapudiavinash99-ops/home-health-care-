from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from app.models.vitals_meds import MedicationStatus

class VitalSignBase(BaseModel):
    temperature: Optional[float] = None
    blood_pressure: Optional[str] = None
    heart_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None
    oxygen_saturation: Optional[float] = None
    blood_glucose: Optional[float] = None
    weight: Optional[float] = None

class VitalSignCreate(VitalSignBase):
    patient_id: int
    visit_id: Optional[int] = None

class VitalSignResponse(VitalSignBase):
    id: int
    patient_id: int
    visit_id: Optional[int] = None
    recorded_at: datetime
    
    class Config:
        from_attributes = True

class MedicationBase(BaseModel):
    patient_id: int
    medicine_name: str
    dosage: str
    frequency: str
    route: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    instructions: Optional[str] = None

class MedicationCreate(MedicationBase):
    pass

class MedicationUpdate(BaseModel):
    status: MedicationStatus

class MedicationResponse(MedicationBase):
    id: int
    prescribed_by: int
    status: MedicationStatus
    
    class Config:
        from_attributes = True
