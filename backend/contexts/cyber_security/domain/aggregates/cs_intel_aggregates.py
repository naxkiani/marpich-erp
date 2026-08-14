"""P210-H Threat Intelligence aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class CsIntelValidatedRoot(AggregateRoot):
    tenant_id: str
    intel_ref: str
    validated: bool
    trust_score: float
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def validate(
        cls,
        *,
        tenant_id: str,
        intel_ref: str,
        validated: bool = True,
        trust_score: float = 0.8,
    ) -> CsIntelValidatedRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.intel.tenant_required")
        if not validated or trust_score <= 0:
            raise ValueError(
                "cyber_security.intel.threat_intelligence_cannot_be_validated"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            intel_ref=intel_ref.strip(),
            validated=True,
            trust_score=trust_score,
            status="validated",
        )
        root.pending_events.append("ThreatEnriched")
        root.pending_events.append("UnvalidatedIntelRejected")
        root.history.append({"event": "ThreatIntelligenceValidated"})
        return root

    def is_unvalidated(self) -> bool:
        return not self.validated or self.trust_score <= 0


@dataclass(eq=False, kw_only=True)
class CsIntelProactiveHuntRoot(AggregateRoot):
    tenant_id: str
    hunt_ref: str
    proactive: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def launch(
        cls, *, tenant_id: str, hunt_ref: str, proactive: bool = True
    ) -> CsIntelProactiveHuntRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.intel.hunt_tenant_required")
        if not proactive:
            raise ValueError("cyber_security.intel.threat_hunting_reactive_only")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            hunt_ref=hunt_ref.strip(),
            proactive=True,
            status="started",
        )
        root.pending_events.append("ThreatHuntStarted")
        root.pending_events.append("ReactiveOnlyHuntRejected")
        root.history.append({"event": "ProactiveHuntLaunched"})
        return root

    def is_reactive_only(self) -> bool:
        return not self.proactive


@dataclass(eq=False, kw_only=True)
class CsIntelKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str
    graph_ref: str
    integrated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def bind(
        cls, *, tenant_id: str, graph_ref: str, integrated: bool = True
    ) -> CsIntelKnowledgeGraphRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.intel.kg_tenant_required")
        if not integrated:
            raise ValueError(
                "cyber_security.intel.knowledge_graph_integration_absent"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            graph_ref=graph_ref.strip(),
            integrated=True,
            status="bound",
        )
        root.pending_events.append("AbsentKgRejected")
        root.history.append({"event": "KnowledgeGraphBound"})
        return root

    def is_absent(self) -> bool:
        return not self.integrated


@dataclass(eq=False, kw_only=True)
class CsIntelExplainableAiRoot(AggregateRoot):
    tenant_id: str
    advisory_ref: str
    explainable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def advise(
        cls, *, tenant_id: str, advisory_ref: str, explainable: bool = True
    ) -> CsIntelExplainableAiRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.intel.ai_tenant_required")
        if not explainable:
            raise ValueError(
                "cyber_security.intel.ai_cannot_explain_recommendations"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            advisory_ref=advisory_ref.strip(),
            explainable=True,
            status="advised",
        )
        root.pending_events.append("UnexplainableAiRejected")
        root.history.append({"event": "ExplainableAiAdvisory"})
        return root

    def is_unexplainable(self) -> bool:
        return not self.explainable


@dataclass(eq=False, kw_only=True)
class CsIntelConnectedDetectionRoot(AggregateRoot):
    tenant_id: str
    pack_ref: str
    connected: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, pack_ref: str, connected: bool = True
    ) -> CsIntelConnectedDetectionRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.intel.det_tenant_required")
        if not connected:
            raise ValueError(
                "cyber_security.intel.detection_engineering_disconnected"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            pack_ref=pack_ref.strip(),
            connected=True,
            status="published",
        )
        root.pending_events.append("DetectionRuleGenerated")
        root.pending_events.append("DisconnectedDetectionRejected")
        root.history.append({"event": "DetectionEngineeringConnected"})
        return root

    def is_disconnected(self) -> bool:
        return not self.connected


@dataclass(eq=False, kw_only=True)
class CsIntelStandardsSharingRoot(AggregateRoot):
    tenant_id: str
    channel_ref: str
    standards_based: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls,
        *,
        tenant_id: str,
        channel_ref: str,
        standards_based: bool = True,
    ) -> CsIntelStandardsSharingRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.intel.share_tenant_required")
        if not standards_based:
            raise ValueError(
                "cyber_security.intel.intelligence_sharing_lacks_standards"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            channel_ref=channel_ref.strip(),
            standards_based=True,
            status="published",
        )
        root.pending_events.append("ThreatPublished")
        root.pending_events.append("NonStandardSharingRejected")
        root.history.append({"event": "StandardsBasedSharing"})
        return root

    def lacks_standards(self) -> bool:
        return not self.standards_based


@dataclass(eq=False, kw_only=True)
class CsIntelAttributionRoot(AggregateRoot):
    tenant_id: str
    actor_ref: str
    attribution_supported: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        actor_ref: str,
        attribution_supported: bool = True,
    ) -> CsIntelAttributionRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.intel.attr_tenant_required")
        if not attribution_supported:
            raise ValueError(
                "cyber_security.intel.threat_actor_attribution_unsupported"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            actor_ref=actor_ref.strip(),
            attribution_supported=True,
            status="registered",
        )
        root.pending_events.append("ThreatActorDiscovered")
        root.pending_events.append("UnsupportedAttributionRejected")
        root.history.append({"event": "ThreatActorAttributed"})
        return root

    def is_unsupported(self) -> bool:
        return not self.attribution_supported


@dataclass(eq=False, kw_only=True)
class CsIntelCampaignDetectedRoot(AggregateRoot):
    tenant_id: str
    campaign_ref: str
    actor_ref: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def detect(
        cls, *, tenant_id: str, campaign_ref: str, actor_ref: str
    ) -> CsIntelCampaignDetectedRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.intel.campaign_tenant_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            campaign_ref=campaign_ref.strip(),
            actor_ref=actor_ref.strip(),
            status="detected",
        )
        root.pending_events.append("CampaignDetected")
        root.pending_events.append("ThreatFeedCollected")
        root.history.append({"event": "CampaignDetected"})
        return root
