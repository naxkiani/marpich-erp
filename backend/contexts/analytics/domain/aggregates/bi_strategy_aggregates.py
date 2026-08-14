"""P213-A BI strategy aggregates — quality-gate invariants."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import UTC, datetime
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

@dataclass(eq=False, kw_only=True)
class BiStrategyProfileRoot(AggregateRoot):
    tenant_id: str
    strategy_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, strategy_ref: str, complete: bool = True):
        if not tenant_id.strip():
            raise ValueError("analytics.strategy.tenant_required")
        if not complete:
            raise ValueError("analytics.strategy.enterprise_bi_architecture_is_incomplete")
        root = cls(id=UniqueId.generate(), tenant_id=tenant_id.strip(), strategy_ref=strategy_ref.strip(), complete=True, status="published")
        root.pending_events.append("BiStrategyPublished")
        return root

    def is_incomplete(self) -> bool:
        return not self.complete
