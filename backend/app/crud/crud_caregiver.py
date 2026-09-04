from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import Caregiver, User
from app.schemas.caregiver import CaregiverCreate, CaregiverUpdate
from app.models.appointment import Appointment

async def get_caregiver_by_user_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(Caregiver).where(Caregiver.user_id == user_id))
    return result.scalars().first()

async def get_all_caregivers(db: AsyncSession):
    result = await db.execute(select(Caregiver))
    return result.scalars().all()

async def create_caregiver(db: AsyncSession, caregiver_in: CaregiverCreate, user_id: int):
    db_cg = Caregiver(**caregiver_in.dict(), user_id=user_id)
    db.add(db_cg)
    await db.commit()
    await db.refresh(db_cg)
    return db_cg

async def update_caregiver(db: AsyncSession, db_cg: Caregiver, caregiver_in: CaregiverUpdate):
    update_data = caregiver_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_cg, field, value)
    db.add(db_cg)
    await db.commit()
    await db.refresh(db_cg)
    return db_cg

async def get_caregiver_appointments(db: AsyncSession, caregiver_id: int):
    result = await db.execute(select(Appointment).where(Appointment.caregiver_id == caregiver_id))
    return result.scalars().all()
