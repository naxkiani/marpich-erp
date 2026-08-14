"""P213-A Enterprise BI strategy — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P213-A"
ADR = 394
SOR = "analytics"
API_PREFIX = "/api/v1/analytics"
PRODUCT = (
    "Enterprise Business Intelligence, Analytics & "
    "Decision Intelligence Platform"
)
CAPABILITY = "CAP-PLT-BI-001"

PRINCIPLE = (
    "Enterprise intelligence transforms trusted data "
    "into strategic organizational decisions."
)

CORE_DOMAIN = "enterprise_decision_intelligence_management"

SUPPORTING_DOMAINS: tuple[str, ...] = (
    "business_intelligence",
    "analytics_management",
    "metrics_management",
    "insight_generation",
    "decision_automation",
    "intelligence_governance",
    "bi_asset_lifecycle",
    "kpi_semantic_layer",
)

BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "BC-01",
        "name": "business_intelligence_core_context",
        "responsibilities": (
            "reporting",
            "dashboards",
            "kpis",
            "business_metrics",
        ),
    },
    {
        "id": "BC-02",
        "name": "analytics_intelligence_context",
        "responsibilities": (
            "analytics_models",
            "data_analysis",
            "pattern_discovery",
        ),
    },
    {
        "id": "BC-03",
        "name": "decision_intelligence_context",
        "responsibilities": (
            "decision_support",
            "recommendations",
            "optimization",
        ),
    },
    {
        "id": "BC-04",
        "name": "business_metrics_context",
        "responsibilities": (
            "metric_governance",
            "semantic_definitions",
            "kpi_management",
        ),
    },
    {
        "id": "BC-05",
        "name": "intelligence_governance_context",
        "responsibilities": (
            "analytics_governance",
            "model_governance",
            "insight_validation",
        ),
    },
)

# Section 4 — MEOS Intelligence Architecture Layers
ARCHITECTURE_LAYERS: tuple[str, ...] = (
    "data_foundation_layer",
    "analytical_processing_layer",
    "semantic_intelligence_layer",
    "analytics_layer",
    "decision_intelligence_layer",
    "ai_automation_layer",
)

BI_ASSET_LIFECYCLE: tuple[str, ...] = (
    "create",
    "validate",
    "publish",
    "consume",
    "optimize",
)

DECISION_MODEL: tuple[str, ...] = (
    "business_context",
    "data_evidence",
    "analytics_result",
    "ai_recommendation",
    "intelligent_decision",
)

FABRIC_FLOW: tuple[str, ...] = (
    "insight",
    "recommendation",
    "decision",
    "business_action",
)

GRAPH_NODES: tuple[str, ...] = (
    "BusinessMetric",
    "Insight",
    "Decision",
    "DataAsset",
    "Process",
    "Organization",
    "Customer",
    "Risk",
)

GRAPH_RELATIONSHIPS: tuple[str, ...] = (
    "Metric_DEPENDS_ON_Data",
    "Insight_GENERATED_FROM_Analytics",
    "Decision_IMPACTS_BusinessProcess",
)

AI_AGENTS: tuple[str, ...] = (
    "ai_business_analyst",
    "ai_insight_generator",
    "ai_decision_advisor",
    "ai_trend_analyst",
    "ai_strategy_assistant",
)

COMMANDS: tuple[str, ...] = (
    "CreateInsightCommand",
    "PublishReportCommand",
    "UpdateMetricCommand",
    "GenerateRecommendationCommand",
    "PublishBiStrategy",
    "RegisterBiCapability",
    "AlignDataMesh",
)

QUERIES: tuple[str, ...] = (
    "GetDashboardQuery",
    "GetInsightQuery",
    "GetMetricQuery",
    "GetDecisionQuery",
    "GetBiStrategy",
    "GetBiArchitecture",
    "GetBiReadiness",
)

DOMAIN_EVENTS: tuple[str, ...] = (
    "InsightGeneratedEvent",
    "MetricUpdatedEvent",
    "DecisionCreatedEvent",
    "AnalyticsExecutedEvent",
    "BiStrategyPublished",
    "BiCapabilityRegistered",
    "DataMeshAligned",
    "AiNativeBiConfirmed",
    "ZeroTrustAligned",
    "PrivacyByDesignConfirmed",
    "CloudNativeConfirmed",
    "ScalabilityConfirmed",
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "name": "bi-core-service",
        "responsibility": "BI fabric orchestration and asset lifecycle",
        "database_boundary": "analytics_bi_core",
        "api_boundary": "/api/v1/analytics/strategy",
        "events": "analytics.bi.*",
        "security_model": "zero_trust_via_p207_p208",
    },
    {
        "name": "analytics-service",
        "responsibility": "Analytics models and pattern discovery",
        "database_boundary": "analytics_processing",
        "api_boundary": "/api/v1/analytics/advanced",
        "events": "analytics.model.*",
        "security_model": "zero_trust_via_p208",
    },
    {
        "name": "metrics-service",
        "responsibility": "Metric governance and semantic KPIs",
        "database_boundary": "analytics_metrics",
        "api_boundary": "/api/v1/analytics/olap",
        "events": "analytics.metric.*",
        "security_model": "via_p212_semantic_alignment",
    },
    {
        "name": "insight-service",
        "responsibility": "Insight generation and validation",
        "database_boundary": "analytics_insights",
        "api_boundary": "/api/v1/analytics/strategy/insights",
        "events": "analytics.insight.*",
        "security_model": "via_enterprise_ai",
    },
    {
        "name": "decision-intelligence-service",
        "responsibility": "Recommendations and decision tracking",
        "database_boundary": "analytics_decisions",
        "api_boundary": "/api/v1/analytics/prescriptive",
        "events": "analytics.decision.*",
        "security_model": "via_policy_engine",
    },
    {
        "name": "visualization-service",
        "responsibility": "Dashboards, reports, visualization workspace",
        "database_boundary": "analytics_visualization",
        "api_boundary": "/api/v1/analytics/reporting",
        "events": "analytics.visualization.*",
        "security_model": "zero_trust_via_p208",
    },
)

API_SURFACES: tuple[str, ...] = (
    "/api/v1/analytics",
    "/api/v1/analytics/strategy",
    "/api/v1/analytics/reporting",
    "/api/v1/analytics/olap",
    "/api/v1/analytics/advanced",
    "/api/v1/analytics/prescriptive",
)

CLOUD_NATIVE: tuple[str, ...] = (
    "kubernetes_deployment",
    "microservice_runtime",
    "data_processing_infrastructure",
    "analytics_compute_layer",
    "observability_foundation",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_bi_strategy",
    "enterprise_intelligence_domain_model_ddd",
    "bounded_context_architecture",
    "meos_intelligence_architecture_layers",
    "enterprise_bi_platform_foundation",
    "decision_intelligence_foundation",
    "knowledge_graph_integration",
    "digital_twin_integration",
    "ai_native_intelligence_foundation",
    "security_governance_foundation",
    "cqrs_foundation",
    "microservice_foundation",
    "api_first_foundation",
    "cloud_native_foundation",
    "operating_model",
    "production_readiness_checklist",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "enterprise_bi_architecture_is_incomplete",
    "analytics_architecture_is_missing",
    "decision_intelligence_foundation_is_missing",
    "ddd_domain_model_is_missing",
    "cqrs_architecture_is_missing",
    "microservices_architecture_is_missing",
    "api_first_design_is_missing",
    "ai_native_bi_is_missing",
    "knowledge_graph_integration_is_missing",
    "digital_twin_integration_is_missing",
    "governance_alignment_is_missing",
    "data_mesh_alignment_is_missing",
    "event_driven_architecture_is_missing",
    "sibling_business_intelligence_bc",
)


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "adr": ADR,
        "sor": SOR,
        "product": PRODUCT,
        "capability": CAPABILITY,
        "principle": PRINCIPLE,
        "core_domain": CORE_DOMAIN,
        "aggregate": "EnterpriseInsightAggregate",
        "fabric": "meos_enterprise_intelligence_fabric",
        "transforms": "governed_data_assets_to_actionable_bi_predictive_insights_decisions",
        "builds_on": [
            "P212",
            "P212-A",
            "P212-E",
            "P212-F",
            "P212-G",
            "P212-J",
            "P212-K",
            "P212-L",
            "P212-M",
            "P212-N",
            "P212-O",
            "ADR-392",
            "ADR-393",
            "ADR-376",
            "ADR-402",
            "ADR-404",
        ],
        "follow_up_modules": ["P213-B", "P213-C", "P213-D"],
        "architecture": {
            "layers": list(ARCHITECTURE_LAYERS),
            "layer_count": len(ARCHITECTURE_LAYERS),
            "flow": list(FABRIC_FLOW),
        },
        "domains": {
            "supporting": list(SUPPORTING_DOMAINS),
            "supporting_count": len(SUPPORTING_DOMAINS),
            "core": CORE_DOMAIN,
        },
        "bounded_contexts": {
            "contexts": [dict(bc) for bc in BOUNDED_CONTEXTS],
            "context_count": len(BOUNDED_CONTEXTS),
        },
        "bi_foundation": {
            "includes": (
                "reporting_engine",
                "dashboard_engine",
                "kpi_management",
                "visualization_platform",
                "business_analytics_workspace",
            ),
            "asset_lifecycle": list(BI_ASSET_LIFECYCLE),
        },
        "decision_intelligence": {
            "present_required": True,
            "capabilities": (
                "decision_modelling",
                "context_analysis",
                "recommendation_generation",
                "impact_analysis",
                "decision_tracking",
            ),
            "model": list(DECISION_MODEL),
        },
        "knowledge_graph_integration": {
            "present_required": True,
            "via_p212_j": True,
            "nodes": list(GRAPH_NODES),
            "relationships": list(GRAPH_RELATIONSHIPS),
        },
        "digital_twin_integration": {
            "present_required": True,
            "via_p212_l": True,
            "capabilities": (
                "business_scenario_simulation",
                "decision_impact_prediction",
                "future_state_analysis",
                "enterprise_optimization",
            ),
        },
        "ai_native": {
            "present_required": True,
            "via_enterprise_ai": True,
            "agents": list(AI_AGENTS),
            "agent_count": len(AI_AGENTS),
            "capabilities": (
                "generate_insights",
                "explain_analytics",
                "recommend_actions",
                "predict_outcomes",
            ),
        },
        "security_governance": {
            "via_p207": True,
            "via_p208": True,
            "via_p211": True,
            "via_p212": True,
            "controls": (
                "analytics_access_control",
                "data_usage_policies",
                "auditability",
                "privacy_protection",
            ),
        },
        "microservices": {
            "services": [dict(s) for s in MICROSERVICES],
            "service_count": len(MICROSERVICES),
        },
        "cqrs": {
            "commands": list(COMMANDS),
            "queries": list(QUERIES),
            "events": list(DOMAIN_EVENTS),
            "event_count": len(DOMAIN_EVENTS),
            "command_count": len(COMMANDS),
            "query_count": len(QUERIES),
        },
        "api_first": {
            "present_required": True,
            "surfaces": list(API_SURFACES),
            "rest": True,
            "graphql": True,
            "event_apis": True,
            "via_api_gateway": True,
            "security_controls": (
                "analytics.dashboards.read",
                "zero_trust",
                "tenant_isolation",
                "audit_logging",
            ),
        },
        "cloud_native": {
            "capabilities": list(CLOUD_NATIVE),
            "capability_count": len(CLOUD_NATIVE),
        },
        "cursor_outputs": {
            "outputs": list(CURSOR_OUTPUTS),
            "count": len(CURSOR_OUTPUTS),
        },
        "quality_gates": {"reject_if": list(QUALITY_GATES_REJECT_IF)},
        "production_readiness": {
            "verdict": "ENTERPRISE_GRADE",
            "checklist": {
                "enterprise_intelligence_foundation": True,
                "bi_architecture": True,
                "analytics_architecture": True,
                "decision_intelligence_model": True,
                "ddd_model": True,
                "cqrs_model": True,
                "api_foundation": True,
                "microservice_foundation": True,
                "ai_intelligence_foundation": True,
                "knowledge_graph_integration": True,
                "digital_twin_integration": True,
                "foundation_tests": True,
                "strategy_api_live": True,
            },
        },
        "bi_architecture_complete_required": True,
        "analytics_architecture_present_required": True,
        "decision_intelligence_foundation_present_required": True,
        "ddd_domain_model_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_driven_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_design_present_required": True,
        "data_mesh_alignment_present_required": True,
        "ai_native_bi_present_required": True,
        "knowledge_graph_integration_present_required": True,
        "digital_twin_integration_present_required": True,
        "governance_alignment_present_required": True,
        "sibling_business_intelligence_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/strategy",
        "forbidden_sibling_bc": [
            "business_intelligence",
            "decision_intelligence",
            "reporting_platform",
            "metric_governance_platform",
            "visualization_platform",
            "bi_core",
        ],
    }


def strategy_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /analytics/strategy",
            "GET /analytics/strategy/readiness",
        ],
    }


def production_readiness() -> dict[str, Any]:
    return catalog()["production_readiness"] | {"prompt_id": PROMPT_ID}
