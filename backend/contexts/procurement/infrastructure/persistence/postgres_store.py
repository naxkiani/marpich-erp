"""PostgreSQL repositories — Procurement bounded context."""
from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy import select

from contexts.procurement.domain.aggregates.purchase_requisition import (
    PurchaseRequisition,
    RequisitionStatus,
)
from contexts.procurement.domain.ports.repositories import IRequisitionRepository
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import ProcurementRequisitionRow


class PostgresRequisitionRepository(IRequisitionRepository):
    async def save(self, requisition: PurchaseRequisition) -> None:
        async with session_scope(tenant_id=requisition.tenant_id) as session:
            row = await session.get(ProcurementRequisitionRow, UUID(str(requisition.id)))
            if row is None:
                session.add(
                    ProcurementRequisitionRow(
                        id=UUID(str(requisition.id)),
                        tenant_id=requisition.tenant_id,
                        sku=requisition.sku,
                        quantity=requisition.quantity,
                        quantity_available=requisition.quantity_available,
                        reorder_threshold=requisition.reorder_threshold,
                        stock_id=UUID(str(requisition.stock_id)) if requisition.stock_id else None,
                        status=requisition.status.value,
                        reason=requisition.reason,
                        correlation_id=requisition.correlation_id,
                        created_at=requisition.created_at,
                        updated_at=requisition.updated_at,
                        submitted_at=requisition.submitted_at,
                        approved_at=requisition.approved_at,
                        received_at=requisition.received_at,
                    )
                )
            else:
                row.status = requisition.status.value
                row.quantity = requisition.quantity
                row.updated_at = requisition.updated_at
                row.submitted_at = requisition.submitted_at
                row.approved_at = requisition.approved_at
                row.received_at = requisition.received_at
                row.correlation_id = requisition.correlation_id

    async def find_by_id(
        self, tenant_id: str, requisition_id: UniqueId
    ) -> PurchaseRequisition | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.get(ProcurementRequisitionRow, UUID(str(requisition_id)))
            return _requisition_from_row(row) if row and row.tenant_id == tenant_id else None

    async def find_open_draft_by_sku(self, tenant_id: str, sku: str) -> PurchaseRequisition | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(ProcurementRequisitionRow).where(
                    ProcurementRequisitionRow.tenant_id == tenant_id,
                    ProcurementRequisitionRow.sku == sku.strip().upper(),
                    ProcurementRequisitionRow.status == RequisitionStatus.DRAFT.value,
                )
            )
            return _requisition_from_row(row) if row else None

    async def list_requisitions(self, tenant_id: str) -> list[PurchaseRequisition]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(ProcurementRequisitionRow).where(
                        ProcurementRequisitionRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_requisition_from_row(r) for r in rows]


def _requisition_from_row(row: ProcurementRequisitionRow) -> PurchaseRequisition:
    return PurchaseRequisition(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        sku=row.sku,
        quantity=Decimal(str(row.quantity)),
        quantity_available=Decimal(str(row.quantity_available)),
        reorder_threshold=Decimal(str(row.reorder_threshold)),
        stock_id=UniqueId.from_string(str(row.stock_id)) if row.stock_id else None,
        status=RequisitionStatus(row.status),
        reason=row.reason,
        correlation_id=row.correlation_id or "",
        created_at=row.created_at,
        updated_at=row.updated_at,
        submitted_at=row.submitted_at,
        approved_at=row.approved_at,
        received_at=getattr(row, "received_at", None),
    )
