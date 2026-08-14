"""P217-D aggregates — biotechnology infrastructure invariants."""
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
class BioInfrastructureRoot(AggregateRoot):
    tenant_id: str; infra_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, infra_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.infrastructure.bio_infrastructure_architecture_is_missing")
        return _mk(cls, tenant_id, "infra_ref", infra_ref, "biotechnology.infrastructure.bio_infrastructure_architecture_is_missing", "BioInfraProvisionedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ScientificComputingRoot(AggregateRoot):
    tenant_id: str; compute_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, compute_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.infrastructure.scientific_computing_platform_is_missing")
        return _mk(cls, tenant_id, "compute_ref", compute_ref, "biotechnology.infrastructure.scientific_computing_platform_is_missing", "ScientificWorkflowStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioCloudRoot(AggregateRoot):
    tenant_id: str; cloud_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, cloud_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.infrastructure.bio_cloud_architecture_is_missing")
        return _mk(cls, tenant_id, "cloud_ref", cloud_ref, "biotechnology.infrastructure.bio_cloud_architecture_is_missing", "BioInfraProvisionedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioDataInfraRoot(AggregateRoot):
    tenant_id: str; data_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, data_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.infrastructure.data_infrastructure_is_missing")
        return _mk(cls, tenant_id, "data_ref", data_ref, "biotechnology.infrastructure.data_infrastructure_is_missing", "BioInfraProvisionedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AiComputeRoot(AggregateRoot):
    tenant_id: str; ai_compute_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ai_compute_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.infrastructure.ai_compute_foundation_is_missing")
        return _mk(cls, tenant_id, "ai_compute_ref", ai_compute_ref, "biotechnology.infrastructure.ai_compute_foundation_is_missing", "GpuClusterScaledEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class LaboratoryIntegrationRoot(AggregateRoot):
    tenant_id: str; lab_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, lab_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.infrastructure.laboratory_integration_is_missing")
        return _mk(cls, tenant_id, "lab_ref", lab_ref, "biotechnology.infrastructure.laboratory_integration_is_missing", "LabDeviceConnectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class InfraSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.infrastructure.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "biotechnology.infrastructure.security_architecture_is_missing", "BioInfraSecurityViolationEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ObservabilityRoot(AggregateRoot):
    tenant_id: str; observability_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, observability_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.infrastructure.observability_architecture_is_missing")
        return _mk(cls, tenant_id, "observability_ref", observability_ref, "biotechnology.infrastructure.observability_architecture_is_missing", "BioInfraProvisionedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ResilienceRoot(AggregateRoot):
    tenant_id: str; resilience_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, resilience_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.infrastructure.disaster_recovery_is_missing")
        return _mk(cls, tenant_id, "resilience_ref", resilience_ref, "biotechnology.infrastructure.disaster_recovery_is_missing", "BioInfraRecoveredEvent")
    def is_missing(self)->bool: return not self.present
