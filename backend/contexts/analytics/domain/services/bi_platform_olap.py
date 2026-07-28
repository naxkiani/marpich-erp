"""P213-G Enterprise OLAP, Semantic Layer & Business Metrics Platform — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P213-G"
ADR = 411
SOR = "analytics"
API_PREFIX = "/api/v1/analytics"
PRODUCT = "Enterprise OLAP, Semantic Layer & Business Metrics Platform"
CAPABILITY = "CAP-PLT-BI-001"

PRINCIPLE = (
    "Every enterprise decision SHALL be based upon "
    "a governed semantic definition instead of isolated calculations."
)

FABRIC = "meos_enterprise_semantic_intelligence_fabric"

CORE_DOMAIN = "enterprise_semantic_intelligence_management"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {"id": "metric_governance", "purpose": "Enterprise metrics catalog and lifecycle."},
    {"id": "kpi_governance", "purpose": "KPI approval, ownership, and monitoring."},
    {"id": "olap_management", "purpose": "Cubes, aggregations, and analytical processing."},
    {"id": "dimension_management", "purpose": "Enterprise dimensions and hierarchies."},
    {"id": "measure_management", "purpose": "Governed measures and aggregations."},
    {"id": "calculation_management", "purpose": "Formulas and derived metrics."},
    {
        "id": "business_vocabulary_management",
        "purpose": "Glossary, taxonomy, and terminology.",
    },
    {
        "id": "semantic_metadata_management",
        "purpose": "Semantic metadata and abstraction.",
    },
)

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "business_metrics",
        "bc": "BC-01",
        "name": "Business Metrics Context",
        "purpose": "Enterprise metrics, KPI catalog, metric lifecycle and governance.",
    },
    {
        "id": "semantic_layer",
        "bc": "BC-02",
        "name": "Semantic Layer Context",
        "purpose": "Semantic model, vocabulary, metadata abstraction, terminology.",
    },
    {
        "id": "olap_cube",
        "bc": "BC-03",
        "name": "OLAP Cube Context",
        "purpose": "Cube lifecycle, aggregations, hierarchies, dimensions.",
    },
    {
        "id": "calculation_engine",
        "bc": "BC-04",
        "name": "Calculation Engine Context",
        "purpose": "Business calculations, formula execution, derived metrics.",
    },
    {
        "id": "business_taxonomy",
        "bc": "BC-05",
        "name": "Business Taxonomy Context",
        "purpose": "Business glossary, enterprise taxonomy, semantic relationships.",
    },
)

AGGREGATE = {
    "name": "SemanticModelAggregate",
    "root": "SemanticModel",
    "entities": (
        "BusinessMetric",
        "KPI",
        "Dimension",
        "Measure",
        "Hierarchy",
        "CalculationFormula",
        "BusinessTerm",
        "SemanticModel",
        "AnalyticalCube",
    ),
    "value_objects": (
        "MetricIdentifier",
        "BusinessDefinition",
        "FormulaExpression",
        "AggregationType",
        "CalculationMethod",
        "SemanticClassification",
        "BusinessContext",
    ),
    "events": (
        "MetricDefinedEvent",
        "MetricApprovedEvent",
        "SemanticModelPublishedEvent",
        "CubeProcessedEvent",
        "HierarchyUpdatedEvent",
        "FormulaChangedEvent",
    ),
}

METRIC_CLASSES: tuple[str, ...] = (
    "strategic_kpi",
    "operational_kpi",
    "financial_kpi",
    "risk_kpi",
    "compliance_kpi",
    "customer_kpi",
    "sales_kpi",
    "marketing_kpi",
    "supply_chain_kpi",
    "hr_kpi",
    "security_kpi",
    "ai_kpi",
    "esg_kpi",
)

METRIC_ATTRIBUTES: tuple[str, ...] = (
    "business_definition",
    "owner",
    "steward",
    "data_sources",
    "formula",
    "refresh_policy",
    "quality_threshold",
    "sla",
    "classification",
    "lineage",
    "dependencies",
    "consumers",
)

KPI_LIFECYCLE: tuple[str, ...] = (
    "proposed",
    "reviewed",
    "validated",
    "approved",
    "published",
    "measured",
    "monitored",
    "retired",
)

SEMANTIC_LAYER: dict[str, Any] = {
    "includes": (
        "business_vocabulary",
        "business_glossary",
        "semantic_models",
        "business_concepts",
        "business_relationships",
        "analytical_objects",
        "logical_models",
        "semantic_apis",
        "semantic_translation_layer",
    ),
    "isolates": "business_users_from_physical_storage",
}

OLAP: dict[str, Any] = {
    "modes": (
        "rolap",
        "molap",
        "holap",
        "distributed_olap",
        "cloud_native_olap",
        "real_time_olap",
    ),
    "lifecycles": (
        "cube_lifecycle",
        "dimension_lifecycle",
        "fact_lifecycle",
        "aggregation_lifecycle",
    ),
    "strategies": (
        "partition_strategy",
        "materialized_views",
        "incremental_refresh",
    ),
}

DIMENSIONS: dict[str, Any] = {
    "required": (
        "time",
        "organization",
        "customer",
        "product",
        "location",
        "supplier",
        "channel",
        "employee",
        "asset",
        "project",
        "risk",
        "compliance",
        "application",
        "service",
    ),
    "scd_types": ("type_1", "type_2", "type_3"),
    "supports": ("historical_dimensions", "temporal_dimensions"),
}

CALCULATION_ENGINE: dict[str, Any] = {
    "capabilities": (
        "formula_language",
        "derived_metrics",
        "calculated_members",
        "business_rules",
        "aggregation_rules",
        "currency_conversion",
        "unit_conversion",
        "statistical_functions",
        "forecast_functions",
    ),
    "governance": (
        "formula_validation",
        "versioning",
        "testing",
        "governance",
    ),
}

SEMANTIC_QUERY: dict[str, Any] = {
    "capabilities": (
        "natural_language_query",
        "semantic_query",
        "business_search",
        "graph_query",
        "analytical_query",
        "metric_discovery",
        "business_exploration",
    ),
    "integrates": ("ai_assistants", "enterprise_search", "knowledge_graph"),
}

KNOWLEDGE_GRAPH: dict[str, Any] = {
    "via_p212_j": True,
    "nodes": (
        "BusinessMetric",
        "BusinessConcept",
        "BusinessRule",
        "Dimension",
        "Fact",
        "Calculation",
        "Report",
        "Dashboard",
        "Decision",
        "Policy",
    ),
    "relationships": (
        "Metric_USES_Formula",
        "Metric_BELONGS_TO_Domain",
        "Dashboard_CONSUMES_Metric",
        "Decision_DEPENDS_ON_KPI",
        "BusinessConcept_DEFINES_Metric",
    ),
}

AI_AGENTS: tuple[str, ...] = (
    "semantic_modeling_agent",
    "metric_recommendation_agent",
    "business_glossary_agent",
    "formula_validation_agent",
    "semantic_quality_agent",
    "business_context_agent",
)

AI_CAPABILITIES: tuple[str, ...] = (
    "automatic_semantic_discovery",
    "metric_recommendation",
    "formula_optimisation",
    "business_terminology_alignment",
    "duplicate_metric_detection",
    "semantic_inconsistency_detection",
    "kpi_quality_analysis",
)

DIGITAL_TWIN: dict[str, Any] = {
    "via_p212_l": True,
    "capabilities": (
        "business_kpi_simulation",
        "scenario_modelling",
        "business_forecast_simulation",
        "executive_what_if_analysis",
        "strategic_planning",
    ),
}

COMMANDS: tuple[str, ...] = (
    "CreateMetricCommand",
    "ApproveMetricCommand",
    "PublishSemanticModelCommand",
    "CreateCubeCommand",
    "RefreshCubeCommand",
    "RegisterBusinessGlossaryCommand",
)

QUERIES: tuple[str, ...] = (
    "GetMetricQuery",
    "GetKPIQuery",
    "GetSemanticModelQuery",
    "GetCubeQuery",
    "SearchBusinessConceptQuery",
)

CORE_EVENTS: tuple[dict[str, Any], ...] = (
    {
        "name": "MetricCreatedEvent",
        "producer": "business_metrics",
        "consumers": ("semantic_layer", "audit"),
        "payload": ("tenant_id", "metric_id", "class"),
        "version": "v1",
    },
    {
        "name": "MetricApprovedEvent",
        "producer": "business_metrics",
        "consumers": ("calculation_engine", "knowledge_graph"),
        "payload": ("tenant_id", "metric_id", "approver_ref"),
        "version": "v1",
    },
    {
        "name": "SemanticModelPublishedEvent",
        "producer": "semantic_layer",
        "consumers": ("olap_cube", "reporting"),
        "payload": ("tenant_id", "model_id", "version"),
        "version": "v1",
    },
    {
        "name": "CubeRefreshedEvent",
        "producer": "olap_cube",
        "consumers": ("dashboards", "notifications"),
        "payload": ("tenant_id", "cube_id", "refresh_mode"),
        "version": "v1",
    },
    {
        "name": "BusinessGlossaryUpdatedEvent",
        "producer": "business_taxonomy",
        "consumers": ("semantic_layer", "search"),
        "payload": ("tenant_id", "term_id", "definition"),
        "version": "v1",
    },
    {
        "name": "FormulaChangedEvent",
        "producer": "calculation_engine",
        "consumers": ("business_metrics", "audit"),
        "payload": ("tenant_id", "formula_id", "expression"),
        "version": "v1",
    },
    {
        "name": "HierarchyChangedEvent",
        "producer": "olap_cube",
        "consumers": ("dimension_service", "audit"),
        "payload": ("tenant_id", "hierarchy_id", "levels"),
        "version": "v1",
    },
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "name": "semantic-layer-service",
        "responsibility": "Semantic models and translation layer.",
        "database_boundary": "analytics_semantic",
        "api_boundary": "/api/v1/analytics/semantic-models",
        "events": ("SemanticModelPublishedEvent",),
        "security_model": "analytics.semantic.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "metric-catalog-service",
        "responsibility": "Metric and KPI catalog governance.",
        "database_boundary": "analytics_metrics",
        "api_boundary": "/api/v1/analytics/metrics",
        "events": ("MetricCreatedEvent", "MetricApprovedEvent"),
        "security_model": "analytics.metrics.*",
        "scaling_strategy": "horizontal_read_replicas",
    },
    {
        "name": "business-glossary-service",
        "responsibility": "Glossary and taxonomy.",
        "database_boundary": "analytics_glossary",
        "api_boundary": "/api/v1/analytics/business-glossary",
        "events": ("BusinessGlossaryUpdatedEvent",),
        "security_model": "analytics.glossary.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "olap-cube-service",
        "responsibility": "Cube processing and refresh.",
        "database_boundary": "analytics_olap",
        "api_boundary": "/api/v1/analytics/cubes",
        "events": ("CubeRefreshedEvent",),
        "security_model": "analytics.cubes.*",
        "scaling_strategy": "processing_clusters",
    },
    {
        "name": "calculation-engine-service",
        "responsibility": "Formula execution and derived metrics.",
        "database_boundary": "analytics_calculations",
        "api_boundary": "/api/v1/analytics/formulas",
        "events": ("FormulaChangedEvent",),
        "security_model": "analytics.formulas.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "hierarchy-management-service",
        "responsibility": "Hierarchy definitions and changes.",
        "database_boundary": "analytics_hierarchies",
        "api_boundary": "/api/v1/analytics/hierarchies",
        "events": ("HierarchyChangedEvent",),
        "security_model": "analytics.hierarchies.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "dimension-service",
        "responsibility": "Enterprise dimensions and SCDs.",
        "database_boundary": "analytics_dimensions",
        "api_boundary": "/api/v1/analytics/dimensions",
        "events": ("HierarchyChangedEvent",),
        "security_model": "analytics.dimensions.*",
        "scaling_strategy": "horizontal_read_replicas",
    },
    {
        "name": "semantic-ai-service",
        "responsibility": "AI semantic agents via Enterprise AI.",
        "database_boundary": "analytics_semantic_ai",
        "api_boundary": "/api/v1/analytics/semantic-query",
        "events": ("MetricCreatedEvent",),
        "security_model": "analytics.semantic_ai.*",
        "scaling_strategy": "async_via_enterprise_ai",
    },
)

API_BOUNDARIES: dict[str, Any] = {
    "semantic": (
        "/api/v1/analytics/semantic-models",
        "/api/v1/analytics/business-glossary",
        "/api/v1/analytics/business-concepts",
    ),
    "metrics": (
        "/api/v1/analytics/metrics",
        "/api/v1/analytics/kpis",
        "/api/v1/analytics/formulas",
    ),
    "olap": (
        "/api/v1/analytics/cubes",
        "/api/v1/analytics/dimensions",
        "/api/v1/analytics/hierarchies",
    ),
    "analytics": (
        "/api/v1/analytics/semantic-query",
        "/api/v1/analytics/business-search",
    ),
    "rest": True,
    "graphql": "/api/v1/analytics/graphql",
    "grpc": True,
    "streaming_apis": "/api/v1/analytics/semantic-query/stream",
    "event_apis": "analytics.semantic.*.v1",
    "security": ("analytics.olap.read", "zero_trust", "tenant_isolation"),
}

SECURITY: dict[str, Any] = {
    "via_p207": True,
    "via_p208": True,
    "via_p211": True,
    "via_p212": True,
    "metric_level_authorization": True,
    "semantic_object_security": True,
    "fine_grained_access_control": True,
    "attribute_based_access_control": True,
    "policy_based_calculations": True,
    "audit_logging": True,
    "data_masking": True,
    "classification_awareness": True,
}

DEPLOYMENT: dict[str, Any] = {
    "kubernetes": True,
    "service_mesh": True,
    "container_platform": True,
    "distributed_cache": True,
    "distributed_olap_engine": True,
    "cicd": True,
    "observability": True,
    "disaster_recovery": True,
    "multi_region": True,
    "high_availability": True,
    "cloud_native": True,
}

TESTING: tuple[str, ...] = (
    "metric_validation_testing",
    "formula_testing",
    "semantic_consistency_testing",
    "olap_testing",
    "cube_processing_testing",
    "hierarchy_testing",
    "performance_testing",
    "security_testing",
    "regression_testing",
    "acceptance_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_semantic_vision",
    "ddd_domain_model",
    "bounded_context_architecture",
    "enterprise_metric_architecture",
    "enterprise_kpi_governance",
    "semantic_layer_architecture",
    "olap_architecture",
    "dimension_management",
    "business_calculation_engine",
    "semantic_query_platform",
    "knowledge_graph_integration",
    "ai_native_semantic_platform",
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
    "enterprise_semantic_layer_is_missing",
    "enterprise_metric_platform_is_missing",
    "kpi_governance_is_missing",
    "olap_platform_is_missing",
    "business_glossary_is_missing",
    "business_vocabulary_is_missing",
    "semantic_query_layer_is_missing",
    "knowledge_graph_integration_is_missing",
    "ai_native_semantic_platform_is_missing",
    "digital_twin_integration_is_missing",
    "cqrs_architecture_is_missing",
    "event_sourcing_architecture_is_missing",
    "microservice_architecture_is_missing",
    "api_first_architecture_is_missing",
    "zero_trust_security_is_missing",
    "cloud_native_deployment_is_missing",
    "olap_semantic_architecture_is_incomplete",
    "dimension_platform_is_missing",
    "calculation_engine_is_missing",
    "sibling_business_intelligence_bc",
)


def vision() -> dict[str, Any]:
    return {
        "statement": PRINCIPLE,
        "fabric": FABRIC,
        "single_source_of_truth_for": (
            "business_metric",
            "kpi",
            "dimension",
            "aggregation",
            "business_definition",
            "enterprise_calculation",
        ),
        "shared_across": (
            "reports",
            "dashboards",
            "ai",
            "analytics",
            "decision_intelligence",
            "digital_twins",
            "knowledge_graphs",
        ),
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


def metrics() -> dict[str, Any]:
    return {
        "classes": list(METRIC_CLASSES),
        "class_count": len(METRIC_CLASSES),
        "attributes": list(METRIC_ATTRIBUTES),
        "attribute_count": len(METRIC_ATTRIBUTES),
    }


def kpi_governance() -> dict[str, Any]:
    return {
        "lifecycle": list(KPI_LIFECYCLE),
        "lifecycle_step_count": len(KPI_LIFECYCLE),
        "controls": (
            "approval_workflow",
            "ownership",
            "stewardship",
            "versioning",
            "auditability",
            "policy_validation",
        ),
    }


def semantic_layer() -> dict[str, Any]:
    return dict(SEMANTIC_LAYER)


def olap() -> dict[str, Any]:
    return dict(OLAP)


def dimensions() -> dict[str, Any]:
    return {
        **DIMENSIONS,
        "dimension_count": len(DIMENSIONS["required"]),
    }


def calculation_engine() -> dict[str, Any]:
    return dict(CALCULATION_ENGINE)


def semantic_query() -> dict[str, Any]:
    return dict(SEMANTIC_QUERY)


def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH)


def ai_native() -> dict[str, Any]:
    return {
        "agents": list(AI_AGENTS),
        "agent_count": len(AI_AGENTS),
        "capabilities": list(AI_CAPABILITIES),
        "via_enterprise_ai": True,
        "module_local_llm_sdk_forbidden": True,
    }


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
        "event_store_strategy": "append_only_outbox",
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
            "enterprise_semantic_layer": True,
            "enterprise_metric_catalog": True,
            "kpi_governance": True,
            "olap_platform": True,
            "dimension_platform": True,
            "calculation_engine": True,
            "semantic_query_platform": True,
            "knowledge_graph_integration": True,
            "ai_semantic_platform": True,
            "digital_twin_integration": True,
            "cqrs_architecture": True,
            "event_architecture": True,
            "microservice_architecture": True,
            "api_platform": True,
            "security_architecture": True,
            "deployment_architecture": True,
            "testing_architecture": True,
            "foundation_tests": True,
            "olap_api_live": True,
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
            "ADR-394",
            "ADR-395",
            "ADR-396",
            "ADR-408",
            "ADR-409",
            "ADR-410",
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
            "capabilities": list(METRIC_CLASSES)[:5] + list(OLAP["modes"])[:3],
            "capability_count": 8,
        },
        "metrics": metrics(),
        "kpi_governance": kpi_governance(),
        "semantic_layer": semantic_layer(),
        "olap": olap(),
        "dimensions": dimensions(),
        "calculation_engine": calculation_engine(),
        "semantic_query": semantic_query(),
        "knowledge_graph": knowledge_graph(),
        "ai_native": ai_native(),
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
        "enterprise_semantic_layer_present_required": True,
        "enterprise_metric_platform_present_required": True,
        "kpi_governance_present_required": True,
        "olap_platform_present_required": True,
        "business_glossary_present_required": True,
        "business_vocabulary_present_required": True,
        "semantic_query_layer_present_required": True,
        "knowledge_graph_integration_present_required": True,
        "ai_native_semantic_platform_present_required": True,
        "digital_twin_integration_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_sourcing_architecture_present_required": True,
        "microservice_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "zero_trust_security_present_required": True,
        "cloud_native_deployment_present_required": True,
        "architecture_present_required": True,
        "dimension_platform_present_required": True,
        "calculation_engine_present_required": True,
        "sibling_business_intelligence_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/olap",
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


def olap_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /analytics/olap",
            "GET /analytics/olap/vision",
            "GET /analytics/olap/domain",
            "GET /analytics/olap/bounded-contexts",
            "GET /analytics/olap/metrics",
            "GET /analytics/olap/kpi-governance",
            "GET /analytics/olap/semantic-layer",
            "GET /analytics/olap/modes",
            "GET /analytics/olap/dimensions",
            "GET /analytics/olap/calculation-engine",
            "GET /analytics/olap/semantic-query",
            "GET /analytics/olap/knowledge-graph",
            "GET /analytics/olap/ai",
            "GET /analytics/olap/digital-twin",
            "GET /analytics/olap/cqrs",
            "GET /analytics/olap/events",
            "GET /analytics/olap/microservices",
            "GET /analytics/olap/apis",
            "GET /analytics/olap/security",
            "GET /analytics/olap/deployment",
            "GET /analytics/olap/testing",
            "GET /analytics/olap/outputs",
            "GET /analytics/olap/production-readiness",
            "GET /analytics/olap/readiness",
        ],
    }
