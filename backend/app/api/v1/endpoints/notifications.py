from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.crud import crud_notification
from app.schemas.notification import NotificationResponse, NotificationCreate
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[NotificationResponse])
async def read_notifications(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    notifs = await crud_notification.get_user_notifications(db, user_id=current_user.id)
    return notifs

@router.put("/{notif_id}/read", response_model=NotificationResponse)
async def mark_notification_read(
    notif_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    notif = await crud_notification.mark_as_read(db, notification_id=notif_id, user_id=current_user.id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notif

# Internal/Admin endpoint for generating notifications
@router.post("/", response_model=NotificationResponse)
async def create_notification(
    *,
    db: AsyncSession = Depends(deps.get_db),
    notif_in: NotificationCreate,
    current_user: User = Depends(deps.role_required(["ADMIN"]))
) -> Any:
    notif = await crud_notification.create_notification(db, notif_in=notif_in)
    return notif
