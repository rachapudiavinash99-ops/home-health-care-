from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Date
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

class CarePlanStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    PAUSED = "PAUSED"
    CANCELLED = "CANCELLED"

class CarePlan(Base):
    __tablename__ = "care_plans"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    diagnosis = Column(String, nullable=False)
    goals = Column(String)
    instructions = Column(String)
    required_services = Column(String)
    frequency = Column(String)
    
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    follow_up_date = Column(Date, nullable=True)
    
    status = Column(Enum(CarePlanStatus), default=CarePlanStatus.ACTIVE)
    
    patient = relationship("Patient")
    doctor = relationship("User")
