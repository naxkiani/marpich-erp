"""POS terminal aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class TerminalStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass(eq=False, kw_only=True)
class Terminal(AggregateRoot):
    tenant_id: str
    terminal_code: str
    store_name: str
    status: TerminalStatus = TerminalStatus.ACTIVE
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(cls, *, tenant_id: str, terminal_code: str, store_name: str) -> Terminal:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            terminal_code=terminal_code.strip().upper(),
            store_name=store_name.strip(),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "terminal_code": self.terminal_code,
            "store_name": self.store_name,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
        }
