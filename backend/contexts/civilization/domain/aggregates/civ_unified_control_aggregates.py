"""P219-Z aggregates — unified enterprise control plane invariants."""
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
class UnifiedEnterpriseControlPlaneRoot(AggregateRoot):
    tenant_id: str; control_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, control_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.unified_control.unified_enterprise_control_plane_is_missing")
        return _mk(
            cls, tenant_id, "control_ref", control_ref,
            "civilization.unified_control.unified_enterprise_control_plane_is_missing",
            "ControlPlaneActivatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class IntegratedEnterpriseIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; intel_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, intel_ref: str, present: bool = True):
        if not present:
            raise ValueError(
                "civilization.unified_control.integrated_enterprise_intelligence_platform_is_missing"
            )
        return _mk(
            cls, tenant_id, "intel_ref", intel_ref,
            "civilization.unified_control.integrated_enterprise_intelligence_platform_is_missing",
            "IntelligenceFederatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class UnifiedEnterpriseCoordinationPlatformRoot(AggregateRoot):
    tenant_id: str; coord_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, coord_ref: str, present: bool = True):
        if not present:
            raise ValueError(
                "civilization.unified_control.unified_enterprise_coordination_platform_is_missing"
            )
        return _mk(
            cls, tenant_id, "coord_ref", coord_ref,
            "civilization.unified_control.unified_enterprise_coordination_platform_is_missing",
            "CrossDomainOrchestrationStartedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EnterpriseGovernanceFabricRoot(AggregateRoot):
    tenant_id: str; fabric_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, fabric_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.unified_control.enterprise_governance_fabric_is_missing")
        return _mk(
            cls, tenant_id, "fabric_ref", fabric_ref,
            "civilization.unified_control.enterprise_governance_fabric_is_missing",
            "GovernanceFabricEnforcedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CrossDomainOrchestrationPlatformRoot(AggregateRoot):
    tenant_id: str; orch_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, orch_ref: str, present: bool = True):
        if not present:
            raise ValueError(
                "civilization.unified_control.cross_domain_orchestration_platform_is_missing"
            )
        return _mk(
            cls, tenant_id, "orch_ref", orch_ref,
            "civilization.unified_control.cross_domain_orchestration_platform_is_missing",
            "CrossDomainOrchestrationCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EnterpriseDigitalTwinFederationRoot(AggregateRoot):
    tenant_id: str; federation_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, federation_ref: str, present: bool = True):
        if not present:
            raise ValueError(
                "civilization.unified_control.enterprise_digital_twin_federation_is_missing"
            )
        return _mk(
            cls, tenant_id, "federation_ref", federation_ref,
            "civilization.unified_control.enterprise_digital_twin_federation_is_missing",
            "DigitalTwinsFederatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class StrategicDecisionSupportPlatformRoot(AggregateRoot):
    tenant_id: str; decision_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, decision_ref: str, present: bool = True):
        if not present:
            raise ValueError(
                "civilization.unified_control.strategic_decision_support_platform_is_missing"
            )
        return _mk(
            cls, tenant_id, "decision_ref", decision_ref,
            "civilization.unified_control.strategic_decision_support_platform_is_missing",
            "StrategicDecisionSupportPublishedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosUnifiedEnterpriseCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.unified_control.meos_unified_enterprise_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.unified_control.meos_unified_enterprise_core_is_missing",
            "HumanAuthorizationGrantedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class UnifiedControlKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.unified_control.unified_control_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.unified_control.unified_control_knowledge_graph_is_missing",
            "UnifiedKnowledgeGraphUpdatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present
