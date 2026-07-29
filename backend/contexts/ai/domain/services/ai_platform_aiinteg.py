"""P214-M Enterprise AI Integration, AI API Gateway & Intelligent AI Service Mesh — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P214-M"
ADR = 433
SOR = "ai"
API_PREFIX = "/api/v1/ai"
PRODUCT = (
    "Enterprise AI Integration, AI API Gateway & Intelligent AI Service Mesh Platform"
)
CAPABILITY = "CAP-PLT-AI-001"

PRINCIPLE = (
    "Enterprise AI Integration Platform SHALL provide the secure, intelligent "
    "and autonomous communication fabric that connects all AI capabilities across MEOS."
)

FABRIC = "meos_intelligent_ai_integration_fabric"

CORE_DOMAIN = "enterprise_ai_integration_management"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {"id": "api_gateway", "purpose": "API exposure, management, routing, security."},
    {"id": "ai_service_mesh", "purpose": "Service communication, traffic, discovery, resilience."},
    {"id": "ai_communication", "purpose": "Secure AI service and agent messaging."},
    {"id": "event_integration", "purpose": "Event streaming, routing, governance."},
    {"id": "ai_workflow", "purpose": "AI workflow orchestration and automation."},
    {"id": "model_serving", "purpose": "Model endpoints, inference routing, optimization."},
    {"id": "agent_communication", "purpose": "Agent-to-agent and tool communication."},
    {"id": "integration_governance", "purpose": "Policies, contracts, compliance, audit."},
    {"id": "traffic_intelligence", "purpose": "Dynamic, cost and performance-aware routing."},
)

AGGREGATE = {
    "name": "EnterpriseAIIntegrationAggregate",
    "root": "EnterpriseAIIntegration",
    "entities": (
        "AIServiceEndpoint",
        "AIAPI",
        "AIModelEndpoint",
        "AIAgentEndpoint",
        "ServiceMeshNode",
        "IntegrationPolicy",
        "RoutingRule",
        "EventChannel",
        "WorkflowDefinition",
        "CommunicationSession",
        "IntegrationContract",
    ),
    "value_objects": (
        "APIIdentifier",
        "ServiceIdentifier",
        "EndpointIdentifier",
        "RoutingDecision",
        "SecurityContext",
        "TrafficPolicy",
        "IntegrationVersion",
        "LatencyMetric",
    ),
    "events": (
        "AIServiceRegisteredEvent",
        "APIExposureCreatedEvent",
        "RoutingPolicyChangedEvent",
        "ServiceConnectedEvent",
        "IntegrationFailureDetectedEvent",
        "TrafficOptimizedEvent",
        "CommunicationCompletedEvent",
    ),
}

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "ai_api_gateway",
        "bc": "BC-01",
        "name": "AI API Gateway Context",
        "purpose": "API exposure, management, request routing, security enforcement.",
    },
    {
        "id": "ai_service_mesh",
        "bc": "BC-02",
        "name": "AI Service Mesh Context",
        "purpose": "Service communication, traffic management, discovery, resilience.",
    },
    {
        "id": "ai_event_fabric",
        "bc": "BC-03",
        "name": "AI Event Fabric Context",
        "purpose": "Event streaming, routing, governance via platform Event Fabric.",
    },
    {
        "id": "ai_workflow_integration",
        "bc": "BC-04",
        "name": "AI Workflow Integration Context",
        "purpose": "AI workflow orchestration, process automation, cross-system execution.",
    },
    {
        "id": "ai_model_serving",
        "bc": "BC-05",
        "name": "AI Model Serving Context",
        "purpose": "Model endpoints, inference routing, model selection, serving optimization.",
    },
    {
        "id": "ai_agent_communication",
        "bc": "BC-06",
        "name": "AI Agent Communication Context",
        "purpose": "Agent-to-agent communication, collaboration, tool communication.",
    },
    {
        "id": "integration_governance",
        "bc": "BC-07",
        "name": "Integration Governance Context",
        "purpose": "Policies, contracts, compliance, audit.",
    },
)

AI_API_GATEWAY = {
    "present_required": True,
    "name": "MEOS AI API Gateway",
    "via_api_gateway": True,
    "supports": (
        "ai_apis",
        "llm_apis",
        "model_apis",
        "agent_apis",
        "knowledge_apis",
        "data_apis",
        "business_apis",
    ),
    "capabilities": (
        "api_discovery",
        "api_security",
        "authentication",
        "authorization",
        "rate_limiting",
        "request_transformation",
        "response_validation",
        "api_analytics",
    ),
    "note": "Platform API Gateway owns edge; AI catalog defines AI route contracts via ACL.",
}

INTELLIGENT_ROUTING = {
    "present_required": True,
    "platform": "ai_traffic_intelligence_platform",
    "supports": (
        "dynamic_routing",
        "model_selection",
        "load_balancing",
        "context_aware_routing",
        "cost_aware_routing",
        "performance_aware_routing",
    ),
    "uses": (
        "ai_operations_data",
        "ai_performance_intelligence",
        "policy_intelligence",
    ),
    "via_p214_j": True,
}

AI_SERVICE_MESH = {
    "present_required": True,
    "manages": (
        "ai_microservices",
        "model_services",
        "agent_services",
        "knowledge_services",
        "data_services",
        "security_services",
    ),
    "capabilities": (
        "service_discovery",
        "traffic_control",
        "observability",
        "encryption",
        "resilience",
        "fault_injection",
    ),
}

MODEL_SERVING_GATEWAY = {
    "present_required": True,
    "via_p214_l": True,
    "via_p214_d": True,
    "supports": (
        "machine_learning_models",
        "deep_learning_models",
        "foundation_models",
        "llms",
        "custom_ai_models",
    ),
    "capabilities": (
        "model_routing",
        "version_selection",
        "canary_deployment",
        "ab_testing",
        "inference_optimization",
    ),
}

AGENT_COMMUNICATION = {
    "present_required": True,
    "via_p214_f": True,
    "supports": (
        "agent_discovery",
        "agent_identity",
        "agent_messaging",
        "agent_collaboration",
        "agent_workflow",
        "agent_negotiation",
    ),
}

EVENT_DRIVEN_INTEGRATION = {
    "present_required": True,
    "via_event_fabric": True,
    "events": (
        "model_events",
        "agent_events",
        "knowledge_events",
        "security_events",
        "governance_events",
        "operational_events",
    ),
    "capabilities": (
        "event_streaming",
        "event_processing",
        "event_routing",
        "event_replay",
        "event_governance",
    ),
}

WORKFLOW_ORCHESTRATION = {
    "present_required": True,
    "via_workflow_engine": True,
    "supports": (
        "multi_agent_workflows",
        "ai_business_processes",
        "decision_workflows",
        "automation_pipelines",
        "human_approval_workflows",
    ),
}

INTEGRATION_SECURITY = {
    "present_required": True,
    "zero_trust": True,
    "integrates": ("P207", "P208", "P209", "P210", "P211", "P214-I"),
    "implements": (
        "zero_trust_communication",
        "mtls",
        "api_security",
        "token_security",
        "policy_enforcement",
        "communication_audit",
    ),
}

INTEGRATION_KNOWLEDGE_GRAPH = {
    "present_required": True,
    "via_p214_g": True,
    "represents": (
        "services",
        "apis",
        "models",
        "agents",
        "dependencies",
        "policies",
        "events",
        "communication_paths",
    ),
    "enables": (
        "impact_analysis",
        "dependency_discovery",
        "failure_prediction",
        "optimization",
    ),
}

INTEGRATION_DIGITAL_TWIN = {
    "present_required": True,
    "represents": (
        "api_state",
        "service_state",
        "traffic_state",
        "dependency_state",
        "performance_state",
        "security_state",
    ),
    "enables": (
        "simulation",
        "optimization",
        "capacity_planning",
        "autonomous_management",
    ),
}

OBSERVABILITY = {
    "present_required": True,
    "via_p214_j": True,
    "via_observability": True,
    "monitors": (
        "api_traffic",
        "service_communication",
        "latency",
        "errors",
        "availability",
        "security_events",
        "ai_inference_traffic",
        "agent_communication",
    ),
}

COMMANDS: tuple[str, ...] = (
    "RegisterAIServiceCommand",
    "CreateAPICommand",
    "ConfigureRoutingCommand",
    "ConnectServiceCommand",
    "PublishEventChannelCommand",
    "UpdateIntegrationPolicyCommand",
)

QUERIES: tuple[str, ...] = (
    "GetAPIQuery",
    "GetServiceStatusQuery",
    "GetRoutingStatusQuery",
    "GetCommunicationHistoryQuery",
    "GetIntegrationHealthQuery",
)

CORE_EVENTS: tuple[dict[str, str], ...] = (
    {"name": "APIRegisteredEvent", "owner": "ai", "consumers": "audit,gateway"},
    {"name": "ServiceConnectedEvent", "owner": "ai", "consumers": "observability,aiops"},
    {"name": "RoutingChangedEvent", "owner": "ai", "consumers": "gateway,audit"},
    {"name": "MessageDeliveredEvent", "owner": "ai", "consumers": "agents,observability"},
    {"name": "IntegrationFailedEvent", "owner": "ai", "consumers": "aiops,notifications"},
    {"name": "PolicyViolationDetectedEvent", "owner": "ai", "consumers": "governance,aisec,audit"},
    {"name": "TrafficOptimizedEvent", "owner": "ai", "consumers": "analytics,aiops"},
    {"name": "CommunicationCompletedEvent", "owner": "ai", "consumers": "audit"},
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "id": "api_gateway_service",
        "responsibility": "AI API contract and exposure orchestration",
        "api": "/ai/aiinteg/gateway",
        "db": "ai_*",
        "events": ("APIRegisteredEvent",),
        "security": ("ai.assist.read",),
        "scaling": "edge_ha",
    },
    {
        "id": "service_discovery_service",
        "responsibility": "AI service registry and discovery",
        "api": "/ai/aiinteg/discovery",
        "db": "ai_*",
        "events": ("ServiceConnectedEvent",),
        "security": ("ai.assist.read",),
        "scaling": "control_plane",
    },
    {
        "id": "routing_intelligence_service",
        "responsibility": "dynamic cost and performance-aware routing",
        "api": "/ai/aiinteg/routing",
        "db": "ai_*",
        "events": ("RoutingChangedEvent", "TrafficOptimizedEvent"),
        "security": ("ai.assist.infer",),
        "scaling": "stateless_replicas",
    },
    {
        "id": "service_mesh_control_service",
        "responsibility": "mesh policy and resilience control plane",
        "api": "/ai/aiinteg/mesh",
        "db": "ai_*",
        "events": ("ServiceConnectedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "control_plane",
    },
    {
        "id": "model_serving_gateway_service",
        "responsibility": "inference routing and canary selection",
        "api": "/ai/aiinteg/serving",
        "db": "ai_*",
        "events": ("RoutingChangedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "online_low_latency",
    },
    {
        "id": "agent_communication_service",
        "responsibility": "agent messaging and collaboration fabric",
        "api": "/ai/aiinteg/agents",
        "db": "ai_*",
        "events": ("MessageDeliveredEvent", "CommunicationCompletedEvent"),
        "security": ("ai.assist.infer",),
        "scaling": "async_workers",
    },
    {
        "id": "event_streaming_service",
        "responsibility": "AI event channel contracts to Event Fabric",
        "api": "/ai/aiinteg/events",
        "db": "ai_*",
        "events": ("APIRegisteredEvent",),
        "security": ("ai.assist.read",),
        "scaling": "stream_consumers",
    },
    {
        "id": "workflow_service",
        "responsibility": "AI workflow orchestration via Workflow Engine",
        "api": "/ai/aiinteg/workflows",
        "db": "ai_*",
        "events": ("CommunicationCompletedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "worker_pools",
    },
    {
        "id": "integration_governance_service",
        "responsibility": "integration policies contracts compliance",
        "api": "/ai/aiinteg/governance",
        "db": "ai_*",
        "events": ("PolicyViolationDetectedEvent",),
        "security": ("ai.assist.read",),
        "scaling": "policy_evaluate",
    },
    {
        "id": "traffic_analytics_service",
        "responsibility": "AI traffic and latency analytics",
        "api": "/ai/aiinteg/traffic",
        "db": "ai_*",
        "events": ("TrafficOptimizedEvent", "IntegrationFailedEvent"),
        "security": ("ai.assist.read",),
        "scaling": "analytics_pipeline",
    },
)

API_SURFACES: tuple[str, ...] = (
    "/api/v1/ai/aiinteg/gateway",
    "/api/v1/ai/aiinteg/mesh",
    "/api/v1/ai/aiinteg/routing",
    "/api/v1/ai/aiinteg/serving",
    "/api/v1/ai/aiinteg/agents",
    "/api/v1/ai/aiinteg/events",
    "/api/v1/ai/aiinteg/workflows",
    "/api/v1/ai/aiinteg/governance",
)

API_STYLES: tuple[str, ...] = ("REST", "GraphQL", "gRPC", "Streaming", "Event")

SECURITY = dict(INTEGRATION_SECURITY)

DEPLOYMENT = {
    "present_required": True,
    "cloud_native": True,
    "via_p213_o": True,
    "components": (
        "kubernetes",
        "api_gateway_cluster",
        "service_mesh_control_plane",
        "event_streaming_cluster",
        "workflow_engine",
        "security_gateway",
        "observability_stack",
    ),
}

TESTING: tuple[str, ...] = (
    "api_testing",
    "integration_testing",
    "service_mesh_testing",
    "event_testing",
    "performance_testing",
    "security_testing",
    "failure_testing",
    "chaos_engineering",
    "scalability_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_ai_integration_vision",
    "ddd_domain_model",
    "bounded_context_map",
    "ai_api_gateway_platform",
    "intelligent_routing_engine",
    "ai_service_mesh",
    "model_serving_gateway",
    "agent_communication_fabric",
    "event_driven_ai_integration",
    "ai_workflow_orchestration",
    "integration_security",
    "integration_knowledge_graph",
    "integration_digital_twin",
    "cqrs_commands_queries",
    "event_sourcing_schema",
    "microservice_boundaries",
    "observability_architecture",
    "cloud_native_deployment",
    "testing_architecture",
    "quality_gates_dod",
    "adr_433",
    "enterprise_ai_aiinteg_law",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "enterprise_ai_api_gateway_is_missing",
    "intelligent_service_mesh_is_missing",
    "ai_communication_fabric_is_missing",
    "model_serving_gateway_is_missing",
    "agent_communication_platform_is_missing",
    "event_integration_platform_is_missing",
    "workflow_orchestration_is_missing",
    "integration_governance_is_missing",
    "security_architecture_is_missing",
    "knowledge_graph_integration_is_missing",
    "digital_twin_integration_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "api_first_architecture_is_missing",
    "zero_trust_security_is_missing",
    "cloud_native_deployment_is_missing",
    "sibling_ai_bc",
)


def vision() -> dict[str, Any]:
    return {
        "role": "MEOS Intelligent AI Integration Fabric",
        "principle": PRINCIPLE,
        "equation": (
            "AI Services + AI Models + AI Agents + Enterprise Systems + Data "
            "Platforms + Security Platforms + Governance Platforms → API Gateway "
            "→ Service Mesh → Event Fabric → Policy Engine → Intelligent Routing "
            "→ Autonomous Integration"
        ),
        "pillars": (
            "intelligent_connectivity_required",
            "traditional_api_gateway_insufficient_alone",
            "dynamic_routing_for_ai_workloads",
            "secure_agent_communication",
            "policy_aware_integration",
            "event_driven_autonomous_systems",
        ),
        "strategic_role": {
            "intelligent_connectivity": (
                "AI ecosystems span models, agents, LLMs, apps, and enterprise "
                "systems — connectivity must be secure and context-aware."
            ),
            "traditional_gateway_insufficient": (
                "Static CRUD gateways lack model selection, cost-aware routing, "
                "and agent collaboration semantics."
            ),
            "dynamic_routing": (
                "AI workloads need performance, cost, and policy-aware routing "
                "tied to AIOps and model intelligence."
            ),
            "secure_agent_communication": (
                "Agents require identity, mTLS, and audited messaging — not ad-hoc RPC."
            ),
            "policy_aware_integration": (
                "Every AI hop evaluates authZ, RAI, and security policies."
            ),
            "event_driven": (
                "Autonomous systems communicate via Event Fabric with replay and governance."
            ),
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
        "contexts": [dict(c) for c in LOGICAL_BOUNDED_CONTEXTS],
        "context_count": len(LOGICAL_BOUNDED_CONTEXTS),
        "logical_partitions_same_sor": True,
    }


def gateway() -> dict[str, Any]:
    return dict(AI_API_GATEWAY)


def routing() -> dict[str, Any]:
    return dict(INTELLIGENT_ROUTING)


def mesh() -> dict[str, Any]:
    return dict(AI_SERVICE_MESH)


def serving() -> dict[str, Any]:
    return dict(MODEL_SERVING_GATEWAY)


def agents() -> dict[str, Any]:
    return dict(AGENT_COMMUNICATION)


def events_fabric() -> dict[str, Any]:
    return dict(EVENT_DRIVEN_INTEGRATION)


def workflows() -> dict[str, Any]:
    return dict(WORKFLOW_ORCHESTRATION)


def security() -> dict[str, Any]:
    return dict(SECURITY)


def knowledge_graph() -> dict[str, Any]:
    return dict(INTEGRATION_KNOWLEDGE_GRAPH)


def digital_twin() -> dict[str, Any]:
    return dict(INTEGRATION_DIGITAL_TWIN)


def observability() -> dict[str, Any]:
    return dict(OBSERVABILITY)


def cqrs() -> dict[str, Any]:
    return {
        "commands": list(COMMANDS),
        "command_count": len(COMMANDS),
        "queries": list(QUERIES),
        "query_count": len(QUERIES),
        "alignment_present_required": True,
    }


def events() -> dict[str, Any]:
    return {
        "core_events": [dict(e) for e in CORE_EVENTS],
        "core_event_count": len(CORE_EVENTS),
        "event_driven_required": True,
        "retention_policy": "tenant_scoped_immutable_append",
        "version_strategy": "event_version_field",
        "ownership": "ai",
    }


def microservices() -> dict[str, Any]:
    return {
        "services": [dict(s) for s in MICROSERVICES],
        "service_count": len(MICROSERVICES),
        "logical_decomposition": True,
    }


def api() -> dict[str, Any]:
    return {
        "surfaces": list(API_SURFACES),
        "styles": list(API_STYLES),
        "api_first_present_required": True,
    }


def integrations() -> dict[str, Any]:
    return {
        "peers": (
            "P207",
            "P208",
            "P209",
            "P210",
            "P211",
            "P213-O",
            "P214-D",
            "P214-E",
            "P214-F",
            "P214-G",
            "P214-H",
            "P214-I",
            "P214-J",
            "P214-K",
            "P214-L",
            "api_gateway",
            "event_fabric",
            "workflow",
            "observability",
        ),
        "via_events_and_acl": True,
    }


def deployment() -> dict[str, Any]:
    return dict(DEPLOYMENT)


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
            "enterprise_ai_api_gateway": True,
            "intelligent_service_mesh": True,
            "ai_communication_fabric": True,
            "model_serving_gateway": True,
            "agent_communication": True,
            "event_fabric": True,
            "workflow_platform": True,
            "integration_governance": True,
            "cqrs_architecture": True,
            "event_architecture": True,
            "microservice_architecture": True,
            "api_platform": True,
            "security_architecture": True,
            "digital_twin": True,
            "knowledge_graph": True,
            "deployment_architecture": True,
            "testing_architecture": True,
            "foundation_tests": True,
            "aiinteg_api_live": True,
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
            "P214-A",
            "P214-B",
            "P214-C",
            "P214-D",
            "P214-E",
            "P214-F",
            "P214-G",
            "P214-H",
            "P214-I",
            "P214-J",
            "P214-K",
            "P214-L",
            "ADR-421",
            "ADR-422",
            "ADR-423",
            "ADR-424",
            "ADR-425",
            "ADR-426",
            "ADR-427",
            "ADR-428",
            "ADR-429",
            "ADR-430",
            "ADR-431",
            "ADR-432",
            "API_GATEWAY_ARCHITECTURE",
            "ENTERPRISE_EVENT_BUS",
            "AI_PLATFORM_STANDARD",
        ],
        "vision": vision(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "gateway": gateway(),
        "routing": routing(),
        "mesh": mesh(),
        "serving": serving(),
        "agents": agents(),
        "events_fabric": events_fabric(),
        "workflows": workflows(),
        "security": security(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "observability": observability(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "api": api(),
        "integrations": integrations(),
        "deployment": deployment(),
        "testing": testing(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "enterprise_ai_api_gateway_present_required": True,
        "intelligent_service_mesh_present_required": True,
        "ai_communication_fabric_present_required": True,
        "model_serving_gateway_present_required": True,
        "agent_communication_platform_present_required": True,
        "event_integration_platform_present_required": True,
        "workflow_orchestration_present_required": True,
        "integration_governance_present_required": True,
        "security_architecture_present_required": True,
        "knowledge_graph_integration_present_required": True,
        "digital_twin_integration_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "zero_trust_security_present_required": True,
        "cloud_native_deployment_present_required": True,
        "sibling_ai_bc_forbidden": True,
        "module_local_ai_gateway_forbidden": True,
        "platform_api_gateway_owns_edge": True,
        "platform_event_fabric_owns_bus": True,
        "via_enterprise_ai": True,
        "via_api_gateway": True,
        "api_prefix": f"{API_PREFIX}/aiinteg",
        "forbidden_sibling_bc": [
            "ai_integration",
            "ai_api_gateway",
            "ai_service_mesh",
            "ai_communication",
            "ai_connectivity",
            "model_serving_gateway",
            "generative_ai",
            "llm_platform",
            "ai_core",
            "vector_intelligence",
            "ml_platform",
        ],
    }


def aiinteg_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /ai/aiinteg",
            "GET /ai/aiinteg/vision",
            "GET /ai/aiinteg/domain",
            "GET /ai/aiinteg/bounded-contexts",
            "GET /ai/aiinteg/gateway",
            "GET /ai/aiinteg/routing",
            "GET /ai/aiinteg/mesh",
            "GET /ai/aiinteg/serving",
            "GET /ai/aiinteg/agents",
            "GET /ai/aiinteg/events-fabric",
            "GET /ai/aiinteg/workflows",
            "GET /ai/aiinteg/security",
            "GET /ai/aiinteg/knowledge-graph",
            "GET /ai/aiinteg/digital-twin",
            "GET /ai/aiinteg/observability",
            "GET /ai/aiinteg/cqrs",
            "GET /ai/aiinteg/events",
            "GET /ai/aiinteg/microservices",
            "GET /ai/aiinteg/integrations",
            "GET /ai/aiinteg/api",
            "GET /ai/aiinteg/deployment",
            "GET /ai/aiinteg/testing",
            "GET /ai/aiinteg/outputs",
            "GET /ai/aiinteg/production-readiness",
            "GET /ai/aiinteg/readiness",
        ],
    }
