"""Enterprise Loan Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class LoanType(StrEnum):
    PERSONAL = "personal"
    BUSINESS = "business"
    EDUCATION = "education"
    CONSTRUCTION = "construction"
    MORTGAGE = "mortgage"
    MICROFINANCE = "microfinance"
    AGRICULTURE = "agriculture"


class LoanStatus(StrEnum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    DISBURSED = "disbursed"
    ACTIVE = "active"
    RESTRUCTURED = "restructured"
    SETTLED = "settled"
    CLOSED = "closed"
    REJECTED = "rejected"


class InstallmentStatus(StrEnum):
    SCHEDULED = "scheduled"
    DUE = "due"
    PAID = "paid"
    OVERDUE = "overdue"
    WAIVED = "waived"


class LoanTransactionType(StrEnum):
    DISBURSEMENT = "disbursement"
    REPAYMENT = "repayment"
    PENALTY = "penalty"
    SETTLEMENT = "settlement"
    EARLY_CLOSURE = "early_closure"


class TransactionStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    POSTED = "posted"
    REJECTED = "rejected"


class CollateralStatus(StrEnum):
    PENDING = "pending"
    VERIFIED = "verified"
    RELEASED = "released"


class RiskGrade(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(eq=False, kw_only=True)
class LoanProfile(AggregateRoot):
    tenant_id: str
    account_id: str
    customer_id: str
    loan_type: str
    status: str = LoanStatus.DRAFT.value
    loan_ref: str
    currency: str
    principal: float = 0.0
    outstanding_principal: float = 0.0
    interest_rate_annual: float = 0.0
    tenure_months: int = 12
    emi_amount: float = 0.0
    total_interest_paid: float = 0.0
    total_penalties_paid: float = 0.0
    gl_account_code: str | None = None
    disbursed_at: datetime | None = None
    maturity_date: datetime | None = None
    closed_at: datetime | None = None
    credit_risk_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        account_id: str,
        customer_id: str,
        loan_type: str,
        loan_ref: str,
        currency: str,
        principal: float,
        interest_rate_annual: float,
        tenure_months: int,
        emi_amount: float,
        gl_account_code: str | None = None,
    ) -> LoanProfile:
        LoanType(loan_type)
        maturity = datetime.now(UTC) + timedelta(days=tenure_months * 30)
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            account_id=account_id,
            customer_id=customer_id,
            loan_type=loan_type,
            loan_ref=loan_ref.strip().upper(),
            currency=currency,
            principal=round(principal, 2),
            outstanding_principal=0.0,
            interest_rate_annual=round(interest_rate_annual, 4),
            tenure_months=tenure_months,
            emi_amount=round(emi_amount, 2),
            gl_account_code=gl_account_code,
            maturity_date=maturity,
        )

    def submit(self) -> None:
        if self.status != LoanStatus.DRAFT.value:
            raise ValueError("not_draft")
        self.status = LoanStatus.PENDING_APPROVAL.value
        self.updated_at = datetime.now(UTC)

    def approve(self) -> None:
        if self.status != LoanStatus.PENDING_APPROVAL.value:
            raise ValueError("not_pending_approval")
        self.status = LoanStatus.APPROVED.value
        self.updated_at = datetime.now(UTC)

    def reject(self) -> None:
        if self.status not in {LoanStatus.PENDING_APPROVAL.value, LoanStatus.DRAFT.value}:
            raise ValueError("cannot_reject")
        self.status = LoanStatus.REJECTED.value
        self.updated_at = datetime.now(UTC)

    def disburse(self, amount: float) -> None:
        if self.status != LoanStatus.APPROVED.value:
            raise ValueError("not_approved")
        self.status = LoanStatus.DISBURSED.value
        self.outstanding_principal = round(amount, 2)
        self.disbursed_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def activate(self) -> None:
        if self.status != LoanStatus.DISBURSED.value:
            raise ValueError("not_disbursed")
        self.status = LoanStatus.ACTIVE.value
        self.updated_at = datetime.now(UTC)

    def apply_repayment(self, principal_part: float, interest_part: float, penalty: float = 0.0) -> None:
        self.outstanding_principal = round(max(0, self.outstanding_principal - principal_part), 2)
        self.total_interest_paid = round(self.total_interest_paid + interest_part, 2)
        self.total_penalties_paid = round(self.total_penalties_paid + penalty, 2)
        if self.outstanding_principal <= 0:
            self.status = LoanStatus.CLOSED.value
            self.closed_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def restructure(self, *, tenure_months: int, interest_rate_annual: float, emi_amount: float) -> None:
        if self.status not in {LoanStatus.ACTIVE.value, LoanStatus.RESTRUCTURED.value}:
            raise ValueError("cannot_restructure")
        self.status = LoanStatus.RESTRUCTURED.value
        self.tenure_months = tenure_months
        self.interest_rate_annual = interest_rate_annual
        self.emi_amount = emi_amount
        self.maturity_date = datetime.now(UTC) + timedelta(days=tenure_months * 30)
        self.status = LoanStatus.ACTIVE.value
        self.updated_at = datetime.now(UTC)

    def settle(self, settlement_amount: float) -> None:
        if self.status not in {LoanStatus.ACTIVE.value, LoanStatus.RESTRUCTURED.value}:
            raise ValueError("cannot_settle")
        self.outstanding_principal = 0.0
        self.status = LoanStatus.SETTLED.value
        self.closed_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def early_close(self) -> None:
        if self.status not in {LoanStatus.ACTIVE.value, LoanStatus.RESTRUCTURED.value}:
            raise ValueError("cannot_close")
        self.outstanding_principal = 0.0
        self.status = LoanStatus.CLOSED.value
        self.closed_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "account_id": self.account_id,
            "customer_id": self.customer_id,
            "loan_type": self.loan_type,
            "status": self.status,
            "loan_ref": self.loan_ref,
            "currency": self.currency,
            "principal": self.principal,
            "outstanding_principal": self.outstanding_principal,
            "interest_rate_annual": self.interest_rate_annual,
            "tenure_months": self.tenure_months,
            "emi_amount": self.emi_amount,
            "total_interest_paid": self.total_interest_paid,
            "total_penalties_paid": self.total_penalties_paid,
            "gl_account_code": self.gl_account_code,
            "disbursed_at": self.disbursed_at.isoformat() if self.disbursed_at else None,
            "maturity_date": self.maturity_date.isoformat() if self.maturity_date else None,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
            "credit_risk_id": self.credit_risk_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class LoanCollateral(AggregateRoot):
    tenant_id: str
    loan_id: str
    collateral_type: str
    description: str
    estimated_value: float
    currency: str
    status: str = CollateralStatus.PENDING.value
    lien_ref: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        loan_id: str,
        collateral_type: str,
        description: str,
        estimated_value: float,
        currency: str,
    ) -> LoanCollateral:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            loan_id=loan_id,
            collateral_type=collateral_type,
            description=description.strip(),
            estimated_value=round(estimated_value, 2),
            currency=currency,
        )

    def verify(self) -> None:
        self.status = CollateralStatus.VERIFIED.value

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "loan_id": self.loan_id,
            "collateral_type": self.collateral_type,
            "description": self.description,
            "estimated_value": self.estimated_value,
            "currency": self.currency,
            "status": self.status,
            "lien_ref": self.lien_ref,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class LoanGuarantor(AggregateRoot):
    tenant_id: str
    loan_id: str
    guarantor_name: str
    guarantor_id_ref: str
    relationship: str = ""
    guaranteed_amount: float = 0.0
    currency: str = "USD"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        loan_id: str,
        guarantor_name: str,
        guarantor_id_ref: str,
        relationship: str = "",
        guaranteed_amount: float = 0.0,
        currency: str = "USD",
    ) -> LoanGuarantor:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            loan_id=loan_id,
            guarantor_name=guarantor_name.strip(),
            guarantor_id_ref=guarantor_id_ref.strip(),
            relationship=relationship,
            guaranteed_amount=round(guaranteed_amount, 2),
            currency=currency,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "loan_id": self.loan_id,
            "guarantor_name": self.guarantor_name,
            "guarantor_id_ref": self.guarantor_id_ref,
            "relationship": self.relationship,
            "guaranteed_amount": self.guaranteed_amount,
            "currency": self.currency,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class LoanInstallment(AggregateRoot):
    tenant_id: str
    loan_id: str
    installment_number: int
    due_date: datetime
    principal_due: float
    interest_due: float
    total_due: float
    status: str = InstallmentStatus.SCHEDULED.value
    paid_at: datetime | None = None
    penalty_amount: float = 0.0

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        loan_id: str,
        installment_number: int,
        due_date: datetime,
        principal_due: float,
        interest_due: float,
    ) -> LoanInstallment:
        total = round(principal_due + interest_due, 2)
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            loan_id=loan_id,
            installment_number=installment_number,
            due_date=due_date,
            principal_due=round(principal_due, 2),
            interest_due=round(interest_due, 2),
            total_due=total,
        )

    def mark_paid(self, *, penalty: float = 0.0) -> None:
        self.status = InstallmentStatus.PAID.value
        self.penalty_amount = round(penalty, 2)
        self.paid_at = datetime.now(UTC)

    def mark_overdue(self) -> None:
        if self.status == InstallmentStatus.SCHEDULED.value:
            self.status = InstallmentStatus.OVERDUE.value

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "loan_id": self.loan_id,
            "installment_number": self.installment_number,
            "due_date": self.due_date.isoformat(),
            "principal_due": self.principal_due,
            "interest_due": self.interest_due,
            "total_due": self.total_due,
            "status": self.status,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "penalty_amount": self.penalty_amount,
        }


@dataclass(eq=False, kw_only=True)
class LoanTransaction(AggregateRoot):
    tenant_id: str
    loan_id: str
    account_id: str
    transaction_ref: str
    transaction_type: str
    amount: float
    principal_part: float = 0.0
    interest_part: float = 0.0
    penalty_amount: float = 0.0
    currency: str
    status: str = TransactionStatus.PENDING.value
    kernel_journal_id: str | None = None
    approved_by: str | None = None
    posted_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        loan_id: str,
        account_id: str,
        transaction_ref: str,
        transaction_type: str,
        amount: float,
        currency: str,
        principal_part: float = 0.0,
        interest_part: float = 0.0,
        penalty_amount: float = 0.0,
        auto_approve: bool = False,
    ) -> LoanTransaction:
        status = TransactionStatus.APPROVED.value if auto_approve else TransactionStatus.PENDING.value
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            loan_id=loan_id,
            account_id=account_id,
            transaction_ref=transaction_ref.strip().upper(),
            transaction_type=transaction_type,
            amount=round(amount, 2),
            principal_part=round(principal_part, 2),
            interest_part=round(interest_part, 2),
            penalty_amount=round(penalty_amount, 2),
            currency=currency,
            status=status,
        )

    def approve(self, *, approved_by: str) -> None:
        if self.status == TransactionStatus.PENDING.value:
            self.status = TransactionStatus.APPROVED.value
            self.approved_by = approved_by

    def mark_posted(self, *, journal_id: str | None = None) -> None:
        self.status = TransactionStatus.POSTED.value
        self.kernel_journal_id = journal_id
        self.posted_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "loan_id": self.loan_id,
            "account_id": self.account_id,
            "transaction_ref": self.transaction_ref,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "principal_part": self.principal_part,
            "interest_part": self.interest_part,
            "penalty_amount": self.penalty_amount,
            "currency": self.currency,
            "status": self.status,
            "kernel_journal_id": self.kernel_journal_id,
            "approved_by": self.approved_by,
            "posted_at": self.posted_at.isoformat() if self.posted_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class LoanCreditRiskAnalysis(AggregateRoot):
    tenant_id: str
    loan_id: str
    risk_score: float
    risk_grade: str
    recommendation: str
    factors: list[dict] = field(default_factory=list)
    dti_ratio: float = 0.0
    collateral_coverage_pct: float = 0.0
    ai_provider_ref: str | None = None
    analyzed_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        loan_id: str,
        risk_score: float,
        risk_grade: str,
        recommendation: str,
        factors: list[dict],
        dti_ratio: float = 0.0,
        collateral_coverage_pct: float = 0.0,
        ai_provider_ref: str | None = None,
    ) -> LoanCreditRiskAnalysis:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            loan_id=loan_id,
            risk_score=round(risk_score, 2),
            risk_grade=risk_grade,
            recommendation=recommendation,
            factors=factors,
            dti_ratio=round(dti_ratio, 4),
            collateral_coverage_pct=round(collateral_coverage_pct, 2),
            ai_provider_ref=ai_provider_ref,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "loan_id": self.loan_id,
            "risk_score": self.risk_score,
            "risk_grade": self.risk_grade,
            "recommendation": self.recommendation,
            "factors": self.factors,
            "dti_ratio": self.dti_ratio,
            "collateral_coverage_pct": self.collateral_coverage_pct,
            "ai_provider_ref": self.ai_provider_ref,
            "analyzed_at": self.analyzed_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class LoanWorkflowRequest(AggregateRoot):
    tenant_id: str
    loan_id: str
    request_type: str
    status: str = "pending"
    required_levels: int = 1
    current_level: int = 0
    approver_ids: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        loan_id: str,
        request_type: str,
        required_levels: int = 1,
    ) -> LoanWorkflowRequest:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            loan_id=loan_id,
            request_type=request_type,
            required_levels=required_levels,
        )

    def approve(self, *, approver_id: str) -> None:
        if self.status != "pending":
            raise ValueError("not_pending")
        self.approver_ids.append(approver_id)
        self.current_level += 1
        if self.current_level >= self.required_levels:
            self.status = "approved"

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "loan_id": self.loan_id,
            "request_type": self.request_type,
            "status": self.status,
            "required_levels": self.required_levels,
            "current_level": self.current_level,
            "approver_ids": self.approver_ids,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class LoanAuditEntry(AggregateRoot):
    tenant_id: str
    loan_id: str
    action: str
    actor_id: str | None = None
    detail: str = ""
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        loan_id: str,
        action: str,
        actor_id: str | None = None,
        detail: str = "",
    ) -> LoanAuditEntry:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            loan_id=loan_id,
            action=action,
            actor_id=actor_id,
            detail=detail,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "loan_id": self.loan_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "detail": self.detail,
            "occurred_at": self.occurred_at.isoformat(),
        }
