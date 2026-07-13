"""Enterprise Scheduler presentation schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreateJobRequest(BaseModel):
    name: str
    job_type: str
    cron_expression: str = ""
    calendar_rule: str = ""
    recurrence_rule: str = ""
    event_pattern: str = ""
    workflow_ref: str = ""
    priority: int | None = None
    max_retries: int | None = None
    depends_on: list[str] = Field(default_factory=list)
    payload: dict = Field(default_factory=dict)


class RegisterDependencyRequest(BaseModel):
    job_ref: str
    depends_on_job_ref: str
    required_status: str = "succeeded"
