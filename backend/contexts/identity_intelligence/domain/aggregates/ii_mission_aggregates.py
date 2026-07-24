"""P207-B Mission / Vision / Scope aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

OBJECTIVE_CATEGORIES = frozenset(
    {
        "identity_intelligence",
        "security_intelligence",
        "operational_intelligence",
        "governance_intelligence",
    }
)

PEER_SORS = frozenset(
    {
        "directory",
        "identity_governance",
        "authentication",
        "privileged_access",
        "identity",
        "authorization",
        "identity_digital_twin",
        "ai",
    }
)


@dataclass(eq=False, kw_only=True)
class MissionCharterRoot(AggregateRoot):
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
    ) -> MissionCharterRoot:
        if not tenant_id.strip():
            raise ValueError("ii.mvs.tenant_required")
        if not mission_text.strip() or not vision_text.strip():
            raise ValueError("ii.mvs.mission_vision_absent")
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
class EnterpriseScopeBoundaryRoot(AggregateRoot):
    tenant_id: str
    boundary_ref: str
    in_scope_defined: bool
    out_of_scope_defined: bool
    replaces_peers: bool
    excluded_peers: tuple[str, ...]
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        boundary_ref: str,
        in_scope_defined: bool = True,
        out_of_scope_defined: bool = True,
        replaces_peers: bool = False,
        excluded_peers: tuple[str, ...] | None = None,
    ) -> EnterpriseScopeBoundaryRoot:
        if not tenant_id.strip():
            raise ValueError("ii.mvs.scope_tenant_required")
        if not in_scope_defined:
            raise ValueError("ii.mvs.enterprise_scope_undefined")
        if not out_of_scope_defined:
            raise ValueError("ii.mvs.out_of_scope_unclear")
        if replaces_peers:
            raise ValueError("ii.mvs.replaces_peer_sors")
        peers = excluded_peers or (
            "directory",
            "identity_governance",
            "authentication",
            "privileged_access",
        )
        if not set(peers).issubset(PEER_SORS | {"master_identity"}):
            # allow master_identity as planned P206 label
            invalid = set(peers) - PEER_SORS - {"master_identity"}
            if invalid:
                raise ValueError("ii.mvs.peer_invalid")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            boundary_ref=boundary_ref.strip(),
            in_scope_defined=True,
            out_of_scope_defined=True,
            replaces_peers=False,
            excluded_peers=tuple(peers),
            status="defined",
        )
        root.pending_events.append("ScopeBoundaryDefined")
        root.history.append({"event": "ScopeBoundaryDefined"})
        return root

    def reject_peer_replacement(self) -> None:
        self.pending_events.append("PeerSorReplacementRejected")
        self.history.append({"event": "PeerSorReplacementRejected"})

    def is_undefined(self) -> bool:
        return not (self.in_scope_defined and self.out_of_scope_defined)


@dataclass(eq=False, kw_only=True)
class StrategicObjectiveSetRoot(AggregateRoot):
    tenant_id: str
    set_ref: str
    categories: tuple[str, ...]
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        set_ref: str,
        categories: tuple[str, ...] | None = None,
    ) -> StrategicObjectiveSetRoot:
        if not tenant_id.strip():
            raise ValueError("ii.mvs.obj_tenant_required")
        cats = categories or tuple(OBJECTIVE_CATEGORIES)
        if not cats or not set(cats).issubset(OBJECTIVE_CATEGORIES):
            raise ValueError("ii.mvs.strategic_objectives_undefined")
        if set(cats) != OBJECTIVE_CATEGORIES:
            raise ValueError("ii.mvs.strategic_objectives_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            set_ref=set_ref.strip(),
            categories=tuple(cats),
            status="registered",
        )
        root.pending_events.append("StrategicObjectiveRegistered")
        root.history.append({"event": "StrategicObjectiveRegistered"})
        return root

    def is_undefined(self) -> bool:
        return set(self.categories) != OBJECTIVE_CATEGORIES


@dataclass(eq=False, kw_only=True)
class MeosArchitecturePlacementRoot(AggregateRoot):
    tenant_id: str
    placement_ref: str
    intelligence_layer: bool
    human_control: bool
    chatbot_only: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def map(
        cls,
        *,
        tenant_id: str,
        placement_ref: str,
        intelligence_layer: bool = True,
        human_control: bool = True,
        chatbot_only: bool = False,
    ) -> MeosArchitecturePlacementRoot:
        if not tenant_id.strip():
            raise ValueError("ii.mvs.placement_tenant_required")
        if not intelligence_layer:
            raise ValueError("ii.mvs.intelligence_layer_absent")
        if not human_control:
            raise ValueError("ii.mvs.human_control_removed")
        if chatbot_only:
            raise ValueError("ii.mvs.ai_only_chatbot")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            placement_ref=placement_ref.strip(),
            intelligence_layer=True,
            human_control=True,
            chatbot_only=False,
            status="mapped",
        )
        root.pending_events.append("MeosPlacementMapped")
        root.history.append({"event": "MeosPlacementMapped"})
        return root

    def is_absent_intelligence_layer(self) -> bool:
        return not self.intelligence_layer
