from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.crud import crud_billing, crud_appointment
from app.schemas.billing import InvoiceCreate, InvoiceResponse, PaymentRequest, PaymentResponse
from app.models.user import User
from app.models.appointment import AppointmentState

router = APIRouter()

@router.post("/invoices", response_model=InvoiceResponse)
async def generate_invoice(
    *,
    db: AsyncSession = Depends(deps.get_db),
    invoice_in: InvoiceCreate,
    current_user: User = Depends(deps.role_required(["ADMIN"]))
) -> Any:
    appt = await crud_appointment.get_appointment(db, invoice_in.appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if appt.status != AppointmentState.COMPLETED:
        raise HTTPException(status_code=400, detail="Cannot invoice an incomplete appointment")
        
    invoice = await crud_billing.create_invoice(db, invoice_in=invoice_in, patient_id=appt.patient_id)
    return invoice

@router.get("/invoices", response_model=List[InvoiceResponse])
async def read_all_invoices(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["ADMIN", "DOCTOR", "CAREGIVER"]))
) -> Any:
    invoices = await crud_billing.get_all_invoices(db)
    return invoices

@router.get("/invoices/patient/{patient_id}", response_model=List[InvoiceResponse])
async def read_invoices(
    patient_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["ADMIN", "PATIENT"]))
) -> Any:
    # RBAC logic for patient
    invoices = await crud_billing.get_patient_invoices(db, patient_id=patient_id)
    return invoices

@router.post("/payments", response_model=PaymentResponse)
async def make_test_payment(
    *,
    db: AsyncSession = Depends(deps.get_db),
    payment_in: PaymentRequest,
    current_user: User = Depends(deps.role_required(["PATIENT", "ADMIN"]))
) -> Any:
    invoice = await crud_billing.get_invoice(db, payment_in.invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
        
    if invoice.status == "PAID":
        raise HTTPException(status_code=400, detail="Invoice is already paid")
        
    payment = await crud_billing.process_sandbox_payment(
        db, invoice_id=payment_in.invoice_id, amount=payment_in.amount, method=payment_in.payment_method
    )
    return payment
