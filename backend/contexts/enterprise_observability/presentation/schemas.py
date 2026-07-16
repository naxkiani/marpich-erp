"""Enterprise Observability presentation schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreateAlertRequest(BaseModel):
    signal: str
    metric_key: str
    operator: str = "gt"
    threshold: float
    severity: str = "warning"


class CreateIncidentRequest(BaseModel):
    title: str
    severity: str = "warning"
    source_signal: str
    summary: str = ""
    correlation_id: str = ""


class ResolveIncidentRequest(BaseModel):
    resolution_summary: str = ""


class IngestLogRequest(BaseModel):
    level: str = "INFO"
    logger: str = "marpich.application"
    message: str
    context_name: str = ""
    duration_ms: float | None = None
    status: int | None = None
    metadata: dict = Field(default_factory=dict)


class RecordTraceRequest(BaseModel):
    span_name: str
    service_name: str = "marpich-backend"
    duration_ms: float
    status: str = "ok"
    context_name: str = ""
    parent_ref: str = ""
    attributes: dict = Field(default_factory=dict)
