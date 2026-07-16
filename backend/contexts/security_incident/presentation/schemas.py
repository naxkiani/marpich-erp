"""Enterprise Security Incident Platform API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class DetectIncidentRequest(BaseModel):
    title: str
    description: str
    classification: str
    severity: str = "medium"
    source_module: str = ""


class ClassifyIncidentRequest(BaseModel):
    classification: str
    severity: str


class InvestigateIncidentRequest(BaseModel):
    assigned_to: str = ""


class ContainIncidentRequest(BaseModel):
    actions: list[str] = Field(default_factory=list)


class RecoverIncidentRequest(BaseModel):
    actions: list[str] = Field(default_factory=list)


class RootCauseRequest(BaseModel):
    root_cause: str


class ResolveIncidentRequest(BaseModel):
    root_cause: str = ""


class CollectEvidenceRequest(BaseModel):
    evidence_type: str
    description: str


class RecordLessonRequest(BaseModel):
    title: str
    summary: str
    recommendations: list[str] = Field(default_factory=list)


class NotifyIncidentRequest(BaseModel):
    channel: str = "email"
    recipient: str
    subject: str = ""
    message: str = ""
