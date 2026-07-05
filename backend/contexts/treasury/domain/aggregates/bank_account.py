"""Enterprise Bank Account Management aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class BankStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class BankBranchStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class BankAccountType(StrEnum):
    CURRENT = "current"
    SAVINGS = "savings"
    INVESTMENT = "investment"
    LOAN = "loan"
    ESCROW = "escrow"
    VIRTUAL = "virtual"


class BankAccountStatus(StrEnum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    FROZEN = "frozen"
    CLOSED = "closed"


class SignatoryStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REVOKED = "revoked"


class BankDocumentType(StrEnum):
    KYC = "kyc"
    MANDATE = "mandate"
    CONTRACT = "contract"
    STATEMENT = "statement"
    AUTHORIZATION = "authorization"


class BankDocumentStatus(StrEnum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"


@dataclass(eq=False, kw_only=True)
class Bank(AggregateRoot):
    tenant_id: str
    organization_id: str | None
    code: str
    name: str
    swift_bic: str | None
    country: str
    status: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        code: str,
        name: str,
        country: str = "US",
        organization_id: str | None = None,
        swift_bic: str | None = None,
    ) -> Bank:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            organization_id=organization_id,
            code=code.strip().upper(),
            name=name.strip(),
            swift_bic=swift_bic.strip().upper() if swift_bic else None,
            country=country.strip().upper(),
            status=BankStatus.ACTIVE.value,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "organization_id": self.organization_id,
            "code": self.code,
            "name": self.name,
            "swift_bic": self.swift_bic,
            "country": self.country,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class BankBranch(AggregateRoot):
    tenant_id: str
    organization_id: str | None
    bank_id: str
    code: str
    name: str
    address: str | None
    routing_number: str | None
    swift_bic: str | None
    status: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        bank_id: str,
        code: str,
        name: str,
        organization_id: str | None = None,
        address: str | None = None,
        routing_number: str | None = None,
        swift_bic: str | None = None,
    ) -> BankBranch:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            organization_id=organization_id,
            bank_id=bank_id,
            code=code.strip().upper(),
            name=name.strip(),
            address=address,
            routing_number=routing_number,
            swift_bic=swift_bic.strip().upper() if swift_bic else None,
            status=BankBranchStatus.ACTIVE.value,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "organization_id": self.organization_id,
            "bank_id": self.bank_id,
            "code": self.code,
            "name": self.name,
            "address": self.address,
            "routing_number": self.routing_number,
            "swift_bic": self.swift_bic,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class BankAccount(AggregateRoot):
    tenant_id: str
    organization_id: str | None
    bank_id: str
    branch_id: str | None
    code: str
    name: str
    account_type: str
    currency: str
    iban: str | None
    swift_bic: str | None
    routing_number: str | None
    account_number: str | None
    virtual_account_ref: str | None
    gl_account_code: str | None
    status: str
    balance: float = 0.0
    workflow_instance_id: str | None = None
    approved_by: str | None = None
    approved_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create_draft(
        cls,
        *,
        tenant_id: str,
        bank_id: str,
        code: str,
        name: str,
        account_type: str,
        currency: str = "USD",
        organization_id: str | None = None,
        branch_id: str | None = None,
        iban: str | None = None,
        swift_bic: str | None = None,
        routing_number: str | None = None,
        account_number: str | None = None,
        virtual_account_ref: str | None = None,
        gl_account_code: str | None = None,
        opening_balance: float = 0.0,
        require_approval: bool = True,
    ) -> BankAccount:
        status = (
            BankAccountStatus.DRAFT.value
            if require_approval
            else BankAccountStatus.ACTIVE.value
        )
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            organization_id=organization_id,
            bank_id=bank_id,
            branch_id=branch_id,
            code=code.strip().upper(),
            name=name.strip(),
            account_type=account_type,
            currency=currency.strip().upper(),
            iban=iban.strip().upper().replace(" ", "") if iban else None,
            swift_bic=swift_bic.strip().upper() if swift_bic else None,
            routing_number=routing_number,
            account_number=account_number,
            virtual_account_ref=virtual_account_ref,
            gl_account_code=gl_account_code,
            status=status,
            balance=round(opening_balance, 2),
        )

    def submit_for_approval(self) -> None:
        if self.status != BankAccountStatus.DRAFT.value:
            raise ValueError("only_draft_can_submit")
        self.status = BankAccountStatus.PENDING_APPROVAL.value

    def approve(self, actor_id: str, workflow_instance_id: str | None = None) -> None:
        if self.status not in (
            BankAccountStatus.DRAFT.value,
            BankAccountStatus.PENDING_APPROVAL.value,
        ):
            raise ValueError("not_pending_approval")
        self.status = BankAccountStatus.ACTIVE.value
        self.approved_by = actor_id
        self.approved_at = datetime.now(UTC)
        self.workflow_instance_id = workflow_instance_id

    def reject(self) -> None:
        if self.status != BankAccountStatus.PENDING_APPROVAL.value:
            raise ValueError("not_pending_approval")
        self.status = BankAccountStatus.DRAFT.value

    def suspend(self) -> None:
        if self.status != BankAccountStatus.ACTIVE.value:
            raise ValueError("only_active_can_suspend")
        self.status = BankAccountStatus.SUSPENDED.value

    def freeze(self) -> None:
        if self.status not in (BankAccountStatus.ACTIVE.value, BankAccountStatus.SUSPENDED.value):
            raise ValueError("cannot_freeze")
        self.status = BankAccountStatus.FROZEN.value

    def close(self) -> None:
        if self.status == BankAccountStatus.CLOSED.value:
            raise ValueError("already_closed")
        self.status = BankAccountStatus.CLOSED.value

    def assert_operable(self) -> None:
        if self.status != BankAccountStatus.ACTIVE.value:
            raise ValueError("account_not_operable")

    def to_dict(self, *, mask_sensitive: bool = True) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "organization_id": self.organization_id,
            "bank_id": self.bank_id,
            "branch_id": self.branch_id,
            "code": self.code,
            "name": self.name,
            "account_type": self.account_type,
            "currency": self.currency,
            "iban": _mask_value(self.iban, mask_sensitive),
            "swift_bic": self.swift_bic,
            "routing_number": _mask_value(self.routing_number, mask_sensitive),
            "account_number": _mask_value(self.account_number, mask_sensitive),
            "virtual_account_ref": self.virtual_account_ref,
            "gl_account_code": self.gl_account_code,
            "status": self.status,
            "balance": self.balance,
            "workflow_instance_id": self.workflow_instance_id,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class AuthorizedSignatory(AggregateRoot):
    tenant_id: str
    organization_id: str | None
    bank_account_id: str
    name: str
    role: str
    email: str | None
    authority_limit: float | None
    status: str
    approved_by: str | None = None
    approved_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        bank_account_id: str,
        name: str,
        role: str = "signatory",
        organization_id: str | None = None,
        email: str | None = None,
        authority_limit: float | None = None,
    ) -> AuthorizedSignatory:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            organization_id=organization_id,
            bank_account_id=bank_account_id,
            name=name.strip(),
            role=role,
            email=email,
            authority_limit=authority_limit,
            status=SignatoryStatus.PENDING.value,
        )

    def approve(self, actor_id: str) -> None:
        self.status = SignatoryStatus.APPROVED.value
        self.approved_by = actor_id
        self.approved_at = datetime.now(UTC)

    def revoke(self) -> None:
        self.status = SignatoryStatus.REVOKED.value

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "organization_id": self.organization_id,
            "bank_account_id": self.bank_account_id,
            "name": self.name,
            "role": self.role,
            "email": self.email,
            "authority_limit": self.authority_limit,
            "status": self.status,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class BankAccountDocument(AggregateRoot):
    tenant_id: str
    organization_id: str | None
    bank_account_id: str
    document_type: str
    reference: str
    file_name: str | None
    status: str
    verified_by: str | None = None
    verified_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def attach(
        cls,
        *,
        tenant_id: str,
        bank_account_id: str,
        document_type: str,
        reference: str,
        organization_id: str | None = None,
        file_name: str | None = None,
    ) -> BankAccountDocument:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            organization_id=organization_id,
            bank_account_id=bank_account_id,
            document_type=document_type,
            reference=reference.strip(),
            file_name=file_name,
            status=BankDocumentStatus.PENDING.value,
        )

    def verify(self, actor_id: str) -> None:
        self.status = BankDocumentStatus.VERIFIED.value
        self.verified_by = actor_id
        self.verified_at = datetime.now(UTC)

    def reject(self) -> None:
        self.status = BankDocumentStatus.REJECTED.value

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "organization_id": self.organization_id,
            "bank_account_id": self.bank_account_id,
            "document_type": self.document_type,
            "reference": self.reference,
            "file_name": self.file_name,
            "status": self.status,
            "verified_by": self.verified_by,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None,
            "created_at": self.created_at.isoformat(),
        }


def _mask_value(value: str | None, mask: bool) -> str | None:
    if not value or not mask:
        return value
    if len(value) <= 4:
        return "****"
    return f"{'*' * (len(value) - 4)}{value[-4:]}"
