"""Enterprise subledger aggregates — AR, AP, inventory, payroll, and more."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class SubledgerType(StrEnum):
    ACCOUNTS_RECEIVABLE = "accounts_receivable"
    ACCOUNTS_PAYABLE = "accounts_payable"
    INVENTORY = "inventory"
    PAYROLL = "payroll"
    TREASURY = "treasury"
    ASSETS = "assets"
    LOANS = "loans"
    PROJECTS = "projects"
    STUDENTS = "students"
    PATIENTS = "patients"
    TAXES = "taxes"
    CURRENCY_EXCHANGE = "currency_exchange"


class SubledgerEntryStatus(StrEnum):
    DRAFT = "draft"
    POSTED = "posted"
    REVERSED = "reversed"
    RECONCILED = "reconciled"


class SubledgerReconciliationStatus(StrEnum):
    OPEN = "open"
    MATCHED = "matched"
    PARTIAL_MATCH = "partial_match"
    VARIANCE = "variance"


@dataclass(eq=False, kw_only=True)
class Subledger(AggregateRoot):
    tenant_id: str
    subledger_type: str
    name: str
    control_account_key: str
    posting_rule_id: str
    source_context: str
    journal_type: str
    normal_balance: str = "debit"
    is_active: bool = True
    auto_post_to_gl: bool = True
    entry_count: int = 0
    posted_balance: float = 0.0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        subledger_type: str,
        name: str,
        control_account_key: str,
        posting_rule_id: str,
        source_context: str,
        journal_type: str,
        normal_balance: str = "debit",
        auto_post_to_gl: bool = True,
    ) -> Subledger:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            subledger_type=subledger_type,
            name=name,
            control_account_key=control_account_key,
            posting_rule_id=posting_rule_id,
            source_context=source_context,
            journal_type=journal_type,
            normal_balance=normal_balance,
            auto_post_to_gl=auto_post_to_gl,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "subledger_type": self.subledger_type,
            "name": self.name,
            "control_account_key": self.control_account_key,
            "posting_rule_id": self.posting_rule_id,
            "source_context": self.source_context,
            "journal_type": self.journal_type,
            "normal_balance": self.normal_balance,
            "is_active": self.is_active,
            "auto_post_to_gl": self.auto_post_to_gl,
            "entry_count": self.entry_count,
            "posted_balance": self.posted_balance,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class SubledgerEntry(AggregateRoot):
    tenant_id: str
    subledger_id: str
    subledger_type: str
    source_context: str
    source_document_id: str
    idempotency_key: str
    amount: float
    currency: str = "USD"
    entry_date: str
    reference: str = ""
    counterparty: str | None = None
    description: str = ""
    dimensions: dict = field(default_factory=dict)
    account_mappings: dict = field(default_factory=dict)
    status: str = SubledgerEntryStatus.DRAFT.value
    journal_id: str | None = None
    posting_rule_id: str = ""
    side: str = "debit"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    posted_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        subledger_id: str,
        subledger_type: str,
        source_context: str,
        source_document_id: str,
        idempotency_key: str,
        amount: float,
        entry_date: str,
        currency: str = "USD",
        reference: str = "",
        counterparty: str | None = None,
        description: str = "",
        dimensions: dict | None = None,
        account_mappings: dict | None = None,
        posting_rule_id: str = "",
        side: str = "debit",
    ) -> SubledgerEntry:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            subledger_id=subledger_id,
            subledger_type=subledger_type,
            source_context=source_context,
            source_document_id=source_document_id,
            idempotency_key=idempotency_key,
            amount=round(amount, 2),
            currency=currency,
            entry_date=entry_date,
            reference=reference,
            counterparty=counterparty,
            description=description,
            dimensions=dimensions or {},
            account_mappings=account_mappings or {},
            posting_rule_id=posting_rule_id,
            side=side,
        )

    def mark_posted(self, journal_id: str) -> None:
        self.status = SubledgerEntryStatus.POSTED.value
        self.journal_id = journal_id
        self.posted_at = datetime.now(UTC)

    def mark_reversed(self) -> None:
        self.status = SubledgerEntryStatus.REVERSED.value

    def mark_reconciled(self) -> None:
        self.status = SubledgerEntryStatus.RECONCILED.value

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "subledger_id": self.subledger_id,
            "subledger_type": self.subledger_type,
            "source_context": self.source_context,
            "source_document_id": self.source_document_id,
            "idempotency_key": self.idempotency_key,
            "amount": self.amount,
            "currency": self.currency,
            "entry_date": self.entry_date,
            "reference": self.reference,
            "counterparty": self.counterparty,
            "description": self.description,
            "dimensions": self.dimensions,
            "account_mappings": self.account_mappings,
            "status": self.status,
            "journal_id": self.journal_id,
            "posting_rule_id": self.posting_rule_id,
            "side": self.side,
            "created_at": self.created_at.isoformat(),
            "posted_at": self.posted_at.isoformat() if self.posted_at else None,
        }


@dataclass(eq=False, kw_only=True)
class SubledgerReconciliation(AggregateRoot):
    tenant_id: str
    subledger_id: str
    subledger_type: str
    reconciliation_date: str
    period_id: str | None
    subledger_balance: float
    gl_control_balance: float
    variance: float
    subledger_items: list[dict]
    gl_items: list[dict]
    matched_pairs: list[dict]
    unmatched_subledger: list[dict]
    unmatched_gl: list[dict]
    status: str
    control_account_code: str
    matched_amount: float = 0.0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        subledger_id: str,
        subledger_type: str,
        reconciliation_date: str,
        subledger_balance: float,
        gl_control_balance: float,
        subledger_items: list[dict],
        gl_items: list[dict],
        control_account_code: str,
        period_id: str | None = None,
    ) -> SubledgerReconciliation:
        matched, unmatched_sub, unmatched_gl = match_reconciliation_items(
            subledger_items, gl_items
        )
        matched_amount = round(
            sum(float(p["subledger"].get("amount", 0)) for p in matched), 2
        )
        variance = round(gl_control_balance - subledger_balance, 2)
        if matched and not unmatched_sub and not unmatched_gl and abs(variance) < 0.01:
            status = SubledgerReconciliationStatus.MATCHED.value
        elif matched:
            status = SubledgerReconciliationStatus.PARTIAL_MATCH.value
        elif abs(variance) < 0.01:
            status = SubledgerReconciliationStatus.MATCHED.value
        else:
            status = SubledgerReconciliationStatus.VARIANCE.value
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            subledger_id=subledger_id,
            subledger_type=subledger_type,
            reconciliation_date=reconciliation_date,
            period_id=period_id,
            subledger_balance=subledger_balance,
            gl_control_balance=gl_control_balance,
            variance=variance,
            subledger_items=subledger_items,
            gl_items=gl_items,
            matched_pairs=matched,
            unmatched_subledger=unmatched_sub,
            unmatched_gl=unmatched_gl,
            status=status,
            control_account_code=control_account_code,
            matched_amount=matched_amount,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "subledger_id": self.subledger_id,
            "subledger_type": self.subledger_type,
            "reconciliation_date": self.reconciliation_date,
            "period_id": self.period_id,
            "subledger_balance": self.subledger_balance,
            "gl_control_balance": self.gl_control_balance,
            "variance": self.variance,
            "subledger_items": self.subledger_items,
            "gl_items": self.gl_items,
            "matched_pairs": self.matched_pairs,
            "unmatched_subledger": self.unmatched_subledger,
            "unmatched_gl": self.unmatched_gl,
            "status": self.status,
            "control_account_code": self.control_account_code,
            "matched_amount": self.matched_amount,
            "created_at": self.created_at.isoformat(),
        }


def match_reconciliation_items(
    subledger_items: list[dict], gl_items: list[dict]
) -> tuple[list[dict], list[dict], list[dict]]:
    matched: list[dict] = []
    used_gl: set[int] = set()
    unmatched_sub: list[dict] = []

    for sub_item in subledger_items:
        sub_amount = round(float(sub_item.get("amount", 0)), 2)
        sub_ref = sub_item.get("reference", "") or sub_item.get("source_document_id", "")
        found = False
        for idx, gl_item in enumerate(gl_items):
            if idx in used_gl:
                continue
            gl_amount = round(float(gl_item.get("amount", 0)), 2)
            gl_ref = gl_item.get("reference", "") or gl_item.get("journal_id", "")
            if sub_amount == gl_amount and (
                sub_ref == gl_ref or not sub_ref or not gl_ref
            ):
                matched.append({"subledger": sub_item, "gl": gl_item})
                used_gl.add(idx)
                found = True
                break
        if not found:
            unmatched_sub.append(sub_item)

    unmatched_gl = [g for i, g in enumerate(gl_items) if i not in used_gl]
    return matched, unmatched_sub, unmatched_gl
