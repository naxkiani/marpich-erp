"""Audit API schemas."""
from pydantic import BaseModel, Field


class CreateExportRequest(BaseModel):
    format: str = Field(default="json", pattern=r"^(json|csv)$")
    event_name: str | None = None
    severity: str | None = None
    actor_id: str | None = None
    date_from: str | None = None
    date_to: str | None = None


class RecordEntryRequest(BaseModel):
    action: str = Field(min_length=2, max_length=128)
    resource_type: str = Field(min_length=2, max_length=64)
    resource_id: str | None = None
    severity: str = Field(default="info", pattern=r"^(info|security|compliance)$")
    payload: dict | None = None
