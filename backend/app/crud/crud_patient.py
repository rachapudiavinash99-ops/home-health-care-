from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import Patient, User
from app.schemas.patient import PatientCreate, PatientUpdate

async def get_patient_by_user_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(Patient).where(Patient.user_id == user_id))
    return result.scalars().first()

async def create_patient(db: AsyncSession, patient_in: PatientCreate, user_id: int):
    db_patient = Patient(**patient_in.dict(), user_id=user_id)
    db.add(db_patient)
    await db.commit()
    await db.refresh(db_patient)
    return db_patient

async def get_all_patients(db: AsyncSession):
    result = await db.execute(select(Patient))
    return result.scalars().all()

async def get_patient_by_id(db: AsyncSession, patient_id: int):
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    return result.scalars().first()

async def update_patient(db: AsyncSession, db_patient: Patient, patient_in: PatientUpdate):
    update_data = patient_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_patient, field, value)
    db.add(db_patient)
    await db.commit()
    await db.refresh(db_patient)
    return db_patient

