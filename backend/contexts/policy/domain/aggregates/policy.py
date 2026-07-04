"""Policy aggregate — stable key per tenant + domain."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class Policy(AggregateRoot):
    tenant_id: str
    domain: str
    key: str
    name: str
    description: str | None = None
    organization_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        domain: str,
        key: str,
        name: str,
        description: str | None = None,
        organization_id: str | None = None,
    ) -> Policy:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            domain=domain.strip().lower(),
            key=key.strip().lower(),
            name=name.strip(),
            description=description,
            organization_id=organization_id,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "domain": self.domain,
            "key": self.key,
            "name": self.name,
            "description": self.description,
            "organization_id": self.organization_id,
            "created_at": self.created_at.isoformat(),
        }
