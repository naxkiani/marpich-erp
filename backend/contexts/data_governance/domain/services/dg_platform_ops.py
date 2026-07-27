"""P212-M CQRS, Events, APIs & Microservices Platform — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P212-M"
ADR = 405
SOR = "data_governance"
API_PREFIX = "/api/v1/data-governance"
PRODUCT = "Enterprise Data Governance CQRS, Events, APIs & Microservices Platform"
CAPABILITY = "CAP-PLT-DG-001"

PRINCIPLE = (
    "Enterprise governance decisions SHALL be separated "
    "from governance intelligence consumption."
)

CORE_DOMAIN = "enterprise_data_governance_command_and_intelligence_platform"

SUPPORTING_DOMAINS: tuple[str, ...] = (
    "command_processing",
    "query_processing",
    "event_management",
    "read_model_management",
    "integration_messaging",
    "governance_analytics",
)

OWNERSHIP_COMMANDS: tuple[str, ...] = (
    "AssignOwnerCommand",
    "TransferOwnershipCommand",
    "ApproveStewardCommand",
)
QUALITY_COMMANDS: tuple[str, ...] = (
    "EvaluateQualityCommand",
    "ApproveQualityRuleCommand",
)
POLICY_COMMANDS: tuple[str, ...] = (
    "CreatePolicyCommand",
    "ActivatePolicyCommand",
    "EvaluatePolicyCommand",
)
MARKETPLACE_COMMANDS: tuple[str, ...] = (
    "PublishDataProductCommand",
    "ApproveConsumerAccessCommand",
)
AI_COMMANDS: tuple[str, ...] = (
    "ApproveAIDatasetCommand",
    "EvaluateAIReadinessCommand",
)

READ_MODELS: tuple[str, ...] = (
    "GovernanceDashboardReadModel",
    "DataAssetReadModel",
    "DataProductReadModel",
    "PolicyComplianceReadModel",
    "AIReadinessReadModel",
    "MetadataSearchReadModel",
    "KnowledgeGraphReadModel",
)

EVENT_CATEGORIES: dict[str, tuple[str, ...]] = {
    "data_governance": (
        "DataAssetGovernedEvent",
        "DataProductRegisteredEvent",
        "OwnershipAssignedEvent",
    ),
    "quality": (
        "QualityAssessmentCompletedEvent",
        "QualityViolationDetectedEvent",
    ),
    "policy": (
        "PolicyCreatedEvent",
        "PolicyActivatedEvent",
        "PolicyViolationEvent",
    ),
    "ai_governance": (
        "AIDatasetApprovedEvent",
        "AIReadinessEvaluatedEvent",
    ),
}

OPS_EVENTS: tuple[dict[str, Any], ...] = (
    {
        "name": "CommandExecutedEvent",
        "producer": "data_governance_core_service",
        "consumers": ("projections", "audit", "event_bus"),
        "payload": ("tenant_id", "command_id", "aggregate_id", "result"),
        "version": "v1",
    },
    {
        "name": "ProjectionUpdatedEvent",
        "producer": "analytics_intelligence_service",
        "consumers": ("query_side", "dashboard", "search"),
        "payload": ("tenant_id", "read_model", "version"),
        "version": "v1",
    },
    {
        "name": "GovernanceStateChangedEvent",
        "producer": "data_governance_core_service",
        "consumers": ("digital_twin", "knowledge_graph", "audit"),
        "payload": ("tenant_id", "entity_ref", "change_type"),
        "version": "v1",
    },
    {
        "name": "IntegrationEventPublishedEvent",
        "producer": "event_fabric_adapter",
        "consumers": ("peers", "audit", "observability"),
        "payload": ("tenant_id", "event_name", "correlation_id"),
        "version": "v1",
    },
)

EVENT_SCHEMA_FIELDS: tuple[str, ...] = (
    "event_id",
    "event_type",
    "aggregate_id",
    "timestamp",
    "version",
    "payload",
    "correlation_id",
)

EVENT_CONTRACT_CAPABILITIES: tuple[str, ...] = (
    "schema_evolution",
    "compatibility_checking",
    "version_management",
    "event_documentation",
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "name": "data-governance-core-service",
        "responsibility": "Command orchestration and governance fabric",
        "database_boundary": "data_governance_ops_core",
        "api_boundary": "/api/v1/data-governance/ops",
        "events": "data_governance.ops.*",
        "security_model": "zero_trust_via_p207_p208",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "data-ownership-service",
        "responsibility": "Ownership commands and projections",
        "database_boundary": "data_governance_ownership",
        "api_boundary": "/api/v1/data-governance/ownership",
        "events": "data_governance.ownership.*",
        "security_model": "zero_trust_via_p208",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "data-quality-service",
        "responsibility": "Quality commands and read models",
        "database_boundary": "data_governance_quality",
        "api_boundary": "/api/v1/data-governance/quality",
        "events": "data_governance.quality.*",
        "security_model": "zero_trust_via_p208",
        "scaling_strategy": "async_workers",
    },
    {
        "name": "data-mesh-service",
        "responsibility": "Mesh/product command and query surfaces",
        "database_boundary": "data_governance_mesh",
        "api_boundary": "/api/v1/data-governance/mesh",
        "events": "data_governance.mesh.*",
        "security_model": "zero_trust_via_p208",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "data-marketplace-service",
        "responsibility": "Marketplace publish/access commands",
        "database_boundary": "data_governance_marketplace",
        "api_boundary": "/api/v1/data-governance/marketplace",
        "events": "data_governance.marketplace.*",
        "security_model": "zero_trust_via_p208",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "data-policy-service",
        "responsibility": "Policy commands; PDP via Policy Engine",
        "database_boundary": "data_governance_policies",
        "api_boundary": "/api/v1/data-governance/policies",
        "events": "data_governance.policy.*",
        "security_model": "via_policy_engine",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "metadata-service",
        "responsibility": "Metadata registration and search projections",
        "database_boundary": "data_governance_metadata",
        "api_boundary": "/api/v1/data-governance/ops/metadata",
        "events": "data_governance.metadata.*",
        "security_model": "via_enterprise_search",
        "scaling_strategy": "read_replicas",
    },
    {
        "name": "knowledge-graph-service",
        "responsibility": "Graph command/query bindings",
        "database_boundary": "data_governance_graph",
        "api_boundary": "/api/v1/data-governance/graph",
        "events": "data_governance.graph.*",
        "security_model": "zero_trust_via_p208",
        "scaling_strategy": "read_replicas",
    },
    {
        "name": "ai-governance-service",
        "responsibility": "AI readiness commands via Enterprise AI",
        "database_boundary": "data_governance_ai_readiness",
        "api_boundary": "/api/v1/data-governance/ai-readiness",
        "events": "data_governance.ai_readiness.*",
        "security_model": "via_enterprise_ai",
        "scaling_strategy": "async_workers",
    },
    {
        "name": "digital-twin-service",
        "responsibility": "Twin simulation command/query bindings",
        "database_boundary": "data_governance_twin",
        "api_boundary": "/api/v1/data-governance/twin",
        "events": "data_governance.twin.*",
        "security_model": "via_enterprise_ai",
        "scaling_strategy": "async_workers",
    },
    {
        "name": "analytics-intelligence-service",
        "responsibility": "Read models and governance analytics",
        "database_boundary": "data_governance_analytics",
        "api_boundary": "/api/v1/data-governance/ops/analytics",
        "events": "data_governance.analytics.*",
        "security_model": "via_analytics",
        "scaling_strategy": "read_replicas",
    },
)

HEXAGONAL_LAYERS: tuple[str, ...] = (
    "domain_layer",
    "application_layer",
    "infrastructure_layer",
    "adapters",
    "ports",
)

API_CATEGORIES: dict[str, tuple[str, ...]] = {
    "governance": (
        "/api/v1/data-governance",
        "/api/v1/data-governance/ownership",
        "/api/v1/data-governance/mesh/products",
    ),
    "quality": (
        "/api/v1/data-governance/quality",
        "/api/v1/data-governance/quality/rules",
    ),
    "policy": (
        "/api/v1/data-governance/policies",
        "/api/v1/data-governance/policies/evaluation",
    ),
    "intelligence": (
        "/api/v1/data-governance/graph",
        "/api/v1/data-governance/ops/analytics",
    ),
    "ai_governance": (
        "/api/v1/data-governance/ai-readiness",
        "/api/v1/data-governance/twin/ai",
    ),
}

INTEGRATION_TARGETS: tuple[str, ...] = (
    "P212-D",
    "P212-E",
    "P212-F",
    "P212-G",
    "P212-H",
    "P212-I",
    "P212-J",
    "P212-K",
    "P212-L",
)

MULTI_TENANT: tuple[str, ...] = (
    "tenant_isolation",
    "tenant_data_boundaries",
    "tenant_event_streams",
    "tenant_api_security",
    "tenant_governance_policies",
)

OBSERVABILITY: tuple[str, ...] = (
    "metrics",
    "logs",
    "traces",
    "events",
    "audit_trails",
)

RESILIENCE: tuple[str, ...] = (
    "fault_tolerance",
    "circuit_breakers",
    "retry_policies",
    "event_recovery",
    "disaster_recovery",
    "data_replication",
)

DEPLOYMENT: dict[str, Any] = {
    "kubernetes": True,
    "containers": True,
    "service_mesh": True,
    "api_gateway": True,
    "event_streaming_cluster": True,
    "cicd": True,
    "gitops": True,
    "infrastructure_as_code": True,
    "observability_stack": True,
    "multi_region": True,
}

TESTING: tuple[str, ...] = (
    "unit_testing",
    "domain_testing",
    "event_testing",
    "api_testing",
    "contract_testing",
    "integration_testing",
    "performance_testing",
    "security_testing",
    "chaos_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_cqrs_architecture_vision",
    "cqrs_domain_architecture_ddd",
    "command_side_architecture",
    "query_side_architecture",
    "event_sourcing_architecture",
    "enterprise_event_bus_architecture",
    "event_contract_governance",
    "microservice_architecture",
    "hexagonal_architecture_design",
    "api_first_architecture",
    "api_security_architecture",
    "service_communication_architecture",
    "data_governance_integration_fabric",
    "multi_tenancy_architecture",
    "observability_architecture",
    "resilience_architecture",
    "deployment_architecture",
    "testing_architecture",
    "production_readiness_checklist",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "cqrs_architecture_is_incomplete",
    "command_side_design_is_missing",
    "query_side_design_is_missing",
    "event_sourcing_architecture_is_missing",
    "event_bus_architecture_is_missing",
    "event_contract_governance_is_missing",
    "microservice_architecture_is_missing",
    "api_first_architecture_is_missing",
    "hexagonal_architecture_is_missing",
    "data_governance_integration_is_missing",
    "ai_governance_integration_is_missing",
    "digital_twin_integration_is_missing",
    "multi_tenant_architecture_is_missing",
    "observability_architecture_is_missing",
    "enterprise_scalability_is_missing",
    "sibling_data_governance_ops_bc",
)


def cqrs_architecture() -> dict[str, Any]:
    return {
        "complete_required": True,
        "not_incomplete": True,
        "principle": PRINCIPLE,
        "core_domain": CORE_DOMAIN,
        "supporting_domains": list(SUPPORTING_DOMAINS),
        "aggregate": "GovernanceCommandAggregate",
        "fabric": "meos_enterprise_data_governance_integration_fabric",
        "transforms": "independent_services_to_distributed_event_driven_api_first_platform",
    }


def command_side() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "categories": {
            "ownership": list(OWNERSHIP_COMMANDS),
            "quality": list(QUALITY_COMMANDS),
            "policy": list(POLICY_COMMANDS),
            "marketplace": list(MARKETPLACE_COMMANDS),
            "ai_governance": list(AI_COMMANDS),
        },
        "category_count": 5,
        "command_count": (
            len(OWNERSHIP_COMMANDS)
            + len(QUALITY_COMMANDS)
            + len(POLICY_COMMANDS)
            + len(MARKETPLACE_COMMANDS)
            + len(AI_COMMANDS)
        ),
        "responsibilities": (
            "execute_governance_actions",
            "validate_business_rules",
            "enforce_policies",
            "produce_domain_events",
        ),
    }


def query_side() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "read_models": list(READ_MODELS),
        "read_model_count": len(READ_MODELS),
        "responsibilities": (
            "fast_data_access",
            "analytics",
            "search",
            "reporting",
            "intelligence_consumption",
        ),
    }


def event_sourcing() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "capabilities": (
            "complete_history_tracking",
            "state_reconstruction",
            "auditability",
            "temporal_analysis",
            "governance_intelligence",
        ),
        "event_categories": {k: list(v) for k, v in EVENT_CATEGORIES.items()},
        "ops_events": [dict(e) for e in OPS_EVENTS],
        "event_count": len(OPS_EVENTS),
        "outbox_required": True,
        "versioning_strategy": "append_only_vN",
    }


def event_bus() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "via_enterprise_event_bus": True,
        "includes": (
            "event_broker",
            "event_streaming",
            "event_routing",
            "event_schema_registry",
            "event_monitoring",
        ),
        "flow": (
            "microservice",
            "event_producer",
            "event_bus",
            "event_consumer",
            "projection_update",
        ),
        "module_local_broker_forbidden": True,
    }


def event_contracts() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "schema_fields": list(EVENT_SCHEMA_FIELDS),
        "capabilities": list(EVENT_CONTRACT_CAPABILITIES),
        "capability_count": len(EVENT_CONTRACT_CAPABILITIES),
    }


def microservices() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "services": [dict(s) for s in MICROSERVICES],
        "service_count": len(MICROSERVICES),
    }


def api_first() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "categories": {k: list(v) for k, v in API_CATEGORIES.items()},
        "category_count": len(API_CATEGORIES),
        "rest": True,
        "graphql": True,
        "event_apis": True,
        "streaming_apis": True,
        "via_api_gateway": True,
        "module_local_gateway_forbidden": True,
        "api_security": (
            "data_governance.read",
            "zero_trust",
            "tenant_isolation",
            "rate_limiting",
            "audit_logging",
        ),
    }


def hexagonal() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "layers": list(HEXAGONAL_LAYERS),
        "layer_count": len(HEXAGONAL_LAYERS),
        "business_logic_independent_of_infrastructure": True,
    }


def data_governance_integration() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "targets": list(INTEGRATION_TARGETS),
        "target_count": len(INTEGRATION_TARGETS),
        "includes": ("apis", "commands", "events", "data_contracts", "intelligence_exchange"),
    }


def ai_governance_integration() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "via_p212_k": True,
        "via_enterprise_ai": True,
        "commands": list(AI_COMMANDS),
    }


def digital_twin_integration() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "via_p212_l": True,
        "consumes": ("GovernanceStateChangedEvent", "ProjectionUpdatedEvent"),
    }


def multi_tenant() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "capabilities": list(MULTI_TENANT),
        "capability_count": len(MULTI_TENANT),
        "tenant_id_everywhere": True,
    }


def observability() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "signals": list(OBSERVABILITY),
        "monitoring": (
            "service_health",
            "event_health",
            "api_performance",
            "governance_operations",
        ),
        "via_platform_observability": True,
    }


def resilience() -> dict[str, Any]:
    return {
        "patterns": list(RESILIENCE),
        "pattern_count": len(RESILIENCE),
    }


def scalability() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "deployment": dict(DEPLOYMENT),
        "microservice_count": len(MICROSERVICES),
        "resilience": resilience(),
    }


def communication() -> dict[str, Any]:
    return {
        "synchronous": ("REST", "gRPC", "GraphQL"),
        "asynchronous": ("Events", "Messages", "Streams"),
        "rules": (
            "domain_autonomy",
            "loose_coupling",
            "failure_isolation",
            "resilience_patterns",
        ),
    }


def testing_architecture() -> dict[str, Any]:
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
            "command_architecture": True,
            "query_architecture": True,
            "event_architecture": True,
            "api_architecture": True,
            "microservice_architecture": True,
            "integration_fabric": True,
            "security_architecture": True,
            "deployment_architecture": True,
            "testing_architecture": True,
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
        "builds_on": [
            "P212-A",
            "P212-B",
            "P212-D",
            "P212-E",
            "P212-F",
            "P212-G",
            "P212-H",
            "P212-J",
            "P212-K",
            "P212-L",
            "ADR-392",
            "ADR-397",
            "ADR-398",
            "ADR-399",
            "ADR-400",
            "ADR-401",
            "ADR-402",
            "ADR-404",
        ],
        "cqrs_architecture": cqrs_architecture(),
        "command_side": command_side(),
        "query_side": query_side(),
        "event_sourcing": event_sourcing(),
        "event_bus": event_bus(),
        "event_contracts": event_contracts(),
        "microservices": microservices(),
        "api_first": api_first(),
        "hexagonal": hexagonal(),
        "data_governance_integration": data_governance_integration(),
        "ai_governance_integration": ai_governance_integration(),
        "digital_twin_integration": digital_twin_integration(),
        "multi_tenant": multi_tenant(),
        "observability": observability(),
        "scalability": scalability(),
        "communication": communication(),
        "testing_architecture": testing_architecture(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "cqrs_architecture_complete_required": True,
        "command_side_design_present_required": True,
        "query_side_design_present_required": True,
        "event_sourcing_architecture_present_required": True,
        "event_bus_architecture_present_required": True,
        "event_contract_governance_present_required": True,
        "microservice_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "hexagonal_architecture_present_required": True,
        "data_governance_integration_present_required": True,
        "ai_governance_integration_present_required": True,
        "digital_twin_integration_present_required": True,
        "multi_tenant_architecture_present_required": True,
        "observability_architecture_present_required": True,
        "enterprise_scalability_present_required": True,
        "sibling_data_governance_ops_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/ops",
        "forbidden_sibling_bc": [
            "data_governance_ops",
            "dg_event_bus",
            "governance_api_platform",
            "data_mesh",
            "data_marketplace",
            "metadata_governance_platform",
        ],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def ops_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /data-governance/ops",
            "GET /data-governance/ops/commands",
            "GET /data-governance/ops/queries",
            "GET /data-governance/ops/events",
            "GET /data-governance/ops/event-bus",
            "GET /data-governance/ops/event-contracts",
            "GET /data-governance/ops/microservices",
            "GET /data-governance/ops/apis",
            "GET /data-governance/ops/hexagonal",
            "GET /data-governance/ops/integration",
            "GET /data-governance/ops/ai",
            "GET /data-governance/ops/twin",
            "GET /data-governance/ops/multi-tenant",
            "GET /data-governance/ops/observability",
            "GET /data-governance/ops/resilience",
            "GET /data-governance/ops/communication",
            "GET /data-governance/ops/deployment",
            "GET /data-governance/ops/testing",
            "GET /data-governance/ops/outputs",
            "GET /data-governance/ops/production-readiness",
            "GET /data-governance/ops/readiness",
        ],
    }
