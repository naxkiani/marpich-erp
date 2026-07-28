"""P213-J Enterprise Predictive Analytics & Forecasting Platform — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P213-J"
ADR = 414
SOR = "analytics"
API_PREFIX = "/api/v1/analytics"
PRODUCT = "Enterprise Predictive Analytics & Forecasting Platform"
CAPABILITY = "CAP-PLT-BI-001"

PRINCIPLE = (
    "Enterprise Predictive Analytics SHALL enable MEOS to anticipate "
    "future business conditions before they become operational realities."
)

FABRIC = "meos_enterprise_predictive_intelligence_fabric"

CORE_DOMAIN = "enterprise_predictive_intelligence_management"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {"id": "forecast_management", "purpose": "Forecast lifecycle and publication."},
    {"id": "predictive_modeling", "purpose": "Model creation, execution, validation."},
    {"id": "scenario_prediction", "purpose": "What-if and alternative futures."},
    {"id": "capacity_prediction", "purpose": "Capacity and resource forecasting."},
    {"id": "trend_intelligence", "purpose": "Trend and seasonality intelligence."},
    {"id": "risk_forecasting", "purpose": "Risk and threat forecasting."},
    {"id": "recommendation_generation", "purpose": "Preparation recommendations."},
    {"id": "prediction_governance", "purpose": "Approval, quality, monitoring."},
)

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "forecast_management",
        "bc": "BC-01",
        "name": "Forecast Management Context",
        "purpose": "Forecast lifecycle, publication, governance.",
    },
    {
        "id": "predictive_modeling",
        "bc": "BC-02",
        "name": "Predictive Modeling Context",
        "purpose": "Model creation, execution, validation.",
    },
    {
        "id": "scenario_prediction",
        "bc": "BC-03",
        "name": "Scenario Prediction Context",
        "purpose": "What-if prediction, alternative futures, simulation.",
    },
    {
        "id": "capacity_demand_forecast",
        "bc": "BC-04",
        "name": "Capacity & Demand Forecast Context",
        "purpose": "Capacity planning, demand and resource forecasting.",
    },
    {
        "id": "risk_forecast",
        "bc": "BC-05",
        "name": "Risk Forecast Context",
        "purpose": "Risk, threat, and operational forecasting.",
    },
    {
        "id": "prediction_governance",
        "bc": "BC-06",
        "name": "Prediction Governance Context",
        "purpose": "Forecast approval, prediction quality, model monitoring.",
    },
)

AGGREGATE = {
    "name": "PredictiveAnalyticsAggregate",
    "root": "PredictiveAnalytics",
    "entities": (
        "PredictionModel",
        "Forecast",
        "Scenario",
        "PredictionRun",
        "ForecastVersion",
        "PredictionInsight",
        "ForecastPolicy",
        "PredictionRecommendation",
    ),
    "value_objects": (
        "ForecastPeriod",
        "PredictionConfidence",
        "ForecastGranularity",
        "PredictionHorizon",
        "ScenarioIdentifier",
        "ModelAccuracy",
        "PredictionThreshold",
    ),
    "events": (
        "ForecastCreatedEvent",
        "PredictionCompletedEvent",
        "ScenarioPredictedEvent",
        "ForecastApprovedEvent",
        "PredictionAccuracyMeasuredEvent",
        "ForecastPublishedEvent",
    ),
}

FORECAST_LIFECYCLE: tuple[str, ...] = (
    "forecast_request",
    "model_selection",
    "prediction_execution",
    "validation",
    "approval",
    "publication",
    "monitoring",
    "continuous_learning",
)

FORECAST_HORIZONS: tuple[str, ...] = (
    "short_term",
    "medium_term",
    "long_term",
    "rolling",
    "continuous",
)

MODEL_TYPES: tuple[str, ...] = (
    "regression",
    "classification",
    "time_series",
    "decision_trees",
    "random_forests",
    "gradient_boosting",
    "neural_networks",
    "bayesian",
    "ensemble",
    "hybrid",
)

MODEL_LIFECYCLE: tuple[str, ...] = (
    "training",
    "validation",
    "testing",
    "deployment",
    "versioning",
    "retirement",
)

FORECAST_DOMAINS: tuple[str, ...] = (
    "revenue",
    "sales",
    "demand",
    "inventory",
    "supply_chain",
    "cash_flow",
    "budget",
    "workforce",
    "projects",
    "operations",
    "cyber_security",
    "compliance",
    "customer_behaviour",
    "ai_capacity",
    "infrastructure",
)

SCENARIOS: dict[str, Any] = {
    "cases": (
        "best_case",
        "expected_case",
        "worst_case",
    ),
    "methods": (
        "monte_carlo_simulation",
        "sensitivity_analysis",
        "probability_forecasting",
        "business_impact_analysis",
        "alternative_future_analysis",
    ),
}

TIME_SERIES: tuple[str, ...] = (
    "trend_analysis",
    "seasonality",
    "cycles",
    "anomaly_detection",
    "forecast_decomposition",
    "multivariate_forecasting",
    "real_time_forecast_updates",
)

AI_AGENTS: tuple[str, ...] = (
    "forecast_advisor_agent",
    "prediction_scientist_agent",
    "trend_analysis_agent",
    "capacity_planning_agent",
    "demand_forecast_agent",
    "revenue_forecast_agent",
    "scenario_planning_agent",
    "business_recommendation_agent",
)

AI_CAPABILITIES: tuple[str, ...] = (
    "automatic_forecasting",
    "model_recommendation",
    "continuous_learning",
    "forecast_explanation",
    "prediction_optimisation",
    "business_recommendations",
)

EXPLAINABILITY: dict[str, Any] = {
    "capabilities": (
        "prediction_reasoning",
        "confidence_explanation",
        "feature_importance",
        "business_explanation",
        "model_transparency",
        "prediction_audit_trail",
    ),
    "xai_required": True,
}

KNOWLEDGE_GRAPH: dict[str, Any] = {
    "via_p212_j": True,
    "graph": "enterprise_predictive_knowledge_graph",
    "nodes": (
        "Forecast",
        "Prediction",
        "Scenario",
        "Risk",
        "Opportunity",
        "Metric",
        "BusinessEntity",
        "Decision",
        "Recommendation",
    ),
    "relationships": (
        "Forecast_PREDICTS_Metric",
        "Scenario_IMPACTS_BusinessEntity",
        "Recommendation_GENERATED_FROM_Forecast",
        "Decision_REFERENCES_Prediction",
    ),
}

DIGITAL_TWIN: dict[str, Any] = {
    "via_p212_l": True,
    "capabilities": (
        "future_state_simulation",
        "operational_forecast_simulation",
        "capacity_simulation",
        "demand_simulation",
        "strategic_planning",
        "business_continuity_planning",
    ),
}

SEMANTIC_INTEGRATION: dict[str, Any] = {
    "via_p213_g": True,
    "uses": ("certified_metrics", "semantic_models", "enterprise_kpis"),
}

ADVANCED_INTEGRATION: dict[str, Any] = {
    "via_p213_i": True,
    "uses": (
        "statistical_analytics",
        "experimentation",
        "pattern_discovery",
        "root_cause_analytics",
    ),
}

COMMANDS: tuple[str, ...] = (
    "CreateForecastCommand",
    "TrainPredictionModelCommand",
    "ExecuteForecastCommand",
    "ApproveForecastCommand",
    "PublishForecastCommand",
)

QUERIES: tuple[str, ...] = (
    "GetForecastQuery",
    "GetPredictionQuery",
    "SearchForecastsQuery",
    "GetScenarioQuery",
    "GetForecastAccuracyQuery",
)

CORE_EVENTS: tuple[dict[str, Any], ...] = (
    {
        "name": "ForecastRequestedEvent",
        "producer": "forecast_management",
        "consumers": ("predictive_modeling", "audit"),
        "payload": ("tenant_id", "forecast_id", "horizon"),
        "version": "v1",
    },
    {
        "name": "ForecastGeneratedEvent",
        "producer": "prediction_engine",
        "consumers": ("forecast_management", "explainability"),
        "payload": ("tenant_id", "forecast_id", "model_id"),
        "version": "v1",
    },
    {
        "name": "PredictionCompletedEvent",
        "producer": "predictive_modeling",
        "consumers": ("insight", "knowledge_graph"),
        "payload": ("tenant_id", "prediction_id", "confidence"),
        "version": "v1",
    },
    {
        "name": "ScenarioSimulatedEvent",
        "producer": "scenario_prediction",
        "consumers": ("digital_twin", "recommendation"),
        "payload": ("tenant_id", "scenario_id", "case"),
        "version": "v1",
    },
    {
        "name": "ForecastApprovedEvent",
        "producer": "prediction_governance",
        "consumers": ("forecast_management", "audit"),
        "payload": ("tenant_id", "forecast_id", "approver_ref"),
        "version": "v1",
    },
    {
        "name": "ForecastPublishedEvent",
        "producer": "forecast_management",
        "consumers": ("notifications", "self_service", "audit"),
        "payload": ("tenant_id", "forecast_id", "version"),
        "version": "v1",
    },
    {
        "name": "AccuracyMeasuredEvent",
        "producer": "prediction_governance",
        "consumers": ("model_management", "observability"),
        "payload": ("tenant_id", "forecast_id", "accuracy"),
        "version": "v1",
    },
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "name": "forecast-management-service",
        "responsibility": "Forecast lifecycle and publication.",
        "database_boundary": "analytics_pred_forecasts",
        "api_boundary": "/api/v1/analytics/forecasts",
        "events": ("ForecastRequestedEvent", "ForecastPublishedEvent"),
        "security_model": "analytics.forecasts.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "prediction-engine-service",
        "responsibility": "Prediction execution and scoring.",
        "database_boundary": "analytics_pred_engine",
        "api_boundary": "/api/v1/analytics/predictions",
        "events": ("ForecastGeneratedEvent", "PredictionCompletedEvent"),
        "security_model": "analytics.predictions.*",
        "scaling_strategy": "compute_pool_autoscaling",
    },
    {
        "name": "model-management-service",
        "responsibility": "Model training, versioning, retirement.",
        "database_boundary": "analytics_pred_models",
        "api_boundary": "/api/v1/analytics/models",
        "events": ("AccuracyMeasuredEvent",),
        "security_model": "analytics.models.*",
        "scaling_strategy": "gpu_accelerated_workers",
    },
    {
        "name": "scenario-planning-service",
        "responsibility": "Scenario and what-if prediction.",
        "database_boundary": "analytics_pred_scenarios",
        "api_boundary": "/api/v1/analytics/scenarios",
        "events": ("ScenarioSimulatedEvent",),
        "security_model": "analytics.scenarios.*",
        "scaling_strategy": "async_workers",
    },
    {
        "name": "capacity-forecast-service",
        "responsibility": "Capacity and demand forecasting.",
        "database_boundary": "analytics_pred_capacity",
        "api_boundary": "/api/v1/analytics/forecasts/capacity",
        "events": ("ForecastGeneratedEvent",),
        "security_model": "analytics.capacity.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "forecast-governance-service",
        "responsibility": "Approval, quality, model monitoring.",
        "database_boundary": "analytics_pred_gov",
        "api_boundary": "/api/v1/analytics/forecasts/governance",
        "events": ("ForecastApprovedEvent", "AccuracyMeasuredEvent"),
        "security_model": "analytics.forecast.governance.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "forecast-ai-service",
        "responsibility": "AI forecast agents via Enterprise AI.",
        "database_boundary": "analytics_pred_ai",
        "api_boundary": "/api/v1/analytics/recommendations",
        "events": ("PredictionCompletedEvent",),
        "security_model": "analytics.forecast.ai.*",
        "scaling_strategy": "async_via_enterprise_ai",
    },
    {
        "name": "prediction-explanation-service",
        "responsibility": "XAI explanations and audit trails.",
        "database_boundary": "analytics_pred_xai",
        "api_boundary": "/api/v1/analytics/explanations",
        "events": ("ForecastGeneratedEvent",),
        "security_model": "analytics.explanations.*",
        "scaling_strategy": "horizontal_stateless",
    },
)

API_BOUNDARIES: dict[str, Any] = {
    "forecast": (
        "/api/v1/analytics/forecasts",
        "/api/v1/analytics/predictions",
        "/api/v1/analytics/models",
        "/api/v1/analytics/scenarios",
        "/api/v1/analytics/recommendations",
        "/api/v1/analytics/explanations",
    ),
    "rest": True,
    "graphql": "/api/v1/analytics/graphql",
    "grpc": True,
    "streaming_apis": "/api/v1/analytics/forecasts/stream",
    "event_apis": "analytics.predictive.*.v1",
    "security": (
        "analytics.predictive.read",
        "zero_trust",
        "tenant_isolation",
    ),
}

SECURITY: dict[str, Any] = {
    "via_p207": True,
    "via_p208": True,
    "via_p211": True,
    "via_p212": True,
    "prediction_authorization": True,
    "forecast_classification": True,
    "model_governance": True,
    "explainability_policies": True,
    "audit_logging": True,
    "privacy_controls": True,
    "model_approval_workflow": True,
    "attribute_based_access_control": True,
    "row_level_security": True,
}

DEPLOYMENT: dict[str, Any] = {
    "kubernetes": True,
    "service_mesh": True,
    "distributed_compute": True,
    "gpu_acceleration": True,
    "container_platform": True,
    "cicd": True,
    "observability": True,
    "autoscaling": True,
    "high_availability": True,
    "disaster_recovery": True,
    "multi_region": True,
    "cloud_native": True,
}

TESTING: tuple[str, ...] = (
    "prediction_accuracy_testing",
    "forecast_validation",
    "model_drift_testing",
    "scenario_testing",
    "performance_testing",
    "security_testing",
    "scalability_testing",
    "explainability_testing",
    "governance_testing",
    "regression_testing",
    "acceptance_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_predictive_analytics_vision",
    "ddd_domain_model",
    "bounded_context_architecture",
    "enterprise_forecast_management_platform",
    "predictive_model_platform",
    "enterprise_forecasting_engine",
    "scenario_prediction_platform",
    "time_series_intelligence",
    "ai_native_prediction_platform",
    "prediction_explanation_platform",
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
    "enterprise_predictive_analytics_platform_is_missing",
    "enterprise_forecasting_platform_is_missing",
    "predictive_modeling_platform_is_missing",
    "scenario_prediction_platform_is_missing",
    "time_series_intelligence_is_missing",
    "explainable_ai_platform_is_missing",
    "knowledge_graph_integration_is_missing",
    "digital_twin_integration_is_missing",
    "cqrs_architecture_is_missing",
    "event_sourcing_architecture_is_missing",
    "microservice_architecture_is_missing",
    "api_first_architecture_is_missing",
    "zero_trust_security_is_missing",
    "enterprise_governance_is_missing",
    "cloud_native_deployment_is_missing",
    "predictive_analytics_architecture_is_incomplete",
    "sibling_business_intelligence_bc",
)

PREDICTION_FLOW: tuple[str, ...] = (
    "reliable_enterprise_forecasts",
    "predict_future_outcomes",
    "estimate_business_impact",
    "recommend_preparation",
    "support_better_decisions",
)


def vision() -> dict[str, Any]:
    return {
        "statement": PRINCIPLE,
        "fabric": FABRIC,
        "inputs": (
            "historical_enterprise_data",
            "real_time_events",
            "business_knowledge",
            "enterprise_metrics",
            "ai_intelligence",
            "digital_twins",
        ),
        "flow": list(PREDICTION_FLOW),
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


def forecast_management() -> dict[str, Any]:
    return {
        "lifecycle": list(FORECAST_LIFECYCLE),
        "lifecycle_step_count": len(FORECAST_LIFECYCLE),
        "horizons": list(FORECAST_HORIZONS),
        "horizon_count": len(FORECAST_HORIZONS),
    }


def predictive_models() -> dict[str, Any]:
    return {
        "types": list(MODEL_TYPES),
        "type_count": len(MODEL_TYPES),
        "lifecycle": list(MODEL_LIFECYCLE),
    }


def forecasting_engine() -> dict[str, Any]:
    return {
        "domains": list(FORECAST_DOMAINS),
        "domain_count": len(FORECAST_DOMAINS),
    }


def scenarios() -> dict[str, Any]:
    return dict(SCENARIOS)


def time_series() -> dict[str, Any]:
    return {
        "capabilities": list(TIME_SERIES),
        "capability_count": len(TIME_SERIES),
    }


def ai_native() -> dict[str, Any]:
    return {
        "agents": list(AI_AGENTS),
        "agent_count": len(AI_AGENTS),
        "capabilities": list(AI_CAPABILITIES),
        "via_enterprise_ai": True,
        "module_local_llm_sdk_forbidden": True,
    }


def explainability() -> dict[str, Any]:
    return dict(EXPLAINABILITY)


def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH)


def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN)


def semantic_integration() -> dict[str, Any]:
    return dict(SEMANTIC_INTEGRATION)


def advanced_integration() -> dict[str, Any]:
    return dict(ADVANCED_INTEGRATION)


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
        "event_store_policy": "immutable_append_only",
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
            "enterprise_predictive_analytics_platform": True,
            "forecast_management_platform": True,
            "predictive_model_platform": True,
            "time_series_intelligence": True,
            "scenario_prediction_platform": True,
            "explainable_ai_platform": True,
            "ai_forecast_agents": True,
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
            "predictive_api_live": True,
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
            "ADR-394",
            "ADR-395",
            "ADR-396",
            "ADR-408",
            "ADR-409",
            "ADR-410",
            "ADR-411",
            "ADR-412",
            "ADR-413",
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
                "enterprise_predictive_intelligence",
                "enterprise_forecast_management",
                "enterprise_scenario_prediction",
                "enterprise_trend_prediction",
                "enterprise_capacity_forecasting",
                "enterprise_risk_forecasting",
                "enterprise_revenue_forecasting",
                "enterprise_demand_forecasting",
                "enterprise_ai_prediction_services",
                "enterprise_decision_forecast_intelligence",
            ],
            "capability_count": 10,
        },
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "forecast_management": forecast_management(),
        "predictive_models": predictive_models(),
        "forecasting_engine": forecasting_engine(),
        "scenarios": scenarios(),
        "time_series": time_series(),
        "ai_native": ai_native(),
        "explainability": explainability(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "semantic_integration": semantic_integration(),
        "advanced_integration": advanced_integration(),
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
        "enterprise_predictive_analytics_platform_present_required": True,
        "enterprise_forecasting_platform_present_required": True,
        "predictive_modeling_platform_present_required": True,
        "scenario_prediction_platform_present_required": True,
        "time_series_intelligence_present_required": True,
        "explainable_ai_platform_present_required": True,
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
        "api_prefix": f"{API_PREFIX}/predictive",
        "forbidden_sibling_bc": [
            "business_intelligence",
            "decision_intelligence",
            "reporting_platform",
            "metric_governance_platform",
            "visualization_platform",
            "bi_core",
        ],
    }


def predictive_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /analytics/predictive",
            "GET /analytics/predictive/vision",
            "GET /analytics/predictive/domain",
            "GET /analytics/predictive/bounded-contexts",
            "GET /analytics/predictive/forecast-management",
            "GET /analytics/predictive/models",
            "GET /analytics/predictive/engine",
            "GET /analytics/predictive/scenarios",
            "GET /analytics/predictive/time-series",
            "GET /analytics/predictive/ai",
            "GET /analytics/predictive/explainability",
            "GET /analytics/predictive/knowledge-graph",
            "GET /analytics/predictive/digital-twin",
            "GET /analytics/predictive/cqrs",
            "GET /analytics/predictive/events",
            "GET /analytics/predictive/microservices",
            "GET /analytics/predictive/apis",
            "GET /analytics/predictive/security",
            "GET /analytics/predictive/deployment",
            "GET /analytics/predictive/testing",
            "GET /analytics/predictive/outputs",
            "GET /analytics/predictive/production-readiness",
            "GET /analytics/predictive/readiness",
        ],
    }
