"""Deposit Management aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class DepositType(StrEnum):
    SAVINGS = "savings"
    CURRENT = "current"
    TERM = "term"
    RECURRING = "recurring"


class DepositStatus(StrEnum):
    PENDING_APPROVAL = "pending_approval"
    ACTIVE = "active"
    MATURED = "matured"
    RENEWED = "renewed"
    CLOSED = "closed"


class TransactionType(StrEnum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    INTEREST_CREDIT = "interest_credit"
    MATURITY_PAYOUT = "maturity_payout"
    PROFIT_DISTRIBUTION = "profit_distribution"


class TransactionStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    POSTED = "posted"


class AccrualStatus(StrEnum):
    ACCRUED = "accrued"
    POSTED = "posted"
    REVERSED = "reversed"


class WorkflowStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class DistributionMethod(StrEnum):
    INTEREST = "interest"
    PROFIT_SHARING = "profit_sharing"


@dataclass(eq=False, kw_only=True)
class ProfitDistributionRule(AggregateRoot):
    tenant_id: str
    rule_code: str
    name: str
    deposit_type: str
    method: str
    rate_annual: float = 0.0
    profit_share_pct: float = 0.0
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        rule_code: str,
        name: str,
        deposit_type: str,
        method: str = DistributionMethod.INTEREST.value,
        rate_annual: float = 0.0,
        profit_share_pct: float = 0.0,
    ) -> ProfitDistributionRule:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            rule_code=rule_code.strip().upper(),
            name=name.strip(),
            deposit_type=deposit_type,
            method=method,
            rate_annual=round(rate_annual, 4),
            profit_share_pct=round(profit_share_pct, 4),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "rule_code": self.rule_code,
            "name": self.name,
            "deposit_type": self.deposit_type,
            "method": self.method,
            "rate_annual": self.rate_annual,
            "profit_share_pct": self.profit_share_pct,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class DepositProfile(AggregateRoot):
    tenant_id: str
    account_id: str
    customer_id: str
    deposit_type: str
    status: str = DepositStatus.PENDING_APPROVAL.value
    currency: str
    principal: float = 0.0
    interest_rate_annual: float = 0.0
    profit_rule_id: str | None = None
    tenure_months: int | None = None
    maturity_date: datetime | None = None
    auto_renew: bool = False
    recurring_amount: float = 0.0
    recurring_day: int = 1
    accrued_interest: float = 0.0
    total_interest_paid: float = 0.0
    gl_account_code: str | None = None
    opened_at: datetime | None = None
    closed_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        account_id: str,
        customer_id: str,
        deposit_type: str,
        currency: str,
        principal: float = 0.0,
        interest_rate_annual: float = 0.0,
        profit_rule_id: str | None = None,
        tenure_months: int | None = None,
        auto_renew: bool = False,
        recurring_amount: float = 0.0,
        recurring_day: int = 1,
        gl_account_code: str | None = None,
        requires_approval: bool = True,
    ) -> DepositProfile:
        DepositType(deposit_type)
        maturity = None
        if deposit_type == DepositType.TERM.value and tenure_months:
            maturity = datetime.now(UTC) + timedelta(days=tenure_months * 30)
        status = (
            DepositStatus.PENDING_APPROVAL.value
            if requires_approval
            else DepositStatus.ACTIVE.value
        )
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            account_id=account_id,
            customer_id=customer_id,
            deposit_type=deposit_type,
            status=status,
            currency=currency,
            principal=round(principal, 2),
            interest_rate_annual=interest_rate_annual,
            profit_rule_id=profit_rule_id,
            tenure_months=tenure_months,
            maturity_date=maturity,
            auto_renew=auto_renew,
            recurring_amount=round(recurring_amount, 2),
            recurring_day=recurring_day,
            gl_account_code=gl_account_code,
            opened_at=None if requires_approval else datetime.now(UTC),
        )

    def approve_opening(self) -> None:
        if self.status != DepositStatus.PENDING_APPROVAL.value:
            raise ValueError("not_pending_approval")
        self.status = DepositStatus.ACTIVE.value
        self.opened_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def mark_matured(self) -> None:
        if self.deposit_type != DepositType.TERM.value:
            raise ValueError("not_term_deposit")
        self.status = DepositStatus.MATURED.value
        self.updated_at = datetime.now(UTC)

    def renew(self, *, tenure_months: int, interest_rate_annual: float | None = None) -> None:
        if self.status not in {DepositStatus.MATURED.value, DepositStatus.ACTIVE.value}:
            raise ValueError("cannot_renew")
        self.status = DepositStatus.RENEWED.value
        self.tenure_months = tenure_months
        self.maturity_date = datetime.now(UTC) + timedelta(days=tenure_months * 30)
        if interest_rate_annual is not None:
            self.interest_rate_annual = interest_rate_annual
        self.status = DepositStatus.ACTIVE.value
        self.updated_at = datetime.now(UTC)

    def add_accrual(self, amount: float) -> None:
        self.accrued_interest = round(self.accrued_interest + amount, 2)
        self.updated_at = datetime.now(UTC)

    def post_interest(self, amount: float) -> None:
        self.accrued_interest = round(max(0, self.accrued_interest - amount), 2)
        self.total_interest_paid = round(self.total_interest_paid + amount, 2)
        self.principal = round(self.principal + amount, 2)
        self.updated_at = datetime.now(UTC)

    def close(self) -> None:
        self.status = DepositStatus.CLOSED.value
        self.closed_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "account_id": self.account_id,
            "customer_id": self.customer_id,
            "deposit_type": self.deposit_type,
            "status": self.status,
            "currency": self.currency,
            "principal": self.principal,
            "interest_rate_annual": self.interest_rate_annual,
            "profit_rule_id": self.profit_rule_id,
            "tenure_months": self.tenure_months,
            "maturity_date": self.maturity_date.isoformat() if self.maturity_date else None,
            "auto_renew": self.auto_renew,
            "recurring_amount": self.recurring_amount,
            "recurring_day": self.recurring_day,
            "accrued_interest": self.accrued_interest,
            "total_interest_paid": self.total_interest_paid,
            "gl_account_code": self.gl_account_code,
            "opened_at": self.opened_at.isoformat() if self.opened_at else None,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class DepositTransaction(AggregateRoot):
    tenant_id: str
    deposit_id: str
    account_id: str
    transaction_ref: str
    transaction_type: str
    amount: float
    currency: str
    status: str = TransactionStatus.PENDING.value
    penalty_amount: float = 0.0
    net_amount: float = 0.0
    kernel_journal_id: str | None = None
    approved_by: str | None = None
    posted_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        deposit_id: str,
        account_id: str,
        transaction_ref: str,
        transaction_type: str,
        amount: float,
        currency: str,
        penalty_amount: float = 0.0,
        auto_approve: bool = False,
    ) -> DepositTransaction:
        net = round(amount - penalty_amount, 2) if transaction_type == TransactionType.WITHDRAWAL.value else round(amount, 2)
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            deposit_id=deposit_id,
            account_id=account_id,
            transaction_ref=transaction_ref.strip().upper(),
            transaction_type=transaction_type,
            amount=round(amount, 2),
            currency=currency,
            penalty_amount=round(penalty_amount, 2),
            net_amount=net,
            status=TransactionStatus.APPROVED.value if auto_approve else TransactionStatus.PENDING.value,
        )

    def approve(self, *, approved_by: str) -> None:
        if self.status != TransactionStatus.PENDING.value:
            raise ValueError("not_pending")
        self.status = TransactionStatus.APPROVED.value
        self.approved_by = approved_by

    def reject(self) -> None:
        if self.status != TransactionStatus.PENDING.value:
            raise ValueError("not_pending")
        self.status = TransactionStatus.REJECTED.value

    def mark_posted(self, *, journal_id: str | None = None) -> None:
        self.status = TransactionStatus.POSTED.value
        self.kernel_journal_id = journal_id
        self.posted_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "deposit_id": self.deposit_id,
            "account_id": self.account_id,
            "transaction_ref": self.transaction_ref,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "currency": self.currency,
            "status": self.status,
            "penalty_amount": self.penalty_amount,
            "net_amount": self.net_amount,
            "kernel_journal_id": self.kernel_journal_id,
            "approved_by": self.approved_by,
            "posted_at": self.posted_at.isoformat() if self.posted_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class DepositInterestAccrual(AggregateRoot):
    tenant_id: str
    deposit_id: str
    accrual_ref: str
    period_start: datetime
    period_end: datetime
    principal_base: float
    rate_annual: float
    accrued_amount: float
    status: str = AccrualStatus.ACCRUED.value
    kernel_journal_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        deposit_id: str,
        accrual_ref: str,
        period_start: datetime,
        period_end: datetime,
        principal_base: float,
        rate_annual: float,
        accrued_amount: float,
    ) -> DepositInterestAccrual:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            deposit_id=deposit_id,
            accrual_ref=accrual_ref.strip().upper(),
            period_start=period_start,
            period_end=period_end,
            principal_base=round(principal_base, 2),
            rate_annual=round(rate_annual, 4),
            accrued_amount=round(accrued_amount, 2),
        )

    def mark_posted(self, journal_id: str | None = None) -> None:
        self.status = AccrualStatus.POSTED.value
        self.kernel_journal_id = journal_id

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "deposit_id": self.deposit_id,
            "accrual_ref": self.accrual_ref,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "principal_base": self.principal_base,
            "rate_annual": self.rate_annual,
            "accrued_amount": self.accrued_amount,
            "status": self.status,
            "kernel_journal_id": self.kernel_journal_id,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class DepositCertificate(AggregateRoot):
    tenant_id: str
    deposit_id: str
    certificate_number: str
    issue_date: datetime
    maturity_date: datetime | None
    principal: float
    rate_annual: float
    currency: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        deposit_id: str,
        certificate_number: str,
        issue_date: datetime,
        maturity_date: datetime | None,
        principal: float,
        rate_annual: float,
        currency: str,
    ) -> DepositCertificate:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            deposit_id=deposit_id,
            certificate_number=certificate_number.strip().upper(),
            issue_date=issue_date,
            maturity_date=maturity_date,
            principal=round(principal, 2),
            rate_annual=round(rate_annual, 4),
            currency=currency,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "deposit_id": self.deposit_id,
            "certificate_number": self.certificate_number,
            "issue_date": self.issue_date.isoformat(),
            "maturity_date": self.maturity_date.isoformat() if self.maturity_date else None,
            "principal": self.principal,
            "rate_annual": self.rate_annual,
            "currency": self.currency,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class DepositStatement(AggregateRoot):
    tenant_id: str
    deposit_id: str
    statement_ref: str
    period_start: datetime
    period_end: datetime
    opening_balance: float
    closing_balance: float
    total_credits: float
    total_debits: float
    interest_earned: float
    line_items: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        deposit_id: str,
        statement_ref: str,
        period_start: datetime,
        period_end: datetime,
        opening_balance: float,
        closing_balance: float,
        total_credits: float,
        total_debits: float,
        interest_earned: float,
        line_items: list[dict],
    ) -> DepositStatement:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            deposit_id=deposit_id,
            statement_ref=statement_ref.strip().upper(),
            period_start=period_start,
            period_end=period_end,
            opening_balance=round(opening_balance, 2),
            closing_balance=round(closing_balance, 2),
            total_credits=round(total_credits, 2),
            total_debits=round(total_debits, 2),
            interest_earned=round(interest_earned, 2),
            line_items=line_items,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "deposit_id": self.deposit_id,
            "statement_ref": self.statement_ref,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "opening_balance": self.opening_balance,
            "closing_balance": self.closing_balance,
            "total_credits": self.total_credits,
            "total_debits": self.total_debits,
            "interest_earned": self.interest_earned,
            "line_items": self.line_items,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class DepositWorkflowRequest(AggregateRoot):
    tenant_id: str
    deposit_id: str
    transaction_id: str | None
    request_type: str
    status: str = WorkflowStatus.PENDING.value
    required_levels: int = 1
    approved_levels: int = 0
    approver_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    resolved_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        deposit_id: str,
        request_type: str,
        transaction_id: str | None = None,
        required_levels: int = 1,
    ) -> DepositWorkflowRequest:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            deposit_id=deposit_id,
            transaction_id=transaction_id,
            request_type=request_type,
            required_levels=required_levels,
        )

    def approve(self, *, approver_id: str) -> None:
        if self.status != WorkflowStatus.PENDING.value:
            raise ValueError("not_pending")
        self.approved_levels += 1
        self.approver_id = approver_id
        if self.approved_levels >= self.required_levels:
            self.status = WorkflowStatus.APPROVED.value
            self.resolved_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "deposit_id": self.deposit_id,
            "transaction_id": self.transaction_id,
            "request_type": self.request_type,
            "status": self.status,
            "required_levels": self.required_levels,
            "approved_levels": self.approved_levels,
            "approver_id": self.approver_id,
            "created_at": self.created_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
        }


@dataclass(eq=False, kw_only=True)
class DepositAuditEntry(AggregateRoot):
    tenant_id: str
    deposit_id: str
    action: str
    actor_id: str | None
    detail: str
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        deposit_id: str,
        action: str,
        actor_id: str | None = None,
        detail: str = "",
    ) -> DepositAuditEntry:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            deposit_id=deposit_id,
            action=action,
            actor_id=actor_id,
            detail=detail,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "deposit_id": self.deposit_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "detail": self.detail,
            "occurred_at": self.occurred_at.isoformat(),
        }
