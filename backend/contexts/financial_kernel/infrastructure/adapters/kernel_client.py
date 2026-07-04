"""IFinancialKernel adapter."""
from __future__ import annotations

from contexts.financial_kernel.application.service import FinancialKernelApplicationService
from shared.application.ports.financial_kernel import (
    IFinancialKernel,
    JournalLine,
    JournalPostResult,
    TrialBalanceLine,
)


class FinancialKernelClient(IFinancialKernel):
    def __init__(self, service: FinancialKernelApplicationService) -> None:
        self._service = service

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
    ) -> JournalPostResult:
        result = await self._service.post_journal(
            tenant_id=tenant_id,
            source_context=source_context,
            source_document_id=source_document_id,
            lines=[line.to_dict() for line in lines],
            currency=currency,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
        )
        if not result.succeeded:
            raise ValueError(result.error or "post_failed")
        data = result.unwrap()
        return JournalPostResult(
            journal_id=data["id"],
            status=data["status"],
            total_debit=str(data["total_debits"]),
            total_credit=str(data["total_credits"]),
        )

    async def get_trial_balance(self, *, tenant_id: str) -> list[TrialBalanceLine]:
        rows = (await self._service.get_trial_balance(tenant_id)).unwrap()
        return [
            TrialBalanceLine(
                account_code=r["account_code"],
                account_name=r["account_name"],
                debit_balance=str(r["debit_balance"]),
                credit_balance=str(r["credit_balance"]),
            )
            for r in rows
        ]

    async def list_accounts(self, *, tenant_id: str) -> list[dict]:
        return (await self._service.list_accounts(tenant_id)).unwrap()

    async def convert_currency(
        self, *, tenant_id: str, amount: str, from_currency: str, to_currency: str
    ) -> dict:
        return (
            await self._service.convert_currency(
                tenant_id=tenant_id,
                amount=amount,
                from_currency=from_currency,
                to_currency=to_currency,
            )
        ).unwrap()

    async def calculate_tax(
        self, *, tenant_id: str, amount: str, tax_code: str, jurisdiction: str
    ) -> dict:
        return (
            await self._service.calculate_tax(
                tenant_id=tenant_id,
                amount=amount,
                tax_code=tax_code,
                jurisdiction=jurisdiction,
            )
        ).unwrap()
