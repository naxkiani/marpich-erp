"""P215-O aggregates — quantum testing / validation / benchmarking / certification invariants."""
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
class QuantumTestingPlatformRoot(AggregateRoot):
    tenant_id: str; testing_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, testing_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.quality.quantum_testing_platform_is_missing")
        return _mk(cls, tenant_id, "testing_ref", testing_ref, "quantum.quality.quantum_testing_platform_is_missing", "QuantumTestCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumValidationPlatformRoot(AggregateRoot):
    tenant_id: str; validation_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, validation_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.quality.quantum_validation_platform_is_missing")
        return _mk(cls, tenant_id, "validation_ref", validation_ref, "quantum.quality.quantum_validation_platform_is_missing", "ValidationCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumBenchmarkingPlatformRoot(AggregateRoot):
    tenant_id: str; benchmark_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, benchmark_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.quality.quantum_benchmarking_platform_is_missing")
        return _mk(cls, tenant_id, "benchmark_ref", benchmark_ref, "quantum.quality.quantum_benchmarking_platform_is_missing", "BenchmarkGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumQaPlatformRoot(AggregateRoot):
    tenant_id: str; qa_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, qa_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.quality.quantum_qa_platform_is_missing")
        return _mk(cls, tenant_id, "qa_ref", qa_ref, "quantum.quality.quantum_qa_platform_is_missing", "TestExecutionCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumCertificationPlatformRoot(AggregateRoot):
    tenant_id: str; certification_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, certification_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.quality.quantum_certification_platform_is_missing")
        return _mk(cls, tenant_id, "certification_ref", certification_ref, "quantum.quality.quantum_certification_platform_is_missing", "CertificationIssuedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QualityIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; intelligence_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, intelligence_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.quality.quality_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "intelligence_ref", intelligence_ref, "quantum.quality.quality_intelligence_platform_is_missing", "QualityImprovementTriggeredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QualityKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.quality.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.quality.knowledge_graph_integration_is_missing", "QuantumTestCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QualityDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.quality.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.quality.digital_twin_integration_is_missing", "BenchmarkGeneratedEvent")
    def is_missing(self)->bool: return not self.present
