"""P216-L aggregates — public safety / civil protection invariants."""
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
    obj = root_cls(id=UniqueId.generate(), tenant_id=tid, **{ref_name: ref_value.strip()}, present=True, status="enabled")
    obj.pending_events.append(event)
    return obj

@dataclass(eq=False, kw_only=True)
class PublicSafetyRoboticsRoot(AggregateRoot):
    tenant_id: str; robotics_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, robotics_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.public_safety.public_safety_robotics_platform_is_missing")
        return _mk(cls, tenant_id, "robotics_ref", robotics_ref, "robotics.public_safety.public_safety_robotics_platform_is_missing", "DroneSurveyCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class EmergencyResponseRoot(AggregateRoot):
    tenant_id: str; emergency_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, emergency_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.public_safety.emergency_response_platform_is_missing")
        return _mk(cls, tenant_id, "emergency_ref", emergency_ref, "robotics.public_safety.emergency_response_platform_is_missing", "EmergencyActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class DisasterRecoveryRoot(AggregateRoot):
    tenant_id: str; recovery_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, recovery_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.public_safety.disaster_recovery_platform_is_missing")
        return _mk(cls, tenant_id, "recovery_ref", recovery_ref, "robotics.public_safety.disaster_recovery_platform_is_missing", "RecoveryInitiatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CivilProtectionRoot(AggregateRoot):
    tenant_id: str; protection_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, protection_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.public_safety.civil_protection_platform_is_missing")
        return _mk(cls, tenant_id, "protection_ref", protection_ref, "robotics.public_safety.civil_protection_platform_is_missing", "IncidentReportedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SituationIntelligenceRoot(AggregateRoot):
    tenant_id: str; intelligence_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, intelligence_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.public_safety.situation_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "intelligence_ref", intelligence_ref, "robotics.public_safety.situation_intelligence_platform_is_missing", "IncidentReportedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class DisasterDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.public_safety.disaster_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "robotics.public_safety.disaster_digital_twin_is_missing", "DroneSurveyCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PublicSafetyKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.public_safety.public_safety_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "robotics.public_safety.public_safety_knowledge_graph_is_missing", "AfterActionReviewCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PublicSafetySecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.public_safety.zero_trust_security_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "robotics.public_safety.zero_trust_security_is_missing", "EmergencyActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MultiRegionResilienceRoot(AggregateRoot):
    tenant_id: str; resilience_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, resilience_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.public_safety.multi_region_resilience_is_missing")
        return _mk(cls, tenant_id, "resilience_ref", resilience_ref, "robotics.public_safety.multi_region_resilience_is_missing", "InfrastructureRecoveredEvent")
    def is_missing(self)->bool: return not self.present
