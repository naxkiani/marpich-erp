"""P210-L Ops fabric aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class CsOpsLooseCouplingRoot(AggregateRoot):
    tenant_id: str
    service_ref: str
    tightly_coupled: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def bind(
        cls,
        *,
        tenant_id: str,
        service_ref: str,
        tightly_coupled: bool = False,
    ) -> CsOpsLooseCouplingRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.ops.tenant_required")
        if tightly_coupled:
            raise ValueError("cyber_security.ops.services_tightly_coupled")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            service_ref=service_ref.strip(),
            tightly_coupled=False,
            status="bound",
        )
        root.pending_events.append("TightCouplingRejected")
        root.history.append({"event": "LooseCouplingEnforced"})
        return root

    def is_tightly_coupled(self) -> bool:
        return self.tightly_coupled


@dataclass(eq=False, kw_only=True)
class CsOpsImmutableEventsRoot(AggregateRoot):
    tenant_id: str
    event_ref: str
    immutable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def append(
        cls, *, tenant_id: str, event_ref: str, immutable: bool = True
    ) -> CsOpsImmutableEventsRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.ops.event_tenant_required")
        if not immutable:
            raise ValueError("cyber_security.ops.events_mutable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            event_ref=event_ref.strip(),
            immutable=True,
            status="appended",
        )
        root.pending_events.append("SecurityEventReceived")
        root.pending_events.append("MutableEventRejected")
        root.history.append({"event": "ImmutableEventAppended"})
        return root

    def is_mutable(self) -> bool:
        return not self.immutable


@dataclass(eq=False, kw_only=True)
class CsOpsSecuredApisRoot(AggregateRoot):
    tenant_id: str
    api_ref: str
    secured: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def protect(
        cls, *, tenant_id: str, api_ref: str, secured: bool = True
    ) -> CsOpsSecuredApisRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.ops.api_tenant_required")
        if not secured:
            raise ValueError("cyber_security.ops.apis_lack_security_controls")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            api_ref=api_ref.strip(),
            secured=True,
            status="protected",
        )
        root.pending_events.append("UnsecuredApiRejected")
        root.history.append({"event": "ApiSecurityControlsApplied"})
        return root

    def lacks_security(self) -> bool:
        return not self.secured


@dataclass(eq=False, kw_only=True)
class CsOpsCqrsSeparationRoot(AggregateRoot):
    tenant_id: str
    model_ref: str
    separated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enforce(
        cls, *, tenant_id: str, model_ref: str, separated: bool = True
    ) -> CsOpsCqrsSeparationRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.ops.cqrs_tenant_required")
        if not separated:
            raise ValueError("cyber_security.ops.cqrs_separation_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            model_ref=model_ref.strip(),
            separated=True,
            status="separated",
        )
        root.pending_events.append("IncompleteCqrsRejected")
        root.history.append({"event": "CqrsSeparationEnforced"})
        return root

    def is_incomplete(self) -> bool:
        return not self.separated


@dataclass(eq=False, kw_only=True)
class CsOpsIndependentScaleRoot(AggregateRoot):
    tenant_id: str
    service_ref: str
    independent: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, service_ref: str, independent: bool = True
    ) -> CsOpsIndependentScaleRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.ops.scale_tenant_required")
        if not independent:
            raise ValueError(
                "cyber_security.ops.microservices_cannot_scale_independently"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            service_ref=service_ref.strip(),
            independent=True,
            status="enabled",
        )
        root.pending_events.append("NonIndependentScaleRejected")
        root.history.append({"event": "IndependentScaleEnabled"})
        return root

    def cannot_scale_independently(self) -> bool:
        return not self.independent


@dataclass(eq=False, kw_only=True)
class CsOpsObservabilityRoot(AggregateRoot):
    tenant_id: str
    plane_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, plane_ref: str, present: bool = True
    ) -> CsOpsObservabilityRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.ops.obs_tenant_required")
        if not present:
            raise ValueError("cyber_security.ops.observability_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            plane_ref=plane_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("MissingObservabilityRejected")
        root.history.append({"event": "ObservabilityEnabled"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CsOpsAiIntegrableRoot(AggregateRoot):
    tenant_id: str
    integration_ref: str
    possible: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, integration_ref: str, possible: bool = True
    ) -> CsOpsAiIntegrableRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.ops.ai_tenant_required")
        if not possible:
            raise ValueError("cyber_security.ops.ai_integration_impossible")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            integration_ref=integration_ref.strip(),
            possible=True,
            status="enabled",
        )
        root.pending_events.append("AIInsightGenerated")
        root.pending_events.append("ImpossibleAiRejected")
        root.history.append({"event": "AiIntegrationEnabled"})
        return root

    def is_impossible(self) -> bool:
        return not self.possible


@dataclass(eq=False, kw_only=True)
class CsOpsEventGovernanceRoot(AggregateRoot):
    tenant_id: str
    schema_ref: str
    governed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def govern(
        cls, *, tenant_id: str, schema_ref: str, governed: bool = True
    ) -> CsOpsEventGovernanceRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.ops.gov_tenant_required")
        if not governed:
            raise ValueError("cyber_security.ops.event_governance_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            schema_ref=schema_ref.strip(),
            governed=True,
            status="governed",
        )
        root.pending_events.append("EventGoverned")
        root.pending_events.append("UngovernedEventRejected")
        root.history.append({"event": "EventGovernanceApplied"})
        return root

    def is_absent(self) -> bool:
        return not self.governed
