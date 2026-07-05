"""Banking Payment Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class TransferType(StrEnum):
    INTERNAL = "internal"
    INTER_BRANCH = "inter_branch"
    BANK_TO_BANK = "bank_to_bank"
    BULK = "bulk"
    BILL_PAYMENT = "bill_payment"
    GOVERNMENT_PAYMENT = "government_payment"
    SALARY_TRANSFER = "salary_transfer"
    MERCHANT_PAYMENT = "merchant_payment"
    QR_PAYMENT = "qr_payment"
    REAL_TIME = "real_time"


class TransferStatus(StrEnum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class FraudStatus(StrEnum):
    CLEAR = "clear"
    REVIEW = "review"
    BLOCKED = "blocked"


class StandingOrderFrequency(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass(eq=False, kw_only=True)
class PaymentBeneficiary(AggregateRoot):
    tenant_id: str
    customer_id: str
    beneficiary_ref: str
    name: str
    account_number: str
    bank_code: str = ""
    branch_code: str = ""
    currency: str = "USD"
    beneficiary_type: str = "external"
    active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        customer_id: str,
        beneficiary_ref: str,
        name: str,
        account_number: str,
        bank_code: str = "",
        branch_code: str = "",
        currency: str = "USD",
        beneficiary_type: str = "external",
    ) -> PaymentBeneficiary:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            customer_id=customer_id,
            beneficiary_ref=beneficiary_ref,
            name=name.strip(),
            account_number=account_number.strip(),
            bank_code=bank_code,
            branch_code=branch_code,
            currency=currency,
            beneficiary_type=beneficiary_type,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "customer_id": self.customer_id,
            "beneficiary_ref": self.beneficiary_ref,
            "name": self.name,
            "account_number": self.account_number,
            "bank_code": self.bank_code,
            "branch_code": self.branch_code,
            "currency": self.currency,
            "beneficiary_type": self.beneficiary_type,
            "active": self.active,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class PaymentTransfer(AggregateRoot):
    tenant_id: str
    transfer_ref: str
    transfer_type: str
    status: str = TransferStatus.DRAFT.value
    source_account_id: str
    destination_account_id: str | None = None
    beneficiary_id: str | None = None
    customer_id: str
    amount: float
    currency: str
    channel: str = "digital"
    branch_id: str = ""
    destination_branch_id: str = ""
    batch_id: str | None = None
    standing_order_id: str | None = None
    scheduled_at: datetime | None = None
    qr_payload: str = ""
    merchant_ref: str = ""
    bill_ref: str = ""
    government_ref: str = ""
    salary_ref: str = ""
    narrative: str = ""
    fraud_status: str = FraudStatus.CLEAR.value
    fraud_score: float = 0.0
    journal_id: str | None = None
    executed_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        transfer_ref: str,
        transfer_type: str,
        source_account_id: str,
        customer_id: str,
        amount: float,
        currency: str,
        destination_account_id: str | None = None,
        beneficiary_id: str | None = None,
        channel: str = "digital",
        branch_id: str = "",
        destination_branch_id: str = "",
        batch_id: str | None = None,
        standing_order_id: str | None = None,
        scheduled_at: datetime | None = None,
        qr_payload: str = "",
        merchant_ref: str = "",
        bill_ref: str = "",
        government_ref: str = "",
        salary_ref: str = "",
        narrative: str = "",
    ) -> PaymentTransfer:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            transfer_ref=transfer_ref,
            transfer_type=transfer_type,
            source_account_id=source_account_id,
            destination_account_id=destination_account_id,
            beneficiary_id=beneficiary_id,
            customer_id=customer_id,
            amount=round(amount, 2),
            currency=currency,
            channel=channel,
            branch_id=branch_id,
            destination_branch_id=destination_branch_id,
            batch_id=batch_id,
            standing_order_id=standing_order_id,
            scheduled_at=scheduled_at,
            qr_payload=qr_payload,
            merchant_ref=merchant_ref,
            bill_ref=bill_ref,
            government_ref=government_ref,
            salary_ref=salary_ref,
            narrative=narrative.strip(),
        )

    def submit(self) -> None:
        if self.status != TransferStatus.DRAFT.value:
            raise ValueError("not_draft")
        self.status = TransferStatus.PENDING_APPROVAL.value
        self.updated_at = datetime.now(UTC)

    def approve(self) -> None:
        if self.status != TransferStatus.PENDING_APPROVAL.value:
            raise ValueError("not_pending_approval")
        self.status = TransferStatus.APPROVED.value
        self.updated_at = datetime.now(UTC)

    def schedule(self) -> None:
        if self.status not in {TransferStatus.APPROVED.value, TransferStatus.DRAFT.value}:
            raise ValueError("cannot_schedule")
        self.status = TransferStatus.SCHEDULED.value
        self.updated_at = datetime.now(UTC)

    def start_processing(self) -> None:
        if self.status not in {
            TransferStatus.APPROVED.value,
            TransferStatus.SCHEDULED.value,
            TransferStatus.PENDING_APPROVAL.value,
        }:
            raise ValueError("cannot_process")
        self.status = TransferStatus.PROCESSING.value
        self.updated_at = datetime.now(UTC)

    def complete(self, *, journal_id: str | None = None) -> None:
        self.status = TransferStatus.COMPLETED.value
        self.journal_id = journal_id
        self.executed_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def fail(self, reason: str = "") -> None:
        self.status = TransferStatus.FAILED.value
        self.narrative = f"{self.narrative} | failed: {reason}".strip(" |")
        self.updated_at = datetime.now(UTC)

    def set_fraud(self, *, status: str, score: float) -> None:
        self.fraud_status = status
        self.fraud_score = round(score, 2)
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "transfer_ref": self.transfer_ref,
            "transfer_type": self.transfer_type,
            "status": self.status,
            "source_account_id": self.source_account_id,
            "destination_account_id": self.destination_account_id,
            "beneficiary_id": self.beneficiary_id,
            "customer_id": self.customer_id,
            "amount": self.amount,
            "currency": self.currency,
            "channel": self.channel,
            "branch_id": self.branch_id,
            "destination_branch_id": self.destination_branch_id,
            "batch_id": self.batch_id,
            "standing_order_id": self.standing_order_id,
            "scheduled_at": self.scheduled_at.isoformat() if self.scheduled_at else None,
            "qr_payload": self.qr_payload,
            "merchant_ref": self.merchant_ref,
            "bill_ref": self.bill_ref,
            "government_ref": self.government_ref,
            "salary_ref": self.salary_ref,
            "narrative": self.narrative,
            "fraud_status": self.fraud_status,
            "fraud_score": self.fraud_score,
            "journal_id": self.journal_id,
            "executed_at": self.executed_at.isoformat() if self.executed_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class PaymentBatch(AggregateRoot):
    tenant_id: str
    batch_ref: str
    transfer_type: str
    source_account_id: str
    customer_id: str
    total_amount: float
    currency: str
    item_count: int = 0
    status: str = TransferStatus.DRAFT.value
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        batch_ref: str,
        transfer_type: str,
        source_account_id: str,
        customer_id: str,
        currency: str = "USD",
    ) -> PaymentBatch:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            batch_ref=batch_ref,
            transfer_type=transfer_type,
            source_account_id=source_account_id,
            customer_id=customer_id,
            total_amount=0.0,
            currency=currency,
        )

    def add_item(self, amount: float) -> None:
        self.total_amount = round(self.total_amount + amount, 2)
        self.item_count += 1

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "batch_ref": self.batch_ref,
            "transfer_type": self.transfer_type,
            "source_account_id": self.source_account_id,
            "customer_id": self.customer_id,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "item_count": self.item_count,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class StandingOrder(AggregateRoot):
    tenant_id: str
    order_ref: str
    customer_id: str
    source_account_id: str
    destination_account_id: str | None = None
    beneficiary_id: str | None = None
    transfer_type: str
    amount: float
    currency: str
    frequency: str
    next_run_at: datetime
    active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        order_ref: str,
        customer_id: str,
        source_account_id: str,
        transfer_type: str,
        amount: float,
        currency: str,
        frequency: str,
        next_run_at: datetime,
        destination_account_id: str | None = None,
        beneficiary_id: str | None = None,
    ) -> StandingOrder:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            order_ref=order_ref,
            customer_id=customer_id,
            source_account_id=source_account_id,
            destination_account_id=destination_account_id,
            beneficiary_id=beneficiary_id,
            transfer_type=transfer_type,
            amount=round(amount, 2),
            currency=currency,
            frequency=frequency,
            next_run_at=next_run_at,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "order_ref": self.order_ref,
            "customer_id": self.customer_id,
            "source_account_id": self.source_account_id,
            "destination_account_id": self.destination_account_id,
            "beneficiary_id": self.beneficiary_id,
            "transfer_type": self.transfer_type,
            "amount": self.amount,
            "currency": self.currency,
            "frequency": self.frequency,
            "next_run_at": self.next_run_at.isoformat(),
            "active": self.active,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class PaymentWorkflowRequest(AggregateRoot):
    tenant_id: str
    transfer_id: str
    request_type: str
    status: str = "pending"
    required_levels: int = 1
    current_level: int = 0
    approver_ids: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls, *, tenant_id: str, transfer_id: str, request_type: str, required_levels: int = 1
    ) -> PaymentWorkflowRequest:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            transfer_id=transfer_id,
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
            "transfer_id": self.transfer_id,
            "request_type": self.request_type,
            "status": self.status,
            "required_levels": self.required_levels,
            "current_level": self.current_level,
            "approver_ids": self.approver_ids,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class PaymentFraudCheck(AggregateRoot):
    tenant_id: str
    transfer_id: str
    risk_score: float
    status: str
    factors: list[dict]
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls, *, tenant_id: str, transfer_id: str, risk_score: float, status: str, factors: list[dict]
    ) -> PaymentFraudCheck:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            transfer_id=transfer_id,
            risk_score=round(risk_score, 2),
            status=status,
            factors=factors,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "transfer_id": self.transfer_id,
            "risk_score": self.risk_score,
            "status": self.status,
            "factors": self.factors,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class PaymentAuditEntry(AggregateRoot):
    tenant_id: str
    transfer_id: str
    action: str
    actor_id: str | None = None
    detail: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls, *, tenant_id: str, transfer_id: str, action: str, actor_id: str | None = None, detail: str = ""
    ) -> PaymentAuditEntry:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            transfer_id=transfer_id,
            action=action,
            actor_id=actor_id,
            detail=detail,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "transfer_id": self.transfer_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "detail": self.detail,
            "created_at": self.created_at.isoformat(),
        }
