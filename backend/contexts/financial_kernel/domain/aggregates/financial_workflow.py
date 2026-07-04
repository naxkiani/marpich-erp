"""Financial workflow aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class FinancialWorkflowType(StrEnum):
    APPROVAL = "approval"
    PAYMENT = "payment"
    PURCHASE = "purchase"
    EXPENSE = "expense"
    TRANSFER = "transfer"
    BUDGET = "budget"
    INVOICE = "invoice"
    PAYROLL = "payroll"
    TAX = "tax"
    TREASURY = "treasury"


class FinancialWorkflowStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    ESCALATED = "escalated"
    APPROVED = "approved"
    REJECTED = "rejected"
    SIGNED = "signed"
    COMPLETED = "completed"


@dataclass(eq=False, kw_only=True)
class WorkflowHistoryEntry:
    action: str
    actor_id: str
    details: dict
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict:
        return {
            "action": self.action,
            "actor_id": self.actor_id,
            "details": self.details,
            "occurred_at": self.occurred_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class FinancialWorkflow(AggregateRoot):
    tenant_id: str
    workflow_type: str
    source_context: str
    source_document_id: str
    idempotency_key: str
    status: FinancialWorkflowStatus
    assignee_id: str
    escalated_to: str | None
    amount: float | None
    currency: str
    sla_hours: int
    sla_deadline: datetime
    escalated_at: datetime | None
    ai_recommendation: dict | None
    signature: dict | None
    history: list[WorkflowHistoryEntry]
    metadata: dict
    started_by: str
    completed_at: datetime | None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def start(
        cls,
        *,
        tenant_id: str,
        workflow_type: str,
        source_context: str,
        source_document_id: str,
        idempotency_key: str,
        assignee_id: str,
        sla_hours: int,
        sla_deadline: datetime,
        started_by: str,
        amount: float | None = None,
        currency: str = "USD",
        metadata: dict | None = None,
        ai_recommendation: dict | None = None,
    ) -> FinancialWorkflow:
        history = [
            WorkflowHistoryEntry(
                action="started",
                actor_id=started_by,
                details={"workflow_type": workflow_type, "assignee_id": assignee_id},
            )
        ]
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            workflow_type=workflow_type,
            source_context=source_context,
            source_document_id=source_document_id,
            idempotency_key=idempotency_key,
            status=FinancialWorkflowStatus.PENDING,
            assignee_id=assignee_id,
            escalated_to=None,
            amount=round(amount, 2) if amount is not None else None,
            currency=currency.strip().upper(),
            sla_hours=sla_hours,
            sla_deadline=sla_deadline,
            escalated_at=None,
            ai_recommendation=ai_recommendation,
            signature=None,
            history=history,
            metadata=dict(metadata or {}),
            started_by=started_by,
            completed_at=None,
        )

    def _audit(self, action: str, actor_id: str, details: dict | None = None) -> None:
        self.history.append(
            WorkflowHistoryEntry(action=action, actor_id=actor_id, details=details or {})
        )

    def approve(self, actor_id: str, comment: str = "") -> None:
        if self.status in (FinancialWorkflowStatus.REJECTED, FinancialWorkflowStatus.COMPLETED):
            raise ValueError("workflow_terminal")
        self.status = FinancialWorkflowStatus.APPROVED
        self._audit("approved", actor_id, {"comment": comment})

    def reject(self, actor_id: str, comment: str = "") -> None:
        if self.status in (FinancialWorkflowStatus.REJECTED, FinancialWorkflowStatus.COMPLETED):
            raise ValueError("workflow_terminal")
        self.status = FinancialWorkflowStatus.REJECTED
        self.completed_at = datetime.now(UTC)
        self._audit("rejected", actor_id, {"comment": comment})

    def escalate(self, actor_id: str, escalated_to: str) -> None:
        if self.status in (FinancialWorkflowStatus.REJECTED, FinancialWorkflowStatus.COMPLETED):
            raise ValueError("workflow_terminal")
        self.status = FinancialWorkflowStatus.ESCALATED
        self.escalated_to = escalated_to
        self.escalated_at = datetime.now(UTC)
        self._audit("escalated", actor_id, {"escalated_to": escalated_to})

    def sign(self, signature: dict, actor_id: str) -> None:
        if self.status != FinancialWorkflowStatus.APPROVED:
            raise ValueError("not_approved")
        self.signature = signature
        self.status = FinancialWorkflowStatus.SIGNED
        self._audit("signed", actor_id, {"algorithm": signature.get("algorithm")})

    def complete(self, actor_id: str) -> None:
        if self.status not in (FinancialWorkflowStatus.APPROVED, FinancialWorkflowStatus.SIGNED):
            raise ValueError("not_ready_to_complete")
        self.status = FinancialWorkflowStatus.COMPLETED
        self.completed_at = datetime.now(UTC)
        self._audit("completed", actor_id, {})

    def set_ai_recommendation(self, recommendation: dict, actor_id: str = "ai") -> None:
        self.ai_recommendation = recommendation
        self._audit("ai_recommendation", actor_id, recommendation)

    def is_sla_breached(self, now: datetime | None = None) -> bool:
        check = now or datetime.now(UTC)
        return (
            self.status in (FinancialWorkflowStatus.PENDING, FinancialWorkflowStatus.IN_PROGRESS)
            and check > self.sla_deadline
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "workflow_type": self.workflow_type,
            "source_context": self.source_context,
            "source_document_id": self.source_document_id,
            "idempotency_key": self.idempotency_key,
            "status": self.status.value,
            "assignee_id": self.assignee_id,
            "escalated_to": self.escalated_to,
            "amount": self.amount,
            "currency": self.currency,
            "sla_hours": self.sla_hours,
            "sla_deadline": self.sla_deadline.isoformat(),
            "sla_breached": self.is_sla_breached(),
            "escalated_at": self.escalated_at.isoformat() if self.escalated_at else None,
            "ai_recommendation": self.ai_recommendation,
            "signature": self.signature,
            "history": [h.to_dict() for h in self.history],
            "metadata": self.metadata,
            "started_by": self.started_by,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat(),
        }
