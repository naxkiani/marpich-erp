"""P217-N aggregates — biotechnology bio regulatory invariants."""
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
class BioRegulatoryPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_regulatory.bio_regulatory_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "biotechnology.bio_regulatory.bio_regulatory_platform_is_missing", "BioRegulatoryPlatformActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class RegulatoryAiRoot(AggregateRoot):
    tenant_id: str; ai_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ai_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_regulatory.regulatory_ai_is_missing")
        return _mk(cls, tenant_id, "ai_ref", ai_ref, "biotechnology.bio_regulatory.regulatory_ai_is_missing", "RegulationUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BiomedicalComplianceRoot(AggregateRoot):
    tenant_id: str; compliance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, compliance_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_regulatory.biomedical_compliance_is_missing")
        return _mk(cls, tenant_id, "compliance_ref", compliance_ref, "biotechnology.bio_regulatory.biomedical_compliance_is_missing", "ComplianceApprovedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class LifeScienceGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_regulatory.life_science_governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "biotechnology.bio_regulatory.life_science_governance_is_missing", "BioRegulatoryGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class RegulatoryKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_regulatory.regulatory_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "biotechnology.bio_regulatory.regulatory_knowledge_graph_is_missing", "RequirementDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class RegulatoryDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_regulatory.digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "biotechnology.bio_regulatory.digital_twin_is_missing", "RegulatoryRiskDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class RegulatoryAgentsRoot(AggregateRoot):
    tenant_id: str; agents_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, agents_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_regulatory.ai_agents_are_missing")
        return _mk(cls, tenant_id, "agents_ref", agents_ref, "biotechnology.bio_regulatory.ai_agents_are_missing", "RiskResolvedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioRegulatoryEthicsRoot(AggregateRoot):
    tenant_id: str; ethics_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ethics_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_regulatory.ethics_is_missing")
        return _mk(cls, tenant_id, "ethics_ref", ethics_ref, "biotechnology.bio_regulatory.ethics_is_missing", "BioRegulatoryGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioRegulatorySecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_regulatory.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "biotechnology.bio_regulatory.security_architecture_is_missing", "ComplianceViolationDetectedEvent")
    def is_missing(self)->bool: return not self.present
