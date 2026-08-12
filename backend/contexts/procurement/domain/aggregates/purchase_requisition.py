"""Purchase requisition aggregate — CAP-ENT-040 Procurement Lifecycle."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum

from contexts.procurement.domain.events.integration_events import (
    PurchaseOrderApprovedIntegration,
    RequisitionCreatedIntegration,
    RequisitionSubmittedIntegration,
)
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId


class RequisitionStatus(StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    CANCELLED = "cancelled"


@dataclass(eq=False, kw_only=True)
class PurchaseRequisition(AggregateRoot):
    tenant_id: str
    sku: str
    quantity: Decimal
    quantity_available: Decimal
    reorder_threshold: Decimal
    reason: str
    stock_id: UniqueId | None = None
    status: RequisitionStatus = RequisitionStatus.DRAFT
    correlation_id: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    submitted_at: datetime | None = None
    approved_at: datetime | None = None

    @classmethod
    def draft_from_reorder(
        cls,
        *,
        tenant_id: str,
        sku: str,
        quantity: Decimal,
        quantity_available: Decimal,
        reorder_threshold: Decimal,
        stock_id: UniqueId | None,
        correlation_id: str,
    ) -> PurchaseRequisition:
        if quantity <= 0:
            raise ValueError("procurement.errors.invalid_quantity")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            sku=sku.strip().upper(),
            quantity=quantity,
            quantity_available=quantity_available,
            reorder_threshold=reorder_threshold,
            stock_id=stock_id,
            reason="inventory.reorder.triggered",
            correlation_id=correlation_id,
        )

    def created_event(self) -> RequisitionCreatedIntegration:
        return RequisitionCreatedIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=self.correlation_id,
            requisition_id=self.id,
            sku=self.sku,
            quantity=str(self.quantity),
            quantity_available=str(self.quantity_available),
            reorder_threshold=str(self.reorder_threshold),
        )

    def submit(self, *, correlation_id: str) -> RequisitionSubmittedIntegration:
        if self.status != RequisitionStatus.DRAFT:
            raise ValueError("procurement.errors.requisition_not_draft")
        self.status = RequisitionStatus.SUBMITTED
        self.submitted_at = datetime.now(UTC)
        self.updated_at = self.submitted_at
        self.correlation_id = correlation_id or self.correlation_id
        return RequisitionSubmittedIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=self.correlation_id,
            requisition_id=self.id,
            sku=self.sku,
            quantity=str(self.quantity),
        )

    def approve(self, *, correlation_id: str) -> PurchaseOrderApprovedIntegration:
        if self.status != RequisitionStatus.SUBMITTED:
            raise ValueError("procurement.errors.requisition_not_submitted")
        self.status = RequisitionStatus.APPROVED
        self.approved_at = datetime.now(UTC)
        self.updated_at = self.approved_at
        self.correlation_id = correlation_id or self.correlation_id
        return PurchaseOrderApprovedIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=self.correlation_id,
            requisition_id=self.id,
            sku=self.sku,
            quantity=str(self.quantity),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "sku": self.sku,
            "quantity": str(self.quantity),
            "quantity_available": str(self.quantity_available),
            "reorder_threshold": str(self.reorder_threshold),
            "stock_id": str(self.stock_id) if self.stock_id else None,
            "status": self.status.value,
            "reason": self.reason,
            "correlation_id": self.correlation_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "submitted_at": self.submitted_at.isoformat() if self.submitted_at else None,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
        }
