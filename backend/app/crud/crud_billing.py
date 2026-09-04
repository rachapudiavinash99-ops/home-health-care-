from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.billing import Invoice, Payment, InvoiceStatus
from app.schemas.billing import InvoiceCreate
import uuid

async def create_invoice(db: AsyncSession, invoice_in: InvoiceCreate, patient_id: int):
    total = invoice_in.base_price + invoice_in.additional_charges + invoice_in.tax - invoice_in.discount
    inv_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
    
    db_obj = Invoice(
        **invoice_in.dict(),
        patient_id=patient_id,
        invoice_number=inv_number,
        total=total
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_all_invoices(db: AsyncSession):
    result = await db.execute(
        select(Invoice).options(selectinload(Invoice.payments))
    )
    return result.scalars().all()

async def get_patient_invoices(db: AsyncSession, patient_id: int):
    result = await db.execute(
        select(Invoice).options(selectinload(Invoice.payments)).where(Invoice.patient_id == patient_id)
    )
    return result.scalars().all()

async def get_invoice(db: AsyncSession, invoice_id: int):
    result = await db.execute(
        select(Invoice).options(selectinload(Invoice.payments)).where(Invoice.id == invoice_id)
    )
    return result.scalars().first()

async def process_sandbox_payment(db: AsyncSession, invoice_id: int, amount: float, method: str):
    tx_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
    payment = Payment(
        invoice_id=invoice_id,
        amount=amount,
        transaction_id=tx_id,
        payment_method=method,
        status="SUCCESS"
    )
    db.add(payment)
    
    # Update invoice status
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    invoice = result.scalars().first()
    if invoice:
        # In a real system, you'd calculate total paid vs total due
        invoice.status = InvoiceStatus.PAID
        db.add(invoice)
        
    await db.commit()
    await db.refresh(payment)
    return payment
