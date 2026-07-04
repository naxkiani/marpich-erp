"""Accounting repository port."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.accounting.domain.aggregates.billing_encounter import BillingEncounter
from shared.domain.value_objects.unique_id import UniqueId


class IBillingRepository(ABC):
    @abstractmethod
    async def save(self, billing: BillingEncounter) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, billing_id: UniqueId) -> BillingEncounter | None: ...

    @abstractmethod
    async def find_by_external_encounter(
        self, tenant_id: str, external_encounter_id: str
    ) -> BillingEncounter | None: ...

    @abstractmethod
    async def list_billings(self, tenant_id: str) -> list[BillingEncounter]: ...
