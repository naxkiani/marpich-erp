"""Enterprise Risk Platform API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class RegisterRiskRequest(BaseModel):
    title: str = Field(min_length=3, max_length=500)
    category: str
    likelihood: int = Field(ge=1, le=5)
    impact: int = Field(ge=1, le=5)
    owner_id: str = ""
    source_module: str = ""
    mitigation_plan: str = ""


class PredictRiskRequest(BaseModel):
    category: str | None = None
