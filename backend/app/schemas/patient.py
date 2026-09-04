from pydantic import BaseModel
from typing import Optional

class PatientBase(BaseModel):
    full_name: str
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    full_name: Optional[str] = None

class PatientResponse(PatientBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True
