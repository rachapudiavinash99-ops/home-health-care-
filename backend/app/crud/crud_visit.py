from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.visit import Visit
from app.schemas.visit import VisitCreate, VisitUpdate
from datetime import datetime

async def create_visit(db: AsyncSession, visit_in: VisitCreate):
    db_obj = Visit(**visit_in.dict())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_visit_by_appointment(db: AsyncSession, appointment_id: int):
    result = await db.execute(select(Visit).where(Visit.appointment_id == appointment_id))
    return result.scalars().first()

async def update_visit(db: AsyncSession, db_visit: Visit, visit_in: VisitUpdate):
    update_data = visit_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_visit, field, value)
    db.add(db_visit)
    await db.commit()
    await db.refresh(db_visit)
    return db_visit
