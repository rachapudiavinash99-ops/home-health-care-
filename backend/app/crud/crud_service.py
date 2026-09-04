from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate

async def get_service(db: AsyncSession, service_id: int):
    result = await db.execute(select(Service).where(Service.id == service_id))
    return result.scalars().first()

async def get_all_services(db: AsyncSession, active_only: bool = True):
    query = select(Service)
    if active_only:
        query = query.where(Service.is_active == True)
    result = await db.execute(query)
    return result.scalars().all()

async def create_service(db: AsyncSession, service_in: ServiceCreate):
    db_service = Service(**service_in.dict())
    db.add(db_service)
    await db.commit()
    await db.refresh(db_service)
    return db_service
