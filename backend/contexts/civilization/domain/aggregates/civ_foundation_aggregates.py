"""P219 aggregates — civilization OS foundation invariants."""
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
class CivilizationOperatingSystemRoot(AggregateRoot):
    tenant_id: str; cos_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, cos_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.foundation.civilization_operating_system_is_missing")
        return _mk(cls, tenant_id, "cos_ref", cos_ref, "civilization.foundation.civilization_operating_system_is_missing", "CivilizationInitializedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationOsKernelRoot(AggregateRoot):
    tenant_id: str; kernel_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kernel_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.foundation.civilization_os_kernel_is_missing")
        return _mk(cls, tenant_id, "kernel_ref", kernel_ref, "civilization.foundation.civilization_os_kernel_is_missing", "SystemConnectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class PlanetaryIntelligenceRoot(AggregateRoot):
    tenant_id: str; planetary_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, planetary_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.foundation.planetary_intelligence_governance_is_missing")
        return _mk(cls, tenant_id, "planetary_ref", planetary_ref, "civilization.foundation.planetary_intelligence_governance_is_missing", "PolicyEvaluatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class HumanCivilizationRoot(AggregateRoot):
    tenant_id: str; human_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, human_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.foundation.human_civilization_management_platform_is_missing")
        return _mk(cls, tenant_id, "human_ref", human_ref, "civilization.foundation.human_civilization_management_platform_is_missing", "SocialChangeDetectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class InfrastructureIntelligenceRoot(AggregateRoot):
    tenant_id: str; infra_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, infra_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.foundation.global_infrastructure_intelligence_is_missing")
        return _mk(cls, tenant_id, "infra_ref", infra_ref, "civilization.foundation.global_infrastructure_intelligence_is_missing", "InfrastructureOptimizedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.foundation.civilization_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "civilization.foundation.civilization_digital_twin_is_missing", "CivilizationScenarioGeneratedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.foundation.civilization_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "civilization.foundation.civilization_knowledge_graph_is_missing", "SystemConnectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.foundation.civilization_governance_architecture_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "civilization.foundation.civilization_governance_architecture_is_missing", "PolicyEvaluatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class MeosCivilizationOsCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.foundation.meos_civilization_os_core_is_missing")
        return _mk(cls, tenant_id, "core_ref", core_ref, "civilization.foundation.meos_civilization_os_core_is_missing", "EvolutionMilestoneReachedEvent")
    def is_missing(self) -> bool: return not self.present
