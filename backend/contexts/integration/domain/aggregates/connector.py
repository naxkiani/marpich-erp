"""Third-party connector configuration."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class ConnectorType(StrEnum):
    CRM = "crm"
    ERP = "erp"
    CUSTOM = "custom"


@dataclass(eq=False, kw_only=True)
class Connector(AggregateRoot):
    tenant_id: str
    connector_type: ConnectorType
    name: str
    config: dict
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        connector_type: ConnectorType,
        name: str,
        config: dict | None = None,
        is_active: bool = True,
    ) -> Connector:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            connector_type=connector_type,
            name=name.strip(),
            config=config or {},
            is_active=is_active,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "connector_type": self.connector_type.value,
            "name": self.name,
            "config": self.config,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }
