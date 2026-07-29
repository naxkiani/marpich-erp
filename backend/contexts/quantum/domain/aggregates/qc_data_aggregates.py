"""P215-I aggregates — quantum data intelligence invariants."""
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
class DataIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; data_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, data_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.data.quantum_data_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "data_ref", data_ref, "quantum.data.quantum_data_intelligence_platform_is_missing", "QuantumDataRegisteredEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class KnowledgeGraphPlatformRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.data.quantum_knowledge_graph_platform_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.data.quantum_knowledge_graph_platform_is_missing", "KnowledgeEntityCreatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class DataGovernancePlatformRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.data.quantum_data_governance_platform_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "quantum.data.quantum_data_governance_platform_is_missing", "PolicyAppliedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class DataMeshRoot(AggregateRoot):
    tenant_id: str; mesh_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, mesh_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.data.quantum_data_mesh_architecture_is_missing")
        return _mk(cls, tenant_id, "mesh_ref", mesh_ref, "quantum.data.quantum_data_mesh_architecture_is_missing", "DataProductPublishedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class DataProductPlatformRoot(AggregateRoot):
    tenant_id: str; product_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, product_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.data.quantum_data_product_platform_is_missing")
        return _mk(cls, tenant_id, "product_ref", product_ref, "quantum.data.quantum_data_product_platform_is_missing", "QuantumDataProductCreatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class MetadataIntelligenceRoot(AggregateRoot):
    tenant_id: str; metadata_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, metadata_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.data.metadata_intelligence_is_missing")
        return _mk(cls, tenant_id, "metadata_ref", metadata_ref, "quantum.data.metadata_intelligence_is_missing", "MetadataDiscoveredEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class DataQualityRoot(AggregateRoot):
    tenant_id: str; quality_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, quality_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.data.data_quality_intelligence_is_missing")
        return _mk(cls, tenant_id, "quality_ref", quality_ref, "quantum.data.data_quality_intelligence_is_missing", "DataQualityValidatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class DataLineageRoot(AggregateRoot):
    tenant_id: str; lineage_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, lineage_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.data.data_lineage_intelligence_is_missing")
        return _mk(cls, tenant_id, "lineage_ref", lineage_ref, "quantum.data.data_lineage_intelligence_is_missing", "QuantumLineageDiscoveredEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class DataTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.data.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.data.digital_twin_integration_is_missing", "QuantumDataRegisteredEvent")
    def is_missing(self)->bool: return not self.present
