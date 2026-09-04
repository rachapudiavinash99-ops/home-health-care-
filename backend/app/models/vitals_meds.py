from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base_class import Base

class MedicationStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    DISCONTINUED = "DISCONTINUED"

class VitalSign(Base):
    __tablename__ = "vital_signs"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    visit_id = Column(Integer, ForeignKey("visits.id"), nullable=True)
    
    recorded_at = Column(DateTime(timezone=True), default=func.now())
    temperature = Column(Float)
    blood_pressure = Column(String)
    heart_rate = Column(Integer)
    respiratory_rate = Column(Integer)
    oxygen_saturation = Column(Float)
    blood_glucose = Column(Float)
    weight = Column(Float)
    
    patient = relationship("Patient")
    visit = relationship("Visit")

class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    prescribed_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    medicine_name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    route = Column(String)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    instructions = Column(String)
    status = Column(Enum(MedicationStatus), default=MedicationStatus.ACTIVE)
    
    patient = relationship("Patient")
    doctor = relationship("User")
