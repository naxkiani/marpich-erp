"""P212-H Data Policy aggregates — quality-gate invariants."""
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
class DgPolicyArchitectureRoot(AggregateRoot):
    tenant_id: str
    architecture_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, architecture_ref: str, complete: bool = True
    ) -> "DgPolicyArchitectureRoot":
        tid = _tid(tenant_id, "data_governance.policies.tenant_0_required")
        if not complete:
            raise ValueError("data_governance.policies.data_policy_architecture_is_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            architecture_ref=architecture_ref.strip(),
            complete=True,
            status="ok",
        )
        root.pending_events.append("DataPolicyCreatedEvent")
        root.history.append({"event": "DgPolicyArchitectureRoot"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete



@dataclass(eq=False, kw_only=True)
class DgPolicyLifecycleRoot(AggregateRoot):
    tenant_id: str
    lifecycle_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, lifecycle_ref: str, present: bool = True
    ) -> "DgPolicyLifecycleRoot":
        tid = _tid(tenant_id, "data_governance.policies.tenant_1_required")
        if not present:
            raise ValueError("data_governance.policies.policy_lifecycle_management_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            lifecycle_ref=lifecycle_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("PolicyActivatedEvent")
        root.history.append({"event": "DgPolicyLifecycleRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgPolicyRuleEngineRoot(AggregateRoot):
    tenant_id: str
    engine_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, engine_ref: str, present: bool = True
    ) -> "DgPolicyRuleEngineRoot":
        tid = _tid(tenant_id, "data_governance.policies.tenant_2_required")
        if not present:
            raise ValueError("data_governance.policies.policy_rule_engine_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            engine_ref=engine_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("PolicyEvaluatedEvent")
        root.history.append({"event": "DgPolicyRuleEngineRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgGovernanceAutomationRoot(AggregateRoot):
    tenant_id: str
    automation_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, automation_ref: str, present: bool = True
    ) -> "DgGovernanceAutomationRoot":
        tid = _tid(tenant_id, "data_governance.policies.tenant_3_required")
        if not present:
            raise ValueError("data_governance.policies.governance_automation_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            automation_ref=automation_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("PolicyEvaluatedEvent")
        root.history.append({"event": "DgGovernanceAutomationRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgPolicyIntelligenceRoot(AggregateRoot):
    tenant_id: str
    intel_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, intel_ref: str, present: bool = True
    ) -> "DgPolicyIntelligenceRoot":
        tid = _tid(tenant_id, "data_governance.policies.tenant_4_required")
        if not present:
            raise ValueError("data_governance.policies.policy_intelligence_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            intel_ref=intel_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("PolicyEvaluatedEvent")
        root.history.append({"event": "DgPolicyIntelligenceRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgAiGovernanceRoot(AggregateRoot):
    tenant_id: str
    ai_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, ai_ref: str, present: bool = True
    ) -> "DgAiGovernanceRoot":
        tid = _tid(tenant_id, "data_governance.policies.tenant_5_required")
        if not present:
            raise ValueError("data_governance.policies.ai_governance_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ai_ref=ai_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataPolicyCreatedEvent")
        root.history.append({"event": "DgAiGovernanceRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgPolicyKnowledgeGraphRoot(AggregateRoot):
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
    ) -> "DgPolicyKnowledgeGraphRoot":
        tid = _tid(tenant_id, "data_governance.policies.tenant_6_required")
        if not present:
            raise ValueError("data_governance.policies.knowledge_graph_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            graph_ref=graph_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("PolicyApprovedEvent")
        root.history.append({"event": "DgPolicyKnowledgeGraphRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgPolicyDigitalTwinRoot(AggregateRoot):
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
    ) -> "DgPolicyDigitalTwinRoot":
        tid = _tid(tenant_id, "data_governance.policies.tenant_7_required")
        if not present:
            raise ValueError("data_governance.policies.digital_twin_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("PolicyViolationDetectedEvent")
        root.history.append({"event": "DgPolicyDigitalTwinRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgPolicyCqrsRoot(AggregateRoot):
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
    ) -> "DgPolicyCqrsRoot":
        tid = _tid(tenant_id, "data_governance.policies.tenant_8_required")
        if not present:
            raise ValueError("data_governance.policies.cqrs_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            cqrs_ref=cqrs_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("PolicyApprovedEvent")
        root.history.append({"event": "DgPolicyCqrsRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgPolicyEventSourcingRoot(AggregateRoot):
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
    ) -> "DgPolicyEventSourcingRoot":
        tid = _tid(tenant_id, "data_governance.policies.tenant_9_required")
        if not present:
            raise ValueError("data_governance.policies.event_sourcing_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            es_ref=es_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("PolicyRetiredEvent")
        root.history.append({"event": "DgPolicyEventSourcingRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgPolicyMicroservicesRoot(AggregateRoot):
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
    ) -> "DgPolicyMicroservicesRoot":
        tid = _tid(tenant_id, "data_governance.policies.tenant_10_required")
        if not present:
            raise ValueError("data_governance.policies.microservices_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ms_ref=ms_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("PolicyActivatedEvent")
        root.history.append({"event": "DgPolicyMicroservicesRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgPolicyZeroTrustRoot(AggregateRoot):
    tenant_id: str
    zt_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def confirm(
        cls, *, tenant_id: str, zt_ref: str, present: bool = True
    ) -> "DgPolicyZeroTrustRoot":
        tid = _tid(tenant_id, "data_governance.policies.tenant_11_required")
        if not present:
            raise ValueError("data_governance.policies.zero_trust_alignment_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            zt_ref=zt_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("PolicyExceptionGrantedEvent")
        root.history.append({"event": "DgPolicyZeroTrustRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgPolicyScalabilityRoot(AggregateRoot):
    tenant_id: str
    scale_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def confirm(
        cls, *, tenant_id: str, scale_ref: str, present: bool = True
    ) -> "DgPolicyScalabilityRoot":
        tid = _tid(tenant_id, "data_governance.policies.tenant_12_required")
        if not present:
            raise ValueError("data_governance.policies.enterprise_scalability_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            scale_ref=scale_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("PolicyViolationDetectedEvent")
        root.history.append({"event": "DgPolicyScalabilityRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present
