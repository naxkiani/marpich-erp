"""P213-N CQRS, Events, APIs & Microservices Platform — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P213-N"
ADR = 418
SOR = "analytics"
API_PREFIX = "/api/v1/analytics"
PRODUCT = "Enterprise BI CQRS, Events, APIs & Microservices Platform"
CAPABILITY = "CAP-PLT-BI-001"

PRINCIPLE = (
    "Every business event SHALL become a durable enterprise event, "
    "every business capability SHALL expose contract-first APIs, "
    "and every analytics service SHALL remain independently deployable."
)

FABRIC = "meos_enterprise_analytics_integration_fabric"

CORE_DOMAIN = "enterprise_analytics_integration_platform"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {"id": "command_processing", "purpose": "Command validation, routing, aggregate execution."},
    {"id": "query_processing", "purpose": "Read models and optimised reporting queries."},
    {"id": "event_streaming", "purpose": "Publish, persist, replay enterprise events."},
    {"id": "api_management", "purpose": "API lifecycle, contracts, governance."},
    {"id": "service_discovery", "purpose": "Service registry and endpoint resolution."},
    {"id": "integration_gateway", "purpose": "Contract translation and external orchestration."},
    {"id": "event_store", "purpose": "Immutable event store and snapshots."},
    {"id": "contract_registry", "purpose": "Versioned API and event schema contracts."},
)

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "command_platform",
        "bc": "BC-01",
        "name": "Command Platform Context",
        "purpose": "Command validation, routing, aggregate execution.",
    },
    {
        "id": "query_platform",
        "bc": "BC-02",
        "name": "Query Platform Context",
        "purpose": "Read models, optimised queries, reporting APIs.",
    },
    {
        "id": "event_platform",
        "bc": "BC-03",
        "name": "Event Platform Context",
        "purpose": "Event publishing, persistence, replay.",
    },
    {
        "id": "api_platform",
        "bc": "BC-04",
        "name": "API Platform Context",
        "purpose": "API lifecycle, governance, security.",
    },
    {
        "id": "integration",
        "bc": "BC-05",
        "name": "Integration Context",
        "purpose": "Service orchestration, external integration, contracts.",
    },
    {
        "id": "messaging",
        "bc": "BC-06",
        "name": "Messaging Context",
        "purpose": "Queues, topics, streams, dead-letter handling.",
    },
)

AGGREGATE = {
    "name": "IntegrationPlatformAggregate",
    "root": "IntegrationPlatform",
    "entities": (
        "Command",
        "Query",
        "Event",
        "ReadModel",
        "EventStream",
        "ApiContract",
        "ServiceEndpoint",
        "ConsumerGroup",
        "Producer",
        "SchemaDefinition",
    ),
    "value_objects": (
        "EventId",
        "CorrelationId",
        "CausationId",
        "ApiVersion",
        "ServiceName",
        "TopicName",
        "RoutingKey",
    ),
    "events": (
        "CommandAcceptedEvent",
        "CommandRejectedEvent",
        "EventPublishedEvent",
        "ReadModelUpdatedEvent",
        "ApiRegisteredEvent",
        "ConsumerSubscribedEvent",
    ),
}

COMMANDS: tuple[str, ...] = (
    "CreateAnalyticsModelCommand",
    "PublishDashboardCommand",
    "GenerateForecastCommand",
    "ApproveRecommendationCommand",
    "ExecuteDecisionCommand",
    "RegisterInsightCommand",
)

QUERIES: tuple[str, ...] = (
    "GetDashboardQuery",
    "SearchInsightsQuery",
    "GetForecastQuery",
    "GetRecommendationQuery",
    "GetDecisionHistoryQuery",
    "GetAnalyticsStatusQuery",
)

CQRS_PLATFORM: dict[str, Any] = {
    "command_bus": True,
    "query_bus": True,
    "validation_pipeline": True,
    "idempotency": True,
    "retry_policies": True,
    "transaction_boundaries": True,
    "commands": list(COMMANDS),
    "queries": list(QUERIES),
}

EVENT_SOURCING: dict[str, Any] = {
    "immutable_event_store": True,
    "aggregate_replay": True,
    "event_snapshots": True,
    "event_versioning": True,
    "event_schema_evolution": True,
    "event_migration": True,
    "event_archiving": True,
    "event_retention": True,
    "event_replay": True,
    "time_travel": True,
    "via_enterprise_event_fabric": True,
    "module_local_event_bus_forbidden": True,
}

EVENT_STREAMING: dict[str, Any] = {
    "apache_kafka_compatibility": True,
    "cloud_event_streaming": True,
    "partitioned_topics": True,
    "consumer_groups": True,
    "event_ordering": True,
    "event_filtering": True,
    "event_routing": True,
    "stream_processing": True,
    "exactly_once_processing": True,
    "at_least_once_processing": True,
    "via_enterprise_event_fabric": True,
}

API_MANAGEMENT: dict[str, Any] = {
    "protocols": (
        "rest",
        "graphql",
        "grpc",
        "async_apis",
        "streaming_apis",
        "webhooks",
        "server_sent_events",
    ),
    "features": (
        "api_gateway",
        "api_registry",
        "api_versioning",
        "api_lifecycle",
        "api_contracts",
        "api_analytics",
        "rate_limiting",
        "quotas",
        "api_monetisation_ready",
    ),
    "via_api_gateway": True,
    "module_local_gateway_forbidden": True,
}

CORE_EVENTS: tuple[dict[str, Any], ...] = (
    {
        "name": "CommandAcceptedEvent",
        "producer": "command_platform",
        "consumers": ("event_platform", "audit"),
        "payload": ("tenant_id", "command_id", "command_type"),
        "version": "v1",
    },
    {
        "name": "CommandRejectedEvent",
        "producer": "command_platform",
        "consumers": ("audit", "observability"),
        "payload": ("tenant_id", "command_id", "reason"),
        "version": "v1",
    },
    {
        "name": "EventPublishedEvent",
        "producer": "event_platform",
        "consumers": ("messaging", "query_platform", "audit"),
        "payload": ("tenant_id", "event_id", "topic"),
        "version": "v1",
    },
    {
        "name": "ReadModelUpdatedEvent",
        "producer": "query_platform",
        "consumers": ("api_platform", "observability"),
        "payload": ("tenant_id", "read_model_id", "version"),
        "version": "v1",
    },
    {
        "name": "ApiRegisteredEvent",
        "producer": "api_platform",
        "consumers": ("contract_registry", "api_gateway"),
        "payload": ("tenant_id", "api_id", "api_version"),
        "version": "v1",
    },
    {
        "name": "ConsumerSubscribedEvent",
        "producer": "messaging",
        "consumers": ("event_platform", "observability"),
        "payload": ("tenant_id", "consumer_group", "topic"),
        "version": "v1",
    },
    {
        "name": "BiCommandExecuted",
        "producer": "command_platform",
        "consumers": ("event_platform", "audit"),
        "payload": ("tenant_id", "command_id", "aggregate_id"),
        "version": "v1",
    },
    {
        "name": "BiProjectionUpdated",
        "producer": "query_platform",
        "consumers": ("api_platform", "reporting"),
        "payload": ("tenant_id", "projection_id", "cursor"),
        "version": "v1",
    },
    {
        "name": "BiIntegrationPublished",
        "producer": "integration",
        "consumers": ("messaging", "audit"),
        "payload": ("tenant_id", "integration_ref", "contract_version"),
        "version": "v1",
    },
    {
        "name": "BiStateChanged",
        "producer": "event_platform",
        "consumers": ("query_platform", "observability"),
        "payload": ("tenant_id", "aggregate_id", "state"),
        "version": "v1",
    },
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "name": "analytics-service",
        "responsibility": "Core analytics SoR orchestration and catalog.",
        "database_boundary": "analytics_*",
        "api_boundary": "/api/v1/analytics",
        "events": ("BiStateChanged", "BiCommandExecuted"),
        "security_model": "analytics.*",
        "scaling_strategy": "horizontal_stateless",
        "deployment_unit": "analytics",
    },
    {
        "name": "forecast-service",
        "responsibility": "Predictive / forecasting surfaces (P213-J).",
        "database_boundary": "analytics_predictive_*",
        "api_boundary": "/api/v1/analytics/predictive",
        "events": ("BiProjectionUpdated",),
        "security_model": "analytics.predictive.*",
        "scaling_strategy": "async_workers",
        "deployment_unit": "analytics",
    },
    {
        "name": "decision-intelligence-service",
        "responsibility": "Autonomous decision intelligence (P213-M).",
        "database_boundary": "analytics_ai_decisions",
        "api_boundary": "/api/v1/analytics/ai",
        "events": ("BiCommandExecuted", "BiIntegrationPublished"),
        "security_model": "analytics.ai.*",
        "scaling_strategy": "async_via_enterprise_ai",
        "deployment_unit": "analytics",
    },
    {
        "name": "reporting-service",
        "responsibility": "Reporting, dashboards, visualization (P213-D).",
        "database_boundary": "analytics_reporting_*",
        "api_boundary": "/api/v1/analytics/reporting",
        "events": ("BiProjectionUpdated", "ReadModelUpdatedEvent"),
        "security_model": "analytics.reporting.*",
        "scaling_strategy": "horizontal_stateless",
        "deployment_unit": "analytics",
    },
    {
        "name": "semantic-layer-service",
        "responsibility": "OLAP, semantic layer, metrics (P213-G).",
        "database_boundary": "analytics_olap_*",
        "api_boundary": "/api/v1/analytics/olap",
        "events": ("BiProjectionUpdated",),
        "security_model": "analytics.olap.*",
        "scaling_strategy": "horizontal_stateless",
        "deployment_unit": "analytics",
    },
    {
        "name": "knowledge-graph-service",
        "responsibility": "Decision knowledge graph (P213-L).",
        "database_boundary": "analytics_graph_*",
        "api_boundary": "/api/v1/analytics/graph",
        "events": ("BiIntegrationPublished",),
        "security_model": "analytics.graph.*",
        "scaling_strategy": "horizontal_stateless",
        "deployment_unit": "analytics",
    },
    {
        "name": "ai-analytics-service",
        "responsibility": "AI-native analytics via Enterprise AI.",
        "database_boundary": "analytics_ai_*",
        "api_boundary": "/api/v1/analytics/ai",
        "events": ("BiIntegrationPublished",),
        "security_model": "analytics.ai.*",
        "scaling_strategy": "async_via_enterprise_ai",
        "deployment_unit": "analytics",
    },
    {
        "name": "recommendation-service",
        "responsibility": "Prescriptive recommendations (P213-K).",
        "database_boundary": "analytics_prescriptive_*",
        "api_boundary": "/api/v1/analytics/prescriptive",
        "events": ("BiCommandExecuted",),
        "security_model": "analytics.prescriptive.*",
        "scaling_strategy": "horizontal_stateless",
        "deployment_unit": "analytics",
    },
    {
        "name": "notification-service",
        "responsibility": "Notification triggers via Notification Platform.",
        "database_boundary": "notifications_*",
        "api_boundary": "/api/v1/notifications",
        "events": ("BiStateChanged",),
        "security_model": "notifications.*",
        "scaling_strategy": "queue_backed",
        "deployment_unit": "notifications",
        "via_notification_platform": True,
    },
    {
        "name": "integration-service",
        "responsibility": "External connectors via Integration Platform.",
        "database_boundary": "integration_*",
        "api_boundary": "/api/v1/integrations",
        "events": ("BiIntegrationPublished",),
        "security_model": "integrations.*",
        "scaling_strategy": "queue_backed",
        "deployment_unit": "integration",
        "via_integration_platform": True,
    },
)

SERVICE_COMMUNICATION: dict[str, Any] = {
    "synchronous": ("rest", "grpc"),
    "asynchronous": ("kafka", "amqp", "cloudevents"),
    "patterns": (
        "request_reply",
        "publish_subscribe",
        "event_notification",
        "saga",
        "outbox",
        "inbox",
        "event_choreography",
        "orchestration",
    ),
    "via_enterprise_event_fabric": True,
    "outbox_required": True,
}

READ_MODELS: dict[str, Any] = {
    "types": (
        "executive",
        "operational",
        "dashboard",
        "reporting",
        "analytics",
        "prediction",
        "decision",
        "knowledge_graph",
    ),
    "materialised_views": True,
    "caching": True,
    "distributed_read_replicas": True,
}

API_BOUNDARIES: dict[str, Any] = {
    "ops": (
        "/api/v1/analytics/ops",
        "/api/v1/analytics/ops/cqrs",
        "/api/v1/analytics/ops/events",
        "/api/v1/analytics/ops/streaming",
        "/api/v1/analytics/ops/apis",
        "/api/v1/analytics/ops/microservices",
        "/api/v1/analytics/ops/communication",
        "/api/v1/analytics/ops/read-models",
        "/api/v1/analytics/ops/security",
        "/api/v1/analytics/ops/observability",
        "/api/v1/analytics/ops/resilience",
        "/api/v1/analytics/ops/deployment",
        "/api/v1/analytics/ops/cicd",
        "/api/v1/analytics/ops/testing",
    ),
    "rest": True,
    "graphql": "/api/v1/analytics/graphql",
    "grpc": True,
    "streaming_apis": True,
    "async_event_apis": "analytics.ops.*.v1",
    "via_api_gateway": True,
    "security": (
        "analytics.ops.read",
        "zero_trust",
        "tenant_isolation",
    ),
}

SECURITY: dict[str, Any] = {
    "via_p207": True,
    "via_p208": True,
    "via_p209": True,
    "via_p210": True,
    "via_p211": True,
    "via_p212": True,
    "oauth2": True,
    "oidc": True,
    "jwt": True,
    "mtls": True,
    "spiffe_spire": True,
    "api_keys": True,
    "fine_grained_authorization": True,
    "rate_limiting": True,
    "api_auditing": True,
    "zero_trust": True,
    "module_local_gateway_forbidden": True,
    "module_local_event_bus_forbidden": True,
}

OBSERVABILITY: dict[str, Any] = {
    "distributed_tracing": True,
    "metrics": True,
    "structured_logging": True,
    "correlation_ids": True,
    "opentelemetry": True,
    "health_checks": True,
    "business_metrics": True,
    "event_metrics": True,
    "service_metrics": True,
    "api_metrics": True,
    "via_platform_observability": True,
    "module_local_metrics_store_forbidden": True,
}

RESILIENCE: dict[str, Any] = {
    "circuit_breaker": True,
    "retry": True,
    "timeout": True,
    "bulkhead": True,
    "fallback": True,
    "rate_limiting": True,
    "dead_letter_queue": True,
    "poison_message_queue": True,
    "disaster_recovery": True,
    "geo_replication": True,
}

DEPLOYMENT: dict[str, Any] = {
    "kubernetes": True,
    "service_mesh": True,
    "ingress_controller": True,
    "api_gateway": True,
    "kafka_cluster": True,
    "redis_cluster": True,
    "object_storage": True,
    "container_registry": True,
    "gitops": True,
    "autoscaling": True,
    "multi_region": True,
    "blue_green": True,
    "canary": True,
    "cloud_native": True,
    "high_availability": True,
    "disaster_recovery": True,
}

CICD: dict[str, Any] = {
    "continuous_integration": True,
    "continuous_delivery": True,
    "continuous_deployment": True,
    "gitops": True,
    "infrastructure_as_code": True,
    "progressive_delivery": True,
    "automated_rollback": True,
    "security_gates": True,
    "policy_validation": True,
}

TESTING: tuple[str, ...] = (
    "unit_testing",
    "integration_testing",
    "consumer_contract_testing",
    "provider_contract_testing",
    "api_testing",
    "event_testing",
    "replay_testing",
    "load_testing",
    "performance_testing",
    "chaos_engineering",
    "security_testing",
    "penetration_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_integration_vision",
    "ddd_domain_model",
    "bounded_context_architecture",
    "cqrs_architecture",
    "event_sourcing_platform",
    "event_streaming_platform",
    "api_management_platform",
    "microservice_platform",
    "service_communication",
    "read_model_architecture",
    "api_security",
    "observability",
    "resilience",
    "cloud_native_deployment",
    "cicd",
    "testing_architecture",
    "quality_gates",
    "production_readiness_checklist",
    "service_discovery",
    "integration_fabric",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "cqrs_architecture_is_incomplete",
    "event_sourcing_platform_is_missing",
    "event_streaming_platform_is_missing",
    "api_management_platform_is_missing",
    "enterprise_integration_platform_is_missing",
    "microservices_platform_is_missing",
    "read_model_architecture_is_missing",
    "api_first_design_is_missing",
    "cloud_native_deployment_is_missing",
    "zero_trust_security_is_missing",
    "observability_is_missing",
    "high_availability_is_missing",
    "disaster_recovery_is_missing",
    "continuous_governance_is_missing",
    "bi_cqrs_architecture_is_incomplete",
    "sibling_business_intelligence_bc",
)

INTEGRATION_FLOW: tuple[str, ...] = (
    "analytics_services",
    "exchange_commands",
    "publish_events",
    "consume_events",
    "synchronise_read_models",
    "expose_apis",
    "collaborate_through_events",
    "operate_independently",
    "scale_independently",
    "recover_independently",
)


def vision() -> dict[str, Any]:
    return {
        "statement": PRINCIPLE,
        "fabric": FABRIC,
        "flow": list(INTEGRATION_FLOW),
        "qualities": (
            "highly_available",
            "fault_tolerant",
            "observable",
            "secure",
            "cloud_native",
        ),
        "via_enterprise_event_fabric": True,
        "via_api_gateway": True,
        "why": {
            "cqrs": "Separate write decisions from read intelligence consumption.",
            "event_sourcing": "Durable, replayable enterprise decision history.",
            "event_streaming": "Independent scale and recovery across services.",
            "api_first": "Contract-first collaboration without shared databases.",
            "microservices": "Independent deployability per analytics capability.",
            "event_driven_bi": "Superior decoupling vs synchronous BI monoliths.",
        },
    }


def domain_model() -> dict[str, Any]:
    return {
        "core_domain": CORE_DOMAIN,
        "supporting_domains": [dict(d) for d in SUPPORTING_DOMAINS],
        "supporting_count": len(SUPPORTING_DOMAINS),
        "aggregate": dict(AGGREGATE),
    }


def bounded_contexts() -> dict[str, Any]:
    return {
        "contexts": list(LOGICAL_BOUNDED_CONTEXTS),
        "context_count": len(LOGICAL_BOUNDED_CONTEXTS),
        "logical_only": True,
        "sibling_bc_forbidden": True,
    }


def cqrs() -> dict[str, Any]:
    return {
        **CQRS_PLATFORM,
        "command_count": len(COMMANDS),
        "query_count": len(QUERIES),
        "alignment_present_required": True,
        "events": [e["name"] for e in CORE_EVENTS],
        "event_count": len(CORE_EVENTS),
    }


def event_sourcing() -> dict[str, Any]:
    return dict(EVENT_SOURCING)


def event_streaming() -> dict[str, Any]:
    return dict(EVENT_STREAMING)


def api_management() -> dict[str, Any]:
    return dict(API_MANAGEMENT)


def events() -> dict[str, Any]:
    return {
        "core_events": [dict(e) for e in CORE_EVENTS],
        "core_event_count": len(CORE_EVENTS),
        "event_driven_required": True,
        "replay_strategy": "outbox_replay_by_event_id",
        "version_strategy": "append_only_vN",
        "via_enterprise_event_fabric": True,
    }


def microservices() -> dict[str, Any]:
    return {
        "services": [dict(s) for s in MICROSERVICES],
        "service_count": len(MICROSERVICES),
        "logical_decomposition": True,
        "database_per_service": True,
        "independently_deployable": True,
    }


def service_communication() -> dict[str, Any]:
    return dict(SERVICE_COMMUNICATION)


def read_models() -> dict[str, Any]:
    return {
        **READ_MODELS,
        "type_count": len(READ_MODELS["types"]),
    }


def api_boundaries() -> dict[str, Any]:
    return dict(API_BOUNDARIES)


def security() -> dict[str, Any]:
    return dict(SECURITY)


def observability() -> dict[str, Any]:
    return dict(OBSERVABILITY)


def resilience() -> dict[str, Any]:
    return dict(RESILIENCE)


def deployment() -> dict[str, Any]:
    return dict(DEPLOYMENT)


def cicd() -> dict[str, Any]:
    return dict(CICD)


def testing() -> dict[str, Any]:
    return {"suites": list(TESTING), "suite_count": len(TESTING)}


def cursor_outputs() -> dict[str, Any]:
    return {"outputs": list(CURSOR_OUTPUTS), "count": len(CURSOR_OUTPUTS)}


def quality_gates() -> dict[str, Any]:
    return {
        "reject_if": list(QUALITY_GATES_REJECT_IF),
        "count": len(QUALITY_GATES_REJECT_IF),
    }


def production_readiness() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "checklist": {
            "cqrs_platform": True,
            "event_sourcing_platform": True,
            "event_streaming_platform": True,
            "api_management_platform": True,
            "enterprise_integration_platform": True,
            "microservices_platform": True,
            "read_models": True,
            "service_discovery": True,
            "api_security": True,
            "observability": True,
            "cloud_native_deployment": True,
            "cicd": True,
            "testing_architecture": True,
            "governance_architecture": True,
            "foundation_tests": True,
            "ops_api_live": True,
        },
        "verdict": "ENTERPRISE_GRADE",
    }


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "adr": ADR,
        "sor": SOR,
        "product": PRODUCT,
        "capability": CAPABILITY,
        "principle": PRINCIPLE,
        "fabric": FABRIC,
        "builds_on": [
            "P213-A",
            "P213-B",
            "P213-C",
            "P213-D",
            "P213-E",
            "P213-F",
            "P213-G",
            "P213-H",
            "P213-I",
            "P213-J",
            "P213-K",
            "P213-L",
            "P213-M",
            "ADR-394",
            "ADR-395",
            "ADR-396",
            "ADR-408",
            "ADR-409",
            "ADR-410",
            "ADR-411",
            "ADR-412",
            "ADR-413",
            "ADR-414",
            "ADR-415",
            "ADR-416",
            "ADR-417",
            "P207",
            "P208",
            "P209",
            "P210",
            "P211",
            "P212",
        ],
        "architecture": {
            "present_required": True,
            "not_incomplete": True,
            "capabilities": [
                "enterprise_cqrs_architecture",
                "enterprise_event_sourcing_platform",
                "enterprise_event_streaming_platform",
                "enterprise_api_management_platform",
                "enterprise_integration_platform",
                "enterprise_messaging_platform",
                "enterprise_analytics_event_fabric",
                "enterprise_microservices_runtime",
                "enterprise_service_discovery",
                "enterprise_distributed_communication_layer",
            ],
            "capability_count": 10,
        },
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "cqrs": cqrs(),
        "event_sourcing": event_sourcing(),
        "event_streaming": event_streaming(),
        "api_management": api_management(),
        "events": events(),
        "microservices": microservices(),
        "service_communication": service_communication(),
        "read_models": read_models(),
        "apis": api_boundaries(),
        "security": security(),
        "observability": observability(),
        "resilience": resilience(),
        "deployment": deployment(),
        "cicd": cicd(),
        "testing": testing(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "cqrs_architecture_present_required": True,
        "event_sourcing_platform_present_required": True,
        "event_streaming_platform_present_required": True,
        "api_management_platform_present_required": True,
        "enterprise_integration_platform_present_required": True,
        "microservices_platform_present_required": True,
        "read_model_architecture_present_required": True,
        "api_first_design_present_required": True,
        "cloud_native_deployment_present_required": True,
        "zero_trust_security_present_required": True,
        "observability_present_required": True,
        "high_availability_present_required": True,
        "disaster_recovery_present_required": True,
        "continuous_governance_present_required": True,
        "architecture_present_required": True,
        "sibling_business_intelligence_bc_forbidden": True,
        "via_enterprise_event_fabric": True,
        "via_api_gateway": True,
        "module_local_event_bus_forbidden": True,
        "module_local_gateway_forbidden": True,
        "api_prefix": f"{API_PREFIX}/ops",
        "forbidden_sibling_bc": [
            "business_intelligence",
            "decision_intelligence",
            "reporting_platform",
            "metric_governance_platform",
            "visualization_platform",
            "bi_core",
        ],
    }


def ops_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /analytics/ops",
            "GET /analytics/ops/vision",
            "GET /analytics/ops/domain",
            "GET /analytics/ops/bounded-contexts",
            "GET /analytics/ops/cqrs",
            "GET /analytics/ops/event-sourcing",
            "GET /analytics/ops/streaming",
            "GET /analytics/ops/apis",
            "GET /analytics/ops/events",
            "GET /analytics/ops/microservices",
            "GET /analytics/ops/communication",
            "GET /analytics/ops/read-models",
            "GET /analytics/ops/security",
            "GET /analytics/ops/observability",
            "GET /analytics/ops/resilience",
            "GET /analytics/ops/deployment",
            "GET /analytics/ops/cicd",
            "GET /analytics/ops/testing",
            "GET /analytics/ops/outputs",
            "GET /analytics/ops/production-readiness",
            "GET /analytics/ops/readiness",
        ],
    }
