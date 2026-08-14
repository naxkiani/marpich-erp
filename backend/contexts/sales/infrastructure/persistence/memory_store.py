"""Sales in-memory repositories."""
from __future__ import annotations

from contexts.sales.domain.aggregates.quotation import Quotation
from contexts.sales.domain.aggregates.sales_order import SalesOrder
from contexts.sales.domain.ports.repositories import IQuotationRepository, ISalesOrderRepository
from shared.domain.value_objects.unique_id import UniqueId


class SalesMemoryStore:
    quotations: dict[str, Quotation] = {}
    orders: dict[str, SalesOrder] = {}

    @classmethod
    def reset(cls) -> None:
        cls.quotations.clear()
        cls.orders.clear()


class InMemoryQuotationRepository(IQuotationRepository):
    async def save(self, quotation: Quotation) -> None:
        SalesMemoryStore.quotations[str(quotation.id)] = quotation

    async def find_by_id(self, tenant_id: str, quotation_id: UniqueId) -> Quotation | None:
        q = SalesMemoryStore.quotations.get(str(quotation_id))
        return q if q and q.tenant_id == tenant_id else None

    async def find_by_opportunity(
        self, tenant_id: str, opportunity_id: UniqueId
    ) -> Quotation | None:
        for q in SalesMemoryStore.quotations.values():
            if (
                q.tenant_id == tenant_id
                and q.opportunity_id
                and str(q.opportunity_id) == str(opportunity_id)
            ):
                return q
        return None

    async def list_quotations(self, tenant_id: str) -> list[Quotation]:
        items = [q for q in SalesMemoryStore.quotations.values() if q.tenant_id == tenant_id]
        return sorted(items, key=lambda q: q.created_at, reverse=True)


class InMemorySalesOrderRepository(ISalesOrderRepository):
    async def save(self, order: SalesOrder) -> None:
        SalesMemoryStore.orders[str(order.id)] = order

    async def find_by_id(self, tenant_id: str, order_id: UniqueId) -> SalesOrder | None:
        o = SalesMemoryStore.orders.get(str(order_id))
        return o if o and o.tenant_id == tenant_id else None

    async def list_orders(self, tenant_id: str) -> list[SalesOrder]:
        items = [o for o in SalesMemoryStore.orders.values() if o.tenant_id == tenant_id]
        return sorted(items, key=lambda o: o.created_at, reverse=True)
