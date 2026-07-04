"""Enterprise Financial Workflow API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class StartFinancialWorkflowRequest(BaseModel):
    workflow_type: str
    source_context: str
    source_document_id: str
    assignee_id: str
    idempotency_key: str | None = None
    amount: float | None = Field(default=None, ge=0)
    currency: str = "USD"
    sla_hours: int | None = Field(default=None, gt=0)
    metadata: dict | None = None


class WorkflowActionRequest(BaseModel):
    comment: str = ""


class EscalateWorkflowRequest(BaseModel):
    escalated_to: str | None = None


class SignWorkflowRequest(BaseModel):
    signer_id: str | None = None
