"""Treasury Workflow aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class WorkflowType(StrEnum):
    TRANSFER_APPROVAL = "transfer_approval"
    PAYMENT_APPROVAL = "payment_approval"
    FUND_REQUEST = "fund_request"
    CASH_REQUEST = "cash_request"
    CASH_TRANSFER = "cash_transfer"
    INVESTMENT_APPROVAL = "investment_approval"
    BANK_ACCOUNT_APPROVAL = "bank_account_approval"


class ApprovalMode(StrEnum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"


class WorkflowStatus(StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    ESCALATED = "escalated"
    CANCELLED = "cancelled"


DEFAULT_SLA_HOURS = 48


@dataclass(eq=False, kw_only=True)
class TreasuryWorkflowDefinition(AggregateRoot):
    tenant_id: str
    name: str
    workflow_type: str
    approval_mode: str
    steps: list[dict]
    sla_hours: int
    is_active: bool = True
    description: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        name: str,
        workflow_type: str,
        approval_mode: str,
        steps: list[dict],
        sla_hours: int = DEFAULT_SLA_HOURS,
        description: str = "",
    ) -> TreasuryWorkflowDefinition:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            name=name.strip(),
            workflow_type=workflow_type,
            approval_mode=approval_mode,
            steps=steps,
            sla_hours=sla_hours,
            description=description,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "name": self.name,
            "workflow_type": self.workflow_type,
            "approval_mode": self.approval_mode,
            "steps": self.steps,
            "sla_hours": self.sla_hours,
            "is_active": self.is_active,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class TreasuryWorkflowLimit(AggregateRoot):
    tenant_id: str
    workflow_type: str
    name: str
    max_amount: float
    currency: str
    approval_levels: int
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        workflow_type: str,
        name: str,
        max_amount: float,
        currency: str = "USD",
        approval_levels: int = 1,
    ) -> TreasuryWorkflowLimit:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            workflow_type=workflow_type,
            name=name.strip(),
            max_amount=round(max_amount, 2),
            currency=currency.strip().upper(),
            approval_levels=approval_levels,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "workflow_type": self.workflow_type,
            "name": self.name,
            "max_amount": self.max_amount,
            "currency": self.currency,
            "approval_levels": self.approval_levels,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class TreasuryWorkflowRequest(AggregateRoot):
    tenant_id: str
    workflow_type: str
    definition_id: str
    approval_mode: str
    status: str
    amount: float
    currency: str
    subject_ref: str
    subject_type: str
    requester_id: str
    title: str
    description: str = ""
    steps: list[dict] = field(default_factory=list)
    delegations: list[dict] = field(default_factory=list)
    digital_signatures: list[dict] = field(default_factory=list)
    sla_due_at: datetime | None = None
    escalated_at: datetime | None = None
    escalated_to: str | None = None
    submitted_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        workflow_type: str,
        definition_id: str,
        approval_mode: str,
        amount: float,
        currency: str,
        subject_ref: str,
        subject_type: str,
        requester_id: str,
        title: str,
        description: str = "",
        steps: list[dict],
        sla_hours: int = DEFAULT_SLA_HOURS,
    ) -> TreasuryWorkflowRequest:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            workflow_type=workflow_type,
            definition_id=definition_id,
            approval_mode=approval_mode,
            status=WorkflowStatus.DRAFT.value,
            amount=round(amount, 2),
            currency=currency.strip().upper(),
            subject_ref=subject_ref,
            subject_type=subject_type,
            requester_id=requester_id,
            title=title.strip(),
            description=description,
            steps=[{**s, "status": "pending"} for s in steps],
        )

    def submit(self, sla_hours: int = DEFAULT_SLA_HOURS) -> None:
        if self.status != WorkflowStatus.DRAFT.value:
            raise ValueError("only_draft_can_submit")
        self.status = WorkflowStatus.PENDING_APPROVAL.value
        self.submitted_at = datetime.now(UTC)
        self.sla_due_at = self.submitted_at + timedelta(hours=sla_hours)
        self.updated_at = datetime.now(UTC)

    def approve_step(
        self,
        *,
        step_id: str,
        approver_id: str,
        signature_hash: str | None = None,
        comment: str = "",
    ) -> None:
        if self.status not in {WorkflowStatus.PENDING_APPROVAL.value, WorkflowStatus.ESCALATED.value}:
            raise ValueError("not_pending_approval")
        step = self._find_step(step_id)
        if not step:
            raise ValueError("step_not_found")
        if step.get("status") == "approved":
            raise ValueError("step_already_approved")

        if self.approval_mode == ApprovalMode.SEQUENTIAL.value:
            ordered = sorted(self.steps, key=lambda s: s.get("order", s.get("level", 0)))
            for s in ordered:
                if s.get("step_id") == step_id:
                    break
                if s.get("status") != "approved":
                    raise ValueError("prior_step_not_approved")

        step["status"] = "approved"
        step["approver_id"] = approver_id
        step["approved_at"] = datetime.now(UTC).isoformat()
        step["comment"] = comment

        if signature_hash:
            self.digital_signatures.append(
                {
                    "step_id": step_id,
                    "approver_id": approver_id,
                    "signature_hash": signature_hash,
                    "signed_at": datetime.now(UTC).isoformat(),
                }
            )

        if self.approval_mode == ApprovalMode.PARALLEL.value:
            if all(s.get("status") == "approved" for s in self.steps):
                self.status = WorkflowStatus.APPROVED.value
                self.completed_at = datetime.now(UTC)
        else:
            pending = [s for s in self.steps if s.get("status") != "approved"]
            if not pending:
                self.status = WorkflowStatus.APPROVED.value
                self.completed_at = datetime.now(UTC)

        self.updated_at = datetime.now(UTC)

    def reject(self, *, approver_id: str, comment: str = "") -> None:
        if self.status not in {WorkflowStatus.PENDING_APPROVAL.value, WorkflowStatus.ESCALATED.value}:
            raise ValueError("not_pending_approval")
        self.status = WorkflowStatus.REJECTED.value
        self.completed_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)
        for step in self.steps:
            if step.get("status") == "pending":
                step["status"] = "skipped"
        self.steps.append(
            {
                "step_id": "rejection",
                "approver_id": approver_id,
                "action": "rejected",
                "comment": comment,
                "at": datetime.now(UTC).isoformat(),
            }
        )

    def delegate(self, *, step_id: str, from_user: str, to_user: str, reason: str = "") -> None:
        step = self._find_step(step_id)
        if not step:
            raise ValueError("step_not_found")
        step["delegated_to"] = to_user
        step["delegated_from"] = from_user
        self.delegations.append(
            {
                "step_id": step_id,
                "from_user": from_user,
                "to_user": to_user,
                "reason": reason,
                "delegated_at": datetime.now(UTC).isoformat(),
            }
        )
        self.updated_at = datetime.now(UTC)

    def escalate(self, *, escalated_to: str, reason: str = "sla_breach") -> None:
        if self.status != WorkflowStatus.PENDING_APPROVAL.value:
            raise ValueError("not_pending_approval")
        self.status = WorkflowStatus.ESCALATED.value
        self.escalated_at = datetime.now(UTC)
        self.escalated_to = escalated_to
        self.updated_at = datetime.now(UTC)

    def execute(self) -> None:
        if self.status != WorkflowStatus.APPROVED.value:
            raise ValueError("not_approved")
        self.status = WorkflowStatus.EXECUTED.value
        self.completed_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def _find_step(self, step_id: str) -> dict | None:
        for step in self.steps:
            if step.get("step_id") == step_id:
                return step
        return None

    def is_sla_breached(self) -> bool:
        if not self.sla_due_at or self.status not in {
            WorkflowStatus.PENDING_APPROVAL.value,
            WorkflowStatus.ESCALATED.value,
        }:
            return False
        return datetime.now(UTC) > self.sla_due_at

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "workflow_type": self.workflow_type,
            "definition_id": self.definition_id,
            "approval_mode": self.approval_mode,
            "status": self.status,
            "amount": self.amount,
            "currency": self.currency,
            "subject_ref": self.subject_ref,
            "subject_type": self.subject_type,
            "requester_id": self.requester_id,
            "title": self.title,
            "description": self.description,
            "steps": self.steps,
            "delegations": self.delegations,
            "digital_signatures": self.digital_signatures,
            "sla_due_at": self.sla_due_at.isoformat() if self.sla_due_at else None,
            "sla_breached": self.is_sla_breached(),
            "escalated_at": self.escalated_at.isoformat() if self.escalated_at else None,
            "escalated_to": self.escalated_to,
            "submitted_at": self.submitted_at.isoformat() if self.submitted_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class TreasuryWorkflowAudit(AggregateRoot):
    tenant_id: str
    request_id: str
    action: str
    actor_id: str | None
    detail: str
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        request_id: str,
        action: str,
        actor_id: str | None = None,
        detail: str = "",
    ) -> TreasuryWorkflowAudit:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            request_id=request_id,
            action=action,
            actor_id=actor_id,
            detail=detail,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "request_id": self.request_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "detail": self.detail,
            "occurred_at": self.occurred_at.isoformat(),
        }
