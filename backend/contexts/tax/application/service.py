"""Tax application service — CAP-ENT-026 Tax Processing.

payroll.run.completed → tax liability. File return for open liabilities.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation

from contexts.tax.domain.aggregates.tax_liability import TaxLiability
from contexts.tax.domain.aggregates.tax_return import TaxReturn
from contexts.tax.domain.ports.repositories import ITaxLiabilityRepository, ITaxReturnRepository
from shared.application.result import Result
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class TaxApplicationService:
    def __init__(
        self,
        liabilities: ITaxLiabilityRepository,
        returns: ITaxReturnRepository,
    ) -> None:
        self._liabilities = liabilities
        self._returns = returns

    async def calculate_from_payroll_run(
        self,
        *,
        tenant_id: str,
        payroll_run_id: str,
        period_label: str,
        total_gross: str,
        currency: str,
        correlation_id: str,
    ) -> Result[dict]:
        run_id = UniqueId.from_string(payroll_run_id)
        existing = await self._liabilities.find_by_payroll_run(tenant_id, run_id)
        if existing:
            return Result.ok(existing.to_dict())
        try:
            base = Decimal(total_gross)
        except (InvalidOperation, ValueError):
            return Result.fail("tax.errors.invalid_base")
        try:
            liability, event = TaxLiability.calculate_from_payroll(
                tenant_id=tenant_id,
                payroll_run_id=run_id,
                period_label=period_label,
                taxable_base=base,
                currency=currency,
                correlation_id=correlation_id,
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._liabilities.save(liability)
        await publish_integration_event(event)
        return Result.ok(liability.to_dict())

    async def list_liabilities(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        items = await self._liabilities.list_all(tenant_id)
        page = items[offset : offset + limit]
        return Result.ok(
            {
                "items": [i.to_dict() for i in page],
                "total": len(items),
                "limit": limit,
                "offset": offset,
            }
        )

    async def list_returns(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        items = await self._returns.list_returns(tenant_id)
        page = items[offset : offset + limit]
        return Result.ok(
            {
                "items": [r.to_dict() for r in page],
                "total": len(items),
                "limit": limit,
                "offset": offset,
            }
        )

    async def file_return(
        self, *, tenant_id: str, period_label: str, correlation_id: str
    ) -> Result[dict]:
        open_items = await self._liabilities.list_open(tenant_id, period_label=period_label)
        if not open_items:
            return Result.fail("tax.errors.no_open_liabilities")
        total = sum((i.tax_amount for i in open_items), Decimal("0"))
        currency = open_items[0].currency
        try:
            tax_return = TaxReturn.draft(
                tenant_id=tenant_id,
                period_label=period_label,
                liability_ids=[i.id for i in open_items],
                total_tax=total,
                currency=currency,
            )
            filed = tax_return.file(correlation_id=correlation_id)
        except ValueError as exc:
            return Result.fail(str(exc))
        for item in open_items:
            item.mark_filed()
            await self._liabilities.save(item)
        await self._returns.save(tax_return)
        await publish_integration_event(filed)
        return Result.ok(tax_return.to_dict())
