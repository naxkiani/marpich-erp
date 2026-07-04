"""Translation key aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class TranslationKey(AggregateRoot):
    tenant_id: str
    namespace: str
    key: str
    default_value: str
    description: str = ""
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        namespace: str,
        key: str,
        default_value: str,
        description: str = "",
    ) -> TranslationKey:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            namespace=namespace.strip(),
            key=key.strip(),
            default_value=default_value,
            description=description.strip(),
        )

    @property
    def qualified_key(self) -> str:
        return f"{self.namespace}.{self.key}"

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "namespace": self.namespace,
            "key": self.key,
            "qualified_key": self.qualified_key,
            "default_value": self.default_value,
            "description": self.description,
            "updated_at": self.updated_at.isoformat(),
        }
