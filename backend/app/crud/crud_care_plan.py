from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.care_plan import CarePlan
from app.schemas.care_plan import CarePlanCreate, CarePlanUpdate

async def create_care_plan(db: AsyncSession, cp_in: CarePlanCreate, doctor_id: int):
    db_obj = CarePlan(**cp_in.dict(), doctor_id=doctor_id)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_all_care_plans(db: AsyncSession):
    result = await db.execute(select(CarePlan))
    return result.scalars().all()

async def get_patient_care_plans(db: AsyncSession, patient_id: int):
    result = await db.execute(select(CarePlan).where(CarePlan.patient_id == patient_id))
    return result.scalars().all()

async def get_doctor_care_plans(db: AsyncSession, doctor_id: int):
    result = await db.execute(select(CarePlan).where(CarePlan.doctor_id == doctor_id))
    return result.scalars().all()

async def get_care_plan(db: AsyncSession, cp_id: int):
    result = await db.execute(select(CarePlan).where(CarePlan.id == cp_id))
    return result.scalars().first()

async def update_care_plan_status(db: AsyncSession, db_cp: CarePlan, status_in: CarePlanUpdate):
    db_cp.status = status_in.status
    db.add(db_cp)
    await db.commit()
    await db.refresh(db_cp)
    return db_cp
