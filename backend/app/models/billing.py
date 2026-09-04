from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base_class import Base

class InvoiceStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
    CANCELLED = "CANCELLED"

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, index=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    
    base_price = Column(Float, nullable=False)
    additional_charges = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    total = Column(Float, nullable=False)
    
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.PENDING)
    invoice_date = Column(DateTime(timezone=True), default=func.now())
    
    patient = relationship("Patient")
    appointment = relationship("Appointment")
    payments = relationship("Payment", back_populates="invoice")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_id = Column(String, unique=True, index=True, nullable=False)
    payment_method = Column(String)  # e.g., 'TEST_CARD', 'CASH'
    status = Column(String, nullable=False)  # e.g., 'SUCCESS', 'FAILED'
    payment_date = Column(DateTime(timezone=True), default=func.now())
    
    invoice = relationship("Invoice", back_populates="payments")
