"""Financial Kernel port — every module posts through this."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class JournalLine:
    account_code: str
    debit: str
    credit: str
    cost_center: str | None = None
    profit_center: str | None = None
    description: str | None = None

    def to_dict(self) -> dict:
        return {
            "account_code": self.account_code,
            "debit": self.debit,
            "credit": self.credit,
            "cost_center": self.cost_center,
            "profit_center": self.profit_center,
            "description": self.description,
        }


@dataclass(frozen=True, slots=True)
class JournalPostResult:
    journal_id: str
    status: str
    total_debit: str
    total_credit: str

    def to_dict(self) -> dict:
        return {
            "journal_id": self.journal_id,
            "status": self.status,
            "total_debit": self.total_debit,
            "total_credit": self.total_credit,
        }


@dataclass(frozen=True, slots=True)
class TrialBalanceLine:
    account_code: str
    account_name: str
    debit_balance: str
    credit_balance: str


class IFinancialKernel(Protocol):
    async def execute_posting(
        self,
        *,
        tenant_id: str,
        rule_id: str,
        source_context: str,
        source_document_id: str,
        currency: str,
        correlation_id: str,
        amount: float | None = None,
        account_mappings: dict[str, str] | None = None,
        lines: list[JournalLine] | None = None,
        description: str = "",
        dimensions: dict[str, str] | None = None,
        tax_amount: float | None = None,
        idempotency_key: str | None = None,
    ) -> JournalPostResult: ...

    async def post_journal(
        self,
        *,
        tenant_id: str,
        source_context: str,
        source_document_id: str,
        lines: list[JournalLine],
        currency: str,
        correlation_id: str,
        idempotency_key: str | None = None,
    ) -> JournalPostResult: ...

    async def get_trial_balance(self, *, tenant_id: str) -> list[TrialBalanceLine]: ...

    async def list_accounts(self, *, tenant_id: str) -> list[dict]: ...

    async def convert_currency(
        self,
        *,
        tenant_id: str,
        amount: str,
        from_currency: str,
        to_currency: str,
    ) -> dict: ...

    async def calculate_tax(
        self,
        *,
        tenant_id: str,
        amount: str,
        tax_code: str,
        jurisdiction: str,
    ) -> dict: ...
