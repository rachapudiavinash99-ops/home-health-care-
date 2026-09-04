from pydantic import BaseModel
from typing import Optional

class CaregiverBase(BaseModel):
    full_name: str
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: Optional[int] = None

class CaregiverCreate(CaregiverBase):
    pass

class CaregiverUpdate(CaregiverBase):
    full_name: Optional[str] = None

class CaregiverResponse(CaregiverBase):
    id: int
    user_id: int
    is_verified: bool
    
    class Config:
        from_attributes = True
