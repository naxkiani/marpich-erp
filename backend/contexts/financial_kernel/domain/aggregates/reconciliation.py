"""Enterprise reconciliation aggregates — bank, cash, subledger, GL, intercompany."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class ReconciliationType(StrEnum):
    BANK = "bank"
    CASH = "cash"
    INTERCOMPANY = "intercompany"
    SUBLEDGER = "subledger"
    GENERAL_LEDGER = "general_ledger"


class ReconciliationStatus(StrEnum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    MATCHED = "matched"
    PARTIAL_MATCH = "partial_match"
    EXCEPTION = "exception"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"


class MatchType(StrEnum):
    AUTOMATIC = "automatic"
    MANUAL = "manual"


class ApprovalAction(StrEnum):
    SUBMIT = "submit"
    APPROVE = "approve"
    REJECT = "reject"
    REOPEN = "reopen"


@dataclass(eq=False, kw_only=True)
class ReconciliationRun(AggregateRoot):
    tenant_id: str
    reconciliation_type: str
    reference_id: str | None
    reference_label: str
    reconciliation_date: str
    period_id: str | None
    left_label: str
    right_label: str
    left_items: list[dict]
    right_items: list[dict]
    matched_pairs: list[dict]
    unmatched_left: list[dict]
    unmatched_right: list[dict]
    left_total: float
    right_total: float
    variance: float
    status: str
    difference_analysis: dict = field(default_factory=dict)
    ai_suggestions: list[dict] = field(default_factory=list)
    exceptions: list[dict] = field(default_factory=list)
    report_summary: dict = field(default_factory=dict)
    approval_status: str = "none"
    submitted_by: str | None = None
    approved_by: str | None = None
    approved_at: datetime | None = None
    rejection_reason: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        reconciliation_type: str,
        reference_id: str | None,
        reference_label: str,
        reconciliation_date: str,
        left_label: str,
        right_label: str,
        left_items: list[dict],
        right_items: list[dict],
        matched_pairs: list[dict],
        unmatched_left: list[dict],
        unmatched_right: list[dict],
        left_total: float,
        right_total: float,
        period_id: str | None = None,
        difference_analysis: dict | None = None,
        ai_suggestions: list[dict] | None = None,
        exceptions: list[dict] | None = None,
        report_summary: dict | None = None,
    ) -> ReconciliationRun:
        variance = round(right_total - left_total, 2)
        if matched_pairs and not unmatched_left and not unmatched_right and abs(variance) < 0.01:
            status = ReconciliationStatus.MATCHED.value
        elif matched_pairs:
            status = ReconciliationStatus.PARTIAL_MATCH.value
        elif unmatched_left or unmatched_right:
            status = ReconciliationStatus.EXCEPTION.value
        else:
            status = ReconciliationStatus.IN_PROGRESS.value
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            reconciliation_type=reconciliation_type,
            reference_id=reference_id,
            reference_label=reference_label,
            reconciliation_date=reconciliation_date,
            period_id=period_id,
            left_label=left_label,
            right_label=right_label,
            left_items=left_items,
            right_items=right_items,
            matched_pairs=matched_pairs,
            unmatched_left=unmatched_left,
            unmatched_right=unmatched_right,
            left_total=round(left_total, 2),
            right_total=round(right_total, 2),
            variance=variance,
            status=status,
            difference_analysis=difference_analysis or {},
            ai_suggestions=ai_suggestions or [],
            exceptions=exceptions or [],
            report_summary=report_summary or {},
        )

    def apply_manual_match(
        self,
        *,
        left_item: dict,
        right_item: dict,
        actor_id: str,
    ) -> None:
        self.matched_pairs.append(
            {
                "left": left_item,
                "right": right_item,
                "match_type": MatchType.MANUAL.value,
                "matched_by": actor_id,
                "matched_at": datetime.now(UTC).isoformat(),
            }
        )
        self.unmatched_left = [
            i for i in self.unmatched_left if i != left_item
        ]
        self.unmatched_right = [
            i for i in self.unmatched_right if i != right_item
        ]
        self._refresh_status()
        self.updated_at = datetime.now(UTC)

    def submit_for_approval(self, *, actor_id: str) -> None:
        self.approval_status = ReconciliationStatus.PENDING_APPROVAL.value
        self.status = ReconciliationStatus.PENDING_APPROVAL.value
        self.submitted_by = actor_id
        self.updated_at = datetime.now(UTC)

    def approve(self, *, actor_id: str) -> None:
        self.approval_status = ReconciliationStatus.APPROVED.value
        self.status = ReconciliationStatus.APPROVED.value
        self.approved_by = actor_id
        self.approved_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def reject(self, *, actor_id: str, reason: str = "") -> None:
        self.approval_status = ReconciliationStatus.REJECTED.value
        self.status = ReconciliationStatus.REJECTED.value
        self.approved_by = actor_id
        self.rejection_reason = reason
        self.updated_at = datetime.now(UTC)

    def _refresh_status(self) -> None:
        if not self.unmatched_left and not self.unmatched_right and abs(self.variance) < 0.01:
            self.status = ReconciliationStatus.MATCHED.value
        elif self.matched_pairs:
            self.status = ReconciliationStatus.PARTIAL_MATCH.value
        else:
            self.status = ReconciliationStatus.EXCEPTION.value
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "reconciliation_type": self.reconciliation_type,
            "reference_id": self.reference_id,
            "reference_label": self.reference_label,
            "reconciliation_date": self.reconciliation_date,
            "period_id": self.period_id,
            "left_label": self.left_label,
            "right_label": self.right_label,
            "left_items": self.left_items,
            "right_items": self.right_items,
            "matched_pairs": self.matched_pairs,
            "unmatched_left": self.unmatched_left,
            "unmatched_right": self.unmatched_right,
            "left_total": self.left_total,
            "right_total": self.right_total,
            "variance": self.variance,
            "status": self.status,
            "difference_analysis": self.difference_analysis,
            "ai_suggestions": self.ai_suggestions,
            "exceptions": self.exceptions,
            "report_summary": self.report_summary,
            "approval_status": self.approval_status,
            "submitted_by": self.submitted_by,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "rejection_reason": self.rejection_reason,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class ReconciliationAuditLog(AggregateRoot):
    tenant_id: str
    reconciliation_id: str
    action: str
    actor_id: str
    before_state: dict | None
    after_state: dict | None
    notes: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        reconciliation_id: str,
        action: str,
        actor_id: str,
        before_state: dict | None = None,
        after_state: dict | None = None,
        notes: str = "",
    ) -> ReconciliationAuditLog:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            reconciliation_id=reconciliation_id,
            action=action,
            actor_id=actor_id,
            before_state=before_state,
            after_state=after_state,
            notes=notes,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "reconciliation_id": self.reconciliation_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "before_state": self.before_state,
            "after_state": self.after_state,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
        }
