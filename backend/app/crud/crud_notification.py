from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate

async def create_notification(db: AsyncSession, notif_in: NotificationCreate):
    db_obj = Notification(**notif_in.dict())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_user_notifications(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Notification).where(Notification.user_id == user_id).order_by(Notification.created_at.desc())
    )
    return result.scalars().all()

async def mark_as_read(db: AsyncSession, notification_id: int, user_id: int):
    result = await db.execute(
        select(Notification).where(Notification.id == notification_id, Notification.user_id == user_id)
    )
    notif = result.scalars().first()
    if notif:
        notif.is_read = True
        db.add(notif)
        await db.commit()
        await db.refresh(notif)
    return notif
