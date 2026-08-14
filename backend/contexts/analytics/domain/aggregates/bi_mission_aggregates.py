"""P213-B BI mission aggregates — quality-gate invariants."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import UTC, datetime
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

@dataclass(eq=False, kw_only=True)
class BiMissionDefinedRoot(AggregateRoot):
    tenant_id: str
    mission_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, mission_ref: str, defined: bool = True):
        if not tenant_id.strip():
            raise ValueError("analytics.mission.tenant_required")
        if not defined:
            raise ValueError("analytics.mission.mission_is_undefined")
        root = cls(id=UniqueId.generate(), tenant_id=tenant_id.strip(), mission_ref=mission_ref.strip(), defined=True, status="published")
        root.pending_events.append("MissionPublished")
        return root

    def is_undefined(self) -> bool:
        return not self.defined
