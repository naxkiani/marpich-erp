"""P212-B Data Governance mission/scope aggregates — quality-gate invariants."""
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
class DgMissionDefinedRoot(AggregateRoot):
    tenant_id: str
    mission_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, mission_ref: str, defined: bool = True
    ) -> DgMissionDefinedRoot:
        tid = _tid(tenant_id, "data_governance.mission.tenant_required")
        if not defined:
            raise ValueError("data_governance.mission.mission_is_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            mission_ref=mission_ref.strip(),
            defined=True,
            status="published",
        )
        root.pending_events.append("MissionPublished")
        root.pending_events.append("UndefinedMissionRejected")
        root.history.append({"event": "MissionDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class DgVisionDefinedRoot(AggregateRoot):
    tenant_id: str
    vision_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, vision_ref: str, defined: bool = True
    ) -> DgVisionDefinedRoot:
        tid = _tid(tenant_id, "data_governance.mission.vision_tenant_required")
        if not defined:
            raise ValueError("data_governance.mission.vision_is_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            vision_ref=vision_ref.strip(),
            defined=True,
            status="published",
        )
        root.pending_events.append("VisionPublished")
        root.pending_events.append("UndefinedVisionRejected")
        root.history.append({"event": "VisionDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class DgEnterpriseScopeDefinedRoot(AggregateRoot):
    tenant_id: str
    scope_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def declare(
        cls, *, tenant_id: str, scope_ref: str, defined: bool = True
    ) -> DgEnterpriseScopeDefinedRoot:
        tid = _tid(tenant_id, "data_governance.mission.scope_tenant_required")
        if not defined:
            raise ValueError(
                "data_governance.mission.enterprise_scope_is_undefined"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            scope_ref=scope_ref.strip(),
            defined=True,
            status="declared",
        )
        root.pending_events.append("ScopeDeclared")
        root.pending_events.append("UndefinedScopeRejected")
        root.history.append({"event": "ScopeDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class DgStrategicObjectivesRoot(AggregateRoot):
    tenant_id: str
    objectives_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls, *, tenant_id: str, objectives_ref: str, present: bool = True
    ) -> DgStrategicObjectivesRoot:
        tid = _tid(tenant_id, "data_governance.mission.obj_tenant_required")
        if not present:
            raise ValueError(
                "data_governance.mission.strategic_objectives_are_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            objectives_ref=objectives_ref.strip(),
            present=True,
            status="registered",
        )
        root.pending_events.append("ObjectivesRegistered")
        root.pending_events.append("MissingObjectivesRejected")
        root.history.append({"event": "ObjectivesPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgOperatingModelRoot(AggregateRoot):
    tenant_id: str
    model_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def establish(
        cls, *, tenant_id: str, model_ref: str, present: bool = True
    ) -> DgOperatingModelRoot:
        tid = _tid(tenant_id, "data_governance.mission.om_tenant_required")
        if not present:
            raise ValueError(
                "data_governance.mission.operating_model_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            model_ref=model_ref.strip(),
            present=True,
            status="established",
        )
        root.pending_events.append("OperatingModelEstablished")
        root.pending_events.append("MissingOperatingModelRejected")
        root.history.append({"event": "OperatingModelPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgMaturityModelRoot(AggregateRoot):
    tenant_id: str
    maturity_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, maturity_ref: str, present: bool = True
    ) -> DgMaturityModelRoot:
        tid = _tid(tenant_id, "data_governance.mission.mat_tenant_required")
        if not present:
            raise ValueError(
                "data_governance.mission.maturity_model_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            maturity_ref=maturity_ref.strip(),
            present=True,
            status="published",
        )
        root.pending_events.append("MaturityModelPublished")
        root.pending_events.append("MissingMaturityModelRejected")
        root.history.append({"event": "MaturityModelPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgAiGovernanceDirectionRoot(AggregateRoot):
    tenant_id: str
    ai_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def establish(
        cls, *, tenant_id: str, ai_ref: str, present: bool = True
    ) -> DgAiGovernanceDirectionRoot:
        tid = _tid(tenant_id, "data_governance.mission.ai_tenant_required")
        if not present:
            raise ValueError(
                "data_governance.mission.ai_governance_direction_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ai_ref=ai_ref.strip(),
            present=True,
            status="established",
        )
        root.pending_events.append("MeosAlignmentConfirmed")
        root.pending_events.append("MissingAiGovernanceDirectionRejected")
        root.history.append({"event": "AiGovernanceDirectionPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgMeosIntegrationAlignmentRoot(AggregateRoot):
    tenant_id: str
    alignment_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def confirm(
        cls, *, tenant_id: str, alignment_ref: str, present: bool = True
    ) -> DgMeosIntegrationAlignmentRoot:
        tid = _tid(tenant_id, "data_governance.mission.align_tenant_required")
        if not present:
            raise ValueError(
                "data_governance.mission.meos_integration_alignment_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            alignment_ref=alignment_ref.strip(),
            present=True,
            status="confirmed",
        )
        root.pending_events.append("MeosAlignmentConfirmed")
        root.pending_events.append("MissingMeosAlignmentRejected")
        root.history.append({"event": "MeosAlignmentPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgDomainBoundariesRoot(AggregateRoot):
    tenant_id: str
    boundary_ref: str
    clear: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def clarify(
        cls, *, tenant_id: str, boundary_ref: str, clear: bool = True
    ) -> DgDomainBoundariesRoot:
        tid = _tid(tenant_id, "data_governance.mission.bound_tenant_required")
        if not clear:
            raise ValueError(
                "data_governance.mission.domain_boundaries_are_unclear"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            boundary_ref=boundary_ref.strip(),
            clear=True,
            status="clear",
        )
        root.pending_events.append("ScopeDeclared")
        root.pending_events.append("UnclearBoundariesRejected")
        root.history.append({"event": "DomainBoundariesClear"})
        return root

    def is_unclear(self) -> bool:
        return not self.clear


@dataclass(eq=False, kw_only=True)
class DgEnterpriseGovernanceStandardRoot(AggregateRoot):
    tenant_id: str
    standard_ref: str
    compliant: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def certify(
        cls, *, tenant_id: str, standard_ref: str, compliant: bool = True
    ) -> DgEnterpriseGovernanceStandardRoot:
        tid = _tid(tenant_id, "data_governance.mission.eg_tenant_required")
        if not compliant:
            raise ValueError(
                "data_governance.mission."
                "enterprise_governance_standard_is_noncompliant"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            standard_ref=standard_ref.strip(),
            compliant=True,
            status="compliant",
        )
        root.pending_events.append("MissionPublished")
        root.pending_events.append("NoncompliantEgStandardRejected")
        root.history.append({"event": "EgStandardCompliant"})
        return root

    def is_noncompliant(self) -> bool:
        return not self.compliant
