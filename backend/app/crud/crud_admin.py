from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.user import Patient, Caregiver, User
from app.models.appointment import Appointment
from app.models.visit import Visit
from app.models.billing import Invoice, InvoiceStatus

async def get_dashboard_stats(db: AsyncSession):
    # 1. Total Patients
    res = await db.execute(select(func.count(Patient.id)))
    total_patients = res.scalar() or 0
    
    # 2. Total Caregivers
    res = await db.execute(select(func.count(Caregiver.id)))
    total_caregivers = res.scalar() or 0
    
    # 3. Total Doctors (Users with DOCTOR role)
    res = await db.execute(select(func.count(User.id)).where(User.role == 'DOCTOR'))
    total_doctors = res.scalar() or 0
    
    # 4. Active appointments (not completed/cancelled)
    res = await db.execute(select(func.count(Appointment.id)).where(Appointment.status.in_(['CONFIRMED', 'ASSIGNED', 'EN_ROUTE', 'ARRIVED', 'IN_PROGRESS'])))
    active_appointments = res.scalar() or 0
    
    # 5. Completed Visits
    res = await db.execute(select(func.count(Visit.id)))
    completed_visits = res.scalar() or 0
    
    # 6. Total Revenue (Paid Invoices)
    res = await db.execute(select(func.sum(Invoice.total)).where(Invoice.status == InvoiceStatus.PAID))
    total_revenue = res.scalar() or 0.0
    
    # 7. Pending Payments (Pending Invoices)
    res = await db.execute(select(func.sum(Invoice.total)).where(Invoice.status == InvoiceStatus.PENDING))
    pending_payments = res.scalar() or 0.0
    
    return {
        "total_patients": total_patients,
        "total_caregivers": total_caregivers,
        "total_doctors": total_doctors,
        "active_appointments": active_appointments,
        "completed_visits": completed_visits,
        "total_revenue": float(total_revenue),
        "pending_payments": float(pending_payments)
    }
