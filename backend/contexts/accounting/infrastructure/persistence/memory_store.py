"""Accounting in-memory persistence."""
from __future__ import annotations

from contexts.accounting.domain.aggregates.billing_encounter import BillingEncounter
from contexts.accounting.domain.ports.repositories import IBillingRepository
from shared.domain.value_objects.unique_id import UniqueId


class AccountingMemoryStore:
    billings: dict[str, BillingEncounter] = {}

    @classmethod
    def reset(cls) -> None:
        cls.billings.clear()


class InMemoryBillingRepository(IBillingRepository):
    async def save(self, billing: BillingEncounter) -> None:
        AccountingMemoryStore.billings[str(billing.id)] = billing

    async def find_by_id(self, tenant_id: str, billing_id: UniqueId) -> BillingEncounter | None:
        b = AccountingMemoryStore.billings.get(str(billing_id))
        return b if b and b.tenant_id == tenant_id else None

    async def find_by_external_encounter(
        self, tenant_id: str, external_encounter_id: str
    ) -> BillingEncounter | None:
        for b in AccountingMemoryStore.billings.values():
            if b.tenant_id == tenant_id and b.external_encounter_id == external_encounter_id:
                return b
        return None

    async def list_billings(self, tenant_id: str) -> list[BillingEncounter]:
        return [b for b in AccountingMemoryStore.billings.values() if b.tenant_id == tenant_id]
