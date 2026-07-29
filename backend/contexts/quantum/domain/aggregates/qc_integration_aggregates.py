"""P215-M aggregates — quantum integration / API gateway / service mesh invariants."""
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
class QuantumIntegrationPlatformRoot(AggregateRoot):
    tenant_id: str; integration_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, integration_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.integration.quantum_integration_platform_is_missing")
        return _mk(cls, tenant_id, "integration_ref", integration_ref, "quantum.integration.quantum_integration_platform_is_missing", "IntegrationWorkflowStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumApiGatewayRoot(AggregateRoot):
    tenant_id: str; gateway_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, gateway_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.integration.quantum_api_gateway_is_missing")
        return _mk(cls, tenant_id, "gateway_ref", gateway_ref, "quantum.integration.quantum_api_gateway_is_missing", "QuantumAPIRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumServiceMeshRoot(AggregateRoot):
    tenant_id: str; mesh_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, mesh_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.integration.quantum_service_mesh_is_missing")
        return _mk(cls, tenant_id, "mesh_ref", mesh_ref, "quantum.integration.quantum_service_mesh_is_missing", "ServiceMeshNodeUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class HybridIntelligenceBridgeRoot(AggregateRoot):
    tenant_id: str; hybrid_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, hybrid_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.integration.hybrid_intelligence_bridge_is_missing")
        return _mk(cls, tenant_id, "hybrid_ref", hybrid_ref, "quantum.integration.hybrid_intelligence_bridge_is_missing", "IntegrationExecutedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class EventIntegrationBackboneRoot(AggregateRoot):
    tenant_id: str; event_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, event_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.integration.event_integration_backbone_is_missing")
        return _mk(cls, tenant_id, "event_ref", event_ref, "quantum.integration.event_integration_backbone_is_missing", "QuantumEventPublishedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CapabilityFederationRoot(AggregateRoot):
    tenant_id: str; capability_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, capability_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.integration.capability_federation_is_missing")
        return _mk(cls, tenant_id, "capability_ref", capability_ref, "quantum.integration.capability_federation_is_missing", "CapabilityRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class IntegrationKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.integration.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.integration.knowledge_graph_integration_is_missing", "QuantumAPIRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class IntegrationDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.integration.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.integration.digital_twin_integration_is_missing", "ServiceFailureDetectedEvent")
    def is_missing(self)->bool: return not self.present
