"""Laboratory repository ports."""
from __future__ import annotations

from typing import Protocol

from contexts.laboratory.domain.aggregates.sample import Sample
from contexts.laboratory.domain.aggregates.test_order import TestOrder
from shared.domain.value_objects.unique_id import UniqueId


class ITestOrderRepository(Protocol):
    async def save(self, order: TestOrder) -> None: ...
    async def find_by_id(self, tenant_id: str, order_id: UniqueId) -> TestOrder | None: ...
    async def find_by_number(self, tenant_id: str, order_number: str) -> TestOrder | None: ...
    async def list_orders(self, tenant_id: str) -> list[TestOrder]: ...


class ISampleRepository(Protocol):
    async def save(self, sample: Sample) -> None: ...
    async def list_samples(self, tenant_id: str) -> list[Sample]: ...
