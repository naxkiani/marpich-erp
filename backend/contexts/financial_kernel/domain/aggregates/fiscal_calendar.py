"""Enterprise fiscal calendar — multiple calendars, close levels, audit."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class PeriodStatus(StrEnum):
    OPEN = "open"
    SOFT_CLOSED = "soft_closed"
    HARD_CLOSED = "hard_closed"
    CLOSED = "closed"  # legacy alias for hard_closed


class PeriodType(StrEnum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    ADJUSTMENT = "adjustment"


class CloseLevel(StrEnum):
    NONE = "none"
    MONTHLY = "monthly"
    QUARTER = "quarter"
    YEAR = "year"
    ADJUSTMENT = "adjustment"


class CloseActionType(StrEnum):
    SOFT_CLOSE = "soft_close"
    HARD_CLOSE = "hard_close"
    MONTHLY_CLOSE = "monthly_close"
    QUARTER_CLOSE = "quarter_close"
    YEAR_CLOSE = "year_close"
    REOPEN = "reopen"


class CloseRequestStatus(StrEnum):
    PENDING = "pending"
    FIRST_APPROVED = "first_approved"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass(eq=False, kw_only=True)
class FiscalCalendar(AggregateRoot):
    tenant_id: str
    organization_id: str | None
    name: str
    description: str = ""
    fiscal_year_start_month: int = 1
    is_default: bool = False
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        organization_id: str | None,
        name: str,
        description: str = "",
        fiscal_year_start_month: int = 1,
        is_default: bool = False,
    ) -> FiscalCalendar:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            organization_id=organization_id,
            name=name.strip(),
            description=description,
            fiscal_year_start_month=fiscal_year_start_month,
            is_default=is_default,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "organization_id": self.organization_id,
            "name": self.name,
            "description": self.description,
            "fiscal_year_start_month": self.fiscal_year_start_month,
            "is_default": self.is_default,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class FiscalCalendarAuditLog(AggregateRoot):
    tenant_id: str
    calendar_id: str | None
    period_id: str | None
    fiscal_year_id: str | None
    action: str
    actor_id: str
    before_state: dict | None
    after_state: dict | None
    correlation_id: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        action: str,
        actor_id: str,
        calendar_id: str | None = None,
        period_id: str | None = None,
        fiscal_year_id: str | None = None,
        before_state: dict | None = None,
        after_state: dict | None = None,
        correlation_id: str = "",
    ) -> FiscalCalendarAuditLog:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            calendar_id=calendar_id,
            period_id=period_id,
            fiscal_year_id=fiscal_year_id,
            action=action,
            actor_id=actor_id,
            before_state=before_state,
            after_state=after_state,
            correlation_id=correlation_id,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "calendar_id": self.calendar_id,
            "period_id": self.period_id,
            "fiscal_year_id": self.fiscal_year_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "before_state": self.before_state,
            "after_state": self.after_state,
            "correlation_id": self.correlation_id,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class FiscalCloseRequest(AggregateRoot):
    tenant_id: str
    period_id: str | None
    fiscal_year_id: str | None
    calendar_id: str | None
    action_type: str
    close_level: str
    requester_id: str
    status: str = CloseRequestStatus.PENDING.value
    first_approver_id: str | None = None
    second_approver_id: str | None = None
    reason: str = ""
    correlation_id: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    resolved_at: datetime | None = None

    @classmethod
    def request(
        cls,
        *,
        tenant_id: str,
        action_type: str,
        close_level: str,
        requester_id: str,
        period_id: str | None = None,
        fiscal_year_id: str | None = None,
        calendar_id: str | None = None,
        reason: str = "",
        correlation_id: str = "",
    ) -> FiscalCloseRequest:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            period_id=period_id,
            fiscal_year_id=fiscal_year_id,
            calendar_id=calendar_id,
            action_type=action_type,
            close_level=close_level,
            requester_id=requester_id,
            reason=reason,
            correlation_id=correlation_id,
        )

    def approve(self, approver_id: str) -> None:
        if self.status == CloseRequestStatus.APPROVED.value:
            raise ValueError("already_approved")
        if self.status == CloseRequestStatus.REJECTED.value:
            raise ValueError("already_rejected")
        if self.requester_id == approver_id:
            raise ValueError("self_approval_forbidden")
        if self.first_approver_id == approver_id:
            raise ValueError("duplicate_approver")
        if not self.first_approver_id:
            self.first_approver_id = approver_id
            self.status = CloseRequestStatus.FIRST_APPROVED.value
            return
        if self.second_approver_id:
            raise ValueError("already_fully_approved")
        self.second_approver_id = approver_id
        self.status = CloseRequestStatus.APPROVED.value
        self.resolved_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "period_id": self.period_id,
            "fiscal_year_id": self.fiscal_year_id,
            "calendar_id": self.calendar_id,
            "action_type": self.action_type,
            "close_level": self.close_level,
            "requester_id": self.requester_id,
            "status": self.status,
            "first_approver_id": self.first_approver_id,
            "second_approver_id": self.second_approver_id,
            "reason": self.reason,
            "correlation_id": self.correlation_id,
            "approval_required": True,
            "created_at": self.created_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
        }


# Configurable close rules — tenant policy may override
FISCAL_CLOSE_RULES: dict[str, dict] = {
    CloseActionType.SOFT_CLOSE.value: {
        "target_status": PeriodStatus.SOFT_CLOSED.value,
        "blocks_new_posting": True,
        "allows_adjustments": True,
        "approval_required": True,
        "financial_lock": True,
    },
    CloseActionType.HARD_CLOSE.value: {
        "target_status": PeriodStatus.HARD_CLOSED.value,
        "blocks_new_posting": True,
        "allows_adjustments": False,
        "approval_required": True,
        "financial_lock": True,
    },
    CloseActionType.MONTHLY_CLOSE.value: {
        "target_status": PeriodStatus.SOFT_CLOSED.value,
        "close_level": CloseLevel.MONTHLY.value,
        "blocks_new_posting": True,
        "allows_adjustments": True,
        "approval_required": True,
        "financial_lock": True,
    },
    CloseActionType.QUARTER_CLOSE.value: {
        "target_status": PeriodStatus.SOFT_CLOSED.value,
        "close_level": CloseLevel.QUARTER.value,
        "blocks_new_posting": True,
        "allows_adjustments": True,
        "approval_required": True,
        "financial_lock": True,
    },
    CloseActionType.YEAR_CLOSE.value: {
        "target_status": PeriodStatus.HARD_CLOSED.value,
        "close_level": CloseLevel.YEAR.value,
        "blocks_new_posting": True,
        "allows_adjustments": False,
        "approval_required": True,
        "financial_lock": True,
    },
    CloseActionType.REOPEN.value: {
        "target_status": PeriodStatus.OPEN.value,
        "blocks_new_posting": False,
        "allows_adjustments": True,
        "approval_required": True,
        "financial_lock": False,
    },
}
