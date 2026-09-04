from pydantic import BaseModel
from typing import Optional

class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    duration_minutes: Optional[int] = None
    base_price: float
    required_qualification: Optional[str] = None
    is_active: Optional[bool] = True

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(ServiceBase):
    name: Optional[str] = None
    base_price: Optional[float] = None

class ServiceResponse(ServiceBase):
    id: int
    
    class Config:
        from_attributes = True
