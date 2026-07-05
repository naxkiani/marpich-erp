"""Enterprise Cash Reconciliation aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class CashReconStatus(StrEnum):
    DRAFT = "draft"
    COUNTED = "counted"
    VERIFIED = "verified"
    PENDING_MANAGER_APPROVAL = "pending_manager_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    CLOSED = "closed"


class VarianceType(StrEnum):
    BALANCED = "balanced"
    CASH_OVER = "cash_over"
    CASH_SHORT = "cash_short"


class ClosingType(StrEnum):
    CASH_CLOSING = "cash_closing"
    SHIFT_CLOSING = "shift_closing"
    BRANCH_CLOSING = "branch_closing"


@dataclass(eq=False, kw_only=True)
class CashReconciliationRun(AggregateRoot):
    tenant_id: str
    location_id: str
    branch_id: str | None
    closing_type: str
    system_balance: float
    counted_amount: float
    variance: float
    variance_type: str
    currency: str
    status: str
    requires_manager_approval: bool
    counted_by: str | None = None
    verified_by: str | None = None
    approved_by: str | None = None
    rejection_reason: str = ""
    ai_anomalies: list[dict] = field(default_factory=list)
    discrepancy_report: dict = field(default_factory=dict)
    notes: str | None = None
    closed_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        location_id: str,
        closing_type: str,
        system_balance: float,
        counted_amount: float,
        currency: str,
        branch_id: str | None = None,
        counted_by: str | None = None,
        notes: str | None = None,
        ai_anomalies: list[dict] | None = None,
        discrepancy_report: dict | None = None,
    ) -> CashReconciliationRun:
        variance = round(counted_amount - system_balance, 2)
        if abs(variance) < 0.01:
            vtype = VarianceType.BALANCED.value
        elif variance > 0:
            vtype = VarianceType.CASH_OVER.value
        else:
            vtype = VarianceType.CASH_SHORT.value

        requires_approval = abs(variance) >= 0.01
        status = CashReconStatus.COUNTED.value

        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            location_id=location_id,
            branch_id=branch_id,
            closing_type=closing_type,
            system_balance=round(system_balance, 2),
            counted_amount=round(counted_amount, 2),
            variance=variance,
            variance_type=vtype,
            currency=currency.strip().upper(),
            status=status,
            requires_manager_approval=requires_approval,
            counted_by=counted_by,
            notes=notes,
            ai_anomalies=ai_anomalies or [],
            discrepancy_report=discrepancy_report or {},
        )

    def verify(self, verified_by: str) -> None:
        if self.status != CashReconStatus.COUNTED.value:
            raise ValueError("not_counted")
        self.status = CashReconStatus.VERIFIED.value
        self.verified_by = verified_by
        if self.requires_manager_approval:
            self.status = CashReconStatus.PENDING_MANAGER_APPROVAL.value
        else:
            self.status = CashReconStatus.APPROVED.value
        self.updated_at = datetime.now(UTC)

    def approve(self, manager_id: str) -> None:
        if self.status != CashReconStatus.PENDING_MANAGER_APPROVAL.value:
            raise ValueError("not_pending_approval")
        self.status = CashReconStatus.APPROVED.value
        self.approved_by = manager_id
        self.updated_at = datetime.now(UTC)

    def reject(self, manager_id: str, reason: str = "") -> None:
        if self.status != CashReconStatus.PENDING_MANAGER_APPROVAL.value:
            raise ValueError("not_pending_approval")
        self.status = CashReconStatus.REJECTED.value
        self.approved_by = manager_id
        self.rejection_reason = reason
        self.updated_at = datetime.now(UTC)

    def close(self) -> None:
        if self.status != CashReconStatus.APPROVED.value:
            raise ValueError("not_approved")
        self.status = CashReconStatus.CLOSED.value
        self.closed_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "location_id": self.location_id,
            "branch_id": self.branch_id,
            "closing_type": self.closing_type,
            "system_balance": self.system_balance,
            "counted_amount": self.counted_amount,
            "variance": self.variance,
            "variance_type": self.variance_type,
            "currency": self.currency,
            "status": self.status,
            "requires_manager_approval": self.requires_manager_approval,
            "counted_by": self.counted_by,
            "verified_by": self.verified_by,
            "approved_by": self.approved_by,
            "rejection_reason": self.rejection_reason,
            "ai_anomalies": self.ai_anomalies,
            "discrepancy_report": self.discrepancy_report,
            "notes": self.notes,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class CashReconciliationAudit(AggregateRoot):
    tenant_id: str
    reconciliation_id: str
    action: str
    actor_id: str | None
    detail: str
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        reconciliation_id: str,
        action: str,
        actor_id: str | None = None,
        detail: str = "",
    ) -> CashReconciliationAudit:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            reconciliation_id=reconciliation_id,
            action=action,
            actor_id=actor_id,
            detail=detail,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "reconciliation_id": self.reconciliation_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "detail": self.detail,
            "occurred_at": self.occurred_at.isoformat(),
        }
