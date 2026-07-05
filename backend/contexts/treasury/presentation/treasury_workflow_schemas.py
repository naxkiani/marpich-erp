"""Treasury Workflow API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class WorkflowStepDefinition(BaseModel):
    step_id: str
    level: int = 1
    role: str
    order: int = 1


class CreateWorkflowDefinitionRequest(BaseModel):
    name: str
    workflow_type: str
    approval_mode: str = "sequential"
    steps: list[WorkflowStepDefinition]
    sla_hours: int = Field(default=48, ge=1, le=720)
    description: str = ""


class CreateWorkflowLimitRequest(BaseModel):
    workflow_type: str
    name: str
    max_amount: float = Field(gt=0)
    currency: str = "USD"
    approval_levels: int = Field(default=1, ge=1, le=5)


class CreateWorkflowRequest(BaseModel):
    workflow_type: str
    amount: float = Field(gt=0)
    currency: str = "USD"
    subject_ref: str
    subject_type: str
    title: str
    description: str = ""
    definition_id: str | None = None


class ApproveStepRequest(BaseModel):
    step_id: str
    comment: str = ""
    with_signature: bool = True


class RejectRequest(BaseModel):
    comment: str = ""


class DelegateRequest(BaseModel):
    step_id: str
    to_user: str
    reason: str = ""


class EscalateRequest(BaseModel):
    escalated_to: str
    reason: str = "sla_breach"
