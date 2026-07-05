"""Banking Customer and Account aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class CustomerType(StrEnum):
    INDIVIDUAL = "individual"
    BUSINESS = "business"
    GOVERNMENT = "government"
    NGO = "ngo"


class KycStatus(StrEnum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"


class RiskRating(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AccountType(StrEnum):
    JOINT = "joint"
    SAVINGS = "savings"
    CURRENT = "current"
    FIXED_DEPOSIT = "fixed_deposit"
    LOAN = "loan"
    VIRTUAL = "virtual"


class AccountStatus(StrEnum):
    PENDING_APPROVAL = "pending_approval"
    ACTIVE = "active"
    DORMANT = "dormant"
    BLOCKED = "blocked"
    FROZEN = "frozen"
    CLOSED = "closed"


class ApprovalStatus(StrEnum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


DEFAULT_GL_MAP: dict[str, str] = {
    AccountType.SAVINGS.value: "customer_deposits",
    AccountType.CURRENT.value: "customer_deposits",
    AccountType.JOINT.value: "customer_deposits",
    AccountType.FIXED_DEPOSIT.value: "customer_deposits",
    AccountType.VIRTUAL.value: "customer_deposits",
    AccountType.LOAN.value: "loans_receivable",
}


@dataclass(eq=False, kw_only=True)
class BankingCustomer(AggregateRoot):
    tenant_id: str
    customer_type: str
    display_name: str
    legal_name: str
    email: str
    phone: str
    organization_id: str | None = None
    branch_id: str | None = None
    kyc_status: str = KycStatus.PENDING.value
    risk_rating: str = RiskRating.LOW.value
    approval_status: str = ApprovalStatus.DRAFT.value
    registration_number: str | None = None
    tax_id: str | None = None
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        customer_type: str,
        display_name: str,
        legal_name: str,
        email: str,
        phone: str,
        organization_id: str | None = None,
        branch_id: str | None = None,
        registration_number: str | None = None,
        tax_id: str | None = None,
    ) -> BankingCustomer:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            customer_type=customer_type,
            display_name=display_name.strip(),
            legal_name=legal_name.strip(),
            email=email.strip().lower(),
            phone=phone.strip(),
            organization_id=organization_id,
            branch_id=branch_id,
            registration_number=registration_number,
            tax_id=tax_id,
        )

    def submit_for_approval(self) -> None:
        if self.approval_status not in {ApprovalStatus.DRAFT.value, ApprovalStatus.REJECTED.value}:
            raise ValueError("cannot_submit_for_approval")
        self.approval_status = ApprovalStatus.PENDING.value
        self.updated_at = datetime.now(UTC)

    def approve(self) -> None:
        if self.approval_status != ApprovalStatus.PENDING.value:
            raise ValueError("not_pending_approval")
        self.approval_status = ApprovalStatus.APPROVED.value
        self.updated_at = datetime.now(UTC)

    def reject(self) -> None:
        if self.approval_status != ApprovalStatus.PENDING.value:
            raise ValueError("not_pending_approval")
        self.approval_status = ApprovalStatus.REJECTED.value
        self.updated_at = datetime.now(UTC)

    def update_kyc_status(self, status: str) -> None:
        KycStatus(status)
        self.kyc_status = status
        self.updated_at = datetime.now(UTC)

    def update_risk_rating(self, rating: str) -> None:
        RiskRating(rating)
        self.risk_rating = rating
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "customer_type": self.customer_type,
            "display_name": self.display_name,
            "legal_name": self.legal_name,
            "email": self.email,
            "phone": self.phone,
            "organization_id": self.organization_id,
            "branch_id": self.branch_id,
            "kyc_status": self.kyc_status,
            "risk_rating": self.risk_rating,
            "approval_status": self.approval_status,
            "registration_number": self.registration_number,
            "tax_id": self.tax_id,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class BankingCustomerKYC(AggregateRoot):
    tenant_id: str
    customer_id: str
    tier: str
    document_type: str
    document_ref: str
    status: str = KycStatus.PENDING.value
    verified_at: datetime | None = None
    verified_by: str | None = None
    notes: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        customer_id: str,
        tier: str,
        document_type: str,
        document_ref: str,
        notes: str = "",
    ) -> BankingCustomerKYC:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            customer_id=customer_id,
            tier=tier,
            document_type=document_type,
            document_ref=document_ref,
            notes=notes,
        )

    def verify(self, *, verified_by: str) -> None:
        self.status = KycStatus.VERIFIED.value
        self.verified_at = datetime.now(UTC)
        self.verified_by = verified_by

    def reject(self, *, reason: str = "") -> None:
        self.status = KycStatus.REJECTED.value
        self.notes = reason

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "customer_id": self.customer_id,
            "tier": self.tier,
            "document_type": self.document_type,
            "document_ref": self.document_ref,
            "status": self.status,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None,
            "verified_by": self.verified_by,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class BankingAccountProduct(AggregateRoot):
    tenant_id: str
    product_code: str
    name: str
    account_type: str
    currency: str
    interest_rate_annual: float = 0.0
    minimum_balance: float = 0.0
    overdraft_limit: float = 0.0
    overdraft_enabled: bool = False
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        product_code: str,
        name: str,
        account_type: str,
        currency: str = "USD",
        interest_rate_annual: float = 0.0,
        minimum_balance: float = 0.0,
        overdraft_limit: float = 0.0,
        overdraft_enabled: bool = False,
    ) -> BankingAccountProduct:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            product_code=product_code.strip().upper(),
            name=name.strip(),
            account_type=account_type,
            currency=currency.strip().upper(),
            interest_rate_annual=round(interest_rate_annual, 4),
            minimum_balance=round(minimum_balance, 2),
            overdraft_limit=round(overdraft_limit, 2),
            overdraft_enabled=overdraft_enabled,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "product_code": self.product_code,
            "name": self.name,
            "account_type": self.account_type,
            "currency": self.currency,
            "interest_rate_annual": self.interest_rate_annual,
            "minimum_balance": self.minimum_balance,
            "overdraft_limit": self.overdraft_limit,
            "overdraft_enabled": self.overdraft_enabled,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class BankingAccount(AggregateRoot):
    tenant_id: str
    customer_id: str
    account_number: str
    account_type: str
    product_code: str
    currency: str
    status: str
    balance: float = 0.0
    available_balance: float = 0.0
    organization_id: str | None = None
    branch_id: str | None = None
    is_joint: bool = False
    joint_holders: list[str] = field(default_factory=list)
    interest_rate_annual: float = 0.0
    minimum_balance: float = 0.0
    overdraft_limit: float = 0.0
    overdraft_enabled: bool = False
    approval_status: str = ApprovalStatus.DRAFT.value
    gl_account_code: str | None = None
    kernel_account_key: str | None = None
    kernel_linked: bool = False
    kernel_journal_id: str | None = None
    kernel_subledger_ref: str | None = None
    parent_account_id: str | None = None
    opened_at: datetime | None = None
    closed_at: datetime | None = None
    last_activity_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        customer_id: str,
        account_number: str,
        account_type: str,
        product_code: str,
        currency: str,
        organization_id: str | None = None,
        branch_id: str | None = None,
        is_joint: bool = False,
        joint_holders: list[str] | None = None,
        interest_rate_annual: float = 0.0,
        minimum_balance: float = 0.0,
        overdraft_limit: float = 0.0,
        overdraft_enabled: bool = False,
        gl_account_code: str | None = None,
        parent_account_id: str | None = None,
        opening_balance: float = 0.0,
        requires_approval: bool = True,
    ) -> BankingAccount:
        kernel_key = DEFAULT_GL_MAP.get(account_type, "customer_deposits")
        status = (
            AccountStatus.PENDING_APPROVAL.value
            if requires_approval
            else AccountStatus.ACTIVE.value
        )
        approval = ApprovalStatus.PENDING.value if requires_approval else ApprovalStatus.APPROVED.value
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            customer_id=customer_id,
            account_number=account_number.strip().upper(),
            account_type=account_type,
            product_code=product_code,
            currency=currency.strip().upper(),
            status=status,
            balance=round(opening_balance, 2),
            available_balance=round(opening_balance, 2),
            organization_id=organization_id,
            branch_id=branch_id,
            is_joint=is_joint,
            joint_holders=joint_holders or [],
            interest_rate_annual=interest_rate_annual,
            minimum_balance=minimum_balance,
            overdraft_limit=overdraft_limit,
            overdraft_enabled=overdraft_enabled,
            approval_status=approval,
            gl_account_code=gl_account_code,
            kernel_account_key=kernel_key,
            parent_account_id=parent_account_id,
            opened_at=None if requires_approval else datetime.now(UTC),
        )

    def link_kernel(
        self,
        *,
        gl_account_code: str,
        journal_id: str | None = None,
        subledger_ref: str | None = None,
    ) -> None:
        self.gl_account_code = gl_account_code
        self.kernel_linked = True
        self.kernel_journal_id = journal_id
        self.kernel_subledger_ref = subledger_ref or f"banking:{self.id}"
        self.updated_at = datetime.now(UTC)

    def approve_opening(self) -> None:
        if self.approval_status != ApprovalStatus.PENDING.value:
            raise ValueError("not_pending_approval")
        self.approval_status = ApprovalStatus.APPROVED.value
        self.status = AccountStatus.ACTIVE.value
        self.opened_at = datetime.now(UTC)
        self.last_activity_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def reject_opening(self) -> None:
        if self.approval_status != ApprovalStatus.PENDING.value:
            raise ValueError("not_pending_approval")
        self.approval_status = ApprovalStatus.REJECTED.value
        self.status = AccountStatus.CLOSED.value
        self.closed_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def transition_status(self, new_status: str) -> None:
        AccountStatus(new_status)
        allowed = ACCOUNT_STATUS_TRANSITIONS.get(self.status, [])
        if new_status not in allowed:
            raise ValueError("invalid_status_transition")
        if new_status == AccountStatus.CLOSED.value:
            self.closed_at = datetime.now(UTC)
        if new_status == AccountStatus.ACTIVE.value:
            self.last_activity_at = datetime.now(UTC)
        self.status = new_status
        self.updated_at = datetime.now(UTC)

    def credit(self, amount: float) -> None:
        if self.status not in OPERATIONAL_STATUSES:
            raise ValueError("account_not_operational")
        self.balance = round(self.balance + amount, 2)
        self.available_balance = round(self.available_balance + amount, 2)
        self.last_activity_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def debit(self, amount: float) -> None:
        if self.status not in OPERATIONAL_STATUSES:
            raise ValueError("account_not_operational")
        limit = self.balance + (self.overdraft_limit if self.overdraft_enabled else 0)
        if amount > limit:
            raise ValueError("insufficient_balance")
        self.balance = round(self.balance - amount, 2)
        self.available_balance = round(self.available_balance - amount, 2)
        self.last_activity_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "customer_id": self.customer_id,
            "account_number": self.account_number,
            "account_type": self.account_type,
            "product_code": self.product_code,
            "currency": self.currency,
            "status": self.status,
            "balance": self.balance,
            "available_balance": self.available_balance,
            "organization_id": self.organization_id,
            "branch_id": self.branch_id,
            "is_joint": self.is_joint,
            "joint_holders": self.joint_holders,
            "interest_rate_annual": self.interest_rate_annual,
            "minimum_balance": self.minimum_balance,
            "overdraft_limit": self.overdraft_limit,
            "overdraft_enabled": self.overdraft_enabled,
            "approval_status": self.approval_status,
            "gl_account_code": self.gl_account_code,
            "kernel_account_key": self.kernel_account_key,
            "kernel_linked": self.kernel_linked,
            "kernel_journal_id": self.kernel_journal_id,
            "kernel_subledger_ref": self.kernel_subledger_ref,
            "parent_account_id": self.parent_account_id,
            "opened_at": self.opened_at.isoformat() if self.opened_at else None,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
            "last_activity_at": self.last_activity_at.isoformat() if self.last_activity_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


OPERATIONAL_STATUSES = {
    AccountStatus.ACTIVE.value,
    AccountStatus.DORMANT.value,
}

ACCOUNT_STATUS_TRANSITIONS: dict[str, list[str]] = {
    AccountStatus.PENDING_APPROVAL.value: [AccountStatus.ACTIVE.value, AccountStatus.CLOSED.value],
    AccountStatus.ACTIVE.value: [
        AccountStatus.DORMANT.value,
        AccountStatus.BLOCKED.value,
        AccountStatus.FROZEN.value,
        AccountStatus.CLOSED.value,
    ],
    AccountStatus.DORMANT.value: [AccountStatus.ACTIVE.value, AccountStatus.CLOSED.value],
    AccountStatus.BLOCKED.value: [AccountStatus.ACTIVE.value, AccountStatus.CLOSED.value],
    AccountStatus.FROZEN.value: [AccountStatus.ACTIVE.value, AccountStatus.CLOSED.value],
    AccountStatus.CLOSED.value: [],
}


@dataclass(eq=False, kw_only=True)
class BankingAccountAudit(AggregateRoot):
    tenant_id: str
    account_id: str
    action: str
    actor_id: str | None
    detail: str
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        account_id: str,
        action: str,
        actor_id: str | None = None,
        detail: str = "",
    ) -> BankingAccountAudit:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            account_id=account_id,
            action=action,
            actor_id=actor_id,
            detail=detail,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "account_id": self.account_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "detail": self.detail,
            "occurred_at": self.occurred_at.isoformat(),
        }
