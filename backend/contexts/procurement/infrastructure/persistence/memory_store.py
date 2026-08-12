"""Procurement in-memory repositories."""
from __future__ import annotations

from contexts.procurement.domain.aggregates.purchase_requisition import (
    PurchaseRequisition,
    RequisitionStatus,
)
from contexts.procurement.domain.ports.repositories import IRequisitionRepository
from shared.domain.value_objects.unique_id import UniqueId


class ProcurementMemoryStore:
    requisitions: dict[str, PurchaseRequisition] = {}

    @classmethod
    def reset(cls) -> None:
        cls.requisitions.clear()


class InMemoryRequisitionRepository(IRequisitionRepository):
    async def save(self, requisition: PurchaseRequisition) -> None:
        ProcurementMemoryStore.requisitions[str(requisition.id)] = requisition

    async def find_by_id(
        self, tenant_id: str, requisition_id: UniqueId
    ) -> PurchaseRequisition | None:
        req = ProcurementMemoryStore.requisitions.get(str(requisition_id))
        return req if req and req.tenant_id == tenant_id else None

    async def find_open_draft_by_sku(self, tenant_id: str, sku: str) -> PurchaseRequisition | None:
        sku_key = sku.strip().upper()
        for req in ProcurementMemoryStore.requisitions.values():
            if (
                req.tenant_id == tenant_id
                and req.sku == sku_key
                and req.status == RequisitionStatus.DRAFT
            ):
                return req
        return None

    async def list_requisitions(self, tenant_id: str) -> list[PurchaseRequisition]:
        items = [r for r in ProcurementMemoryStore.requisitions.values() if r.tenant_id == tenant_id]
        return sorted(items, key=lambda r: r.created_at, reverse=True)
