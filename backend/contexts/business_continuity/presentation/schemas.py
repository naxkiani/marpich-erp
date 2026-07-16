"""Enterprise Business Continuity Platform API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreatePlanRequest(BaseModel):
    title: str
    plan_type: str
    criticality_tier: str
    rpo_hours: int | None = None
    rto_hours: int | None = None
    recovery_steps: list[str] = Field(default_factory=list)


class CreateBackupRequest(BaseModel):
    name: str
    backup_type: str
    frequency_hours: int
    retention_days: int
    rpo_hours: int
    encrypted: bool = True


class InitiateFailoverRequest(BaseModel):
    source_system: str
    target_system: str
    trigger_reason: str


class ScheduleTestRequest(BaseModel):
    plan_ref: str
    test_type: str = "full"


class ActivateEmergencyOpsRequest(BaseModel):
    plan_ref: str | None = None
