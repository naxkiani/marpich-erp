"""Sales repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.sales.domain.aggregates.quotation import Quotation
from contexts.sales.domain.aggregates.sales_order import SalesOrder
from shared.domain.value_objects.unique_id import UniqueId


class IQuotationRepository(ABC):
    @abstractmethod
    async def save(self, quotation: Quotation) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, quotation_id: UniqueId) -> Quotation | None: ...

    @abstractmethod
    async def find_by_opportunity(
        self, tenant_id: str, opportunity_id: UniqueId
    ) -> Quotation | None: ...

    @abstractmethod
    async def list_quotations(self, tenant_id: str) -> list[Quotation]: ...


class ISalesOrderRepository(ABC):
    @abstractmethod
    async def save(self, order: SalesOrder) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, order_id: UniqueId) -> SalesOrder | None: ...

    @abstractmethod
    async def list_orders(self, tenant_id: str) -> list[SalesOrder]: ...
