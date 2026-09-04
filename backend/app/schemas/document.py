from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentResponse(BaseModel):
    id: int
    patient_id: int
    uploaded_by: int
    filename: str
    file_type: str
    file_size: int
    description: Optional[str] = None
    uploaded_at: datetime
    
    class Config:
        from_attributes = True
