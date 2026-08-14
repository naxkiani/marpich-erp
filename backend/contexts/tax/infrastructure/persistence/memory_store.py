"""Tax in-memory repositories."""
from __future__ import annotations

from contexts.tax.domain.aggregates.tax_liability import TaxLiability, TaxLiabilityStatus
from contexts.tax.domain.aggregates.tax_return import TaxReturn
from contexts.tax.domain.ports.repositories import ITaxLiabilityRepository, ITaxReturnRepository
from shared.domain.value_objects.unique_id import UniqueId


class TaxMemoryStore:
    liabilities: dict[str, TaxLiability] = {}
    returns: dict[str, TaxReturn] = {}

    @classmethod
    def reset(cls) -> None:
        cls.liabilities.clear()
        cls.returns.clear()


class InMemoryTaxLiabilityRepository(ITaxLiabilityRepository):
    async def save(self, liability: TaxLiability) -> None:
        TaxMemoryStore.liabilities[str(liability.id)] = liability

    async def find_by_id(self, tenant_id: str, liability_id: UniqueId) -> TaxLiability | None:
        item = TaxMemoryStore.liabilities.get(str(liability_id))
        return item if item and item.tenant_id == tenant_id else None

    async def find_by_payroll_run(
        self, tenant_id: str, payroll_run_id: UniqueId
    ) -> TaxLiability | None:
        for item in TaxMemoryStore.liabilities.values():
            if item.tenant_id == tenant_id and str(item.payroll_run_id) == str(payroll_run_id):
                return item
        return None

    async def list_open(
        self, tenant_id: str, *, period_label: str | None = None
    ) -> list[TaxLiability]:
        items = [
            i
            for i in TaxMemoryStore.liabilities.values()
            if i.tenant_id == tenant_id and i.status == TaxLiabilityStatus.OPEN
        ]
        if period_label:
            label = period_label.strip()
            items = [i for i in items if i.period_label == label]
        return sorted(items, key=lambda i: i.created_at, reverse=True)

    async def list_all(self, tenant_id: str) -> list[TaxLiability]:
        items = [i for i in TaxMemoryStore.liabilities.values() if i.tenant_id == tenant_id]
        return sorted(items, key=lambda i: i.created_at, reverse=True)


class InMemoryTaxReturnRepository(ITaxReturnRepository):
    async def save(self, tax_return: TaxReturn) -> None:
        TaxMemoryStore.returns[str(tax_return.id)] = tax_return

    async def find_by_id(self, tenant_id: str, return_id: UniqueId) -> TaxReturn | None:
        item = TaxMemoryStore.returns.get(str(return_id))
        return item if item and item.tenant_id == tenant_id else None

    async def list_returns(self, tenant_id: str) -> list[TaxReturn]:
        items = [r for r in TaxMemoryStore.returns.values() if r.tenant_id == tenant_id]
        return sorted(items, key=lambda r: r.created_at, reverse=True)
