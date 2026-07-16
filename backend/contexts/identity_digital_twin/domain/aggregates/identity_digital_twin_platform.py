"""Identity Digital Twin aggregates; projections store references, never peer aggregates."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import UTC, datetime
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


def _now() -> datetime: return datetime.now(UTC)

@dataclass(eq=False, kw_only=True)
class DigitalTwin(AggregateRoot):
    tenant_id: str
    twin_ref: str
    identity_ref: str
    attributes: dict = field(default_factory=dict)
    role_refs: list[str] = field(default_factory=list)
    session_refs: list[str] = field(default_factory=list)
    federation_link_refs: list[str] = field(default_factory=list)
    lifecycle_state: str | None = None
    source_versions: dict[str, str] = field(default_factory=dict)
    updated_at: datetime = field(default_factory=_now)

    @classmethod
    def create(cls, *, tenant_id: str, twin_ref: str, identity_ref: str, attributes: dict | None = None) -> "DigitalTwin":
        return cls(id=UniqueId.generate(), tenant_id=tenant_id, twin_ref=twin_ref, identity_ref=identity_ref, attributes=attributes or {})

    def synchronize(self, projection: dict, source_event: str) -> None:
        for key in ("attributes", "role_refs", "session_refs", "federation_link_refs", "lifecycle_state"):
            if key in projection: setattr(self, key, projection[key])
        self.source_versions[source_event] = projection.get("source_version", _now().isoformat())
        self.updated_at = _now()

    def to_dict(self) -> dict:
        return {"twin_ref": self.twin_ref, "identity_ref": self.identity_ref, "attributes": self.attributes, "role_refs": self.role_refs, "session_refs": self.session_refs, "federation_link_refs": self.federation_link_refs, "lifecycle_state": self.lifecycle_state, "source_versions": self.source_versions, "updated_at": self.updated_at.isoformat()}

@dataclass(eq=False, kw_only=True)
class TwinSnapshot(AggregateRoot):
    tenant_id: str
    snapshot_ref: str
    twin_ref: str
    projection: dict
    source_event: str
    captured_at: datetime = field(default_factory=_now)
    def to_dict(self) -> dict: return {"snapshot_ref": self.snapshot_ref, "twin_ref": self.twin_ref, "projection": self.projection, "source_event": self.source_event, "captured_at": self.captured_at.isoformat()}

@dataclass(eq=False, kw_only=True)
class TwinSimulation(AggregateRoot):
    tenant_id: str
    simulation_ref: str
    twin_ref: str
    scenario_type: str
    proposed_change: dict
    outcome: dict = field(default_factory=dict)
    status: str = "completed"
    created_at: datetime = field(default_factory=_now)
    def to_dict(self) -> dict: return {"simulation_ref": self.simulation_ref, "twin_ref": self.twin_ref, "scenario_type": self.scenario_type, "proposed_change": self.proposed_change, "outcome": self.outcome, "status": self.status}

@dataclass(eq=False, kw_only=True)
class TwinDriftAlert(AggregateRoot):
    tenant_id: str
    alert_ref: str
    twin_ref: str
    source_event: str
    drift_fields: list[str]
    severity: str
    status: str = "open"
    detected_at: datetime = field(default_factory=_now)
    def to_dict(self) -> dict: return {"alert_ref": self.alert_ref, "twin_ref": self.twin_ref, "source_event": self.source_event, "drift_fields": self.drift_fields, "severity": self.severity, "status": self.status, "detected_at": self.detected_at.isoformat()}
