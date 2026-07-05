"""Treasury Transaction Engine — enterprise treasury transactions."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class TreasuryTransactionType(StrEnum):
    INTERNAL_TRANSFER = "internal_transfer"
    BANK_TRANSFER = "bank_transfer"
    WIRE_TRANSFER = "wire_transfer"
    CASH_MOVEMENT = "cash_movement"
    FUND_ALLOCATION = "fund_allocation"
    TREASURY_SETTLEMENT = "treasury_settlement"
    INVESTMENT_PURCHASE = "investment_purchase"
    INVESTMENT_SALE = "investment_sale"
    DEBT_PAYMENT = "debt_payment"
    INTEREST_PAYMENT = "interest_payment"
    LOAN_DISBURSEMENT = "loan_disbursement"
    LOAN_REPAYMENT = "loan_repayment"


class TransactionWorkflowStatus(StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    EXECUTED = "executed"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


@dataclass(eq=False, kw_only=True)
class TreasuryTransaction(AggregateRoot):
    tenant_id: str
    transaction_type: str
    status: str
    amount: float
    currency: str
    reference: str
    description: str | None = None
    from_account_id: str | None = None
    to_account_id: str | None = None
    posting_rule_id: str = ""
    required_approval_levels: int = 0
    current_approval_level: int = 0
    approval_history: list[dict] = field(default_factory=list)
    workflow_instance_id: str | None = None
    metadata: dict = field(default_factory=dict)
    executed_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create_draft(
        cls,
        *,
        tenant_id: str,
        transaction_type: str,
        amount: float,
        currency: str,
        reference: str,
        description: str | None = None,
        from_account_id: str | None = None,
        to_account_id: str | None = None,
        posting_rule_id: str = "",
        required_approval_levels: int = 0,
        metadata: dict | None = None,
    ) -> TreasuryTransaction:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            transaction_type=transaction_type,
            status=TransactionWorkflowStatus.DRAFT.value,
            amount=round(amount, 2),
            currency=currency.strip().upper(),
            reference=reference,
            description=description,
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            posting_rule_id=posting_rule_id,
            required_approval_levels=required_approval_levels,
            metadata=metadata or {},
        )

    def submit(self) -> None:
        if self.status != TransactionWorkflowStatus.DRAFT.value:
            raise ValueError("only_draft_can_be_submitted")
        self.status = TransactionWorkflowStatus.SUBMITTED.value

    def enter_approval(self) -> None:
        if self.status != TransactionWorkflowStatus.SUBMITTED.value:
            raise ValueError("only_submitted_can_enter_approval")
        self.status = TransactionWorkflowStatus.PENDING_APPROVAL.value

    def approve(self, *, approver_id: str, level: int, comment: str | None = None) -> None:
        if self.status not in (
            TransactionWorkflowStatus.SUBMITTED.value,
            TransactionWorkflowStatus.PENDING_APPROVAL.value,
        ):
            raise ValueError("transaction_not_awaiting_approval")
        if level != self.current_approval_level + 1:
            raise ValueError("invalid_approval_level")
        self.current_approval_level = level
        self.approval_history.append(
            {
                "level": level,
                "approver_id": approver_id,
                "action": "approved",
                "comment": comment,
                "at": datetime.now(UTC).isoformat(),
            }
        )
        if self.current_approval_level >= self.required_approval_levels:
            self.status = TransactionWorkflowStatus.APPROVED.value

    def reject(self, *, approver_id: str, comment: str | None = None) -> None:
        if self.status not in (
            TransactionWorkflowStatus.SUBMITTED.value,
            TransactionWorkflowStatus.PENDING_APPROVAL.value,
        ):
            raise ValueError("transaction_not_awaiting_approval")
        self.status = TransactionWorkflowStatus.REJECTED.value
        self.approval_history.append(
            {
                "level": self.current_approval_level + 1,
                "approver_id": approver_id,
                "action": "rejected",
                "comment": comment,
                "at": datetime.now(UTC).isoformat(),
            }
        )

    def mark_approved(self) -> None:
        if self.status != TransactionWorkflowStatus.SUBMITTED.value:
            raise ValueError("only_submitted_can_auto_approve")
        self.status = TransactionWorkflowStatus.APPROVED.value

    def mark_executed(self) -> None:
        if self.status != TransactionWorkflowStatus.APPROVED.value:
            raise ValueError("only_approved_can_execute")
        self.status = TransactionWorkflowStatus.EXECUTED.value
        self.executed_at = datetime.now(UTC)

    def cancel(self) -> None:
        if self.status in (
            TransactionWorkflowStatus.EXECUTED.value,
            TransactionWorkflowStatus.CANCELLED.value,
        ):
            raise ValueError("cannot_cancel")
        self.status = TransactionWorkflowStatus.CANCELLED.value

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "transaction_type": self.transaction_type,
            "status": self.status,
            "amount": self.amount,
            "currency": self.currency,
            "reference": self.reference,
            "description": self.description,
            "from_account_id": self.from_account_id,
            "to_account_id": self.to_account_id,
            "posting_rule_id": self.posting_rule_id,
            "required_approval_levels": self.required_approval_levels,
            "current_approval_level": self.current_approval_level,
            "approval_history": self.approval_history,
            "workflow_instance_id": self.workflow_instance_id,
            "metadata": self.metadata,
            "executed_at": self.executed_at.isoformat() if self.executed_at else None,
            "created_at": self.created_at.isoformat(),
        }
