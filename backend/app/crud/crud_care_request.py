from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.care_request import CareRequest
from app.schemas.care_request import CareRequestCreate, CareRequestUpdate

async def create_care_request(db: AsyncSession, request_in: CareRequestCreate, patient_id: int):
    db_obj = CareRequest(**request_in.dict(), patient_id=patient_id)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_patient_requests(db: AsyncSession, patient_id: int):
    result = await db.execute(select(CareRequest).where(CareRequest.patient_id == patient_id))
    return result.scalars().all()

async def get_all_requests(db: AsyncSession):
    result = await db.execute(select(CareRequest))
    return result.scalars().all()
