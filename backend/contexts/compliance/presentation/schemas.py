"""Compliance API schemas."""
from pydantic import BaseModel, Field


class ResolveViolationRequest(BaseModel):
    notes: str = Field(min_length=3, max_length=2000)


class CreateReportRequest(BaseModel):
    report_type: str = Field(pattern=r"^(full|domain|audit|retention)$")
    domain: str | None = None
    format: str = Field(default="json", pattern=r"^(json|csv|pdf)$")
    date_from: str | None = None
    date_to: str | None = None
