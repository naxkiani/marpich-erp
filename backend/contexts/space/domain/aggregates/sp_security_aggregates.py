"""P218-P aggregates — security intelligence invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


def _tid(tenant_id: str, code: str) -> str:
    if not tenant_id.strip():
        raise ValueError(code)
    return tenant_id.strip()


def _mk(root_cls, tenant_id: str, ref_name: str, ref_value: str, err: str, event: str):
    tid = _tid(tenant_id, err + ".tenant")
    obj = root_cls(
        id=UniqueId.generate(), tenant_id=tid, **{ref_name: ref_value.strip()},
        present=True, status="enabled",
    )
    obj.pending_events.append(event)
    return obj


@dataclass(eq=False, kw_only=True)
class SecurityPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("space.security.space_security_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "space.security.space_security_platform_is_missing", "ThreatDetectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CybersecurityRoot(AggregateRoot):
    tenant_id: str; cyber_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, cyber_ref: str, present: bool = True):
        if not present: raise ValueError("space.security.space_cybersecurity_is_missing")
        return _mk(cls, tenant_id, "cyber_ref", cyber_ref, "space.security.space_cybersecurity_is_missing", "CyberAttackIdentifiedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class SatelliteSecurityRoot(AggregateRoot):
    tenant_id: str; satellite_sec_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, satellite_sec_ref: str, present: bool = True):
        if not present: raise ValueError("space.security.satellite_security_is_missing")
        return _mk(cls, tenant_id, "satellite_sec_ref", satellite_sec_ref, "space.security.satellite_security_is_missing", "SatelliteIdentityVerifiedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class OrbitalDefenseRoot(AggregateRoot):
    tenant_id: str; orbital_defense_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, orbital_defense_ref: str, present: bool = True):
        if not present: raise ValueError("space.security.space_defense_intelligence_is_missing")
        return _mk(cls, tenant_id, "orbital_defense_ref", orbital_defense_ref, "space.security.space_defense_intelligence_is_missing", "AssetProtectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class ThreatIntelligenceRoot(AggregateRoot):
    tenant_id: str; threat_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, threat_ref: str, present: bool = True):
        if not present: raise ValueError("space.security.threat_intelligence_is_missing")
        return _mk(cls, tenant_id, "threat_ref", threat_ref, "space.security.threat_intelligence_is_missing", "ThreatNeutralizedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class AutonomousSecurityRoot(AggregateRoot):
    tenant_id: str; autonomy_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, autonomy_ref: str, present: bool = True):
        if not present: raise ValueError("space.security.autonomous_security_operations_is_missing")
        return _mk(cls, tenant_id, "autonomy_ref", autonomy_ref, "space.security.autonomous_security_operations_is_missing", "ResponseExecutedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class SecurityDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.security.security_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.security.security_digital_twin_is_missing", "RecoveryStartedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class SecurityKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("space.security.knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "space.security.knowledge_graph_is_missing", "IncidentCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class SecurityGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("space.security.governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "space.security.governance_is_missing", "SecurityPolicyActivatedEvent")
    def is_missing(self) -> bool: return not self.present
