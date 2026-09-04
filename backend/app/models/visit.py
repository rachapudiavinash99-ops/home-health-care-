from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False, unique=True)
    
    arrival_time = Column(DateTime(timezone=True), default=func.now())
    departure_time = Column(DateTime(timezone=True), nullable=True)
    
    services_provided = Column(String)
    patient_condition = Column(String)
    notes = Column(String)
    follow_up_recommendation = Column(String)
    
    appointment = relationship("Appointment")
