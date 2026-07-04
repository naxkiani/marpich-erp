"""POS receipt aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId

from contexts.pos.domain.events.integration_events import ReceiptIssuedIntegration


@dataclass(eq=False, kw_only=True)
class Receipt(AggregateRoot):
    tenant_id: str
    sale_id: UniqueId
    receipt_number: str
    payload: dict
    issued_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def issue(
        cls,
        *,
        tenant_id: str,
        sale_id: UniqueId,
        receipt_number: str,
        payload: dict,
        correlation_id: str,
    ) -> tuple[Receipt, ReceiptIssuedIntegration]:
        receipt = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            sale_id=sale_id,
            receipt_number=receipt_number,
            payload=payload,
        )
        event = ReceiptIssuedIntegration(
            tenant_id=TenantId.create(tenant_id),
            correlation_id=correlation_id,
            receipt_id=receipt.id,
            sale_id=sale_id,
            receipt_number=receipt_number,
        )
        return receipt, event

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "sale_id": str(self.sale_id),
            "receipt_number": self.receipt_number,
            "payload": self.payload,
            "issued_at": self.issued_at.isoformat(),
        }
