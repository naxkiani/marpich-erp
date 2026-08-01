"""P215-S aggregates — quantum cyber defense / identity / zero trust / resilience invariants."""
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
class QuantumSecurityPlatformRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.resilience.quantum_security_platform_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "quantum.resilience.quantum_security_platform_is_missing", "SecurityPolicyUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PostQuantumCyberDefenseRoot(AggregateRoot):
    tenant_id: str; defense_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, defense_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.resilience.post_quantum_cyber_defense_is_missing")
        return _mk(cls, tenant_id, "defense_ref", defense_ref, "quantum.resilience.post_quantum_cyber_defense_is_missing", "DefenseExecutedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumIdentityFabricRoot(AggregateRoot):
    tenant_id: str; identity_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, identity_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.resilience.quantum_identity_fabric_is_missing")
        return _mk(cls, tenant_id, "identity_ref", identity_ref, "quantum.resilience.quantum_identity_fabric_is_missing", "IdentityAuthenticatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumZeroTrustRoot(AggregateRoot):
    tenant_id: str; zero_trust_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, zero_trust_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.resilience.quantum_zero_trust_is_missing")
        return _mk(cls, tenant_id, "zero_trust_ref", zero_trust_ref, "quantum.resilience.quantum_zero_trust_is_missing", "TrustEvaluationCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ThreatIntelligenceRoot(AggregateRoot):
    tenant_id: str; threat_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, threat_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.resilience.threat_intelligence_is_missing")
        return _mk(cls, tenant_id, "threat_ref", threat_ref, "quantum.resilience.threat_intelligence_is_missing", "ThreatDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SecurityOperationsRoot(AggregateRoot):
    tenant_id: str; soc_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, soc_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.resilience.security_operations_is_missing")
        return _mk(cls, tenant_id, "soc_ref", soc_ref, "quantum.resilience.security_operations_is_missing", "DefenseExecutedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ResilienceIntelligenceRoot(AggregateRoot):
    tenant_id: str; resilience_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, resilience_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.resilience.resilience_intelligence_is_missing")
        return _mk(cls, tenant_id, "resilience_ref", resilience_ref, "quantum.resilience.resilience_intelligence_is_missing", "ResilienceActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ResilienceKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.resilience.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.resilience.knowledge_graph_integration_is_missing", "ThreatDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ResilienceDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.resilience.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.resilience.digital_twin_integration_is_missing", "ResilienceActivatedEvent")
    def is_missing(self)->bool: return not self.present
