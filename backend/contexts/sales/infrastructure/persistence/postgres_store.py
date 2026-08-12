"""PostgreSQL repositories — Sales bounded context."""
from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy import select

from contexts.sales.domain.aggregates.quotation import Quotation, QuotationStatus
from contexts.sales.domain.aggregates.sales_order import SalesOrder, SalesOrderStatus
from contexts.sales.domain.ports.repositories import IQuotationRepository, ISalesOrderRepository
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import SalesOrderRow, SalesQuotationRow


class PostgresQuotationRepository(IQuotationRepository):
    async def save(self, quotation: Quotation) -> None:
        async with session_scope(tenant_id=quotation.tenant_id) as session:
            row = await session.get(SalesQuotationRow, UUID(str(quotation.id)))
            if row is None:
                row = SalesQuotationRow(
                    id=UUID(str(quotation.id)),
                    tenant_id=quotation.tenant_id,
                    contact_id=UUID(str(quotation.contact_id)),
                    opportunity_id=UUID(str(quotation.opportunity_id))
                    if quotation.opportunity_id
                    else None,
                    title=quotation.title,
                    amount=quotation.amount,
                    currency=quotation.currency,
                    status=quotation.status.value,
                    sent_at=quotation.sent_at,
                    accepted_at=quotation.accepted_at,
                )
                session.add(row)
            else:
                row.title = quotation.title
                row.amount = quotation.amount
                row.currency = quotation.currency
                row.status = quotation.status.value
                row.sent_at = quotation.sent_at
                row.accepted_at = quotation.accepted_at
                row.updated_at = quotation.updated_at

    async def find_by_id(self, tenant_id: str, quotation_id: UniqueId) -> Quotation | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.get(SalesQuotationRow, UUID(str(quotation_id)))
            return _quotation_from_row(row) if row and row.tenant_id == tenant_id else None

    async def find_by_opportunity(
        self, tenant_id: str, opportunity_id: UniqueId
    ) -> Quotation | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(SalesQuotationRow).where(
                    SalesQuotationRow.tenant_id == tenant_id,
                    SalesQuotationRow.opportunity_id == UUID(str(opportunity_id)),
                )
            )
            return _quotation_from_row(row) if row else None

    async def list_quotations(self, tenant_id: str) -> list[Quotation]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(SalesQuotationRow).where(SalesQuotationRow.tenant_id == tenant_id)
                )
            ).all()
        return [_quotation_from_row(r) for r in rows]


class PostgresSalesOrderRepository(ISalesOrderRepository):
    async def save(self, order: SalesOrder) -> None:
        async with session_scope(tenant_id=order.tenant_id) as session:
            row = await session.get(SalesOrderRow, UUID(str(order.id)))
            if row is None:
                row = SalesOrderRow(
                    id=UUID(str(order.id)),
                    tenant_id=order.tenant_id,
                    contact_id=UUID(str(order.contact_id)),
                    quotation_id=UUID(str(order.quotation_id)) if order.quotation_id else None,
                    opportunity_id=UUID(str(order.opportunity_id)) if order.opportunity_id else None,
                    title=order.title,
                    amount=order.amount,
                    currency=order.currency,
                    status=order.status.value,
                )
                session.add(row)
            else:
                row.status = order.status.value
                row.updated_at = order.updated_at

    async def find_by_id(self, tenant_id: str, order_id: UniqueId) -> SalesOrder | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.get(SalesOrderRow, UUID(str(order_id)))
            return _order_from_row(row) if row and row.tenant_id == tenant_id else None

    async def list_orders(self, tenant_id: str) -> list[SalesOrder]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(SalesOrderRow).where(SalesOrderRow.tenant_id == tenant_id)
                )
            ).all()
        return [_order_from_row(r) for r in rows]


def _quotation_from_row(row: SalesQuotationRow) -> Quotation:
    return Quotation(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        contact_id=UniqueId.from_string(str(row.contact_id)),
        opportunity_id=UniqueId.from_string(str(row.opportunity_id)) if row.opportunity_id else None,
        title=row.title,
        amount=Decimal(str(row.amount)),
        currency=row.currency,
        status=QuotationStatus(row.status),
        created_at=row.created_at,
        updated_at=row.updated_at,
        sent_at=row.sent_at,
        accepted_at=row.accepted_at,
    )


def _order_from_row(row: SalesOrderRow) -> SalesOrder:
    return SalesOrder(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        contact_id=UniqueId.from_string(str(row.contact_id)),
        quotation_id=UniqueId.from_string(str(row.quotation_id)) if row.quotation_id else None,
        opportunity_id=UniqueId.from_string(str(row.opportunity_id)) if row.opportunity_id else None,
        title=row.title,
        amount=Decimal(str(row.amount)),
        currency=row.currency,
        status=SalesOrderStatus(row.status),
        created_at=row.created_at,
        updated_at=row.updated_at,
    )
