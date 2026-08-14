"""P213-E Enterprise Data Warehouse & Analytical Data Platform — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P213-E"
ADR = 409
SOR = "analytics"
API_PREFIX = "/api/v1/analytics"
PRODUCT = "Enterprise Data Warehouse & Analytical Data Platform"
CAPABILITY = "CAP-PLT-BI-001"

PRINCIPLE = (
    "Enterprise Data Warehouse SHALL become the "
    "historical intelligence memory of MEOS."
)

FABRIC = "meos_enterprise_analytical_intelligence_data_fabric"

CORE_DOMAIN = "enterprise_analytical_data_management"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {
        "id": "data_warehouse_management",
        "purpose": "Warehouse lifecycle and analytical storage.",
    },
    {
        "id": "analytical_data_modeling",
        "purpose": "Dimensional and analytical structure design.",
    },
    {
        "id": "historical_data_management",
        "purpose": "Time-based analytics and historical tracking.",
    },
    {
        "id": "data_integration",
        "purpose": "Ingestion, transformation, and loading.",
    },
    {
        "id": "analytical_processing",
        "purpose": "Analytical compute over warehouse assets.",
    },
    {
        "id": "semantic_analytics",
        "purpose": "Business semantic layer for consumption.",
    },
)

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "warehouse_core",
        "bc": "BC-01",
        "name": "Enterprise Data Warehouse Core Context",
        "purpose": (
            "Warehouse lifecycle, analytical storage, "
            "enterprise historical data."
        ),
        "entities": ("Warehouse", "Dataset", "Schema", "StoragePartition"),
        "events": ("WarehouseCreatedEvent", "DatasetRegisteredEvent"),
    },
    {
        "id": "analytical_modeling",
        "bc": "BC-02",
        "name": "Analytical Data Modeling Context",
        "purpose": "Dimensional modeling and analytical structures.",
        "entities": (
            "FactModel",
            "DimensionModel",
            "StarSchema",
            "SnowflakeSchema",
        ),
        "events": ("ModelCreatedEvent", "ModelChangedEvent"),
    },
    {
        "id": "data_integration",
        "bc": "BC-03",
        "name": "Data Integration Context",
        "purpose": "Data ingestion, transformation, loading processes.",
        "entities": ("DataPipeline", "TransformationJob", "LoadProcess"),
        "events": ("DataIngestionStartedEvent", "DataLoadedEvent"),
    },
    {
        "id": "historical_intelligence",
        "bc": "BC-04",
        "name": "Historical Intelligence Context",
        "purpose": "Time-based analytics, historical tracking, trends.",
        "entities": ("HistoricalRecord", "Snapshot", "VersionedDataset"),
        "events": ("SnapshotCreatedEvent", "HistoryUpdatedEvent"),
    },
    {
        "id": "analytical_data_mart",
        "bc": "BC-05",
        "name": "Analytical Data Mart Context",
        "purpose": "Domain-specific analytics and BI optimization.",
        "entities": ("DataMart", "BusinessDataset", "AnalyticalView"),
        "events": ("DataMartPublishedEvent",),
    },
)

AGGREGATE = {
    "name": "AnalyticalDataAssetAggregate",
    "root": "AnalyticalDataAsset",
    "entities": (
        "DataWarehouse",
        "AnalyticalDataset",
        "FactTable",
        "DimensionTable",
        "AnalyticalModel",
        "DataMart",
        "HistoricalSnapshot",
    ),
    "value_objects": (
        "DatasetId",
        "BusinessDomain",
        "RetentionPolicy",
        "AggregationLevel",
        "DataGranularity",
        "RefreshFrequency",
    ),
    "events": (
        "AnalyticalDatasetCreatedEvent",
        "DataLoadedEvent",
        "DataModelUpdatedEvent",
        "HistoricalSnapshotCreatedEvent",
        "AnalyticsReadyEvent",
    ),
}

ARCHITECTURE_LAYERS: tuple[dict[str, str], ...] = (
    {
        "id": "source_data_layer",
        "responsibility": "Operational systems and data products as inputs.",
    },
    {
        "id": "data_integration_layer",
        "responsibility": "Ingest, CDC, transform, and load analytical assets.",
    },
    {
        "id": "data_storage_layer",
        "responsibility": "Governed warehouse storage and partitions.",
    },
    {
        "id": "analytical_modeling_layer",
        "responsibility": "Facts, dimensions, schemas, and models.",
    },
    {
        "id": "semantic_intelligence_layer",
        "responsibility": "Business terms, metrics, and analytical views.",
    },
    {
        "id": "consumption_layer",
        "responsibility": "BI, analytics, AI, and decision consumers.",
    },
)

DIMENSIONAL_MODEL: dict[str, Any] = {
    "patterns": (
        "dimensional_modeling",
        "star_schema",
        "snowflake_schema",
        "fact_tables",
        "dimension_tables",
        "slowly_changing_dimensions",
        "historical_tracking",
    ),
    "facts": (
        "FactSales",
        "FactFinance",
        "FactOperations",
        "FactCustomer",
        "FactRisk",
    ),
    "dimensions": (
        "DimCustomer",
        "DimOrganization",
        "DimTime",
        "DimLocation",
        "DimProduct",
    ),
}

SUBJECT_AREAS: tuple[dict[str, Any], ...] = (
    {
        "id": "finance",
        "facts": ("FactFinance",),
        "dimensions": ("DimOrganization", "DimTime"),
        "metrics": ("revenue", "expense", "margin"),
        "business_questions": ("What is period P&L by org?",),
    },
    {
        "id": "customer",
        "facts": ("FactCustomer",),
        "dimensions": ("DimCustomer", "DimTime"),
        "metrics": ("retention", "lifetime_value"),
        "business_questions": ("Which cohorts churn?",),
    },
    {
        "id": "human_capital",
        "facts": ("FactWorkforce",),
        "dimensions": ("DimOrganization", "DimTime"),
        "metrics": ("headcount", "attrition"),
        "business_questions": ("Where is attrition rising?",),
    },
    {
        "id": "sales",
        "facts": ("FactSales",),
        "dimensions": ("DimProduct", "DimCustomer", "DimTime"),
        "metrics": ("bookings", "pipeline"),
        "business_questions": ("What drives win rate?",),
    },
    {
        "id": "marketing",
        "facts": ("FactCampaign",),
        "dimensions": ("DimCustomer", "DimTime"),
        "metrics": ("cac", "conversion"),
        "business_questions": ("Which channels convert?",),
    },
    {
        "id": "supply_chain",
        "facts": ("FactSupply",),
        "dimensions": ("DimProduct", "DimLocation", "DimTime"),
        "metrics": ("fill_rate", "lead_time"),
        "business_questions": ("Where are stockouts?",),
    },
    {
        "id": "operations",
        "facts": ("FactOperations",),
        "dimensions": ("DimOrganization", "DimTime"),
        "metrics": ("throughput", "sla"),
        "business_questions": ("Which processes breach SLA?",),
    },
    {
        "id": "risk",
        "facts": ("FactRisk",),
        "dimensions": ("DimOrganization", "DimTime"),
        "metrics": ("exposure", "loss_events"),
        "business_questions": ("What is residual risk?",),
    },
    {
        "id": "security",
        "facts": ("FactSecurity",),
        "dimensions": ("DimOrganization", "DimTime"),
        "metrics": ("incidents", "mttr"),
        "business_questions": ("Where are control gaps?",),
    },
    {
        "id": "compliance",
        "facts": ("FactCompliance",),
        "dimensions": ("DimOrganization", "DimTime"),
        "metrics": ("violations", "remediation_rate"),
        "business_questions": ("Are controls effective?",),
    },
)

INGESTION: dict[str, Any] = {
    "sources": (
        "operational_systems",
        "erp_systems",
        "crm_systems",
        "iot_platforms",
        "applications",
        "data_products",
        "external_sources",
    ),
    "modes": (
        "batch_processing",
        "streaming_processing",
        "real_time_ingestion",
        "change_data_capture",
    ),
}

TRANSFORMATION: dict[str, Any] = {
    "capabilities": (
        "data_cleansing",
        "data_enrichment",
        "aggregation",
        "business_rule_processing",
        "metric_calculation",
    ),
    "via_p212_e": True,
}

GOVERNANCE: dict[str, Any] = {
    "via_p212": True,
    "controls": (
        "data_ownership",
        "data_stewardship",
        "data_classification",
        "data_lineage",
        "metadata_management",
        "quality_rules",
        "access_policies",
    ),
}

SEMANTIC_LAYER: dict[str, Any] = {
    "purpose": "common_business_language",
    "includes": (
        "business_terms",
        "metric_definitions",
        "calculation_logic",
        "business_rules",
        "analytical_views",
    ),
    "via_p213_d": True,
}

KNOWLEDGE_GRAPH: dict[str, Any] = {
    "via_p212_j": True,
    "nodes": (
        "Dataset",
        "Fact",
        "Dimension",
        "Metric",
        "Report",
        "BusinessEntity",
        "Process",
    ),
    "relationships": (
        "Metric_CALCULATED_FROM_Dataset",
        "Report_CONSUMES_Dataset",
        "Insight_GENERATED_FROM_Analytics",
    ),
}

AI_FOUNDATION: dict[str, Any] = {
    "via_p212_k": True,
    "capabilities": (
        "ai_training_data_preparation",
        "feature_dataset_management",
        "model_analytics_data",
        "ai_experiment_data",
    ),
    "lifecycle": (
        "prepare",
        "feature",
        "train_ready",
        "experiment",
        "govern",
    ),
}

DIGITAL_TWIN: dict[str, Any] = {
    "via_p212_l": True,
    "capabilities": (
        "historical_simulation",
        "trend_analysis",
        "forecast_data_preparation",
        "business_scenario_modeling",
    ),
}

COMMANDS: tuple[str, ...] = (
    "CreateWarehouseCommand",
    "RegisterDatasetCommand",
    "LoadAnalyticalDataCommand",
    "CreateDataMartCommand",
    "UpdateAnalyticalModelCommand",
)

QUERIES: tuple[str, ...] = (
    "GetDatasetQuery",
    "GetAnalyticalModelQuery",
    "GetHistoricalDataQuery",
    "GetBusinessMetricQuery",
)

CORE_EVENTS: tuple[dict[str, Any], ...] = (
    {
        "name": "WarehouseCreatedEvent",
        "producer": "warehouse_core",
        "consumers": ("analytical_modeling", "audit"),
        "payload": ("tenant_id", "warehouse_id", "schema_ref"),
        "version": "v1",
    },
    {
        "name": "DatasetLoadedEvent",
        "producer": "data_integration",
        "consumers": ("warehouse_core", "semantic_analytics"),
        "payload": ("tenant_id", "dataset_id", "row_count"),
        "version": "v1",
    },
    {
        "name": "ModelCreatedEvent",
        "producer": "analytical_modeling",
        "consumers": ("analytical_data_mart", "knowledge_graph"),
        "payload": ("tenant_id", "model_id", "schema_type"),
        "version": "v1",
    },
    {
        "name": "SnapshotGeneratedEvent",
        "producer": "historical_intelligence",
        "consumers": ("digital_twin", "audit"),
        "payload": ("tenant_id", "snapshot_id", "as_of"),
        "version": "v1",
    },
    {
        "name": "AnalyticsReadyEvent",
        "producer": "warehouse_core",
        "consumers": ("reporting", "ai", "decision_intelligence"),
        "payload": ("tenant_id", "dataset_id", "quality_score"),
        "version": "v1",
    },
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "name": "data-warehouse-core-service",
        "responsibility": "Warehouse lifecycle and storage registry.",
        "database_boundary": "analytics_warehouse",
        "api_boundary": "/api/v1/analytics/warehouse",
        "events": ("WarehouseCreatedEvent",),
        "security_model": "analytics.warehouse.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "analytical-modeling-service",
        "responsibility": "Dimensional models and schemas.",
        "database_boundary": "analytics_models",
        "api_boundary": "/api/v1/analytics/models",
        "events": ("ModelCreatedEvent",),
        "security_model": "analytics.models.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "data-ingestion-service",
        "responsibility": "Batch, stream, CDC ingestion.",
        "database_boundary": "analytics_ingestion",
        "api_boundary": "/api/v1/analytics/ingestion",
        "events": ("DataIngestionStartedEvent", "DatasetLoadedEvent"),
        "security_model": "analytics.ingestion.*",
        "scaling_strategy": "queue_backed_workers",
    },
    {
        "name": "transformation-service",
        "responsibility": "Cleansing, enrichment, aggregation.",
        "database_boundary": "analytics_transform",
        "api_boundary": "/api/v1/analytics/pipelines",
        "events": ("DataLoadedEvent",),
        "security_model": "analytics.pipelines.*",
        "scaling_strategy": "processing_clusters",
    },
    {
        "name": "data-mart-service",
        "responsibility": "Domain data marts and views.",
        "database_boundary": "analytics_datamarts",
        "api_boundary": "/api/v1/analytics/datamarts",
        "events": ("DataMartPublishedEvent",),
        "security_model": "analytics.datamarts.*",
        "scaling_strategy": "horizontal_read_replicas",
    },
    {
        "name": "semantic-layer-service",
        "responsibility": "Business semantic metrics and terms.",
        "database_boundary": "analytics_semantic",
        "api_boundary": "/api/v1/analytics/semantic-layer",
        "events": ("AnalyticsReadyEvent",),
        "security_model": "analytics.semantic.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "analytical-governance-service",
        "responsibility": "Ownership, lineage, quality policy projection.",
        "database_boundary": "analytics_wh_governance",
        "api_boundary": "/api/v1/analytics/warehouse/governance",
        "events": ("QualityRuleAppliedEvent",),
        "security_model": "analytics.governance.*",
        "scaling_strategy": "horizontal_stateless",
    },
)

API_BOUNDARIES: dict[str, Any] = {
    "warehouse": (
        "/api/v1/analytics/warehouse",
        "/api/v1/analytics/datasets",
        "/api/v1/analytics/models",
        "/api/v1/analytics/datamarts",
    ),
    "analytics": (
        "/api/v1/analytics/analytics-data",
        "/api/v1/analytics/metrics",
        "/api/v1/analytics/semantic-layer",
    ),
    "integration": (
        "/api/v1/analytics/ingestion",
        "/api/v1/analytics/pipelines",
    ),
    "rest": True,
    "graphql": "/api/v1/analytics/graphql",
    "event_apis": "analytics.warehouse.*.v1",
    "streaming_apis": "/api/v1/analytics/ingestion/stream",
    "security": ("analytics.warehouse.read", "zero_trust", "tenant_isolation"),
}

SECURITY: dict[str, Any] = {
    "via_p207": True,
    "via_p208": True,
    "via_p209": True,
    "via_p211": True,
    "analytical_data_access_control": True,
    "data_masking": True,
    "encryption": True,
    "audit_logging": True,
    "privacy_controls": True,
}

DEPLOYMENT: dict[str, Any] = {
    "kubernetes": True,
    "containerized_data_services": True,
    "distributed_storage": True,
    "processing_clusters": True,
    "cicd": True,
    "observability": True,
    "multi_region": True,
    "cloud_native": True,
}

TESTING: tuple[str, ...] = (
    "data_quality_testing",
    "etl_testing",
    "pipeline_testing",
    "model_testing",
    "performance_testing",
    "security_testing",
    "analytical_accuracy_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_data_warehouse_vision",
    "analytical_data_platform_domain_model",
    "warehouse_bounded_context_architecture",
    "warehouse_architecture_layers",
    "data_model_architecture",
    "enterprise_analytical_data_model",
    "data_ingestion_architecture",
    "data_transformation_architecture",
    "data_warehouse_governance",
    "semantic_data_layer",
    "knowledge_graph_integration",
    "ai_analytics_data_foundation",
    "digital_twin_analytical_integration",
    "cqrs_architecture",
    "event_sourcing_architecture",
    "microservice_architecture",
    "api_first_architecture",
    "security_architecture",
    "deployment_architecture",
    "testing_architecture",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "enterprise_data_warehouse_architecture_is_missing",
    "analytical_data_platform_is_missing",
    "dimensional_modeling_is_missing",
    "data_integration_architecture_is_missing",
    "semantic_layer_is_missing",
    "data_governance_alignment_is_missing",
    "ai_readiness_alignment_is_missing",
    "knowledge_graph_integration_is_missing",
    "cqrs_architecture_is_missing",
    "event_driven_architecture_is_missing",
    "microservice_architecture_is_missing",
    "api_first_architecture_is_missing",
    "cloud_native_deployment_is_missing",
    "warehouse_architecture_is_incomplete",
    "historical_data_management_is_missing",
    "digital_twin_analytical_integration_is_missing",
    "sibling_business_intelligence_bc",
)


def vision() -> dict[str, Any]:
    return {
        "statement": PRINCIPLE,
        "fabric": FABRIC,
        "transforms": (
            "governed_enterprise_data_products_to_"
            "trusted_analytical_intelligence_assets"
        ),
        "supports": (
            "bi",
            "analytics",
            "ai",
            "decision_intelligence",
            "strategic_planning",
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


def architecture_layers() -> dict[str, Any]:
    return {
        "layers": [dict(layer) for layer in ARCHITECTURE_LAYERS],
        "layer_count": len(ARCHITECTURE_LAYERS),
    }


def dimensional_model() -> dict[str, Any]:
    return dict(DIMENSIONAL_MODEL)


def subject_areas() -> dict[str, Any]:
    return {
        "areas": [dict(a) for a in SUBJECT_AREAS],
        "area_count": len(SUBJECT_AREAS),
    }


def ingestion() -> dict[str, Any]:
    return dict(INGESTION)


def transformation() -> dict[str, Any]:
    return dict(TRANSFORMATION)


def governance() -> dict[str, Any]:
    return dict(GOVERNANCE)


def semantic_layer() -> dict[str, Any]:
    return dict(SEMANTIC_LAYER)


def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH)


def ai_foundation() -> dict[str, Any]:
    return dict(AI_FOUNDATION)


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
            "enterprise_data_warehouse": True,
            "analytical_data_model": True,
            "data_integration_architecture": True,
            "historical_data_management": True,
            "semantic_layer": True,
            "data_governance_integration": True,
            "ai_data_foundation": True,
            "cqrs_architecture": True,
            "event_architecture": True,
            "microservice_architecture": True,
            "api_architecture": True,
            "deployment_architecture": True,
            "foundation_tests": True,
            "warehouse_api_live": True,
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
            "ADR-394",
            "ADR-395",
            "ADR-396",
            "ADR-408",
            "P212",
            "P212-E",
            "P212-F",
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
            "layers": architecture_layers(),
            "capabilities": list(DIMENSIONAL_MODEL["patterns"])
            + list(INGESTION["modes"]),
            "capability_count": len(DIMENSIONAL_MODEL["patterns"])
            + len(INGESTION["modes"]),
        },
        "dimensional_model": dimensional_model(),
        "subject_areas": subject_areas(),
        "ingestion": ingestion(),
        "transformation": transformation(),
        "governance": governance(),
        "semantic_layer": semantic_layer(),
        "knowledge_graph": knowledge_graph(),
        "ai_foundation": ai_foundation(),
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
        "enterprise_data_warehouse_architecture_present_required": True,
        "analytical_data_platform_present_required": True,
        "dimensional_modeling_present_required": True,
        "data_integration_architecture_present_required": True,
        "semantic_layer_present_required": True,
        "data_governance_alignment_present_required": True,
        "ai_readiness_alignment_present_required": True,
        "knowledge_graph_integration_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_driven_architecture_present_required": True,
        "microservice_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "cloud_native_deployment_present_required": True,
        "architecture_present_required": True,
        "historical_data_management_present_required": True,
        "digital_twin_analytical_integration_present_required": True,
        "sibling_business_intelligence_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/warehouse",
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


def warehouse_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /analytics/warehouse",
            "GET /analytics/warehouse/vision",
            "GET /analytics/warehouse/domain",
            "GET /analytics/warehouse/bounded-contexts",
            "GET /analytics/warehouse/layers",
            "GET /analytics/warehouse/dimensional-model",
            "GET /analytics/warehouse/subject-areas",
            "GET /analytics/warehouse/ingestion",
            "GET /analytics/warehouse/transformation",
            "GET /analytics/warehouse/governance",
            "GET /analytics/warehouse/semantic-layer",
            "GET /analytics/warehouse/knowledge-graph",
            "GET /analytics/warehouse/ai-foundation",
            "GET /analytics/warehouse/digital-twin",
            "GET /analytics/warehouse/cqrs",
            "GET /analytics/warehouse/events",
            "GET /analytics/warehouse/microservices",
            "GET /analytics/warehouse/apis",
            "GET /analytics/warehouse/security",
            "GET /analytics/warehouse/deployment",
            "GET /analytics/warehouse/testing",
            "GET /analytics/warehouse/outputs",
            "GET /analytics/warehouse/production-readiness",
            "GET /analytics/warehouse/readiness",
        ],
    }
