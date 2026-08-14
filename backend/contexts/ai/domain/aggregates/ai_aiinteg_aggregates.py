"""P214-M aggregates — quality-gate invariants."""
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
class AiintegPlatformRoot(AggregateRoot):
    tenant_id: str
    platform_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiinteg.tenant_required")
        if not present:
            raise ValueError("ai.aiinteg.enterprise_ai_api_gateway_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            platform_ref=platform_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("APIRegisteredEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ServiceMeshRoot(AggregateRoot):
    tenant_id: str
    mesh_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, mesh_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiinteg.mesh_tenant_required")
        if not present:
            raise ValueError("ai.aiinteg.intelligent_service_mesh_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            mesh_ref=mesh_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ServiceConnectedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ModelServingRoot(AggregateRoot):
    tenant_id: str
    serving_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, serving_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiinteg.serving_tenant_required")
        if not present:
            raise ValueError("ai.aiinteg.model_serving_gateway_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            serving_ref=serving_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("RoutingChangedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AgentCommunicationRoot(AggregateRoot):
    tenant_id: str
    agent_comm_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, agent_comm_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiinteg.agent_tenant_required")
        if not present:
            raise ValueError("ai.aiinteg.agent_communication_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            agent_comm_ref=agent_comm_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("MessageDeliveredEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EventIntegrationRoot(AggregateRoot):
    tenant_id: str
    event_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, event_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiinteg.event_tenant_required")
        if not present:
            raise ValueError("ai.aiinteg.event_integration_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            event_ref=event_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("APIRegisteredEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class WorkflowIntegrationRoot(AggregateRoot):
    tenant_id: str
    workflow_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, workflow_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiinteg.wf_tenant_required")
        if not present:
            raise ValueError("ai.aiinteg.workflow_orchestration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            workflow_ref=workflow_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("CommunicationCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class IntegrationGovernanceRoot(AggregateRoot):
    tenant_id: str
    governance_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiinteg.gov_tenant_required")
        if not present:
            raise ValueError("ai.aiinteg.integration_governance_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            governance_ref=governance_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("PolicyViolationDetectedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class IntegrationDigitalTwinRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiinteg.twin_tenant_required")
        if not present:
            raise ValueError("ai.aiinteg.digital_twin_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("TrafficOptimizedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
