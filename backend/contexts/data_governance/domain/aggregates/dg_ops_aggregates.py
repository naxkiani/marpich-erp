"""P212-M Ops aggregates — quality-gate invariants."""
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
class DgOpsCqrsRoot(AggregateRoot):
    tenant_id: str
    cqrs_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, cqrs_ref: str, complete: bool = True
    ) -> "DgOpsCqrsRoot":
        tid = _tid(tenant_id, "data_governance.ops.tenant_0_required")
        if not complete:
            raise ValueError("data_governance.ops.cqrs_architecture_is_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            cqrs_ref=cqrs_ref.strip(),
            complete=True,
            status="ok",
        )
        root.pending_events.append("CommandExecutedEvent")
        root.history.append({"event": "DgOpsCqrsRoot"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete



@dataclass(eq=False, kw_only=True)
class DgOpsCommandSideRoot(AggregateRoot):
    tenant_id: str
    command_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls, *, tenant_id: str, command_ref: str, present: bool = True
    ) -> "DgOpsCommandSideRoot":
        tid = _tid(tenant_id, "data_governance.ops.tenant_1_required")
        if not present:
            raise ValueError("data_governance.ops.command_side_design_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            command_ref=command_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("CommandExecutedEvent")
        root.history.append({"event": "DgOpsCommandSideRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgOpsQuerySideRoot(AggregateRoot):
    tenant_id: str
    query_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls, *, tenant_id: str, query_ref: str, present: bool = True
    ) -> "DgOpsQuerySideRoot":
        tid = _tid(tenant_id, "data_governance.ops.tenant_2_required")
        if not present:
            raise ValueError("data_governance.ops.query_side_design_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            query_ref=query_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("ProjectionUpdatedEvent")
        root.history.append({"event": "DgOpsQuerySideRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgOpsEventSourcingRoot(AggregateRoot):
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
    ) -> "DgOpsEventSourcingRoot":
        tid = _tid(tenant_id, "data_governance.ops.tenant_3_required")
        if not present:
            raise ValueError("data_governance.ops.event_sourcing_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            es_ref=es_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("GovernanceStateChangedEvent")
        root.history.append({"event": "DgOpsEventSourcingRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgOpsEventBusRoot(AggregateRoot):
    tenant_id: str
    bus_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, bus_ref: str, present: bool = True
    ) -> "DgOpsEventBusRoot":
        tid = _tid(tenant_id, "data_governance.ops.tenant_4_required")
        if not present:
            raise ValueError("data_governance.ops.event_bus_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            bus_ref=bus_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("IntegrationEventPublishedEvent")
        root.history.append({"event": "DgOpsEventBusRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgOpsEventContractsRoot(AggregateRoot):
    tenant_id: str
    contract_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, contract_ref: str, present: bool = True
    ) -> "DgOpsEventContractsRoot":
        tid = _tid(tenant_id, "data_governance.ops.tenant_5_required")
        if not present:
            raise ValueError("data_governance.ops.event_contract_governance_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            contract_ref=contract_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("IntegrationEventPublishedEvent")
        root.history.append({"event": "DgOpsEventContractsRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgOpsMicroservicesRoot(AggregateRoot):
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
    ) -> "DgOpsMicroservicesRoot":
        tid = _tid(tenant_id, "data_governance.ops.tenant_6_required")
        if not present:
            raise ValueError("data_governance.ops.microservice_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ms_ref=ms_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("CommandExecutedEvent")
        root.history.append({"event": "DgOpsMicroservicesRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgOpsApiFirstRoot(AggregateRoot):
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
    ) -> "DgOpsApiFirstRoot":
        tid = _tid(tenant_id, "data_governance.ops.tenant_7_required")
        if not present:
            raise ValueError("data_governance.ops.api_first_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            api_ref=api_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("ProjectionUpdatedEvent")
        root.history.append({"event": "DgOpsApiFirstRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgOpsHexagonalRoot(AggregateRoot):
    tenant_id: str
    hex_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def align(
        cls, *, tenant_id: str, hex_ref: str, present: bool = True
    ) -> "DgOpsHexagonalRoot":
        tid = _tid(tenant_id, "data_governance.ops.tenant_8_required")
        if not present:
            raise ValueError("data_governance.ops.hexagonal_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            hex_ref=hex_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("CommandExecutedEvent")
        root.history.append({"event": "DgOpsHexagonalRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgOpsDgIntegrationRoot(AggregateRoot):
    tenant_id: str
    integ_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def integrate(
        cls, *, tenant_id: str, integ_ref: str, present: bool = True
    ) -> "DgOpsDgIntegrationRoot":
        tid = _tid(tenant_id, "data_governance.ops.tenant_9_required")
        if not present:
            raise ValueError("data_governance.ops.data_governance_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            integ_ref=integ_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("GovernanceStateChangedEvent")
        root.history.append({"event": "DgOpsDgIntegrationRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgOpsAiIntegrationRoot(AggregateRoot):
    tenant_id: str
    ai_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def integrate(
        cls, *, tenant_id: str, ai_ref: str, present: bool = True
    ) -> "DgOpsAiIntegrationRoot":
        tid = _tid(tenant_id, "data_governance.ops.tenant_10_required")
        if not present:
            raise ValueError("data_governance.ops.ai_governance_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ai_ref=ai_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("CommandExecutedEvent")
        root.history.append({"event": "DgOpsAiIntegrationRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgOpsTwinIntegrationRoot(AggregateRoot):
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
    ) -> "DgOpsTwinIntegrationRoot":
        tid = _tid(tenant_id, "data_governance.ops.tenant_11_required")
        if not present:
            raise ValueError("data_governance.ops.digital_twin_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("GovernanceStateChangedEvent")
        root.history.append({"event": "DgOpsTwinIntegrationRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgOpsMultiTenantRoot(AggregateRoot):
    tenant_id: str
    tenant_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def confirm(
        cls, *, tenant_id: str, tenant_ref: str, present: bool = True
    ) -> "DgOpsMultiTenantRoot":
        tid = _tid(tenant_id, "data_governance.ops.tenant_12_required")
        if not present:
            raise ValueError("data_governance.ops.multi_tenant_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            tenant_ref=tenant_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("IntegrationEventPublishedEvent")
        root.history.append({"event": "DgOpsMultiTenantRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgOpsObservabilityRoot(AggregateRoot):
    tenant_id: str
    obs_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, obs_ref: str, present: bool = True
    ) -> "DgOpsObservabilityRoot":
        tid = _tid(tenant_id, "data_governance.ops.tenant_13_required")
        if not present:
            raise ValueError("data_governance.ops.observability_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            obs_ref=obs_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("ProjectionUpdatedEvent")
        root.history.append({"event": "DgOpsObservabilityRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgOpsScalabilityRoot(AggregateRoot):
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
    ) -> "DgOpsScalabilityRoot":
        tid = _tid(tenant_id, "data_governance.ops.tenant_14_required")
        if not present:
            raise ValueError("data_governance.ops.enterprise_scalability_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            scale_ref=scale_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("CommandExecutedEvent")
        root.history.append({"event": "DgOpsScalabilityRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present
