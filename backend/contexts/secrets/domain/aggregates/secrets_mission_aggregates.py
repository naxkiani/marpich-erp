"""P209-B Mission / Vision / Scope aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

OUT_OF_SCOPE_CLAIMS = frozenset(
    {
        "business_authorization_rules",
        "user_business_profiles",
        "application_business_logic",
        "enterprise_data_classification",
        "network_routing",
    }
)

PEER_SORS = frozenset(
    {
        "authorization",
        "identity",
        "privileged_access",
        "directory",
        "identity_governance",
        "policy",
        "permission_registry",
    }
)


@dataclass(eq=False, kw_only=True)
class SecretsMissionCharterRoot(AggregateRoot):
    """Mission and vision must not be absent."""

    tenant_id: str
    charter_ref: str
    mission_text: str
    vision_text: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls,
        *,
        tenant_id: str,
        charter_ref: str,
        mission_text: str,
        vision_text: str,
    ) -> SecretsMissionCharterRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.mvs.tenant_required")
        if not mission_text.strip() or not vision_text.strip():
            raise ValueError("secrets.mvs.mission_vision_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            charter_ref=charter_ref.strip(),
            mission_text=mission_text.strip(),
            vision_text=vision_text.strip(),
            status="published",
        )
        root.pending_events.append("MissionCharterPublished")
        root.pending_events.append("VisionBlueprintApproved")
        root.history.append({"event": "MissionCharterPublished"})
        return root

    def is_absent(self) -> bool:
        return not (self.mission_text and self.vision_text)


@dataclass(eq=False, kw_only=True)
class SecretsEnterpriseScopeRoot(AggregateRoot):
    """Enterprise scope must be defined."""

    tenant_id: str
    scope_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        scope_ref: str,
        defined: bool = True,
    ) -> SecretsEnterpriseScopeRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.mvs.scope_tenant_required")
        if not defined:
            raise ValueError("secrets.mvs.enterprise_scope_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            scope_ref=scope_ref.strip(),
            defined=True,
            status="defined",
        )
        root.pending_events.append("EnterpriseScopeDefined")
        root.history.append({"event": "EnterpriseScopeDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class SecretsBoundaryRoot(AggregateRoot):
    """Boundaries must be clear; must not own business AuthZ or replace peers."""

    tenant_id: str
    boundary_ref: str
    clear: bool
    owns_business_authorization: bool
    replaces_peers: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def clarify(
        cls,
        *,
        tenant_id: str,
        boundary_ref: str,
        clear: bool = True,
        owns_business_authorization: bool = False,
        replaces_peers: bool = False,
        claimed_out_of_scope: str | None = None,
    ) -> SecretsBoundaryRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.mvs.boundary_tenant_required")
        if not clear:
            raise ValueError("secrets.mvs.boundaries_unclear")
        if owns_business_authorization:
            raise ValueError("secrets.mvs.owns_business_authorization")
        if replaces_peers:
            raise ValueError("secrets.mvs.replaces_peer_sors")
        if claimed_out_of_scope and claimed_out_of_scope in OUT_OF_SCOPE_CLAIMS:
            raise ValueError("secrets.mvs.owns_business_authorization")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            boundary_ref=boundary_ref.strip(),
            clear=True,
            owns_business_authorization=False,
            replaces_peers=False,
            status="clarified",
        )
        root.pending_events.append("BoundaryClarified")
        root.history.append({"event": "BoundaryClarified"})
        return root

    def is_unclear(self) -> bool:
        return (
            not self.clear
            or self.owns_business_authorization
            or self.replaces_peers
        )


@dataclass(eq=False, kw_only=True)
class SecretsCapabilityOwnershipRoot(AggregateRoot):
    """Capability ownership must not be absent."""

    tenant_id: str
    ownership_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        ownership_ref: str,
        present: bool = True,
    ) -> SecretsCapabilityOwnershipRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.mvs.cap_tenant_required")
        if not present:
            raise ValueError("secrets.mvs.capability_ownership_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            ownership_ref=ownership_ref.strip(),
            present=True,
            status="registered",
        )
        root.pending_events.append("CapabilityOwnershipRegistered")
        root.history.append({"event": "CapabilityOwnershipRegistered"})
        return root

    def is_absent(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class SecretsIntegrationCharterRoot(AggregateRoot):
    """Integration responsibilities must not be absent."""

    tenant_id: str
    charter_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def bind(
        cls,
        *,
        tenant_id: str,
        charter_ref: str,
        present: bool = True,
    ) -> SecretsIntegrationCharterRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.mvs.integ_tenant_required")
        if not present:
            raise ValueError(
                "secrets.mvs.integration_responsibilities_absent"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            charter_ref=charter_ref.strip(),
            present=True,
            status="bound",
        )
        root.pending_events.append("IntegrationCharterBound")
        root.history.append({"event": "IntegrationCharterBound"})
        return root

    def is_absent(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class SecretsGovernancePrinciplesRoot(AggregateRoot):
    """Governance principles must not be absent."""

    tenant_id: str
    principles_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls,
        *,
        tenant_id: str,
        principles_ref: str,
        present: bool = True,
    ) -> SecretsGovernancePrinciplesRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.mvs.gov_tenant_required")
        if not present:
            raise ValueError("secrets.mvs.governance_principles_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            principles_ref=principles_ref.strip(),
            present=True,
            status="published",
        )
        root.pending_events.append("GovernancePrinciplesPublished")
        root.history.append({"event": "GovernancePrinciplesPublished"})
        return root

    def is_absent(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class SecretsEvolutionRoadmapRoot(AggregateRoot):
    """Evolution roadmap must not be absent."""

    tenant_id: str
    roadmap_ref: str
    present: bool
    phase_count: int
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls,
        *,
        tenant_id: str,
        roadmap_ref: str,
        present: bool = True,
        phase_count: int = 7,
    ) -> SecretsEvolutionRoadmapRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.mvs.roadmap_tenant_required")
        if not present or phase_count < 1:
            raise ValueError("secrets.mvs.evolution_roadmap_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            roadmap_ref=roadmap_ref.strip(),
            present=True,
            phase_count=phase_count,
            status="published",
        )
        root.pending_events.append("EvolutionRoadmapPublished")
        root.history.append({"event": "EvolutionRoadmapPublished"})
        return root

    def is_absent(self) -> bool:
        return not self.present or self.phase_count < 1


@dataclass(eq=False, kw_only=True)
class SecretsStrategicObjectivesRoot(AggregateRoot):
    """Strategic objectives set for crypto trust."""

    tenant_id: str
    objectives_ref: str
    objective_count: int
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        objectives_ref: str,
        objective_count: int = 5,
    ) -> SecretsStrategicObjectivesRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.mvs.obj_tenant_required")
        if objective_count < 5:
            raise ValueError("secrets.mvs.enterprise_scope_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            objectives_ref=objectives_ref.strip(),
            objective_count=objective_count,
            status="registered",
        )
        root.pending_events.append("StrategicObjectiveRegistered")
        root.pending_events.append("KpiFrameworkPublished")
        root.history.append({"event": "StrategicObjectivesRegistered"})
        return root
