"""P215-R aggregates — quantum strategy / compliance / risk / executive invariants."""
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
class QuantumGovernancePlatformRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.strategy.quantum_governance_platform_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "quantum.strategy.quantum_governance_platform_is_missing", "GovernancePolicyChangedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumStrategyPlatformRoot(AggregateRoot):
    tenant_id: str; strategy_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, strategy_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.strategy.quantum_strategy_platform_is_missing")
        return _mk(cls, tenant_id, "strategy_ref", strategy_ref, "quantum.strategy.quantum_strategy_platform_is_missing", "QuantumStrategyCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumComplianceIntelligenceRoot(AggregateRoot):
    tenant_id: str; compliance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, compliance_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.strategy.quantum_compliance_intelligence_is_missing")
        return _mk(cls, tenant_id, "compliance_ref", compliance_ref, "quantum.strategy.quantum_compliance_intelligence_is_missing", "ComplianceValidatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumRiskIntelligenceRoot(AggregateRoot):
    tenant_id: str; risk_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, risk_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.strategy.quantum_risk_intelligence_is_missing")
        return _mk(cls, tenant_id, "risk_ref", risk_ref, "quantum.strategy.quantum_risk_intelligence_is_missing", "RiskAssessmentCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumExecutiveIntelligenceRoot(AggregateRoot):
    tenant_id: str; executive_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, executive_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.strategy.quantum_executive_intelligence_is_missing")
        return _mk(cls, tenant_id, "executive_ref", executive_ref, "quantum.strategy.quantum_executive_intelligence_is_missing", "ExecutiveDecisionGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumPolicyManagementRoot(AggregateRoot):
    tenant_id: str; policy_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, policy_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.strategy.quantum_policy_management_is_missing")
        return _mk(cls, tenant_id, "policy_ref", policy_ref, "quantum.strategy.quantum_policy_management_is_missing", "GovernancePolicyChangedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumTrustFrameworkRoot(AggregateRoot):
    tenant_id: str; trust_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, trust_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.strategy.quantum_trust_framework_is_missing")
        return _mk(cls, tenant_id, "trust_ref", trust_ref, "quantum.strategy.quantum_trust_framework_is_missing", "ComplianceValidatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class StrategyKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.strategy.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.strategy.knowledge_graph_integration_is_missing", "QuantumStrategyCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class StrategyDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.strategy.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.strategy.digital_twin_integration_is_missing", "RiskAssessmentCompletedEvent")
    def is_missing(self)->bool: return not self.present
