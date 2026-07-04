"""Translation bundle — locale-specific values for keys."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class TranslationBundle(AggregateRoot):
    tenant_id: str
    locale_code: str
    namespace: str
    entries: dict[str, str] = field(default_factory=dict)
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, locale_code: str, namespace: str) -> TranslationBundle:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            locale_code=locale_code.lower(),
            namespace=namespace.strip(),
        )

    def set_entry(self, key: str, value: str) -> None:
        self.entries[key] = value
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "locale_code": self.locale_code,
            "namespace": self.namespace,
            "entries": self.entries,
            "updated_at": self.updated_at.isoformat(),
        }
