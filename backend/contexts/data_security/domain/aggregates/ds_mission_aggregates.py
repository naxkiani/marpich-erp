"""P211-B Data Security mission/scope aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class DsMissionScopeDefinedRoot(AggregateRoot):
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
    ) -> DsMissionScopeDefinedRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.mission.tenant_required")
        if not defined:
            raise ValueError(
                "data_security.mission.data_security_scope_is_undefined"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            scope_ref=scope_ref.strip(),
            defined=True,
            status="defined",
        )
        root.pending_events.append("ScopeDeclared")
        root.pending_events.append("UndefinedScopeRejected")
        root.history.append({"event": "ScopeDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class DsOwnershipModelRoot(AggregateRoot):
    tenant_id: str
    model_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls, *, tenant_id: str, model_ref: str, present: bool = True
    ) -> DsOwnershipModelRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.mission.own_tenant_required")
        if not present:
            raise ValueError(
                "data_security.mission.ownership_model_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            model_ref=model_ref.strip(),
            present=True,
            status="registered",
        )
        root.pending_events.append("OwnershipModelRegistered")
        root.pending_events.append("MissingOwnershipRejected")
        root.history.append({"event": "OwnershipRegistered"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DsPrivacyResponsibilitiesRoot(AggregateRoot):
    tenant_id: str
    charter_ref: str
    clear: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def clarify(
        cls, *, tenant_id: str, charter_ref: str, clear: bool = True
    ) -> DsPrivacyResponsibilitiesRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.mission.priv_tenant_required")
        if not clear:
            raise ValueError(
                "data_security.mission.privacy_responsibilities_are_unclear"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            charter_ref=charter_ref.strip(),
            clear=True,
            status="clarified",
        )
        root.pending_events.append("PrivacyResponsibilitiesClarified")
        root.pending_events.append("UnclearPrivacyRejected")
        root.history.append({"event": "PrivacyClarified"})
        return root

    def is_unclear(self) -> bool:
        return not self.clear


@dataclass(eq=False, kw_only=True)
class DsProtectionPrinciplesRoot(AggregateRoot):
    tenant_id: str
    set_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def adopt(
        cls, *, tenant_id: str, set_ref: str, present: bool = True
    ) -> DsProtectionPrinciplesRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.mission.prin_tenant_required")
        if not present:
            raise ValueError(
                "data_security.mission.data_protection_principles_are_absent"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            set_ref=set_ref.strip(),
            present=True,
            status="adopted",
        )
        root.pending_events.append("PrinciplesAdopted")
        root.pending_events.append("AbsentPrinciplesRejected")
        root.history.append({"event": "PrinciplesPresent"})
        return root

    def is_absent(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DsIntegrationBoundariesRoot(AggregateRoot):
    tenant_id: str
    boundary_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def declare(
        cls, *, tenant_id: str, boundary_ref: str, defined: bool = True
    ) -> DsIntegrationBoundariesRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.mission.int_tenant_required")
        if not defined:
            raise ValueError(
                "data_security.mission.integration_boundaries_are_undefined"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            boundary_ref=boundary_ref.strip(),
            defined=True,
            status="defined",
        )
        root.pending_events.append("IntegrationBoundariesDeclared")
        root.pending_events.append("UndefinedBoundariesRejected")
        root.history.append({"event": "BoundariesDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class DsGovernanceModelRoot(AggregateRoot):
    tenant_id: str
    model_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def complete(
        cls, *, tenant_id: str, model_ref: str, complete: bool = True
    ) -> DsGovernanceModelRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.mission.gov_tenant_required")
        if not complete:
            raise ValueError(
                "data_security.mission.governance_model_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            model_ref=model_ref.strip(),
            complete=True,
            status="complete",
        )
        root.pending_events.append("GovernanceModelCompleted")
        root.pending_events.append("IncompleteGovernanceRejected")
        root.history.append({"event": "GovernanceComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class DsMissionCharterRoot(AggregateRoot):
    tenant_id: str
    charter_ref: str
    published: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, charter_ref: str, published: bool = True
    ) -> DsMissionCharterRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.mission.charter_tenant_required")
        if not published:
            raise ValueError("data_security.mission.mission_not_published")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            charter_ref=charter_ref.strip(),
            published=True,
            status="published",
        )
        root.pending_events.append("MissionPublished")
        root.history.append({"event": "MissionPublished"})
        return root


@dataclass(eq=False, kw_only=True)
class DsVisionCharterRoot(AggregateRoot):
    tenant_id: str
    charter_ref: str
    published: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, charter_ref: str, published: bool = True
    ) -> DsVisionCharterRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.mission.vision_tenant_required")
        if not published:
            raise ValueError("data_security.mission.vision_not_published")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            charter_ref=charter_ref.strip(),
            published=True,
            status="published",
        )
        root.pending_events.append("VisionPublished")
        root.history.append({"event": "VisionPublished"})
        return root
