"""P215-J aggregates — quantum network/internet invariants."""
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
class QuantumInternetPlatformRoot(AggregateRoot):
    tenant_id: str; internet_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, internet_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.network.quantum_internet_platform_is_missing")
        return _mk(cls, tenant_id, "internet_ref", internet_ref, "quantum.network.quantum_internet_platform_is_missing", "QuantumNodeRegisteredEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class NetworkFabricRoot(AggregateRoot):
    tenant_id: str; fabric_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, fabric_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.network.quantum_network_fabric_is_missing")
        return _mk(cls, tenant_id, "fabric_ref", fabric_ref, "quantum.network.quantum_network_fabric_is_missing", "QuantumNetworkOptimizedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class CommunicationPlatformRoot(AggregateRoot):
    tenant_id: str; communication_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, communication_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.network.quantum_communication_platform_is_missing")
        return _mk(cls, tenant_id, "communication_ref", communication_ref, "quantum.network.quantum_communication_platform_is_missing", "QuantumCommunicationStartedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class NodeFederationRoot(AggregateRoot):
    tenant_id: str; federation_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, federation_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.network.quantum_node_federation_is_missing")
        return _mk(cls, tenant_id, "federation_ref", federation_ref, "quantum.network.quantum_node_federation_is_missing", "QuantumNodeRegisteredEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class RoutingIntelligenceRoot(AggregateRoot):
    tenant_id: str; routing_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, routing_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.network.quantum_routing_intelligence_is_missing")
        return _mk(cls, tenant_id, "routing_ref", routing_ref, "quantum.network.quantum_routing_intelligence_is_missing", "NetworkOptimizedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class NetworkControlPlaneRoot(AggregateRoot):
    tenant_id: str; control_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, control_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.network.quantum_network_control_plane_is_missing")
        return _mk(cls, tenant_id, "control_ref", control_ref, "quantum.network.quantum_network_control_plane_is_missing", "NetworkOptimizedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class NetworkSecurityIntegrationRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.network.quantum_security_integration_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "quantum.network.quantum_security_integration_is_missing", "NetworkFailureDetectedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class NetworkTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.network.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.network.digital_twin_integration_is_missing", "NetworkOptimizedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class NetworkKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.network.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.network.knowledge_graph_integration_is_missing", "QuantumNodeRegisteredEvent")
    def is_missing(self)->bool: return not self.present
