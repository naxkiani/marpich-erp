"""P219-T aggregates — civilization intelligence governance & alignment invariants."""
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
class CivilizationIntelligenceGovernancePlatformRoot(AggregateRoot):
    tenant_id: str; igov_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, igov_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.intel_gov.civilization_intelligence_governance_platform_is_missing")
        return _mk(
            cls, tenant_id, "igov_ref", igov_ref,
            "civilization.intel_gov.civilization_intelligence_governance_platform_is_missing",
            "GovernanceChangedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class StrategicAlignmentPlatformRoot(AggregateRoot):
    tenant_id: str; alignment_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, alignment_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.intel_gov.strategic_alignment_platform_is_missing")
        return _mk(
            cls, tenant_id, "alignment_ref", alignment_ref,
            "civilization.intel_gov.strategic_alignment_platform_is_missing",
            "AlignmentVerifiedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EnterprisePolicyIntelligenceRoot(AggregateRoot):
    tenant_id: str; policy_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, policy_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.intel_gov.enterprise_policy_intelligence_is_missing")
        return _mk(
            cls, tenant_id, "policy_ref", policy_ref,
            "civilization.intel_gov.enterprise_policy_intelligence_is_missing",
            "PolicyPublishedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class TrustAndComplianceFrameworkRoot(AggregateRoot):
    tenant_id: str; trust_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, trust_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.intel_gov.trust_and_compliance_framework_is_missing")
        return _mk(
            cls, tenant_id, "trust_ref", trust_ref,
            "civilization.intel_gov.trust_and_compliance_framework_is_missing",
            "ComplianceValidatedEvent",
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
            raise ValueError("civilization.intel_gov.decision_assurance_platform_is_missing")
        return _mk(
            cls, tenant_id, "assurance_ref", assurance_ref,
            "civilization.intel_gov.decision_assurance_platform_is_missing",
            "DecisionApprovedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class GovernanceDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.intel_gov.governance_digital_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.intel_gov.governance_digital_twin_is_missing",
            "GovernanceImprovedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosCivilizationGovernanceAlignmentIntelligenceCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.intel_gov.meos_civilization_governance_alignment_intelligence_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.intel_gov.meos_civilization_governance_alignment_intelligence_core_is_missing",
            "TrustCalculatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class GovernanceKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.intel_gov.governance_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.intel_gov.governance_knowledge_graph_is_missing",
            "ControlValidatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class IntelligenceGovernanceEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.intel_gov.intelligence_governance_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.intel_gov.intelligence_governance_event_architecture_is_missing",
            "AuditCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present

