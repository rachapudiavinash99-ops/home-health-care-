from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

class CareRequestStatus(str, enum.Enum):
    PENDING = "PENDING"
    REVIEWING = "REVIEWING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class CareRequest(Base):
    __tablename__ = "care_requests"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    preferred_date = Column(DateTime, nullable=False)
    preferred_start_time = Column(String, nullable=False)
    duration_hours = Column(Integer, nullable=False)
    medical_requirements = Column(String)
    special_instructions = Column(String)
    status = Column(Enum(CareRequestStatus), default=CareRequestStatus.PENDING)
    
    patient = relationship("Patient")
    service = relationship("Service")
