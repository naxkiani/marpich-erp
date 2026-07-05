"""Interest Calculation Engine API schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CreateRateProfileRequest(BaseModel):
    product_context: str = Field(..., description="deposit | loan | generic")
    rate_type: str = Field(..., description="fixed | floating | promotional")
    rate_annual: float = Field(..., ge=0)
    spread_bps: float = Field(0.0, ge=0)
    index_ref: str = ""
    index_rate_annual: float | None = None
    promotional_until: datetime | None = None
    promotional_rate_annual: float | None = None
    currency: str = "USD"


class RateChangeRequest(BaseModel):
    new_rate_annual: float = Field(..., ge=0)
    rate_type: str | None = None
    effective_from: datetime | None = None
    reason: str = ""
    changed_by: str | None = None


class CalculateInterestRequest(BaseModel):
    product_context: str = Field(..., description="deposit | loan | generic")
    principal: float = Field(..., gt=0)
    frequency: str = Field(..., description="daily | monthly | annual")
    method: str | None = Field(None, description="simple | compound")
    periods: int = Field(1, ge=1)
    days: int | None = Field(None, ge=1)
    profile_id: str | None = None
    rate_annual: float | None = None
    days_overdue: int = Field(0, ge=0)
    profit_pool: float = Field(0.0, ge=0)
    source_ref: str = ""
    currency: str = "USD"


class SimulateInterestRequest(BaseModel):
    product_context: str
    principal: float = Field(..., gt=0)
    frequency: str
    method: str | None = None
    periods: int = Field(1, ge=1)
    days: int | None = Field(None, ge=1)
    profile_id: str | None = None
    rate_annual: float | None = None
    days_overdue: int = Field(0, ge=0)
    profit_pool: float = Field(0.0, ge=0)
    currency: str = "USD"
