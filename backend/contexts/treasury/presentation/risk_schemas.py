"""Enterprise Treasury Risk Platform API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreateRiskLimitRequest(BaseModel):
    risk_type: str
    name: str
    threshold_value: float
    threshold_unit: str
    currency: str = "USD"
    description: str = ""


class UpdateRiskLimitRequest(BaseModel):
    threshold_value: float = Field(gt=0)


class RunStressTestRequest(BaseModel):
    scenario: str
