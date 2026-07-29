"""P214-Z aggregates - master intelligence nexus invariants."""
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
class SupremeControlPlaneRoot(AggregateRoot):
    tenant_id: str; control_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, control_ref: str, present: bool = True):
        if not present: raise ValueError("ai.master.supreme_ai_control_plane_is_missing")
        return _mk(cls, tenant_id, "control_ref", control_ref, "ai.master.supreme_ai_control_plane_is_missing", "MasterIntelligenceActivatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class MasterIntelligenceRoot(AggregateRoot):
    tenant_id: str; master_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, master_ref: str, present: bool = True):
        if not present: raise ValueError("ai.master.enterprise_ai_master_intelligence_architecture_is_missing")
        return _mk(cls, tenant_id, "master_ref", master_ref, "ai.master.enterprise_ai_master_intelligence_architecture_is_missing", "MasterIntelligenceActivatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class FederationRoot(AggregateRoot):
    tenant_id: str; federation_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, federation_ref: str, present: bool = True):
        if not present: raise ValueError("ai.master.ai_federation_layer_is_missing")
        return _mk(cls, tenant_id, "federation_ref", federation_ref, "ai.master.ai_federation_layer_is_missing", "PlatformFederatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class EnterpriseBrainRoot(AggregateRoot):
    tenant_id: str; brain_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, brain_ref: str, present: bool = True):
        if not present: raise ValueError("ai.master.autonomous_enterprise_brain_is_missing")
        return _mk(cls, tenant_id, "brain_ref", brain_ref, "ai.master.autonomous_enterprise_brain_is_missing", "DecisionGeneratedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class DecisionNexusRoot(AggregateRoot):
    tenant_id: str; decision_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, decision_ref: str, present: bool = True):
        if not present: raise ValueError("ai.master.decision_intelligence_nexus_is_missing")
        return _mk(cls, tenant_id, "decision_ref", decision_ref, "ai.master.decision_intelligence_nexus_is_missing", "DecisionGeneratedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class EvolutionCommandRoot(AggregateRoot):
    tenant_id: str; evolution_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, evolution_ref: str, present: bool = True):
        if not present: raise ValueError("ai.master.evolution_command_center_is_missing")
        return _mk(cls, tenant_id, "evolution_ref", evolution_ref, "ai.master.evolution_command_center_is_missing", "EvolutionTriggeredEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class MasterTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("ai.master.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "ai.master.digital_twin_integration_is_missing", "OptimizationCompletedEvent")
    def is_missing(self)->bool: return not self.present
