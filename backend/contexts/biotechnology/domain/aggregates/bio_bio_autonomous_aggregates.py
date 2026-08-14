"""P217-U aggregates — biotechnology bio autonomous invariants."""
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
class BioAutonomousPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_autonomous.bio_autonomous_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "biotechnology.bio_autonomous.bio_autonomous_platform_is_missing", "BioAutonomousPlatformActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousBiologyRoot(AggregateRoot):
    tenant_id: str; biology_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, biology_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_autonomous.autonomous_biology_is_missing")
        return _mk(cls, tenant_id, "biology_ref", biology_ref, "biotechnology.bio_autonomous.autonomous_biology_is_missing", "AutonomousDecisionCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioAiAutonomyRoot(AggregateRoot):
    tenant_id: str; autonomy_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, autonomy_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_autonomous.bio_ai_autonomy_is_missing")
        return _mk(cls, tenant_id, "autonomy_ref", autonomy_ref, "biotechnology.bio_autonomous.bio_ai_autonomy_is_missing", "SystemAdaptedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SelfOptimizingEcosystemRoot(AggregateRoot):
    tenant_id: str; ecosystem_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ecosystem_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_autonomous.self_optimizing_ecosystem_is_missing")
        return _mk(cls, tenant_id, "ecosystem_ref", ecosystem_ref, "biotechnology.bio_autonomous.self_optimizing_ecosystem_is_missing", "OptimizationCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_autonomous.autonomous_bio_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "biotechnology.bio_autonomous.autonomous_bio_digital_twin_is_missing", "AutonomousActionApprovedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_autonomous.autonomous_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "biotechnology.bio_autonomous.autonomous_knowledge_graph_is_missing", "KnowledgeUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousAgentsRoot(AggregateRoot):
    tenant_id: str; agents_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, agents_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_autonomous.ai_autonomous_agents_are_missing")
        return _mk(cls, tenant_id, "agents_ref", agents_ref, "biotechnology.bio_autonomous.ai_autonomous_agents_are_missing", "SystemAdaptedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AdaptiveIntelligenceRoot(AggregateRoot):
    tenant_id: str; adaptive_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, adaptive_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_autonomous.adaptive_intelligence_is_missing")
        return _mk(cls, tenant_id, "adaptive_ref", adaptive_ref, "biotechnology.bio_autonomous.adaptive_intelligence_is_missing", "SystemAdaptedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomyGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_autonomous.safety_governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "biotechnology.bio_autonomous.safety_governance_is_missing", "HumanAutonomyOversightRequiredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioAutonomousGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_autonomous.governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "biotechnology.bio_autonomous.governance_is_missing", "AutonomyGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioAutonomousSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_autonomous.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "biotechnology.bio_autonomous.security_architecture_is_missing", "AutonomyGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present
