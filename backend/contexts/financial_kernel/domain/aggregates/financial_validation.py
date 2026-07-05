"""Enterprise financial validation aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class ValidationCheckType(StrEnum):
    BALANCED_JOURNALS = "balanced_journals"
    POSTING_PERMISSIONS = "posting_permissions"
    FISCAL_PERIOD = "fiscal_period"
    CURRENCY = "currency"
    TAX = "tax"
    BUDGET = "budget"
    ACCOUNT_STATUS = "account_status"
    DUPLICATE_POSTING = "duplicate_posting"
    APPROVAL_STATUS = "approval_status"
    DIMENSION_RULES = "dimension_rules"
    BUSINESS_RULES = "business_rules"


class ValidationOutcome(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"


@dataclass(eq=False, kw_only=True)
class ValidationRun(AggregateRoot):
    tenant_id: str
    source_context: str
    source_document_id: str
    idempotency_key: str | None
    outcome: str
    can_post: bool
    report: dict
    lines: list[dict]
    actor_id: str | None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        source_context: str,
        source_document_id: str,
        report: dict,
        lines: list[dict],
        idempotency_key: str | None = None,
        actor_id: str | None = None,
    ) -> ValidationRun:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            source_context=source_context,
            source_document_id=source_document_id,
            idempotency_key=idempotency_key,
            outcome=(
                ValidationOutcome.PASSED.value
                if report.get("valid")
                else ValidationOutcome.FAILED.value
            ),
            can_post=bool(report.get("can_post")),
            report=report,
            lines=lines,
            actor_id=actor_id,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "source_context": self.source_context,
            "source_document_id": self.source_document_id,
            "idempotency_key": self.idempotency_key,
            "outcome": self.outcome,
            "can_post": self.can_post,
            "report": self.report,
            "lines": self.lines,
            "actor_id": self.actor_id,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class ValidationAuditLog(AggregateRoot):
    tenant_id: str
    validation_run_id: str
    action: str
    actor_id: str
    report_summary: dict
    notes: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        validation_run_id: str,
        action: str,
        actor_id: str,
        report_summary: dict,
        notes: str = "",
    ) -> ValidationAuditLog:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            validation_run_id=validation_run_id,
            action=action,
            actor_id=actor_id,
            report_summary=report_summary,
            notes=notes,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "validation_run_id": self.validation_run_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "report_summary": self.report_summary,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
        }
