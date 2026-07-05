"""Enterprise Cash Forecast API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ForecastLineRequest(BaseModel):
    date: str
    label: str
    category: str
    inflow: float = 0.0
    outflow: float = 0.0
    amount: float | None = None


class CreateForecastPlanRequest(BaseModel):
    name: str
    period_type: str
    period_start: str
    period_end: str
    scenario: str = "base"
    currency: str = "USD"
    opening_balance: float | None = None
    projected_lines: list[ForecastLineRequest]


class AIForecastRequest(BaseModel):
    horizon_days: int = Field(default=90, ge=30, le=365)


class ScenarioSimulationRequest(BaseModel):
    name: str | None = None
