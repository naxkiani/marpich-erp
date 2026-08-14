"""Procurement repository ports."""
from __future__ import annotations

from typing import Protocol

from contexts.procurement.domain.aggregates.purchase_requisition import PurchaseRequisition
from shared.domain.value_objects.unique_id import UniqueId


class IRequisitionRepository(Protocol):
    async def save(self, requisition: PurchaseRequisition) -> None: ...

    async def find_by_id(
        self, tenant_id: str, requisition_id: UniqueId
    ) -> PurchaseRequisition | None: ...

    async def find_open_draft_by_sku(
        self, tenant_id: str, sku: str
    ) -> PurchaseRequisition | None: ...

    async def list_requisitions(self, tenant_id: str) -> list[PurchaseRequisition]: ...
