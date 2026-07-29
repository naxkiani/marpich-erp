"""P215-K Quantum Governance aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


def _tid(tenant_id: str, code: str) -> str:
    if not tenant_id.strip():
        raise ValueError(code)
    return tenant_id.strip()



@dataclass(eq=False, kw_only=True)
class QcGovernancePlatformRoot(AggregateRoot):
    tenant_id: str
    platform_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, platform_ref: str, complete: bool = True
    ) -> "QcGovernancePlatformRoot":
        tid = _tid(tenant_id, "quantum.governance.tenant_0_required")
        if not complete:
            raise ValueError("quantum.governance.quantum_governance_platform_is_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            platform_ref=platform_ref.strip(),
            complete=True,
            status="ok",
        )
        root.pending_events.append("QuantumPolicyCreatedEvent")
        root.history.append({"event": "QcGovernancePlatformRoot"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete



@dataclass(eq=False, kw_only=True)
class QcRegulatoryIntelligenceRoot(AggregateRoot):
    tenant_id: str
    regulation_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, regulation_ref: str, present: bool = True
    ) -> "QcRegulatoryIntelligenceRoot":
        tid = _tid(tenant_id, "quantum.governance.tenant_1_required")
        if not present:
            raise ValueError("quantum.governance.quantum_regulatory_intelligence_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            regulation_ref=regulation_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("RegulationChangedEvent")
        root.history.append({"event": "QcRegulatoryIntelligenceRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class QcResponsibleQuantumRoot(AggregateRoot):
    tenant_id: str
    responsible_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, responsible_ref: str, present: bool = True
    ) -> "QcResponsibleQuantumRoot":
        tid = _tid(tenant_id, "quantum.governance.tenant_2_required")
        if not present:
            raise ValueError("quantum.governance.responsible_quantum_computing_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            responsible_ref=responsible_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("EthicalReviewCompletedEvent")
        root.history.append({"event": "QcResponsibleQuantumRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class QcEthicsFrameworkRoot(AggregateRoot):
    tenant_id: str
    ethics_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, ethics_ref: str, present: bool = True
    ) -> "QcEthicsFrameworkRoot":
        tid = _tid(tenant_id, "quantum.governance.tenant_3_required")
        if not present:
            raise ValueError("quantum.governance.quantum_ethics_framework_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ethics_ref=ethics_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("EthicalReviewCompletedEvent")
        root.history.append({"event": "QcEthicsFrameworkRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class QcRiskManagementRoot(AggregateRoot):
    tenant_id: str
    risk_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, risk_ref: str, present: bool = True
    ) -> "QcRiskManagementRoot":
        tid = _tid(tenant_id, "quantum.governance.tenant_4_required")
        if not present:
            raise ValueError("quantum.governance.quantum_risk_management_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            risk_ref=risk_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("RiskAssessmentCompletedEvent")
        root.history.append({"event": "QcRiskManagementRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class QcComplianceAutomationRoot(AggregateRoot):
    tenant_id: str
    compliance_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, compliance_ref: str, present: bool = True
    ) -> "QcComplianceAutomationRoot":
        tid = _tid(tenant_id, "quantum.governance.tenant_5_required")
        if not present:
            raise ValueError("quantum.governance.quantum_compliance_automation_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            compliance_ref=compliance_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("ComplianceValidatedEvent")
        root.history.append({"event": "QcComplianceAutomationRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class QcAuditIntelligenceRoot(AggregateRoot):
    tenant_id: str
    audit_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, audit_ref: str, present: bool = True
    ) -> "QcAuditIntelligenceRoot":
        tid = _tid(tenant_id, "quantum.governance.tenant_6_required")
        if not present:
            raise ValueError("quantum.governance.quantum_audit_intelligence_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            audit_ref=audit_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("AuditExecutedEvent")
        root.history.append({"event": "QcAuditIntelligenceRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class QcAccountabilityRoot(AggregateRoot):
    tenant_id: str
    accountability_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, accountability_ref: str, present: bool = True
    ) -> "QcAccountabilityRoot":
        tid = _tid(tenant_id, "quantum.governance.tenant_7_required")
        if not present:
            raise ValueError("quantum.governance.accountability_framework_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            accountability_ref=accountability_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("EthicalReviewCompletedEvent")
        root.history.append({"event": "QcAccountabilityRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class QcKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str
    graph_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def integrate(
        cls, *, tenant_id: str, graph_ref: str, present: bool = True
    ) -> "QcKnowledgeGraphRoot":
        tid = _tid(tenant_id, "quantum.governance.tenant_8_required")
        if not present:
            raise ValueError("quantum.governance.knowledge_graph_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            graph_ref=graph_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("QuantumPolicyCreatedEvent")
        root.history.append({"event": "QcKnowledgeGraphRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class QcDigitalTwinRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def integrate(
        cls, *, tenant_id: str, twin_ref: str, present: bool = True
    ) -> "QcDigitalTwinRoot":
        tid = _tid(tenant_id, "quantum.governance.tenant_9_required")
        if not present:
            raise ValueError("quantum.governance.digital_twin_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("RiskAssessmentCompletedEvent")
        root.history.append({"event": "QcDigitalTwinRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class QcCqrsRoot(AggregateRoot):
    tenant_id: str
    cqrs_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def align(
        cls, *, tenant_id: str, cqrs_ref: str, present: bool = True
    ) -> "QcCqrsRoot":
        tid = _tid(tenant_id, "quantum.governance.tenant_10_required")
        if not present:
            raise ValueError("quantum.governance.cqrs_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            cqrs_ref=cqrs_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("QuantumPolicyCreatedEvent")
        root.history.append({"event": "QcCqrsRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class QcEventArchitectureRoot(AggregateRoot):
    tenant_id: str
    es_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, es_ref: str, present: bool = True
    ) -> "QcEventArchitectureRoot":
        tid = _tid(tenant_id, "quantum.governance.tenant_11_required")
        if not present:
            raise ValueError("quantum.governance.event_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            es_ref=es_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("AuditExecutedEvent")
        root.history.append({"event": "QcEventArchitectureRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class QcMicroservicesRoot(AggregateRoot):
    tenant_id: str
    ms_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def declare(
        cls, *, tenant_id: str, ms_ref: str, present: bool = True
    ) -> "QcMicroservicesRoot":
        tid = _tid(tenant_id, "quantum.governance.tenant_12_required")
        if not present:
            raise ValueError("quantum.governance.microservices_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ms_ref=ms_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("ComplianceValidatedEvent")
        root.history.append({"event": "QcMicroservicesRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class QcApiFirstRoot(AggregateRoot):
    tenant_id: str
    api_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def confirm(
        cls, *, tenant_id: str, api_ref: str, present: bool = True
    ) -> "QcApiFirstRoot":
        tid = _tid(tenant_id, "quantum.governance.tenant_13_required")
        if not present:
            raise ValueError("quantum.governance.api_first_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            api_ref=api_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("QuantumPolicyCreatedEvent")
        root.history.append({"event": "QcApiFirstRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class QcCloudNativeRoot(AggregateRoot):
    tenant_id: str
    cloud_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def confirm(
        cls, *, tenant_id: str, cloud_ref: str, present: bool = True
    ) -> "QcCloudNativeRoot":
        tid = _tid(tenant_id, "quantum.governance.tenant_14_required")
        if not present:
            raise ValueError("quantum.governance.cloud_native_governance_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            cloud_ref=cloud_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("RegulationChangedEvent")
        root.history.append({"event": "QcCloudNativeRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present
