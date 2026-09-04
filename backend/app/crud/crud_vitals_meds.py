from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.vitals_meds import VitalSign, Medication
from app.schemas.vitals_meds import VitalSignCreate, MedicationCreate, MedicationUpdate

async def create_vital_sign(db: AsyncSession, vital_in: VitalSignCreate):
    db_obj = VitalSign(**vital_in.dict())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_patient_vitals(db: AsyncSession, patient_id: int):
    result = await db.execute(select(VitalSign).where(VitalSign.patient_id == patient_id))
    return result.scalars().all()

async def create_medication(db: AsyncSession, med_in: MedicationCreate, doctor_id: int):
    db_obj = Medication(**med_in.dict(), prescribed_by=doctor_id)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_patient_medications(db: AsyncSession, patient_id: int):
    result = await db.execute(select(Medication).where(Medication.patient_id == patient_id))
    return result.scalars().all()

async def update_medication_status(db: AsyncSession, med_id: int, status_in: MedicationUpdate):
    result = await db.execute(select(Medication).where(Medication.id == med_id))
    db_obj = result.scalars().first()
    if db_obj:
        db_obj.status = status_in.status
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
    return db_obj
