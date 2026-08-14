"""P217-S aggregates — biotechnology bio security invariants."""
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
class BioSecurityPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_security.bio_security_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "biotechnology.bio_security.bio_security_platform_is_missing", "BioSecurityPlatformActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioCybersecurityRoot(AggregateRoot):
    tenant_id: str; cybersecurity_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, cybersecurity_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_security.bio_cybersecurity_is_missing")
        return _mk(cls, tenant_id, "cybersecurity_ref", cybersecurity_ref, "biotechnology.bio_security.bio_cybersecurity_is_missing", "SecurityThreatDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BiologicalRiskRoot(AggregateRoot):
    tenant_id: str; risk_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, risk_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_security.biological_risk_intelligence_is_missing")
        return _mk(cls, tenant_id, "risk_ref", risk_ref, "biotechnology.bio_security.biological_risk_intelligence_is_missing", "RiskDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ThreatIntelligenceRoot(AggregateRoot):
    tenant_id: str; threat_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, threat_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_security.threat_intelligence_is_missing")
        return _mk(cls, tenant_id, "threat_ref", threat_ref, "biotechnology.bio_security.threat_intelligence_is_missing", "ProtectionActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ResilienceArchitectureRoot(AggregateRoot):
    tenant_id: str; resilience_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, resilience_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_security.resilience_architecture_is_missing")
        return _mk(cls, tenant_id, "resilience_ref", resilience_ref, "biotechnology.bio_security.resilience_architecture_is_missing", "RecoveryStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SecurityKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_security.security_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "biotechnology.bio_security.security_knowledge_graph_is_missing", "RiskResolvedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SecurityDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_security.security_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "biotechnology.bio_security.security_digital_twin_is_missing", "SystemRestoredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SecurityAgentsRoot(AggregateRoot):
    tenant_id: str; agents_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, agents_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_security.ai_agents_are_missing")
        return _mk(cls, tenant_id, "agents_ref", agents_ref, "biotechnology.bio_security.ai_agents_are_missing", "SecurityThreatDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioSecurityGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_security.governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "biotechnology.bio_security.governance_is_missing", "BioSecurityGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioSecuritySecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_security.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "biotechnology.bio_security.security_architecture_is_missing", "BioSecurityGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present
