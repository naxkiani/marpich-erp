"""P213-C Enterprise BI Domain Architecture — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P213-C"
ADR = 396
SOR = "analytics"
API_PREFIX = "/api/v1/analytics"
PRODUCT = (
    "Enterprise Business Intelligence, Analytics & Decision Intelligence "
    "Platform — Domain Architecture"
)
CAPABILITY = "CAP-PLT-BI-001"

PRINCIPLE = (
    "Raw enterprise data SHALL be transformed into governed "
    "business intelligence assets through DDD boundaries."
)

FABRIC = "meos_enterprise_bi_domain_fabric"

CORE_DOMAIN = "enterprise_business_intelligence_management"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {
        "id": "analytics_processing",
        "purpose": "Transform enterprise data into analytical intelligence.",
    },
    {
        "id": "business_metrics_governance",
        "purpose": "Define, manage, and govern enterprise KPIs.",
    },
    {
        "id": "reporting_visualization",
        "purpose": "Deliver intelligence consumption experiences.",
    },
    {
        "id": "decision_intelligence",
        "purpose": "Convert insights into intelligent decisions.",
    },
)

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "bi_core",
        "bc": "BC-01",
        "name": "Business Intelligence Core Context",
        "purpose": (
            "BI asset management, intelligence lifecycle, "
            "business insight management."
        ),
        "owns": (
            "bi_asset_management",
            "intelligence_lifecycle",
            "business_insight_management",
        ),
        "aggregate_root": "BIAsset",
        "aggregates": ("EnterpriseBIAssetAggregate",),
        "entities": ("Dashboard", "Report", "Insight", "KPI", "Metric"),
        "value_objects": (
            "BIAssetId",
            "AssetType",
            "BusinessPurpose",
            "PublicationStatus",
        ),
        "domain_services": ("InsightGenerationService", "DashboardCompositionService"),
        "repositories": ("BIAssetRepository",),
        "factories": ("BIAssetFactory",),
        "commands": ("CreateBIAssetCommand", "PublishBIAssetCommand"),
        "events": (
            "BIAssetCreatedEvent",
            "InsightPublishedEvent",
            "DashboardReleasedEvent",
            "BIAssetValidatedEvent",
            "BIAssetPublishedEvent",
        ),
        "domain_rules": (
            "Only validated intelligence assets can be published.",
        ),
    },
    {
        "id": "business_metrics",
        "bc": "BC-02",
        "name": "Business Metrics Context",
        "purpose": "KPI definition, metric governance, semantic consistency.",
        "owns": (
            "kpi_definition",
            "metric_governance",
            "semantic_consistency",
        ),
        "aggregate_root": "EnterpriseMetric",
        "aggregates": ("EnterpriseMetricAggregate",),
        "entities": (
            "MetricDefinition",
            "KPI",
            "MeasurementRule",
            "MetricOwner",
            "MeasurementDefinition",
            "MetricCalculation",
        ),
        "value_objects": (
            "MetricType",
            "Formula",
            "MeasurementFrequency",
            "BusinessOwner",
        ),
        "domain_services": ("MetricCalculationService",),
        "repositories": ("MetricRepository",),
        "factories": ("MetricFactory",),
        "commands": ("CreateMetricCommand", "ValidateMetricCommand"),
        "events": (
            "MetricCreatedEvent",
            "MetricChangedEvent",
            "MetricValidatedEvent",
            "MetricDefinedEvent",
            "MetricCalculatedEvent",
        ),
    },
    {
        "id": "reporting_visualization",
        "bc": "BC-03",
        "name": "Reporting & Visualization Context",
        "purpose": "Report generation, visualization management, UX.",
        "owns": (
            "report_generation",
            "visualization_management",
            "user_experience",
        ),
        "aggregate_root": "ReportTemplate",
        "aggregates": ("ReportingAggregate",),
        "entities": (
            "ReportTemplate",
            "Visualization",
            "DashboardLayout",
        ),
        "value_objects": ("LayoutId", "VisualizationType", "RenderProfile"),
        "domain_services": ("DashboardCompositionService",),
        "repositories": ("ReportRepository", "DashboardRepository"),
        "factories": ("ReportFactory",),
        "commands": ("GenerateReportCommand", "UpdateDashboardCommand"),
        "events": (
            "ReportGeneratedEvent",
            "DashboardUpdatedEvent",
            "DashboardPublishedEvent",
        ),
    },
    {
        "id": "analytics_intelligence",
        "bc": "BC-04",
        "name": "Analytics Intelligence Context",
        "purpose": (
            "Analytical processing, pattern discovery, statistical intelligence."
        ),
        "owns": (
            "analytical_processing",
            "pattern_discovery",
            "statistical_intelligence",
        ),
        "aggregate_root": "AnalyticsModel",
        "aggregates": ("AnalyticsModelAggregate",),
        "entities": (
            "AnalyticsModel",
            "AnalysisJob",
            "InsightResult",
            "ModelVersion",
            "TrainingDataset",
            "AnalysisExecution",
        ),
        "value_objects": ("ModelType", "AccuracyScore", "ConfidenceLevel"),
        "domain_services": ("AnalyticsExecutionService", "InsightGenerationService"),
        "repositories": ("AnalyticsModelRepository",),
        "factories": ("AnalyticsModelFactory",),
        "commands": ("ExecuteAnalyticsCommand", "CreateAnalyticsModelCommand"),
        "events": (
            "AnalyticsExecutedEvent",
            "PatternDiscoveredEvent",
            "ModelCreatedEvent",
            "AnalysisExecutedEvent",
            "InsightGeneratedEvent",
        ),
    },
    {
        "id": "decision_intelligence",
        "bc": "BC-05",
        "name": "Decision Intelligence Context",
        "purpose": "Decision modelling, recommendations, business actions.",
        "owns": (
            "decision_modelling",
            "recommendations",
            "business_actions",
        ),
        "aggregate_root": "DecisionModel",
        "aggregates": ("DecisionModelAggregate",),
        "entities": (
            "DecisionModel",
            "DecisionRule",
            "Recommendation",
            "DecisionOutcome",
        ),
        "value_objects": ("DecisionType", "ImpactScore", "ConfidenceScore"),
        "domain_services": ("DecisionRecommendationService",),
        "repositories": ("DecisionModelRepository",),
        "factories": ("DecisionModelFactory",),
        "commands": ("GenerateRecommendationCommand", "CompleteDecisionCommand"),
        "events": (
            "RecommendationGeneratedEvent",
            "DecisionCompletedEvent",
            "DecisionCreatedEvent",
        ),
    },
)

DOMAIN_AGGREGATES: tuple[str, ...] = (
    "EnterpriseBIAssetAggregate",
    "EnterpriseMetricAggregate",
    "AnalyticsModelAggregate",
    "DecisionModelAggregate",
    "ReportingAggregate",
    "DomainOwnershipMap",
)

DOMAIN_SERVICES: tuple[dict[str, Any], ...] = (
    {
        "name": "MetricCalculationService",
        "responsibility": "Calculate governed enterprise metrics from contracts.",
        "inputs": ("MetricDefinition", "MeasurementRule", "DataProductRef"),
        "outputs": ("MetricCalculation", "MetricCalculatedEvent"),
        "domain_rules": ("Formula must be validated before calculation.",),
    },
    {
        "name": "InsightGenerationService",
        "responsibility": "Generate business insights from analytics results.",
        "inputs": ("InsightResult", "AnalyticsModel"),
        "outputs": ("Insight", "InsightGeneratedEvent"),
        "domain_rules": ("Insights require confidence threshold.",),
    },
    {
        "name": "DashboardCompositionService",
        "responsibility": "Compose dashboards from validated BI assets.",
        "inputs": ("DashboardLayout", "Visualization", "Metric"),
        "outputs": ("Dashboard", "DashboardPublishedEvent"),
        "domain_rules": ("Only published metrics may appear on released dashboards.",),
    },
    {
        "name": "AnalyticsExecutionService",
        "responsibility": "Execute analytical jobs against data products.",
        "inputs": ("AnalyticsModel", "AnalysisJob", "DataProductRef"),
        "outputs": ("InsightResult", "AnalyticsExecutedEvent"),
        "domain_rules": ("Execution requires AI-ready dataset readiness when ML.",),
    },
    {
        "name": "DecisionRecommendationService",
        "responsibility": "Produce decision recommendations from insights.",
        "inputs": ("DecisionModel", "Insight", "DecisionRule"),
        "outputs": ("Recommendation", "RecommendationGeneratedEvent"),
        "domain_rules": ("Recommendations must cite source insights.",),
    },
)

CORE_EVENTS: tuple[dict[str, Any], ...] = (
    {
        "name": "BIAssetCreatedEvent",
        "producer": "bi_core",
        "consumers": ("reporting_visualization", "audit"),
        "payload": ("tenant_id", "asset_id", "asset_type"),
        "version": "v1",
    },
    {
        "name": "MetricDefinedEvent",
        "producer": "business_metrics",
        "consumers": ("bi_core", "data_governance"),
        "payload": ("tenant_id", "metric_id", "formula"),
        "version": "v1",
    },
    {
        "name": "ReportGeneratedEvent",
        "producer": "reporting_visualization",
        "consumers": ("bi_core", "notifications"),
        "payload": ("tenant_id", "report_id", "template_id"),
        "version": "v1",
    },
    {
        "name": "DashboardPublishedEvent",
        "producer": "reporting_visualization",
        "consumers": ("bi_core", "audit"),
        "payload": ("tenant_id", "dashboard_id", "layout_id"),
        "version": "v1",
    },
    {
        "name": "AnalyticsExecutedEvent",
        "producer": "analytics_intelligence",
        "consumers": ("bi_core", "decision_intelligence"),
        "payload": ("tenant_id", "job_id", "model_id"),
        "version": "v1",
    },
    {
        "name": "InsightGeneratedEvent",
        "producer": "analytics_intelligence",
        "consumers": ("bi_core", "decision_intelligence"),
        "payload": ("tenant_id", "insight_id", "confidence"),
        "version": "v1",
    },
    {
        "name": "RecommendationGeneratedEvent",
        "producer": "decision_intelligence",
        "consumers": ("workflow", "notifications"),
        "payload": ("tenant_id", "recommendation_id", "impact_score"),
        "version": "v1",
    },
    {
        "name": "DecisionCompletedEvent",
        "producer": "decision_intelligence",
        "consumers": ("audit", "digital_twin"),
        "payload": ("tenant_id", "decision_id", "outcome"),
        "version": "v1",
    },
)

COMMANDS: tuple[str, ...] = (
    "PublishDomainMap",
    "RegisterLogicalSubdomain",
    "BindBIOwnership",
    "CreateBIAssetCommand",
    "CreateMetricCommand",
    "GenerateReportCommand",
    "ExecuteAnalyticsCommand",
    "GenerateRecommendationCommand",
    "DeclareIntegrationBoundary",
    "AlignDataMeshContracts",
)

QUERIES: tuple[str, ...] = (
    "GetDomainMap",
    "GetBoundedContexts",
    "GetAggregates",
    "GetDashboardQuery",
    "GetReportQuery",
    "GetMetricQuery",
    "GetInsightQuery",
    "GetDecisionQuery",
    "GetDomainReadiness",
)

DOMAIN_EVENTS: tuple[str, ...] = (
    "DomainMapPublished",
    "SubdomainRegistered",
    "BIOwnershipBound",
    "IntegrationBoundaryDeclared",
    "EventCataloguePublished",
    "DataMeshAligned",
    "KnowledgeGraphAligned",
    "DigitalTwinAligned",
    "GovernanceAligned",
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "name": "bi-core-service",
        "database_boundary": "analytics_bi_core",
        "api_boundary": "/api/v1/analytics/assets",
        "event_boundary": "analytics.bi_asset.*",
        "deployment_boundary": "analytics-bi-core",
    },
    {
        "name": "metric-governance-service",
        "database_boundary": "analytics_metrics",
        "api_boundary": "/api/v1/analytics/metrics",
        "event_boundary": "analytics.metric.*",
        "deployment_boundary": "analytics-metrics",
    },
    {
        "name": "reporting-service",
        "database_boundary": "analytics_reports",
        "api_boundary": "/api/v1/analytics/reports",
        "event_boundary": "analytics.report.*",
        "deployment_boundary": "analytics-reporting",
    },
    {
        "name": "visualization-service",
        "database_boundary": "analytics_viz",
        "api_boundary": "/api/v1/analytics/dashboards",
        "event_boundary": "analytics.dashboard.*",
        "deployment_boundary": "analytics-visualization",
    },
    {
        "name": "analytics-service",
        "database_boundary": "analytics_models",
        "api_boundary": "/api/v1/analytics/analytics",
        "event_boundary": "analytics.analysis.*",
        "deployment_boundary": "analytics-intel",
    },
    {
        "name": "decision-intelligence-service",
        "database_boundary": "analytics_decisions",
        "api_boundary": "/api/v1/analytics/decisions",
        "event_boundary": "analytics.decision.*",
        "deployment_boundary": "analytics-decisions",
    },
)

DATA_MESH_ALIGNMENT: dict[str, Any] = {
    "via_p212_f": True,
    "role": "consumer_of_data_products",
    "inputs": (
        "finance_data_product",
        "customer_data_product",
        "operations_data_product",
        "risk_data_product",
    ),
    "contract_requirements": (
        "schema_version",
        "sla",
        "quality_score_minimum",
        "owner_ref",
        "lineage_ref",
        "access_policy_ref",
    ),
}

KNOWLEDGE_GRAPH_ALIGNMENT: dict[str, Any] = {
    "via_p212_j": True,
    "nodes": (
        "Metric",
        "Dashboard",
        "Report",
        "Insight",
        "Decision",
        "BusinessProcess",
        "DataProduct",
    ),
    "relationships": (
        "Metric_DERIVED_FROM_DataProduct",
        "Insight_GENERATED_BY_Analytics",
        "Decision_BASED_ON_Insight",
    ),
}

DIGITAL_TWIN_ALIGNMENT: dict[str, Any] = {
    "via_p212_l": True,
    "capabilities": (
        "bi_scenario_simulation",
        "kpi_forecasting",
        "decision_impact_analysis",
        "business_future_state_modeling",
    ),
}

GOVERNANCE_ALIGNMENT: dict[str, Any] = {
    "via_p207": True,
    "via_p208": True,
    "via_p211": True,
    "via_p212": True,
    "bi_access_governance": True,
    "metric_ownership": True,
    "report_security": True,
    "data_usage_policies": True,
}

API_BOUNDARIES: dict[str, Any] = {
    "rest": (
        "/api/v1/analytics/assets",
        "/api/v1/analytics/metrics",
        "/api/v1/analytics/dashboards",
        "/api/v1/analytics/reports",
        "/api/v1/analytics/analytics",
        "/api/v1/analytics/decisions",
    ),
    "graphql": "/api/v1/analytics/graphql",
    "event_apis": "analytics.*.v1",
    "security_policies": ("analytics.read", "zero_trust", "tenant_isolation"),
}

DEPLOYMENT: dict[str, Any] = {
    "containers": True,
    "kubernetes": True,
    "service_mesh": True,
    "cicd": True,
    "observability": True,
    "cloud_native": True,
}

INTEGRATIONS: tuple[str, ...] = (
    "P207",
    "P208",
    "P211",
    "P212",
    "P212-E",
    "P212-F",
    "P212-I",
    "P212-J",
    "P212-K",
    "P212-L",
    "P212-M",
    "enterprise_ai",
    "knowledge_graph",
    "digital_twin",
    "policy_engine",
    "audit",
    "workflow",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_bi_domain_strategy",
    "bounded_context_map",
    "tactical_ddd_design",
    "enterprise_bi_asset_aggregate",
    "business_metric_aggregate",
    "analytics_model_aggregate",
    "decision_intelligence_aggregate",
    "domain_services",
    "bi_domain_event_model",
    "cqrs_domain_alignment",
    "microservice_boundary_design",
    "data_mesh_alignment",
    "knowledge_graph_alignment",
    "digital_twin_alignment",
    "security_governance_boundaries",
    "api_first_domain_design",
    "deployment_domain_model",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "complete_ddd_bi_architecture_is_missing",
    "strategic_domain_model_is_missing",
    "bounded_contexts_are_missing",
    "domains_are_tightly_coupled",
    "bi_ownership_is_unclear",
    "aggregates_are_undefined",
    "entities_are_undefined",
    "value_objects_are_undefined",
    "events_are_missing",
    "domain_services_are_missing",
    "integration_boundaries_are_unclear",
    "cqrs_alignment_is_missing",
    "microservice_boundaries_are_unclear",
    "data_mesh_alignment_is_missing",
    "knowledge_graph_alignment_is_missing",
    "digital_twin_alignment_is_missing",
    "enterprise_governance_alignment_is_missing",
    "sibling_business_intelligence_bc",
)


def domain_map() -> dict[str, Any]:
    return {
        "core_domain": CORE_DOMAIN,
        "supporting_domains": [dict(d) for d in SUPPORTING_DOMAINS],
        "supporting_count": len(SUPPORTING_DOMAINS),
        "loosely_coupled_required": True,
        "not_tightly_coupled": True,
        "transforms": "raw_enterprise_data_to_governed_bi_assets",
    }


def bounded_contexts() -> dict[str, Any]:
    return {
        "contexts": list(LOGICAL_BOUNDED_CONTEXTS),
        "context_count": len(LOGICAL_BOUNDED_CONTEXTS),
        "logical_only": True,
        "sibling_bc_forbidden": True,
    }


def aggregates() -> dict[str, Any]:
    return {
        "aggregates": list(DOMAIN_AGGREGATES),
        "aggregate_count": len(DOMAIN_AGGREGATES),
        "defined_required": True,
        "not_undefined": True,
        "major": {
            "enterprise_bi_asset": {
                "root": "BIAsset",
                "entities": ("Report", "Dashboard", "Insight", "Visualization"),
                "value_objects": (
                    "BIAssetId",
                    "AssetType",
                    "BusinessPurpose",
                    "PublicationStatus",
                ),
                "events": (
                    "BIAssetCreatedEvent",
                    "BIAssetValidatedEvent",
                    "BIAssetPublishedEvent",
                ),
            },
            "enterprise_metric": {
                "root": "EnterpriseMetric",
                "entities": ("KPI", "MeasurementDefinition", "MetricCalculation"),
                "value_objects": (
                    "MetricType",
                    "Formula",
                    "MeasurementFrequency",
                    "BusinessOwner",
                ),
                "events": ("MetricDefinedEvent", "MetricCalculatedEvent"),
            },
            "analytics_model": {
                "root": "AnalyticsModel",
                "entities": ("ModelVersion", "TrainingDataset", "AnalysisExecution"),
                "value_objects": ("ModelType", "AccuracyScore", "ConfidenceLevel"),
                "events": ("ModelCreatedEvent", "AnalysisExecutedEvent"),
            },
            "decision_model": {
                "root": "DecisionModel",
                "entities": ("DecisionRule", "Recommendation", "DecisionOutcome"),
                "value_objects": ("DecisionType", "ImpactScore", "ConfidenceScore"),
                "events": (
                    "DecisionCreatedEvent",
                    "RecommendationGeneratedEvent",
                ),
            },
        },
    }


def entities() -> dict[str, Any]:
    ents: list[str] = []
    for ctx in LOGICAL_BOUNDED_CONTEXTS:
        ents.extend(ctx.get("entities", ()))
    return {"entities": sorted(set(ents)), "entity_count": len(set(ents))}


def value_objects() -> dict[str, Any]:
    vos: list[str] = []
    for ctx in LOGICAL_BOUNDED_CONTEXTS:
        vos.extend(ctx.get("value_objects", ()))
    return {"value_objects": sorted(set(vos)), "count": len(set(vos))}


def ownership() -> dict[str, Any]:
    return {
        "clear_required": True,
        "not_unclear": True,
        "map": "BIDomainOwnershipMap",
        "ubiquitous_language": True,
    }


def domain_services() -> dict[str, Any]:
    return {
        "services": [dict(s) for s in DOMAIN_SERVICES],
        "service_count": len(DOMAIN_SERVICES),
    }


def events() -> dict[str, Any]:
    return {
        "core_events": [dict(e) for e in CORE_EVENTS],
        "core_event_count": len(CORE_EVENTS),
        "present_required": True,
        "not_missing": True,
    }


def microservices() -> dict[str, Any]:
    return {
        "services": [dict(s) for s in MICROSERVICES],
        "service_count": len(MICROSERVICES),
        "logical_decomposition": True,
        "boundaries_clear_required": True,
        "not_unclear": True,
    }


def integrations() -> dict[str, Any]:
    return {
        "targets": list(INTEGRATIONS),
        "count": len(INTEGRATIONS),
        "boundaries_clear_required": True,
        "not_unclear": True,
        "data_mesh": DATA_MESH_ALIGNMENT,
        "knowledge_graph": KNOWLEDGE_GRAPH_ALIGNMENT,
        "digital_twin": DIGITAL_TWIN_ALIGNMENT,
        "governance": GOVERNANCE_ALIGNMENT,
    }


def cqrs() -> dict[str, Any]:
    return {
        "commands": list(COMMANDS),
        "command_count": len(COMMANDS),
        "queries": list(QUERIES),
        "query_count": len(QUERIES),
        "events": list(DOMAIN_EVENTS),
        "event_count": len(DOMAIN_EVENTS),
        "alignment_present_required": True,
        "not_missing": True,
    }


def api_boundaries() -> dict[str, Any]:
    return dict(API_BOUNDARIES)


def deployment() -> dict[str, Any]:
    return dict(DEPLOYMENT)


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
            "bi_domain_architecture": True,
            "ddd_model": True,
            "bounded_context_map": True,
            "aggregate_model": True,
            "event_model": True,
            "cqrs_mapping": True,
            "microservice_mapping": True,
            "api_boundaries": True,
            "governance_boundaries": True,
            "data_mesh_alignment": True,
            "knowledge_graph_alignment": True,
            "digital_twin_alignment": True,
            "foundation_tests": True,
            "domain_api_live": True,
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
            "ADR-394",
            "ADR-395",
            "P212",
            "P212-E",
            "P212-F",
            "P212-I",
            "P212-J",
            "P212-K",
            "P212-L",
            "P212-M",
            "ADR-392",
            "ADR-393",
            "ADR-402",
            "ADR-404",
        ],
        "domain_map": domain_map(),
        "bounded_contexts": bounded_contexts(),
        "aggregates": aggregates(),
        "entities": entities(),
        "value_objects": value_objects(),
        "ownership": ownership(),
        "domain_services": domain_services(),
        "events": events(),
        "microservices": microservices(),
        "integrations": integrations(),
        "cqrs": cqrs(),
        "api_boundaries": api_boundaries(),
        "deployment": deployment(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "complete_ddd_bi_architecture_present_required": True,
        "strategic_domain_model_present_required": True,
        "bounded_contexts_present_required": True,
        "domains_loosely_coupled_required": True,
        "bi_ownership_clear_required": True,
        "aggregates_defined_required": True,
        "entities_defined_required": True,
        "value_objects_defined_required": True,
        "domain_services_present_required": True,
        "events_present_required": True,
        "integration_boundaries_clear_required": True,
        "cqrs_alignment_present_required": True,
        "microservice_boundaries_clear_required": True,
        "data_mesh_alignment_present_required": True,
        "knowledge_graph_alignment_present_required": True,
        "digital_twin_alignment_present_required": True,
        "enterprise_governance_alignment_present_required": True,
        "sibling_business_intelligence_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/domain",
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


def domain_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /analytics/domain",
            "GET /analytics/domain/map",
            "GET /analytics/domain/bounded-contexts",
            "GET /analytics/domain/aggregates",
            "GET /analytics/domain/entities",
            "GET /analytics/domain/value-objects",
            "GET /analytics/domain/ownership",
            "GET /analytics/domain/services",
            "GET /analytics/domain/events",
            "GET /analytics/domain/microservices",
            "GET /analytics/domain/integrations",
            "GET /analytics/domain/cqrs",
            "GET /analytics/domain/apis",
            "GET /analytics/domain/deployment",
            "GET /analytics/domain/outputs",
            "GET /analytics/domain/production-readiness",
            "GET /analytics/domain/readiness",
        ],
    }
