"""P211-K Enterprise Data Lineage, Metadata & Intelligence Graph — catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P211-K"
ADR = 386
SOR = "data_security"
API_PREFIX = "/api/v1/data-security"
PRODUCT = (
    "Enterprise Data Security & Privacy Intelligence Platform — "
    "Data Lineage, Metadata & Intelligence Graph"
)
CAPABILITY = "CAP-PLT-DS-001"

MISSION_STATEMENT = (
    "Create an enterprise intelligence platform capable of building complete "
    "data lineage, managing active metadata, creating enterprise knowledge "
    "graphs, understanding data relationships, performing impact analysis, "
    "supporting compliance evidence, enabling AI reasoning over enterprise "
    "data, and providing complete data transparency."
)

VISION_STATEMENT = (
    "Create a Living Enterprise Data Intelligence Graph where every data "
    "asset is connected, every transformation is explainable, every "
    "dependency is visible, every policy relationship is understood, every "
    "risk can be traced, and every AI decision can explain data origin."
)

ARCHITECTURE_FLOW: tuple[str, ...] = (
    "enterprise_data_sources",
    "p211_d_data_discovery",
    "metadata_collection_layer",
    "lineage_extraction_engine",
    "semantic_intelligence_engine",
    "enterprise_knowledge_graph",
    "ai_reasoning_layer",
    "governance_security_intelligence",
)

BOUNDED_CONTEXTS: tuple[str, ...] = (
    "metadata_management",
    "data_lineage",
    "relationship_intelligence",
    "semantic_knowledge",
    "impact_analysis",
    "data_observability",
    "ai_data_reasoning",
)

CORE_ENTITIES: tuple[str, ...] = (
    "DataAsset",
    "MetadataEntity",
    "LineageNode",
    "LineageRelationship",
    "TransformationLogic",
)

METADATA_TYPES: tuple[str, ...] = (
    "technical_metadata",
    "business_metadata",
    "operational_metadata",
    "security_metadata",
)

LINEAGE_KINDS: tuple[str, ...] = (
    "technical_lineage",
    "column_level_lineage",
    "business_lineage",
    "ai_lineage",
)

LINEAGE_RELATIONSHIPS: tuple[str, ...] = (
    "created_from",
    "transformed_by",
    "consumed_by",
    "derived_from",
    "protected_by",
)

KG_NODES: tuple[str, ...] = (
    "data_asset",
    "identity",
    "application",
    "process",
    "policy",
    "classification",
    "risk",
    "compliance_control",
    "ai_model",
    "business_term",
)

KG_RELATIONSHIPS: tuple[str, ...] = (
    "owned_by",
    "uses",
    "transforms",
    "protected_by",
    "accessed_by",
    "governed_by",
    "derived_from",
)

AI_CAPS: tuple[str, ...] = (
    "semantic_understanding",
    "relationship_discovery",
    "pattern_recognition",
    "data_meaning_extraction",
    "anomaly_detection",
    "data_dependency_prediction",
)

AI_AGENTS: tuple[str, ...] = (
    "data_discovery_agent",
    "lineage_intelligence_agent",
    "governance_agent",
    "risk_analysis_agent",
    "compliance_agent",
)

OBSERVABILITY_EVENTS: tuple[str, ...] = (
    "DataQualityIssueDetected",
    "SchemaChanged",
    "PipelineFailed",
    "LineageBroken",
)

COMMANDS: tuple[str, ...] = (
    "RegisterMetadata",
    "CreateLineage",
    "UpdateRelationship",
    "DiscoverDependency",
    "AnalyzeImpact",
    "UpdateKnowledgeGraph",
)

QUERIES: tuple[str, ...] = (
    "GetDataLineage",
    "GetMetadata",
    "SearchDataGraph",
    "GetImpactAnalysis",
    "GetDataHistory",
    "GetDependencyMap",
    "GetIntelligenceReadiness",
)

DOMAIN_EVENTS: tuple[str, ...] = (
    "MetadataCollected",
    "DataAssetRegistered",
    "LineageCreated",
    "RelationshipUpdated",
    "ImpactDetected",
    "KnowledgeGraphUpdated",
    "DataQualityIssueDetected",
    "SchemaChanged",
    "PipelineFailed",
    "LineageBroken",
)

MICROSERVICES: tuple[str, ...] = (
    "metadata-service",
    "lineage-extraction-service",
    "lineage-processing-service",
    "relationship-service",
    "knowledge-graph-service",
    "semantic-intelligence-service",
    "impact-analysis-service",
    "data-observability-service",
    "ai-reasoning-service",
    "digital-twin-service",
)

APIS: tuple[str, ...] = (
    "metadata_api",
    "lineage_api",
    "graph_query_api",
    "impact_analysis_api",
    "search_api",
    "ai_reasoning_api",
    "governance_api",
)

API_STYLES: tuple[str, ...] = ("rest", "graphql", "grpc", "event_streaming")

INTEGRATIONS: tuple[str, ...] = (
    "P207",
    "P208",
    "P209",
    "P210",
    "P211-D",
    "P211-E",
    "P211-G",
    "P211-H",
    "P211-J",
    "enterprise_ai",
    "enterprise_search",
    "integration_platform",
)

CONNECTOR_SCOPES: tuple[str, ...] = (
    "databases",
    "cloud",
    "data_platforms",
    "integration",
    "enterprise",
    "ai",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_data_intelligence_architecture",
    "metadata_domain_model",
    "lineage_engine_architecture",
    "knowledge_graph_model",
    "semantic_intelligence_layer",
    "ai_reasoning_framework",
    "impact_analysis_engine",
    "digital_twin_model",
    "cqrs_architecture",
    "event_catalogue",
    "microservice_blueprint",
    "api_specifications",
    "security_integration_model",
    "data_intelligence_dashboard",
    "production_deployment_blueprint",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "data_origin_is_unknown",
    "data_movement_is_invisible",
    "metadata_is_incomplete",
    "relationships_cannot_be_queried",
    "impact_analysis_is_unavailable",
    "ai_cannot_reason_over_data_context",
    "sibling_intelligence_bc",
)


def architecture() -> dict[str, Any]:
    return {
        "flow": list(ARCHITECTURE_FLOW),
        "layer_count": len(ARCHITECTURE_FLOW),
        "builds_on_discovery": True,
        "builds_on_classification": True,
        "builds_on_dlp": True,
        "builds_on_access": True,
        "builds_on_protection": True,
    }


def domain() -> dict[str, Any]:
    return {
        "bounded_contexts": list(BOUNDED_CONTEXTS),
        "context_count": len(BOUNDED_CONTEXTS),
        "entities": list(CORE_ENTITIES),
        "entity_count": len(CORE_ENTITIES),
    }


def metadata() -> dict[str, Any]:
    return {
        "types": list(METADATA_TYPES),
        "complete_required": True,
        "not_incomplete": True,
        "technical": ["schema", "tables", "columns", "data_types", "storage", "dependencies"],
        "business": [
            "business_meaning",
            "owner",
            "data_steward",
            "business_domain",
            "criticality",
        ],
        "operational": ["usage", "performance", "frequency", "pipeline_status"],
        "security": ["classification", "risk", "access_policy", "encryption_status"],
    }


def lineage() -> dict[str, Any]:
    return {
        "kinds": list(LINEAGE_KINDS),
        "relationships": list(LINEAGE_RELATIONSHIPS),
        "origin_known_required": True,
        "not_unknown_origin": True,
        "movement_visible_required": True,
        "not_invisible_movement": True,
    }


def connectors() -> dict[str, Any]:
    return {
        "scopes": list(CONNECTOR_SCOPES),
        "scope_count": len(CONNECTOR_SCOPES),
        "via_integration_platform": True,
        "vendor_sdk_embed_forbidden": True,
    }


def knowledge_graph() -> dict[str, Any]:
    return {
        "nodes": list(KG_NODES),
        "relationships": list(KG_RELATIONSHIPS),
        "queryable_required": True,
        "not_unqueryable": True,
        "capabilities": [
            "semantic_search",
            "relationship_reasoning",
            "risk_propagation",
            "impact_prediction",
            "root_cause_analysis",
        ],
        "via_enterprise_search": True,
        "module_local_search_forbidden": True,
    }


def ai_reasoning() -> dict[str, Any]:
    return {
        "capabilities": list(AI_CAPS),
        "agents": list(AI_AGENTS),
        "reason_over_context_required": True,
        "not_unable_to_reason": True,
        "via_enterprise_ai": True,
        "module_local_llm_sdk_forbidden": True,
    }


def impact_analysis() -> dict[str, Any]:
    return {
        "capabilities": [
            "change_impact_analysis",
            "dependency_mapping",
            "risk_assessment",
            "business_impact_prediction",
            "compliance_impact_analysis",
        ],
        "available_required": True,
        "not_unavailable": True,
        "example_flow": [
            "database_column_changed",
            "find_dependent_pipelines",
            "find_reports",
            "find_ai_models",
            "calculate_business_impact",
        ],
    }


def observability() -> dict[str, Any]:
    return {
        "monitor": [
            "data_freshness",
            "schema_changes",
            "pipeline_failures",
            "data_quality_issues",
            "unexpected_movement",
        ],
        "events": list(OBSERVABILITY_EVENTS),
    }


def digital_twin() -> dict[str, Any]:
    return {
        "represents": [
            "enterprise_data_landscape",
            "data_relationships",
            "movement_patterns",
            "security_state",
            "governance_state",
        ],
        "capabilities": [
            "simulation",
            "what_if_analysis",
            "impact_prediction",
            "architecture_testing",
        ],
    }


def cqrs() -> dict[str, Any]:
    return {
        "commands": list(COMMANDS),
        "command_count": len(COMMANDS),
        "queries": list(QUERIES),
        "query_count": len(QUERIES),
        "events": list(DOMAIN_EVENTS),
        "event_count": len(DOMAIN_EVENTS),
    }


def microservices() -> dict[str, Any]:
    return {
        "services": list(MICROSERVICES),
        "service_count": len(MICROSERVICES),
        "logical_decomposition": True,
    }


def apis() -> dict[str, Any]:
    return {
        "apis": list(APIS),
        "styles": list(API_STYLES),
        "api_count": len(APIS),
    }


def integrations() -> dict[str, Any]:
    return {"targets": list(INTEGRATIONS), "count": len(INTEGRATIONS)}


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
            "origin_known": True,
            "movement_visible": True,
            "metadata_complete": True,
            "relationships_queryable": True,
            "impact_analysis": True,
            "ai_reasoning": True,
            "no_local_search": True,
            "foundation_tests": True,
            "intelligence_api_live": True,
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
        "mission": MISSION_STATEMENT,
        "vision": VISION_STATEMENT,
        "builds_on": [
            "P211-A",
            "P211-B",
            "P211-C",
            "P211-D",
            "P211-E",
            "P211-F",
            "P211-G",
            "P211-H",
            "P211-I",
            "P211-J",
            "ADR-376",
            "ADR-377",
            "ADR-378",
            "ADR-379",
            "ADR-380",
            "ADR-381",
            "ADR-382",
            "ADR-383",
            "ADR-384",
            "ADR-385",
        ],
        "architecture": architecture(),
        "domain": domain(),
        "metadata": metadata(),
        "lineage": lineage(),
        "connectors": connectors(),
        "knowledge_graph": knowledge_graph(),
        "ai_reasoning": ai_reasoning(),
        "impact_analysis": impact_analysis(),
        "observability": observability(),
        "digital_twin": digital_twin(),
        "cqrs": cqrs(),
        "microservices": microservices(),
        "apis": apis(),
        "integrations": integrations(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "data_origin_known_required": True,
        "data_movement_visible_required": True,
        "metadata_complete_required": True,
        "relationships_queryable_required": True,
        "impact_analysis_available_required": True,
        "ai_reasoning_over_context_required": True,
        "sibling_intelligence_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/intelligence",
        "forbidden_sibling_bc": [
            "data_lineage_platform",
            "metadata_platform",
            "data_intelligence_graph",
        ],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def intelligence_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /data-security/intelligence",
            "GET /data-security/intelligence/architecture",
            "GET /data-security/intelligence/domain",
            "GET /data-security/intelligence/metadata",
            "GET /data-security/intelligence/lineage",
            "GET /data-security/intelligence/connectors",
            "GET /data-security/intelligence/knowledge-graph",
            "GET /data-security/intelligence/ai",
            "GET /data-security/intelligence/impact",
            "GET /data-security/intelligence/observability",
            "GET /data-security/intelligence/digital-twin",
            "GET /data-security/intelligence/cqrs",
            "GET /data-security/intelligence/events",
            "GET /data-security/intelligence/microservices",
            "GET /data-security/intelligence/apis",
            "GET /data-security/intelligence/integrations",
            "GET /data-security/intelligence/outputs",
            "GET /data-security/intelligence/production-readiness",
            "GET /data-security/intelligence/readiness",
        ],
    }
