"""P216-T aggregates — government robotics / digital government invariants."""
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
class GovernmentRoboticsRoot(AggregateRoot):
    tenant_id: str; robotics_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, robotics_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.government.government_robotics_platform_is_missing")
        return _mk(cls, tenant_id, "robotics_ref", robotics_ref, "robotics.government.government_robotics_platform_is_missing", "GovernmentAgentCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousPublicServicesRoot(AggregateRoot):
    tenant_id: str; services_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, services_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.government.autonomous_public_services_is_missing")
        return _mk(cls, tenant_id, "services_ref", services_ref, "robotics.government.autonomous_public_services_is_missing", "PublicServiceCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class DigitalGovernmentRoot(AggregateRoot):
    tenant_id: str; digital_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, digital_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.government.digital_government_intelligence_is_missing")
        return _mk(cls, tenant_id, "digital_ref", digital_ref, "robotics.government.digital_government_intelligence_is_missing", "CitizenInteractionEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SmartGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.government.smart_governance_automation_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "robotics.government.smart_governance_automation_is_missing", "GovernanceRiskDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CitizenIntelligenceRoot(AggregateRoot):
    tenant_id: str; citizen_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, citizen_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.government.citizen_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "citizen_ref", citizen_ref, "robotics.government.citizen_intelligence_platform_is_missing", "CitizenInteractionEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PolicyIntelligenceRoot(AggregateRoot):
    tenant_id: str; policy_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, policy_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.government.policy_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "policy_ref", policy_ref, "robotics.government.policy_intelligence_platform_is_missing", "PolicyImpactCalculatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class GovernmentDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.government.government_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "robotics.government.government_digital_twin_is_missing", "PolicyImpactCalculatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PublicKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.government.public_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "robotics.government.public_knowledge_graph_is_missing", "RegulationChangedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class GovernmentSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.government.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "robotics.government.security_architecture_is_missing", "GovernanceRiskDetectedEvent")
    def is_missing(self)->bool: return not self.present
