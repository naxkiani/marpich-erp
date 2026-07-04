"""Aggregate root — invariants live here."""
from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class ExampleAggregate:
    id: str
    tenant_id: str
    name: str
    _events: list[object] = field(default_factory=list, repr=False)

    @classmethod
    def create(cls, tenant_id: str, name: str) -> ExampleAggregate:
        return cls(id=str(uuid4()), tenant_id=tenant_id, name=name.strip())
