"""P207-L distributed fabric aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

LOGICAL_SERVICES = frozenset(
    {
        "identity-intelligence-service",
        "identity-risk-service",
        "behavior-analytics-service",
        "identity-twin-service",
        "ai-agent-service",
        "knowledge-graph-service",
        "autonomous-operation-service",
        "governance-optimization-service",
    }
)

COMMANDS = frozenset(
    {
        "AnalyzeIdentity",
        "CreateIntelligenceProfile",
        "UpdateIdentityContext",
        "GenerateInsight",
        "CalculateRisk",
        "PredictRisk",
        "UpdateTrustScore",
        "AnalyzeBehavior",
        "DetectAnomaly",
        "CreateBehaviorProfile",
        "CreateTwin",
        "UpdateTwinState",
        "RunSimulation",
        "GenerateAction",
        "ExecuteRemediation",
        "ValidateRecovery",
    }
)

QUERIES = frozenset(
    {
        "GetIdentityIntelligence",
        "GetIdentityContext",
        "GetIdentityHistory",
        "GetRiskProfile",
        "GetRiskFactors",
        "GetPredictionResult",
        "GetBehaviorProfile",
        "GetAnomalies",
        "GetDigitalTwin",
        "GetSimulationResult",
        "GetOptimizationRecommendation",
        "GetAccessRisk",
    }
)

EVENTS = frozenset(
    {
        "IdentityAnalyzed",
        "IdentityProfileCreated",
        "IdentityContextChanged",
        "RiskCalculated",
        "RiskIncreased",
        "RiskPredicted",
        "BehaviorAnalyzed",
        "AnomalyDetected",
        "TwinCreated",
        "TwinUpdated",
        "SimulationCompleted",
        "AgentActivated",
        "RecommendationGenerated",
        "DecisionCompleted",
        "ActionStarted",
        "ActionCompleted",
        "RecoveryCompleted",
    }
)

API_TYPES = frozenset({"rest", "graphql", "event", "ai"})


@dataclass(eq=False, kw_only=True)
class ServiceBoundaryMapRoot(AggregateRoot):
    tenant_id: str
    map_ref: str
    services: tuple[str, ...]
    shared_database: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        map_ref: str,
        services: tuple[str, ...] | None = None,
        shared_database: bool = False,
    ) -> ServiceBoundaryMapRoot:
        if not tenant_id.strip():
            raise ValueError("ii.fabric.tenant_required")
        svc = tuple(services or tuple(LOGICAL_SERVICES))
        if shared_database:
            raise ValueError("ii.fabric.services_share_databases")
        if not set(svc).issuperset(LOGICAL_SERVICES):
            raise ValueError("ii.fabric.service_boundaries_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            map_ref=map_ref.strip(),
            services=svc,
            shared_database=False,
            status="defined",
        )
        root.pending_events.append("ServiceBoundaryDefined")
        root.history.append({"event": "ServiceBoundaryDefined"})
        return root

    def shares_database(self) -> bool:
        return self.shared_database


@dataclass(eq=False, kw_only=True)
class CommandCatalogRoot(AggregateRoot):
    tenant_id: str
    catalog_ref: str
    commands: tuple[str, ...]
    cqrs_clear: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        catalog_ref: str,
        commands: tuple[str, ...] | None = None,
        cqrs_clear: bool = True,
    ) -> CommandCatalogRoot:
        if not tenant_id.strip():
            raise ValueError("ii.fabric.command_tenant_required")
        cmd = tuple(commands or tuple(COMMANDS))
        if not cqrs_clear:
            raise ValueError("ii.fabric.cqrs_boundaries_unclear")
        if not set(cmd).issuperset(COMMANDS):
            raise ValueError("ii.fabric.command_catalog_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            catalog_ref=catalog_ref.strip(),
            commands=cmd,
            cqrs_clear=True,
            status="registered",
        )
        root.pending_events.append("CommandCatalogRegistered")
        root.history.append({"event": "CommandCatalogRegistered"})
        return root

    def boundaries_unclear(self) -> bool:
        return not self.cqrs_clear


@dataclass(eq=False, kw_only=True)
class QueryCatalogRoot(AggregateRoot):
    tenant_id: str
    catalog_ref: str
    queries: tuple[str, ...]
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        catalog_ref: str,
        queries: tuple[str, ...] | None = None,
    ) -> QueryCatalogRoot:
        if not tenant_id.strip():
            raise ValueError("ii.fabric.query_tenant_required")
        qry = tuple(queries or tuple(QUERIES))
        if not set(qry).issuperset(QUERIES):
            raise ValueError("ii.fabric.query_catalog_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            catalog_ref=catalog_ref.strip(),
            queries=qry,
            status="registered",
        )
        root.pending_events.append("QueryCatalogRegistered")
        root.history.append({"event": "QueryCatalogRegistered"})
        return root


@dataclass(eq=False, kw_only=True)
class EventContractCatalogRoot(AggregateRoot):
    tenant_id: str
    catalog_ref: str
    events: tuple[str, ...]
    versioned: bool
    ordered: bool
    replayable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        catalog_ref: str,
        events: tuple[str, ...] | None = None,
        versioned: bool = True,
        ordered: bool = True,
        replayable: bool = True,
    ) -> EventContractCatalogRoot:
        if not tenant_id.strip():
            raise ValueError("ii.fabric.event_tenant_required")
        ev = tuple(events or tuple(EVENTS))
        if not set(ev).issuperset(EVENTS):
            raise ValueError("ii.fabric.events_undefined")
        if not (versioned and ordered and replayable):
            raise ValueError("ii.fabric.events_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            catalog_ref=catalog_ref.strip(),
            events=ev,
            versioned=True,
            ordered=True,
            replayable=True,
            status="registered",
        )
        root.pending_events.append("EventCatalogRegistered")
        root.history.append({"event": "EventCatalogRegistered"})
        return root

    def undefined(self) -> bool:
        return not (self.versioned and self.ordered and self.replayable)


@dataclass(eq=False, kw_only=True)
class ApiSecurityPolicyRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    api_types: tuple[str, ...]
    oauth_enabled: bool
    oidc_enabled: bool
    mtls_enabled: bool
    authz_enabled: bool
    rate_limited: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enforce(
        cls,
        *,
        tenant_id: str,
        policy_ref: str,
        api_types: tuple[str, ...] | None = None,
        oauth_enabled: bool = True,
        oidc_enabled: bool = True,
        mtls_enabled: bool = True,
        authz_enabled: bool = True,
        rate_limited: bool = True,
    ) -> ApiSecurityPolicyRoot:
        if not tenant_id.strip():
            raise ValueError("ii.fabric.api_tenant_required")
        types = tuple(api_types or tuple(API_TYPES))
        if not set(types).issuperset(API_TYPES):
            raise ValueError("ii.fabric.apis_lack_security")
        if not (oauth_enabled and oidc_enabled and mtls_enabled and authz_enabled and rate_limited):
            raise ValueError("ii.fabric.apis_lack_security")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            api_types=types,
            oauth_enabled=True,
            oidc_enabled=True,
            mtls_enabled=True,
            authz_enabled=True,
            rate_limited=True,
            status="enforced",
        )
        root.pending_events.append("ApiSecurityEnforced")
        root.history.append({"event": "ApiSecurityEnforced"})
        return root

    def insecure(self) -> bool:
        return not (
            self.oauth_enabled
            and self.oidc_enabled
            and self.mtls_enabled
            and self.authz_enabled
            and self.rate_limited
        )


@dataclass(eq=False, kw_only=True)
class EventStreamingTopologyRoot(AggregateRoot):
    tenant_id: str
    topology_ref: str
    delivery_guaranteed: bool
    high_throughput: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def design(
        cls,
        *,
        tenant_id: str,
        topology_ref: str,
        delivery_guaranteed: bool = True,
        high_throughput: bool = True,
    ) -> EventStreamingTopologyRoot:
        if not tenant_id.strip():
            raise ValueError("ii.fabric.topology_tenant_required")
        if not (delivery_guaranteed and high_throughput):
            raise ValueError("ii.fabric.event_streaming_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            topology_ref=topology_ref.strip(),
            delivery_guaranteed=True,
            high_throughput=True,
            status="designed",
        )
        root.pending_events.append("EventStreamingDesigned")
        root.history.append({"event": "EventStreamingDesigned"})
        return root


@dataclass(eq=False, kw_only=True)
class ProductionReadinessAssessmentRoot(AggregateRoot):
    tenant_id: str
    assessment_ref: str
    audit_complete: bool
    ai_connected: bool
    kubernetes_ready: bool
    disaster_recovery_ready: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def assess(
        cls,
        *,
        tenant_id: str,
        assessment_ref: str,
        audit_complete: bool = True,
        ai_connected: bool = True,
        kubernetes_ready: bool = True,
        disaster_recovery_ready: bool = True,
    ) -> ProductionReadinessAssessmentRoot:
        if not tenant_id.strip():
            raise ValueError("ii.fabric.readiness_tenant_required")
        if not audit_complete:
            raise ValueError("ii.fabric.audit_history_incomplete")
        if not ai_connected:
            raise ValueError("ii.fabric.ai_integration_disconnected")
        if not (kubernetes_ready and disaster_recovery_ready):
            raise ValueError("ii.fabric.readiness_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            assessment_ref=assessment_ref.strip(),
            audit_complete=True,
            ai_connected=True,
            kubernetes_ready=True,
            disaster_recovery_ready=True,
            status="assessed",
        )
        root.pending_events.append("ProductionReadinessAssessed")
        root.history.append({"event": "ProductionReadinessAssessed"})
        return root

    def audit_incomplete(self) -> bool:
        return not self.audit_complete

    def ai_disconnected(self) -> bool:
        return not self.ai_connected
