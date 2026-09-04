from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentUpdateStatus

async def create_appointment(db: AsyncSession, appt_in: AppointmentCreate):
    db_obj = Appointment(**appt_in.dict())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_appointment(db: AsyncSession, appt_id: int):
    result = await db.execute(select(Appointment).where(Appointment.id == appt_id))
    return result.scalars().first()

async def get_all_appointments(db: AsyncSession):
    result = await db.execute(select(Appointment))
    return result.scalars().all()

async def get_patient_appointments(db: AsyncSession, patient_id: int):
    result = await db.execute(select(Appointment).where(Appointment.patient_id == patient_id))
    return result.scalars().all()

async def update_appointment_status(db: AsyncSession, db_appt: Appointment, status_in: AppointmentUpdateStatus):
    db_appt.status = status_in.status
    db.add(db_appt)
    await db.commit()
    await db.refresh(db_appt)
    return db_appt
