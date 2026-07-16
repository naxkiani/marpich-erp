"""Laboratory in-memory repositories."""
from __future__ import annotations

from contexts.laboratory.domain.aggregates.sample import Sample
from contexts.laboratory.domain.aggregates.test_order import TestOrder
from contexts.laboratory.domain.ports.repositories import ISampleRepository, ITestOrderRepository
from shared.domain.value_objects.unique_id import UniqueId


class LaboratoryMemoryStore:
    orders: dict[str, TestOrder] = {}
    samples: dict[str, Sample] = {}

    @classmethod
    def reset(cls) -> None:
        cls.orders.clear()
        cls.samples.clear()


class InMemoryTestOrderRepository(ITestOrderRepository):
    async def save(self, order: TestOrder) -> None:
        LaboratoryMemoryStore.orders[str(order.id)] = order

    async def find_by_id(self, tenant_id: str, order_id: UniqueId) -> TestOrder | None:
        row = LaboratoryMemoryStore.orders.get(str(order_id))
        return row if row and row.tenant_id == tenant_id else None

    async def find_by_number(self, tenant_id: str, order_number: str) -> TestOrder | None:
        key = order_number.strip().upper()
        for row in LaboratoryMemoryStore.orders.values():
            if row.tenant_id == tenant_id and row.order_number == key:
                return row
        return None

    async def list_orders(self, tenant_id: str) -> list[TestOrder]:
        rows = [r for r in LaboratoryMemoryStore.orders.values() if r.tenant_id == tenant_id]
        return sorted(rows, key=lambda r: r.created_at, reverse=True)


class InMemorySampleRepository(ISampleRepository):
    async def save(self, sample: Sample) -> None:
        LaboratoryMemoryStore.samples[str(sample.id)] = sample

    async def list_samples(self, tenant_id: str) -> list[Sample]:
        rows = [r for r in LaboratoryMemoryStore.samples.values() if r.tenant_id == tenant_id]
        return sorted(rows, key=lambda r: r.received_at, reverse=True)
