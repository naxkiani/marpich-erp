"""P219-Y aggregates — trust, ethics & alignment invariants."""
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
    obj = root_cls(
        id=UniqueId.generate(), tenant_id=tid,
        **{ref_name: ref_value.strip()}, present=True, status="enabled",
    )
    obj.pending_events.append(event)
    return obj


@dataclass(eq=False, kw_only=True)
class EnterpriseTrustPlatformRoot(AggregateRoot):
    tenant_id: str; trust_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, trust_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.trust_ethics.enterprise_trust_platform_is_missing")
        return _mk(
            cls, tenant_id, "trust_ref", trust_ref,
            "civilization.trust_ethics.enterprise_trust_platform_is_missing",
            "TrustEvaluatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EnterpriseEthicsFrameworkRoot(AggregateRoot):
    tenant_id: str; ethics_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, ethics_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.trust_ethics.enterprise_ethics_framework_is_missing")
        return _mk(
            cls, tenant_id, "ethics_ref", ethics_ref,
            "civilization.trust_ethics.enterprise_ethics_framework_is_missing",
            "EthicalImpactAssessedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EnterpriseAlignmentPlatformRoot(AggregateRoot):
    tenant_id: str; alignment_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, alignment_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.trust_ethics.enterprise_alignment_platform_is_missing")
        return _mk(
            cls, tenant_id, "alignment_ref", alignment_ref,
            "civilization.trust_ethics.enterprise_alignment_platform_is_missing",
            "AlignmentVerifiedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ContinuousCompliancePlatformRoot(AggregateRoot):
    tenant_id: str; compliance_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, compliance_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.trust_ethics.continuous_compliance_platform_is_missing")
        return _mk(
            cls, tenant_id, "compliance_ref", compliance_ref,
            "civilization.trust_ethics.continuous_compliance_platform_is_missing",
            "ComplianceCheckedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DecisionAssurancePlatformRoot(AggregateRoot):
    tenant_id: str; assurance_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, assurance_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.trust_ethics.decision_assurance_platform_is_missing")
        return _mk(
            cls, tenant_id, "assurance_ref", assurance_ref,
            "civilization.trust_ethics.decision_assurance_platform_is_missing",
            "AssuranceCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosTrustEthicsAlignmentCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.trust_ethics.meos_trust_ethics_alignment_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.trust_ethics.meos_trust_ethics_alignment_core_is_missing",
            "HumanApprovalGrantedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class TrustEthicsKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.trust_ethics.trust_ethics_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.trust_ethics.trust_ethics_knowledge_graph_is_missing",
            "AssuranceCasePublishedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class TrustEthicsEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.trust_ethics.trust_ethics_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.trust_ethics.trust_ethics_event_architecture_is_missing",
            "ExplainabilityTraceRecordedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class TrustEthicsDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.trust_ethics.trust_ethics_digital_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.trust_ethics.trust_ethics_digital_twin_is_missing",
            "ContinuousAssuranceCycleCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present
