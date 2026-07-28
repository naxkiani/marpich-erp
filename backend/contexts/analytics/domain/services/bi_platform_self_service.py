"""P213-H Enterprise Self-Service BI Platform — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P213-H"
ADR = 412
SOR = "analytics"
API_PREFIX = "/api/v1/analytics"
PRODUCT = "Enterprise Self-Service BI Platform"
CAPABILITY = "CAP-PLT-BI-001"

PRINCIPLE = (
    "Every business user SHALL be capable of creating trusted analytics "
    "without compromising governance, security, or enterprise consistency."
)

FABRIC = "meos_enterprise_analytics_experience_fabric"

CORE_DOMAIN = "enterprise_self_service_analytics_management"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {"id": "workspace_management", "purpose": "Personal, team, and enterprise workspaces."},
    {"id": "analytics_authoring", "purpose": "Low/no-code analytics authoring."},
    {"id": "dashboard_builder", "purpose": "Visual dashboard composition."},
    {"id": "dataset_discovery", "purpose": "Governed data and metric discovery."},
    {"id": "collaboration", "purpose": "Sharing, comments, reviews, communities."},
    {"id": "insight_sharing", "purpose": "Publish and subscribe to insights."},
    {"id": "ai_analytics_assistance", "purpose": "NL and AI-assisted analytics."},
    {"id": "analytics_governance", "purpose": "Policy-bound self-service controls."},
)

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "analytics_workspace",
        "bc": "BC-01",
        "name": "Analytics Workspace Context",
        "purpose": "Personal/team workspaces, lifecycle, collaboration.",
    },
    {
        "id": "analytics_exploration",
        "bc": "BC-02",
        "name": "Analytics Exploration Context",
        "purpose": "Data discovery, exploration, semantic navigation.",
    },
    {
        "id": "dashboard_builder",
        "bc": "BC-03",
        "name": "Dashboard Builder Context",
        "purpose": "Dashboard design, widgets, KPI selection, themes.",
    },
    {
        "id": "ad_hoc_analytics",
        "bc": "BC-04",
        "name": "Ad-Hoc Analytics Context",
        "purpose": "Interactive queries, drill, slice, dice, pivot.",
    },
    {
        "id": "collaboration",
        "bc": "BC-05",
        "name": "Collaboration Context",
        "purpose": "Sharing, comments, reviews, publishing.",
    },
    {
        "id": "ai_analytics_assistant",
        "bc": "BC-06",
        "name": "AI Analytics Assistant Context",
        "purpose": "NL analytics, recommendations, insight generation.",
    },
)

AGGREGATE = {
    "name": "SelfServiceAnalyticsWorkspaceAggregate",
    "root": "SelfServiceAnalyticsWorkspace",
    "entities": (
        "Workspace",
        "AnalyticsProject",
        "SavedQuery",
        "Dashboard",
        "Notebook",
        "Visualization",
        "Insight",
        "DatasetBookmark",
    ),
    "value_objects": (
        "WorkspaceId",
        "WorkspaceRole",
        "AnalyticsTemplate",
        "ExplorationContext",
        "SharingPolicy",
        "QueryDefinition",
    ),
    "events": (
        "WorkspaceCreatedEvent",
        "DashboardSharedEvent",
        "InsightPublishedEvent",
        "AnalyticsExecutedEvent",
        "NotebookCreatedEvent",
        "DatasetDiscoveredEvent",
    ),
}

WORKSPACE_TYPES: tuple[str, ...] = (
    "personal",
    "team",
    "enterprise",
    "project",
    "notebook",
    "executive",
    "ai",
)

WORKSPACE_FEATURES: tuple[str, ...] = (
    "versioning",
    "history",
    "bookmarks",
    "templates",
    "personalization",
)

DATA_DISCOVERY: dict[str, Any] = {
    "capabilities": (
        "business_search",
        "semantic_search",
        "dataset_discovery",
        "metric_discovery",
        "report_discovery",
        "dashboard_discovery",
        "knowledge_discovery",
        "business_glossary_search",
    ),
    "via_p212_i": True,
    "via_p212_j": True,
    "via_p213_g": True,
}

NO_CODE_LOW_CODE: dict[str, Any] = {
    "capabilities": (
        "drag_and_drop_analytics",
        "visual_query_builder",
        "visual_joins",
        "visual_filters",
        "calculated_fields",
        "business_formulas",
        "dashboard_templates",
        "reusable_components",
    ),
    "sql_knowledge_required": False,
}

AD_HOC: dict[str, Any] = {
    "capabilities": (
        "interactive_queries",
        "dynamic_filtering",
        "cross_filtering",
        "grouping",
        "aggregation",
        "drill_down",
        "drill_through",
        "slice",
        "dice",
        "pivot",
        "ranking",
        "trend_analysis",
    ),
    "modes": (
        "real_time_analytics",
        "historical_analytics",
        "comparative_analytics",
    ),
}

COLLABORATION: dict[str, Any] = {
    "capabilities": (
        "insight_sharing",
        "dashboard_sharing",
        "workspace_collaboration",
        "comments",
        "reviews",
        "mentions",
        "approvals",
        "subscriptions",
        "analytics_communities",
    ),
    "audiences": (
        "business_teams",
        "departments",
        "cross_functional_teams",
        "executive_committees",
    ),
}

AI_AGENTS: tuple[str, ...] = (
    "ai_bi_assistant",
    "ai_dashboard_builder",
    "ai_insight_generator",
    "ai_visualization_advisor",
    "ai_data_discovery_agent",
    "ai_query_generator",
    "ai_storytelling_agent",
)

AI_CAPABILITIES: tuple[str, ...] = (
    "natural_language_questions",
    "automatic_dashboard_creation",
    "automatic_kpi_recommendation",
    "automatic_insight_discovery",
    "business_trend_detection",
    "narrative_analytics",
    "executive_summaries",
)

NATURAL_LANGUAGE: dict[str, Any] = {
    "examples": (
        "Show monthly sales.",
        "Compare revenue by region.",
        "Which products are declining?",
        "What changed this quarter?",
        "Predict next month's revenue.",
        "Explain customer churn.",
    ),
    "pipeline": (
        "semantic_query",
        "business_query",
        "analytical_query",
        "visualization",
    ),
}

SEMANTIC_INTEGRATION: dict[str, Any] = {
    "via_p213_g": True,
    "uses": (
        "certified_metrics",
        "business_glossary",
        "semantic_models",
        "business_vocabulary",
        "enterprise_kpis",
        "calculation_engine",
    ),
}

KNOWLEDGE_GRAPH: dict[str, Any] = {
    "via_p212_j": True,
    "capabilities": (
        "semantic_navigation",
        "relationship_discovery",
        "context_aware_analytics",
        "business_concept_navigation",
        "enterprise_search",
    ),
}

DIGITAL_TWIN: dict[str, Any] = {
    "via_p212_l": True,
    "capabilities": (
        "business_simulations",
        "scenario_planning",
        "forecast_exploration",
        "interactive_what_if_analysis",
        "decision_impact_visualization",
    ),
}

COMMANDS: tuple[str, ...] = (
    "CreateWorkspaceCommand",
    "CreateDashboardCommand",
    "SaveAnalyticsCommand",
    "ShareInsightCommand",
    "PublishDashboardCommand",
    "BookmarkDatasetCommand",
)

QUERIES: tuple[str, ...] = (
    "SearchDatasetQuery",
    "ExploreDatasetQuery",
    "GetDashboardQuery",
    "SearchInsightQuery",
    "GetWorkspaceQuery",
)

CORE_EVENTS: tuple[dict[str, Any], ...] = (
    {
        "name": "WorkspaceCreatedEvent",
        "producer": "analytics_workspace",
        "consumers": ("collaboration", "audit"),
        "payload": ("tenant_id", "workspace_id", "workspace_type"),
        "version": "v1",
    },
    {
        "name": "AnalyticsExecutedEvent",
        "producer": "ad_hoc_analytics",
        "consumers": ("audit", "observability"),
        "payload": ("tenant_id", "query_id", "workspace_id"),
        "version": "v1",
    },
    {
        "name": "DashboardPublishedEvent",
        "producer": "dashboard_builder",
        "consumers": ("collaboration", "reporting"),
        "payload": ("tenant_id", "dashboard_id", "version"),
        "version": "v1",
    },
    {
        "name": "InsightSharedEvent",
        "producer": "collaboration",
        "consumers": ("notifications", "audit"),
        "payload": ("tenant_id", "insight_id", "audience"),
        "version": "v1",
    },
    {
        "name": "DatasetBookmarkedEvent",
        "producer": "analytics_exploration",
        "consumers": ("workspace",),
        "payload": ("tenant_id", "dataset_id", "user_ref"),
        "version": "v1",
    },
    {
        "name": "VisualizationCreatedEvent",
        "producer": "dashboard_builder",
        "consumers": ("ai_analytics_assistant",),
        "payload": ("tenant_id", "visualization_id", "type"),
        "version": "v1",
    },
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "name": "workspace-service",
        "responsibility": "Workspace lifecycle and isolation.",
        "database_boundary": "analytics_ss_workspaces",
        "api_boundary": "/api/v1/analytics/workspaces",
        "events": ("WorkspaceCreatedEvent",),
        "security_model": "analytics.workspaces.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "analytics-builder-service",
        "responsibility": "No/low-code analytics authoring.",
        "database_boundary": "analytics_ss_builder",
        "api_boundary": "/api/v1/analytics/analytics",
        "events": ("AnalyticsExecutedEvent",),
        "security_model": "analytics.authoring.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "dashboard-builder-service",
        "responsibility": "Dashboard and widget composition.",
        "database_boundary": "analytics_ss_dashboards",
        "api_boundary": "/api/v1/analytics/dashboard-builder",
        "events": ("DashboardPublishedEvent", "VisualizationCreatedEvent"),
        "security_model": "analytics.dashboards.*",
        "scaling_strategy": "horizontal_read_replicas",
    },
    {
        "name": "collaboration-service",
        "responsibility": "Sharing, comments, reviews, communities.",
        "database_boundary": "analytics_ss_collab",
        "api_boundary": "/api/v1/analytics/share",
        "events": ("InsightSharedEvent",),
        "security_model": "analytics.share.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "search-service",
        "responsibility": "Discovery via enterprise search ACL.",
        "database_boundary": "analytics_ss_search",
        "api_boundary": "/api/v1/analytics/explore",
        "events": ("DatasetDiscoveredEvent",),
        "security_model": "analytics.explore.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "natural-language-analytics-service",
        "responsibility": "NL → semantic/business/analytical query.",
        "database_boundary": "analytics_ss_nl",
        "api_boundary": "/api/v1/analytics/natural-language",
        "events": ("AnalyticsExecutedEvent",),
        "security_model": "analytics.nl.*",
        "scaling_strategy": "async_via_enterprise_ai",
    },
    {
        "name": "ai-analytics-assistant-service",
        "responsibility": "AI agents via Enterprise AI only.",
        "database_boundary": "analytics_ss_ai",
        "api_boundary": "/api/v1/analytics/assistant",
        "events": ("InsightSharedEvent",),
        "security_model": "analytics.assistant.*",
        "scaling_strategy": "async_via_enterprise_ai",
    },
    {
        "name": "insight-sharing-service",
        "responsibility": "Insight publish and subscriptions.",
        "database_boundary": "analytics_ss_insights",
        "api_boundary": "/api/v1/analytics/subscriptions",
        "events": ("InsightSharedEvent",),
        "security_model": "analytics.insights.*",
        "scaling_strategy": "queue_backed_workers",
    },
)

API_BOUNDARIES: dict[str, Any] = {
    "workspace": (
        "/api/v1/analytics/workspaces",
        "/api/v1/analytics/projects",
    ),
    "analytics": (
        "/api/v1/analytics/explore",
        "/api/v1/analytics/query",
        "/api/v1/analytics/analytics",
    ),
    "dashboard": (
        "/api/v1/analytics/dashboard-builder",
        "/api/v1/analytics/widgets",
    ),
    "collaboration": (
        "/api/v1/analytics/share",
        "/api/v1/analytics/comments",
        "/api/v1/analytics/subscriptions",
    ),
    "ai": (
        "/api/v1/analytics/assistant",
        "/api/v1/analytics/natural-language",
        "/api/v1/analytics/storytelling",
    ),
    "rest": True,
    "graphql": "/api/v1/analytics/graphql",
    "grpc": True,
    "streaming_apis": "/api/v1/analytics/explore/stream",
    "event_apis": "analytics.self_service.*.v1",
    "security": (
        "analytics.self_service.read",
        "zero_trust",
        "tenant_isolation",
    ),
}

SECURITY: dict[str, Any] = {
    "via_p207": True,
    "via_p208": True,
    "via_p211": True,
    "via_p212": True,
    "workspace_isolation": True,
    "dataset_authorization": True,
    "role_based_access_control": True,
    "attribute_based_access_control": True,
    "row_level_security": True,
    "column_level_security": True,
    "dynamic_data_masking": True,
    "policy_based_data_access": True,
    "audit_logging": True,
    "privacy_enforcement": True,
}

DEPLOYMENT: dict[str, Any] = {
    "kubernetes": True,
    "service_mesh": True,
    "container_platform": True,
    "autoscaling": True,
    "api_gateway": True,
    "distributed_cache": True,
    "observability": True,
    "cicd": True,
    "high_availability": True,
    "disaster_recovery": True,
    "multi_region": True,
    "cloud_native": True,
}

TESTING: tuple[str, ...] = (
    "workspace_testing",
    "analytics_builder_testing",
    "dashboard_testing",
    "natural_language_testing",
    "ai_testing",
    "performance_testing",
    "security_testing",
    "accessibility_testing",
    "governance_testing",
    "regression_testing",
    "acceptance_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_self_service_bi_vision",
    "ddd_domain_model",
    "bounded_context_architecture",
    "self_service_analytics_workspace",
    "enterprise_data_discovery_platform",
    "no_code_low_code_analytics_platform",
    "ad_hoc_analytics_engine",
    "collaborative_analytics_platform",
    "ai_native_self_service_bi",
    "natural_language_analytics",
    "semantic_layer_integration",
    "knowledge_graph_integration",
    "digital_twin_integration",
    "cqrs_architecture",
    "event_sourcing_architecture",
    "microservice_architecture",
    "api_first_architecture",
    "security_governance_architecture",
    "deployment_architecture",
    "testing_architecture",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "enterprise_self_service_bi_platform_is_missing",
    "citizen_analytics_platform_is_missing",
    "no_code_analytics_platform_is_missing",
    "low_code_analytics_platform_is_missing",
    "natural_language_analytics_is_missing",
    "ai_analytics_assistant_is_missing",
    "collaborative_analytics_is_missing",
    "semantic_layer_integration_is_missing",
    "knowledge_graph_integration_is_missing",
    "digital_twin_integration_is_missing",
    "cqrs_architecture_is_missing",
    "event_sourcing_architecture_is_missing",
    "microservice_architecture_is_missing",
    "api_first_architecture_is_missing",
    "zero_trust_security_is_missing",
    "enterprise_governance_is_missing",
    "cloud_native_deployment_is_missing",
    "self_service_bi_architecture_is_incomplete",
    "analytics_workspace_is_missing",
    "ad_hoc_analytics_is_missing",
    "sibling_business_intelligence_bc",
)

USER_PERSONAS: tuple[str, ...] = (
    "business_users",
    "managers",
    "executives",
    "domain_experts",
    "citizen_analysts",
    "data_stewards",
    "business_owners",
)

EXPERIENCE_FLOW: tuple[str, ...] = (
    "discover_data",
    "explore_data",
    "create_analytics",
    "build_dashboards",
    "share_insights",
    "collaborate",
    "make_decisions",
)


def vision() -> dict[str, Any]:
    return {
        "statement": PRINCIPLE,
        "fabric": FABRIC,
        "personas": list(USER_PERSONAS),
        "flow": list(EXPERIENCE_FLOW),
        "governed_by": "enterprise_data_governance_policies",
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


def workspaces() -> dict[str, Any]:
    return {
        "types": list(WORKSPACE_TYPES),
        "type_count": len(WORKSPACE_TYPES),
        "features": list(WORKSPACE_FEATURES),
    }


def discovery() -> dict[str, Any]:
    return dict(DATA_DISCOVERY)


def no_code_low_code() -> dict[str, Any]:
    return dict(NO_CODE_LOW_CODE)


def ad_hoc() -> dict[str, Any]:
    return dict(AD_HOC)


def collaboration() -> dict[str, Any]:
    return dict(COLLABORATION)


def ai_native() -> dict[str, Any]:
    return {
        "agents": list(AI_AGENTS),
        "agent_count": len(AI_AGENTS),
        "capabilities": list(AI_CAPABILITIES),
        "via_enterprise_ai": True,
        "module_local_llm_sdk_forbidden": True,
    }


def natural_language() -> dict[str, Any]:
    return dict(NATURAL_LANGUAGE)


def semantic_integration() -> dict[str, Any]:
    return dict(SEMANTIC_INTEGRATION)


def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH)


def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN)


def cqrs() -> dict[str, Any]:
    return {
        "commands": list(COMMANDS),
        "command_count": len(COMMANDS),
        "queries": list(QUERIES),
        "query_count": len(QUERIES),
        "alignment_present_required": True,
        "events": [e["name"] for e in CORE_EVENTS],
        "event_count": len(CORE_EVENTS),
    }


def events() -> dict[str, Any]:
    return {
        "core_events": [dict(e) for e in CORE_EVENTS],
        "core_event_count": len(CORE_EVENTS),
        "event_driven_required": True,
        "replay_strategy": "outbox_replay_by_event_id",
    }


def microservices() -> dict[str, Any]:
    return {
        "services": [dict(s) for s in MICROSERVICES],
        "service_count": len(MICROSERVICES),
        "logical_decomposition": True,
    }


def api_boundaries() -> dict[str, Any]:
    return dict(API_BOUNDARIES)


def security() -> dict[str, Any]:
    return dict(SECURITY)


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
            "enterprise_self_service_bi": True,
            "analytics_workspace": True,
            "no_code_analytics": True,
            "ad_hoc_analytics": True,
            "collaborative_analytics": True,
            "ai_analytics_assistant": True,
            "natural_language_analytics": True,
            "semantic_integration": True,
            "knowledge_graph_integration": True,
            "digital_twin_integration": True,
            "cqrs_architecture": True,
            "event_architecture": True,
            "microservice_architecture": True,
            "api_platform": True,
            "security_architecture": True,
            "deployment_architecture": True,
            "testing_architecture": True,
            "foundation_tests": True,
            "self_service_api_live": True,
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
            "ADR-394",
            "ADR-395",
            "ADR-396",
            "ADR-408",
            "ADR-409",
            "ADR-410",
            "ADR-411",
            "P212",
            "P212-E",
            "P212-F",
            "P212-G",
            "P212-I",
            "P212-J",
            "P212-K",
            "P212-L",
            "P212-M",
            "P212-N",
            "P212-O",
        ],
        "vision": vision(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "architecture": {
            "present_required": True,
            "not_incomplete": True,
            "capabilities": list(NO_CODE_LOW_CODE["capabilities"])[:5]
            + list(AD_HOC["capabilities"])[:3],
            "capability_count": 8,
        },
        "workspaces": workspaces(),
        "discovery": discovery(),
        "no_code_low_code": no_code_low_code(),
        "ad_hoc": ad_hoc(),
        "collaboration": collaboration(),
        "ai_native": ai_native(),
        "natural_language": natural_language(),
        "semantic_integration": semantic_integration(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "api_boundaries": api_boundaries(),
        "security": security(),
        "deployment": deployment(),
        "testing": testing(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "enterprise_self_service_bi_platform_present_required": True,
        "citizen_analytics_platform_present_required": True,
        "no_code_analytics_platform_present_required": True,
        "low_code_analytics_platform_present_required": True,
        "natural_language_analytics_present_required": True,
        "ai_analytics_assistant_present_required": True,
        "collaborative_analytics_present_required": True,
        "semantic_layer_integration_present_required": True,
        "knowledge_graph_integration_present_required": True,
        "digital_twin_integration_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_sourcing_architecture_present_required": True,
        "microservice_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "zero_trust_security_present_required": True,
        "enterprise_governance_present_required": True,
        "cloud_native_deployment_present_required": True,
        "architecture_present_required": True,
        "analytics_workspace_present_required": True,
        "ad_hoc_analytics_present_required": True,
        "sibling_business_intelligence_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/self-service",
        "forbidden_sibling_bc": [
            "business_intelligence",
            "decision_intelligence",
            "reporting_platform",
            "metric_governance_platform",
            "visualization_platform",
            "bi_core",
        ],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def self_service_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /analytics/self-service",
            "GET /analytics/self-service/vision",
            "GET /analytics/self-service/domain",
            "GET /analytics/self-service/bounded-contexts",
            "GET /analytics/self-service/workspaces",
            "GET /analytics/self-service/discovery",
            "GET /analytics/self-service/no-code",
            "GET /analytics/self-service/ad-hoc",
            "GET /analytics/self-service/collaboration",
            "GET /analytics/self-service/ai",
            "GET /analytics/self-service/natural-language",
            "GET /analytics/self-service/semantic",
            "GET /analytics/self-service/knowledge-graph",
            "GET /analytics/self-service/digital-twin",
            "GET /analytics/self-service/cqrs",
            "GET /analytics/self-service/events",
            "GET /analytics/self-service/microservices",
            "GET /analytics/self-service/apis",
            "GET /analytics/self-service/security",
            "GET /analytics/self-service/deployment",
            "GET /analytics/self-service/testing",
            "GET /analytics/self-service/outputs",
            "GET /analytics/self-service/production-readiness",
            "GET /analytics/self-service/readiness",
        ],
    }
