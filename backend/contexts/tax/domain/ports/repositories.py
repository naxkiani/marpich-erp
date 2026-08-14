"""Tax repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.tax.domain.aggregates.tax_liability import TaxLiability
from contexts.tax.domain.aggregates.tax_return import TaxReturn
from shared.domain.value_objects.unique_id import UniqueId


class ITaxLiabilityRepository(ABC):
    @abstractmethod
    async def save(self, liability: TaxLiability) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, liability_id: UniqueId) -> TaxLiability | None: ...

    @abstractmethod
    async def find_by_payroll_run(
        self, tenant_id: str, payroll_run_id: UniqueId
    ) -> TaxLiability | None: ...

    @abstractmethod
    async def list_open(self, tenant_id: str, *, period_label: str | None = None) -> list[TaxLiability]: ...

    @abstractmethod
    async def list_all(self, tenant_id: str) -> list[TaxLiability]: ...


class ITaxReturnRepository(ABC):
    @abstractmethod
    async def save(self, tax_return: TaxReturn) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, return_id: UniqueId) -> TaxReturn | None: ...

    @abstractmethod
    async def list_returns(self, tenant_id: str) -> list[TaxReturn]: ...
