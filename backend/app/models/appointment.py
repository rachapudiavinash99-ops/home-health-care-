from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

class AppointmentState(str, enum.Enum):
    CONFIRMED = "CONFIRMED"
    ASSIGNED = "ASSIGNED"
    EN_ROUTE = "EN_ROUTE"
    ARRIVED = "ARRIVED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    care_request_id = Column(Integer, ForeignKey("care_requests.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    caregiver_id = Column(Integer, ForeignKey("caregivers.id"), nullable=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    
    scheduled_date = Column(DateTime, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    
    status = Column(Enum(AppointmentState), default=AppointmentState.CONFIRMED)
    notes = Column(String)
    
    care_request = relationship("CareRequest")
    patient = relationship("Patient")
    caregiver = relationship("Caregiver")
    service = relationship("Service")
