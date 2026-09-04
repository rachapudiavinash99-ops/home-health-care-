from fastapi import APIRouter
from app.api.v1.endpoints import auth

from app.api.v1.endpoints import patients
from app.api.v1.endpoints import services
from app.api.v1.endpoints import care_requests
from app.api.v1.endpoints import appointments
from app.api.v1.endpoints import caregivers
from app.api.v1.endpoints import visits
from app.api.v1.endpoints import care_plans
from app.api.v1.endpoints import vitals_meds
from app.api.v1.endpoints import documents
from app.api.v1.endpoints import billing
from app.api.v1.endpoints import notifications
from app.api.v1.endpoints import admin
api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

api_router.include_router(patients.router, prefix="/patients", tags=["patients"])

api_router.include_router(services.router, prefix="/services", tags=["services"])

api_router.include_router(care_requests.router, prefix="/care-requests", tags=["care-requests"])

api_router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])

api_router.include_router(caregivers.router, prefix="/caregivers", tags=["caregivers"])

api_router.include_router(visits.router, prefix="/visits", tags=["visits"])

api_router.include_router(care_plans.router, prefix="/care-plans", tags=["care-plans"])

api_router.include_router(vitals_meds.router, prefix="/medical", tags=["medical"])

api_router.include_router(documents.router, prefix="/documents", tags=["documents"])

api_router.include_router(billing.router, prefix="/billing", tags=["billing"])

api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])

api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
