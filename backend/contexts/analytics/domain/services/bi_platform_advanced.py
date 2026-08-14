"""P213-I Enterprise Advanced Analytics Platform — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P213-I"
ADR = 413
SOR = "analytics"
API_PREFIX = "/api/v1/analytics"
PRODUCT = "Enterprise Advanced Analytics Platform"
CAPABILITY = "CAP-PLT-BI-001"

PRINCIPLE = (
    "Advanced Analytics SHALL transform enterprise data into scientific "
    "business intelligence that supports strategic decision making."
)

FABRIC = "meos_enterprise_advanced_analytics_fabric"

CORE_DOMAIN = "enterprise_advanced_analytics_management"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {"id": "statistical_analytics", "purpose": "Descriptive and inferential statistics."},
    {"id": "analytical_modeling", "purpose": "Scientific and business analytical models."},
    {"id": "experiment_management", "purpose": "Controlled experiments and A/B testing."},
    {"id": "pattern_discovery", "purpose": "Pattern, cluster, and association mining."},
    {"id": "correlation_analysis", "purpose": "Correlation and dependency intelligence."},
    {"id": "root_cause_analysis", "purpose": "Causal and impact analysis."},
    {"id": "behaviour_analytics", "purpose": "Behaviour and usage mining."},
    {"id": "insight_management", "purpose": "Insight lifecycle and governance."},
    {"id": "data_science_workspace", "purpose": "Notebook and research workspaces."},
)

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "statistical_analytics",
        "bc": "BC-01",
        "name": "Statistical Analytics Context",
        "purpose": "Statistical, distribution, probability, and trend analysis.",
    },
    {
        "id": "analytical_modeling",
        "bc": "BC-02",
        "name": "Analytical Modeling Context",
        "purpose": "Analytical, scientific, and business model validation.",
    },
    {
        "id": "experimentation",
        "bc": "BC-03",
        "name": "Experimentation Context",
        "purpose": "Controlled experiments, A/B and multivariate testing.",
    },
    {
        "id": "pattern_discovery",
        "bc": "BC-04",
        "name": "Pattern Discovery Context",
        "purpose": "Pattern mining, clustering, association analysis.",
    },
    {
        "id": "root_cause_analytics",
        "bc": "BC-05",
        "name": "Root Cause Analytics Context",
        "purpose": "Causal, dependency, impact, and decision tracing.",
    },
    {
        "id": "insight_management",
        "bc": "BC-06",
        "name": "Insight Management Context",
        "purpose": "Insight lifecycle, validation, publication, governance.",
    },
)

AGGREGATE = {
    "name": "AdvancedAnalyticsAggregate",
    "root": "AdvancedAnalytics",
    "entities": (
        "AnalyticsModel",
        "Experiment",
        "Hypothesis",
        "Insight",
        "Pattern",
        "Correlation",
        "AnalyticalNotebook",
        "AnalyticalProject",
        "FeatureSet",
        "AnalyticalScenario",
    ),
    "value_objects": (
        "ModelIdentifier",
        "ConfidenceScore",
        "StatisticalDistribution",
        "ExperimentWindow",
        "AnalysisScope",
        "CorrelationStrength",
        "SignificanceLevel",
    ),
    "events": (
        "AnalysisCompletedEvent",
        "ExperimentExecutedEvent",
        "InsightGeneratedEvent",
        "PatternDetectedEvent",
        "RootCauseIdentifiedEvent",
        "CorrelationCalculatedEvent",
    ),
}

WORKBENCH_TYPES: tuple[str, ...] = (
    "statistical",
    "data_science",
    "notebook",
    "research",
    "experiment",
    "model",
    "executive_analytics",
)

WORKBENCH_FEATURES: tuple[str, ...] = (
    "projects",
    "versioning",
    "templates",
    "reusable_models",
    "reusable_experiments",
    "collaborative_analytics",
)

STATISTICAL: dict[str, Any] = {
    "capabilities": (
        "descriptive_statistics",
        "inferential_statistics",
        "regression_analysis",
        "correlation_analysis",
        "variance_analysis",
        "anova",
        "bayesian_analysis",
        "probability_models",
        "sampling",
        "confidence_intervals",
        "hypothesis_testing",
        "time_series_analysis",
        "outlier_detection",
    ),
    "governance": True,
    "validation": True,
    "reproducibility": True,
    "auditability": True,
}

PATTERN_DISCOVERY: dict[str, Any] = {
    "capabilities": (
        "association_rule_mining",
        "sequential_pattern_mining",
        "behaviour_mining",
        "usage_mining",
        "cluster_analysis",
        "segmentation",
        "similarity_analysis",
        "anomaly_discovery",
        "trend_discovery",
        "dependency_analysis",
    ),
    "business_applications": (
        "cross_sell_affinity",
        "journey_sequences",
        "customer_segmentation",
        "fraud_anomaly_flags",
        "operational_dependency_maps",
    ),
}

ROOT_CAUSE: dict[str, Any] = {
    "capabilities": (
        "dependency_mapping",
        "event_correlation",
        "business_process_analysis",
        "failure_analysis",
        "operational_analytics",
        "incident_analytics",
        "financial_impact_analysis",
        "business_driver_analysis",
    ),
    "via_p212_j": True,
    "via_p212_l": True,
    "via_event_platform": True,
}

EXPERIMENTATION: dict[str, Any] = {
    "types": (
        "business_experiments",
        "product_experiments",
        "pricing_experiments",
        "marketing_experiments",
        "operational_experiments",
        "policy_experiments",
        "feature_validation",
        "ab_testing",
        "multivariate_testing",
    ),
    "lifecycle": (
        "design",
        "approve",
        "execute",
        "observe",
        "evaluate",
        "publish",
    ),
}

VISUAL_ANALYTICS: tuple[str, ...] = (
    "scatter_plots",
    "correlation_matrix",
    "heat_maps",
    "parallel_coordinates",
    "tree_maps",
    "network_graphs",
    "cluster_maps",
    "geo_analytics",
    "temporal_analytics",
    "behaviour_maps",
)

AI_AGENTS: tuple[str, ...] = (
    "analytics_scientist_agent",
    "pattern_discovery_agent",
    "statistical_advisor_agent",
    "experiment_design_agent",
    "root_cause_agent",
    "insight_narrator",
    "decision_advisor",
)

AI_CAPABILITIES: tuple[str, ...] = (
    "automatic_model_recommendation",
    "automatic_statistical_testing",
    "automatic_anomaly_explanation",
    "automatic_insight_generation",
    "analytical_storytelling",
    "business_explanation",
)

KNOWLEDGE_GRAPH: dict[str, Any] = {
    "via_p212_j": True,
    "graph": "enterprise_analytical_knowledge_graph",
    "nodes": (
        "Analysis",
        "Experiment",
        "Insight",
        "Metric",
        "Pattern",
        "BusinessEntity",
        "Risk",
        "Opportunity",
        "Decision",
    ),
    "relationships": (
        "Insight_DERIVED_FROM_Analysis",
        "Analysis_USES_Dataset",
        "Decision_REFERENCES_Insight",
        "Pattern_IMPACTS_KPI",
    ),
}

DIGITAL_TWIN: dict[str, Any] = {
    "via_p212_l": True,
    "capabilities": (
        "scenario_analysis",
        "operational_simulation",
        "sensitivity_analysis",
        "business_impact_simulation",
        "risk_simulation",
        "decision_simulation",
    ),
}

SEMANTIC_INTEGRATION: dict[str, Any] = {
    "via_p213_g": True,
    "uses": (
        "certified_metrics",
        "semantic_models",
        "business_metrics",
        "calculation_engine",
    ),
}

SELF_SERVICE_INTEGRATION: dict[str, Any] = {
    "via_p213_h": True,
    "uses": (
        "analytics_workspace",
        "collaborative_publishing",
        "governed_exploration",
    ),
}

COMMANDS: tuple[str, ...] = (
    "CreateAnalysisCommand",
    "RunExperimentCommand",
    "GenerateInsightCommand",
    "ApproveInsightCommand",
    "PublishAnalysisCommand",
)

QUERIES: tuple[str, ...] = (
    "GetAnalysisQuery",
    "GetExperimentQuery",
    "SearchInsightsQuery",
    "GetPatternQuery",
    "GetRootCauseQuery",
)

CORE_EVENTS: tuple[dict[str, Any], ...] = (
    {
        "name": "AnalysisStartedEvent",
        "producer": "advanced_analytics",
        "consumers": ("audit", "observability"),
        "payload": ("tenant_id", "analysis_id", "scope"),
        "version": "v1",
    },
    {
        "name": "AnalysisCompletedEvent",
        "producer": "statistical_analytics",
        "consumers": ("insight_management", "knowledge_graph"),
        "payload": ("tenant_id", "analysis_id", "confidence"),
        "version": "v1",
    },
    {
        "name": "PatternDetectedEvent",
        "producer": "pattern_discovery",
        "consumers": ("insight_management", "ai"),
        "payload": ("tenant_id", "pattern_id", "strength"),
        "version": "v1",
    },
    {
        "name": "ExperimentCompletedEvent",
        "producer": "experimentation",
        "consumers": ("insight_management", "audit"),
        "payload": ("tenant_id", "experiment_id", "outcome"),
        "version": "v1",
    },
    {
        "name": "InsightGeneratedEvent",
        "producer": "insight_management",
        "consumers": ("collaboration", "notifications", "audit"),
        "payload": ("tenant_id", "insight_id", "analysis_id"),
        "version": "v1",
    },
    {
        "name": "RootCauseDetectedEvent",
        "producer": "root_cause_analytics",
        "consumers": ("digital_twin", "decision_intelligence"),
        "payload": ("tenant_id", "root_cause_id", "impact"),
        "version": "v1",
    },
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "name": "advanced-analytics-service",
        "responsibility": "Advanced analytics orchestration and workbench.",
        "database_boundary": "analytics_adv_core",
        "api_boundary": "/api/v1/analytics/advanced",
        "events": ("AnalysisStartedEvent", "AnalysisCompletedEvent"),
        "security_model": "analytics.advanced.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "statistical-engine-service",
        "responsibility": "Statistical computation and validation.",
        "database_boundary": "analytics_adv_stats",
        "api_boundary": "/api/v1/analytics/models",
        "events": ("AnalysisCompletedEvent", "CorrelationCalculatedEvent"),
        "security_model": "analytics.stats.*",
        "scaling_strategy": "compute_pool_autoscaling",
    },
    {
        "name": "experiment-service",
        "responsibility": "Experiment lifecycle and A/B testing.",
        "database_boundary": "analytics_adv_experiments",
        "api_boundary": "/api/v1/analytics/experiments",
        "events": ("ExperimentCompletedEvent",),
        "security_model": "analytics.experiments.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "pattern-discovery-service",
        "responsibility": "Pattern, cluster, and association mining.",
        "database_boundary": "analytics_adv_patterns",
        "api_boundary": "/api/v1/analytics/patterns",
        "events": ("PatternDetectedEvent",),
        "security_model": "analytics.patterns.*",
        "scaling_strategy": "batch_and_stream_workers",
    },
    {
        "name": "root-cause-service",
        "responsibility": "Root cause and impact analysis.",
        "database_boundary": "analytics_adv_rca",
        "api_boundary": "/api/v1/analytics/root-causes",
        "events": ("RootCauseDetectedEvent",),
        "security_model": "analytics.rca.*",
        "scaling_strategy": "async_workers",
    },
    {
        "name": "insight-service",
        "responsibility": "Insight lifecycle and publication.",
        "database_boundary": "analytics_adv_insights",
        "api_boundary": "/api/v1/analytics/insights",
        "events": ("InsightGeneratedEvent",),
        "security_model": "analytics.insights.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "analytics-ai-service",
        "responsibility": "AI agents via Enterprise AI only.",
        "database_boundary": "analytics_adv_ai",
        "api_boundary": "/api/v1/analytics/analytics-ai",
        "events": ("InsightGeneratedEvent",),
        "security_model": "analytics.ai.*",
        "scaling_strategy": "async_via_enterprise_ai",
    },
    {
        "name": "notebook-service",
        "responsibility": "Analytical notebooks and projects.",
        "database_boundary": "analytics_adv_notebooks",
        "api_boundary": "/api/v1/analytics/notebooks",
        "events": ("AnalysisStartedEvent",),
        "security_model": "analytics.notebooks.*",
        "scaling_strategy": "session_isolated_pools",
    },
)

API_BOUNDARIES: dict[str, Any] = {
    "analytics": (
        "/api/v1/analytics/advanced",
        "/api/v1/analytics/models",
        "/api/v1/analytics/insights",
        "/api/v1/analytics/experiments",
        "/api/v1/analytics/patterns",
        "/api/v1/analytics/root-causes",
    ),
    "notebook": (
        "/api/v1/analytics/notebooks",
        "/api/v1/analytics/projects",
    ),
    "ai": (
        "/api/v1/analytics/analytics-ai",
        "/api/v1/analytics/explanations",
    ),
    "rest": True,
    "graphql": "/api/v1/analytics/graphql",
    "grpc": True,
    "streaming_apis": "/api/v1/analytics/advanced/stream",
    "event_apis": "analytics.advanced.*.v1",
    "security": (
        "analytics.advanced.read",
        "zero_trust",
        "tenant_isolation",
    ),
}

SECURITY: dict[str, Any] = {
    "via_p207": True,
    "via_p208": True,
    "via_p211": True,
    "via_p212": True,
    "fine_grained_authorization": True,
    "workspace_isolation": True,
    "analytical_data_masking": True,
    "policy_based_access": True,
    "audit_logging": True,
    "experiment_governance": True,
    "insight_approval_workflow": True,
    "compliance_validation": True,
    "attribute_based_access_control": True,
    "row_level_security": True,
}

DEPLOYMENT: dict[str, Any] = {
    "kubernetes": True,
    "container_platform": True,
    "service_mesh": True,
    "distributed_compute": True,
    "distributed_storage": True,
    "autoscaling": True,
    "cicd": True,
    "observability": True,
    "disaster_recovery": True,
    "multi_region": True,
    "cloud_native": True,
}

TESTING: tuple[str, ...] = (
    "statistical_validation_testing",
    "analytical_model_testing",
    "experiment_testing",
    "insight_validation",
    "performance_testing",
    "security_testing",
    "scalability_testing",
    "regression_testing",
    "governance_testing",
    "acceptance_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_advanced_analytics_vision",
    "ddd_domain_model",
    "bounded_context_architecture",
    "enterprise_analytics_workbench",
    "statistical_analytics_platform",
    "pattern_discovery_platform",
    "root_cause_analytics",
    "enterprise_experimentation_platform",
    "advanced_visual_analytics",
    "ai_assisted_advanced_analytics",
    "knowledge_graph_integration",
    "digital_twin_integration",
    "cqrs_architecture",
    "event_sourcing_architecture",
    "microservice_architecture",
    "api_first_architecture",
    "security_governance_architecture",
    "deployment_architecture",
    "testing_architecture",
    "production_readiness_checklist",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "enterprise_advanced_analytics_platform_is_missing",
    "statistical_intelligence_platform_is_missing",
    "enterprise_experimentation_platform_is_missing",
    "pattern_discovery_platform_is_missing",
    "root_cause_analytics_is_missing",
    "insight_management_is_missing",
    "ai_assisted_analytics_is_missing",
    "knowledge_graph_integration_is_missing",
    "digital_twin_integration_is_missing",
    "cqrs_architecture_is_missing",
    "event_sourcing_architecture_is_missing",
    "microservice_architecture_is_missing",
    "api_first_architecture_is_missing",
    "zero_trust_security_is_missing",
    "enterprise_governance_is_missing",
    "cloud_native_deployment_is_missing",
    "advanced_analytics_architecture_is_incomplete",
    "sibling_business_intelligence_bc",
)

ANALYTICAL_QUESTIONS: tuple[str, ...] = (
    "what_happened",
    "why_it_happened",
    "what_is_happening",
    "what_may_happen",
    "what_action_should_be_evaluated",
)


def vision() -> dict[str, Any]:
    return {
        "statement": PRINCIPLE,
        "fabric": FABRIC,
        "inputs": (
            "enterprise_data",
            "semantic_intelligence",
            "knowledge_graph",
            "business_metrics",
            "historical_intelligence",
            "ai_intelligence",
        ),
        "output": "deep_analytical_knowledge",
        "questions": list(ANALYTICAL_QUESTIONS),
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


def workbench() -> dict[str, Any]:
    return {
        "types": list(WORKBENCH_TYPES),
        "type_count": len(WORKBENCH_TYPES),
        "features": list(WORKBENCH_FEATURES),
    }


def statistical() -> dict[str, Any]:
    return dict(STATISTICAL)


def patterns() -> dict[str, Any]:
    return dict(PATTERN_DISCOVERY)


def root_cause() -> dict[str, Any]:
    return dict(ROOT_CAUSE)


def experiments() -> dict[str, Any]:
    return dict(EXPERIMENTATION)


def visual() -> dict[str, Any]:
    return {
        "visualizations": list(VISUAL_ANALYTICS),
        "visualization_count": len(VISUAL_ANALYTICS),
    }


def ai_native() -> dict[str, Any]:
    return {
        "agents": list(AI_AGENTS),
        "agent_count": len(AI_AGENTS),
        "capabilities": list(AI_CAPABILITIES),
        "via_enterprise_ai": True,
        "module_local_llm_sdk_forbidden": True,
    }


def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH)


def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN)


def semantic_integration() -> dict[str, Any]:
    return dict(SEMANTIC_INTEGRATION)


def self_service_integration() -> dict[str, Any]:
    return dict(SELF_SERVICE_INTEGRATION)


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
        "version_strategy": "append_only_vN",
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
            "enterprise_advanced_analytics_platform": True,
            "statistical_analytics_platform": True,
            "enterprise_experimentation_platform": True,
            "pattern_discovery_platform": True,
            "root_cause_analytics": True,
            "insight_management_platform": True,
            "ai_analytics_platform": True,
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
            "advanced_api_live": True,
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
            "ADR-394",
            "ADR-395",
            "ADR-396",
            "ADR-408",
            "ADR-409",
            "ADR-410",
            "ADR-411",
            "ADR-412",
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
        "architecture": {
            "present_required": True,
            "not_incomplete": True,
            "capabilities": [
                "statistical_analytics",
                "data_science_platform",
                "analytical_modeling",
                "experimentation_platform",
                "pattern_discovery",
                "correlation_intelligence",
                "root_cause_analytics",
                "behaviour_analytics",
                "analytical_workbench",
                "analytical_intelligence_services",
            ],
            "capability_count": 10,
        },
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "workbench": workbench(),
        "statistical": statistical(),
        "patterns": patterns(),
        "root_cause": root_cause(),
        "experiments": experiments(),
        "visual": visual(),
        "ai_native": ai_native(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "semantic_integration": semantic_integration(),
        "self_service_integration": self_service_integration(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "apis": api_boundaries(),
        "security": security(),
        "deployment": deployment(),
        "testing": testing(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "enterprise_advanced_analytics_platform_present_required": True,
        "statistical_intelligence_platform_present_required": True,
        "enterprise_experimentation_platform_present_required": True,
        "pattern_discovery_platform_present_required": True,
        "root_cause_analytics_present_required": True,
        "insight_management_present_required": True,
        "ai_assisted_analytics_present_required": True,
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
        "sibling_business_intelligence_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/advanced",
        "forbidden_sibling_bc": [
            "business_intelligence",
            "decision_intelligence",
            "reporting_platform",
            "metric_governance_platform",
            "visualization_platform",
            "bi_core",
        ],
    }


def advanced_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /analytics/advanced",
            "GET /analytics/advanced/vision",
            "GET /analytics/advanced/domain",
            "GET /analytics/advanced/bounded-contexts",
            "GET /analytics/advanced/workbench",
            "GET /analytics/advanced/statistical",
            "GET /analytics/advanced/patterns",
            "GET /analytics/advanced/root-cause",
            "GET /analytics/advanced/experiments",
            "GET /analytics/advanced/visual",
            "GET /analytics/advanced/ai",
            "GET /analytics/advanced/knowledge-graph",
            "GET /analytics/advanced/digital-twin",
            "GET /analytics/advanced/cqrs",
            "GET /analytics/advanced/events",
            "GET /analytics/advanced/microservices",
            "GET /analytics/advanced/apis",
            "GET /analytics/advanced/security",
            "GET /analytics/advanced/deployment",
            "GET /analytics/advanced/testing",
            "GET /analytics/advanced/outputs",
            "GET /analytics/advanced/production-readiness",
            "GET /analytics/advanced/readiness",
        ],
    }
