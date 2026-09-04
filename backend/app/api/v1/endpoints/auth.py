from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core import security
from app.core.config import settings
from app.crud import crud_user
from app.schemas.user import UserCreate, UserResponse, Token

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    user = await crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=409,
            detail="The user with this username already exists in the system.",
        )
    user = await crud_user.create_user(db, user_in=user_in)
    return user

@router.post("/login", response_model=Token)
async def login(
    db: AsyncSession = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = await crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.get("/me")
async def get_me(
    current_user: Any = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    from sqlalchemy.future import select
    from app.models.user import Patient, Caregiver, UserRole
    
    full_name = current_user.email.split("@")[0].replace(".", " ").title()
    if current_user.role == UserRole.PATIENT:
        p_res = await db.execute(select(Patient).where(Patient.user_id == current_user.id))
        pat = p_res.scalars().first()
        if pat and pat.full_name:
            full_name = pat.full_name
    elif current_user.role == UserRole.CAREGIVER:
        cg_res = await db.execute(select(Caregiver).where(Caregiver.user_id == current_user.id))
        cg = cg_res.scalars().first()
        if cg and cg.full_name:
            full_name = cg.full_name
    elif current_user.role == UserRole.ADMIN:
        full_name = "Hospital Administrator"
    elif current_user.role == UserRole.DOCTOR:
        full_name = f"Dr. {current_user.email.split('@')[0].replace('dr.', '').title()}"

    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role.value,
        "full_name": full_name,
        "is_active": current_user.is_active
    }

