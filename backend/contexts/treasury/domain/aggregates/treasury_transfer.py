"""Treasury transfer — cheque, EFT, mobile money, digital wallet."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class PaymentInstrument(StrEnum):
    CHEQUE = "cheque"
    ELECTRONIC_TRANSFER = "electronic_transfer"
    MOBILE_MONEY = "mobile_money"
    DIGITAL_WALLET = "digital_wallet"
    CASH = "cash"


class TransferStatus(StrEnum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    EXECUTED = "executed"
    REJECTED = "rejected"


@dataclass(eq=False, kw_only=True)
class TreasuryTransfer(AggregateRoot):
    tenant_id: str
    from_account_id: str
    to_account_id: str
    amount: float
    currency: str
    instrument: str
    status: str
    reference: str
    description: str | None = None
    cheque_number: str | None = None
    workflow_instance_id: str | None = None
    executed_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create_draft(
        cls,
        *,
        tenant_id: str,
        from_account_id: str,
        to_account_id: str,
        amount: float,
        currency: str,
        instrument: str,
        reference: str,
        description: str | None = None,
        cheque_number: str | None = None,
        require_approval: bool = True,
    ) -> TreasuryTransfer:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=round(amount, 2),
            currency=currency.strip().upper(),
            instrument=instrument,
            status=TransferStatus.DRAFT if require_approval else TransferStatus.APPROVED,
            reference=reference,
            description=description,
            cheque_number=cheque_number,
        )

    def submit_for_approval(self) -> None:
        if self.status != TransferStatus.DRAFT:
            raise ValueError("Only draft transfers can be submitted")
        self.status = TransferStatus.PENDING_APPROVAL

    def approve(self, workflow_instance_id: str | None = None) -> None:
        if self.status not in (TransferStatus.DRAFT, TransferStatus.PENDING_APPROVAL):
            raise ValueError("Transfer not awaiting approval")
        self.status = TransferStatus.APPROVED
        if workflow_instance_id:
            self.workflow_instance_id = workflow_instance_id

    def reject(self) -> None:
        if self.status not in (TransferStatus.DRAFT, TransferStatus.PENDING_APPROVAL):
            raise ValueError("Transfer not awaiting approval")
        self.status = TransferStatus.REJECTED

    def mark_executed(self) -> None:
        if self.status != TransferStatus.APPROVED:
            raise ValueError("Only approved transfers can be executed")
        self.status = TransferStatus.EXECUTED
        self.executed_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "from_account_id": self.from_account_id,
            "to_account_id": self.to_account_id,
            "amount": self.amount,
            "currency": self.currency,
            "instrument": self.instrument,
            "status": self.status,
            "reference": self.reference,
            "description": self.description,
            "cheque_number": self.cheque_number,
            "workflow_instance_id": self.workflow_instance_id,
            "executed_at": self.executed_at.isoformat() if self.executed_at else None,
            "created_at": self.created_at.isoformat(),
        }
