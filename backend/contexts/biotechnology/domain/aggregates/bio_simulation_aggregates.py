"""P217-G aggregates — biotechnology simulation invariants."""
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
class SimulationPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.simulation.bio_simulation_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "biotechnology.simulation.bio_simulation_platform_is_missing", "SimulationPlatformActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class DigitalTwinArchitectureRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.simulation.digital_twin_architecture_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "biotechnology.simulation.digital_twin_architecture_is_missing", "DigitalTwinCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SimulationEngineRoot(AggregateRoot):
    tenant_id: str; engine_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, engine_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.simulation.computational_simulation_engine_is_missing")
        return _mk(cls, tenant_id, "engine_ref", engine_ref, "biotechnology.simulation.computational_simulation_engine_is_missing", "SimulationStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class LifeModelingFrameworkRoot(AggregateRoot):
    tenant_id: str; modeling_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, modeling_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.simulation.life_modeling_framework_is_missing")
        return _mk(cls, tenant_id, "modeling_ref", modeling_ref, "biotechnology.simulation.life_modeling_framework_is_missing", "ModelImprovedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SimulationIntelligenceRoot(AggregateRoot):
    tenant_id: str; intelligence_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, intelligence_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.simulation.multi_scale_architecture_is_missing")
        return _mk(cls, tenant_id, "intelligence_ref", intelligence_ref, "biotechnology.simulation.multi_scale_architecture_is_missing", "PredictionGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SimulationModelLifecycleRoot(AggregateRoot):
    tenant_id: str; lifecycle_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, lifecycle_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.simulation.ai_integration_is_missing")
        return _mk(cls, tenant_id, "lifecycle_ref", lifecycle_ref, "biotechnology.simulation.ai_integration_is_missing", "SimulationModelCertifiedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SimulationDomainModelRoot(AggregateRoot):
    tenant_id: str; domain_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, domain_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.simulation.life_modeling_framework_is_missing")
        return _mk(cls, tenant_id, "domain_ref", domain_ref, "biotechnology.simulation.life_modeling_framework_is_missing", "SimulationCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SimulationGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.simulation.governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "biotechnology.simulation.governance_is_missing", "SimulationModelCertifiedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SimulationSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.simulation.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "biotechnology.simulation.security_architecture_is_missing", "SimulationGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present
