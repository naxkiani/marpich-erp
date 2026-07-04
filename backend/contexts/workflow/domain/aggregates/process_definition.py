"""Process definition — versioned approval flow template."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class ProcessDefinition(AggregateRoot):
    tenant_id: str
    key: str
    name: str
    version: int
    steps: list[dict]
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def deploy(
        cls,
        *,
        tenant_id: str,
        key: str,
        name: str,
        steps: list[dict],
        version: int = 1,
    ) -> ProcessDefinition:
        normalized_steps = []
        for index, step in enumerate(steps):
            normalized_steps.append(
                {
                    "key": step["key"],
                    "name": step["name"],
                    "order": index,
                }
            )
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            key=key.strip().lower(),
            name=name.strip(),
            version=version,
            steps=normalized_steps,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "key": self.key,
            "name": self.name,
            "version": self.version,
            "steps": self.steps,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }
