from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.billing import InvoiceStatus

class PaymentResponse(BaseModel):
    id: int
    amount: float
    transaction_id: str
    payment_method: str
    status: str
    payment_date: datetime
    
    class Config:
        from_attributes = True

class InvoiceBase(BaseModel):
    appointment_id: int
    base_price: float
    additional_charges: Optional[float] = 0.0
    discount: Optional[float] = 0.0
    tax: Optional[float] = 0.0

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceResponse(InvoiceBase):
    id: int
    invoice_number: str
    patient_id: int
    total: float
    status: InvoiceStatus
    invoice_date: datetime
    payments: List[PaymentResponse] = []
    
    class Config:
        from_attributes = True

class PaymentRequest(BaseModel):
    invoice_id: int
    amount: float
    payment_method: str = "TEST_CARD"
