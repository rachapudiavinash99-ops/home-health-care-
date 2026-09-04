from pydantic import BaseModel
from typing import Dict, Any

class DashboardStatsResponse(BaseModel):
    total_patients: int
    total_caregivers: int
    total_doctors: int
    active_appointments: int
    completed_visits: int
    total_revenue: float
    pending_payments: float
