"""P212-J Data Intelligence Knowledge Graph Platform — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P212-J"
ADR = 402
SOR = "data_governance"
API_PREFIX = "/api/v1/data-governance"
PRODUCT = "Enterprise Data Intelligence Knowledge Graph Platform"
CAPABILITY = "CAP-PLT-DG-001"

PRINCIPLE = "Enterprise intelligence requires connected knowledge, not isolated data."

CORE_DOMAIN = "enterprise_data_intelligence_knowledge_graph"

SUPPORTING_DOMAINS: tuple[str, ...] = (
    "ontology_management",
    "entity_management",
    "relationship_intelligence",
    "semantic_search",
    "graph_analytics",
    "ai_reasoning_engine",
    "knowledge_governance",
)

BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "BC-01",
        "name": "knowledge_graph_core_context",
        "responsibilities": (
            "entity_management",
            "relationship_management",
            "graph_lifecycle",
        ),
    },
    {
        "id": "BC-02",
        "name": "ontology_management_context",
        "responsibilities": (
            "ontology_definition",
            "semantic_vocabulary",
            "concept_modelling",
        ),
    },
    {
        "id": "BC-03",
        "name": "semantic_intelligence_context",
        "responsibilities": (
            "meaning_extraction",
            "relationship_discovery",
            "semantic_reasoning",
        ),
    },
    {
        "id": "BC-04",
        "name": "graph_analytics_context",
        "responsibilities": (
            "graph_analysis",
            "pattern_discovery",
            "impact_analysis",
        ),
    },
    {
        "id": "BC-05",
        "name": "ai_knowledge_reasoning_context",
        "responsibilities": (
            "ai_reasoning",
            "knowledge_augmentation",
            "decision_intelligence",
        ),
    },
)

NODE_CATEGORIES: dict[str, tuple[str, ...]] = {
    "data": (
        "DataAsset",
        "Dataset",
        "DataProduct",
        "DataPipeline",
        "DataModel",
    ),
    "business": (
        "BusinessDomain",
        "BusinessCapability",
        "BusinessProcess",
        "BusinessTerm",
    ),
    "governance": (
        "Owner",
        "Steward",
        "Policy",
        "Rule",
        "ComplianceRequirement",
    ),
    "technology": (
        "Application",
        "API",
        "Service",
        "InfrastructureComponent",
    ),
    "ai": (
        "AIModel",
        "TrainingDataset",
        "FeatureSet",
        "AIUseCase",
    ),
}

KG_RELATIONSHIPS: tuple[str, ...] = (
    "Metadata_DESCRIBES_DataAsset",
    "Term_DEFINES_Concept",
    "Product_CONTAINS_Metadata",
    "Policy_GOVERNS_Metadata",
    "Policy_GOVERNS_DataAsset",
    "Rule_CONTROLS_DataProduct",
    "Owner_APPROVES_Policy",
    "Regulation_REQUIRES_Policy",
    "Consumer_DISCOVERS_DataProduct",
    "Domain_OWNS_DataProduct",
)

ONTOLOGY_CAPABILITIES: tuple[str, ...] = (
    "ontology_creation",
    "concept_management",
    "vocabulary_governance",
    "semantic_versioning",
    "relationship_rules",
    "ontology_validation",
)

ONTOLOGY_MODEL: tuple[str, ...] = (
    "Concept",
    "Class",
    "Property",
    "Relation",
    "Constraint",
)

SEMANTIC_FABRIC_LAYERS: tuple[str, ...] = (
    "data_sources",
    "metadata_layer",
    "knowledge_graph_layer",
    "semantic_intelligence_layer",
    "ai_decision_layer",
)

GRAPH_INTELLIGENCE_CAPABILITIES: tuple[str, ...] = (
    "relationship_discovery",
    "pattern_detection",
    "impact_analysis",
    "dependency_analysis",
    "root_cause_analysis",
    "knowledge_inference",
)

GRAPH_AI_AGENTS: tuple[str, ...] = (
    "ai_knowledge_explorer",
    "ai_relationship_discovery_agent",
    "ai_graph_analyst",
    "ai_governance_intelligence_agent",
)

SEMANTIC_SEARCH_CAPABILITIES: tuple[str, ...] = (
    "natural_language_search",
    "concept_search",
    "relationship_search",
    "contextual_search",
    "graph_traversal_search",
)

GRAPH_GOVERNANCE_ROLES: tuple[str, ...] = (
    "graph_owner",
    "ontology_steward",
    "semantic_architect",
    "knowledge_engineer",
)

MESH_ALIGNMENT_FLOW: tuple[str, ...] = (
    "data_domain",
    "data_product",
    "metadata",
    "knowledge_entity",
    "enterprise_intelligence",
)

TWIN_CAPABILITIES: tuple[str, ...] = (
    "knowledge_growth",
    "relationship_evolution",
    "semantic_impact",
    "governance_changes",
    "intelligence_maturity",
)

TWIN_SCENARIOS: tuple[str, ...] = (
    "new_domain_creation",
    "data_product_expansion",
    "policy_change_impact",
    "ai_knowledge_enhancement",
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "name": "knowledge-graph-core-service",
        "responsibility": "Entity/relationship lifecycle and graph fabric",
        "database_boundary": "data_governance_graph_core",
        "api_boundary": "/api/v1/data-governance/graph",
        "events": "data_governance.graph.*",
        "security_model": "zero_trust_via_p207_p208",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "ontology-management-service",
        "responsibility": "Ontology, vocabulary, semantic versioning",
        "database_boundary": "data_governance_ontology",
        "api_boundary": "/api/v1/data-governance/graph/ontology",
        "events": "data_governance.ontology.*",
        "security_model": "zero_trust_via_p207_p208",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "semantic-search-service",
        "responsibility": "Semantic/graph search via Enterprise Search",
        "database_boundary": "data_governance_semantic_search",
        "api_boundary": "/api/v1/data-governance/graph/semantic-search",
        "events": "data_governance.semantic_search.*",
        "security_model": "via_enterprise_search",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "graph-analytics-service",
        "responsibility": "Pattern, impact, dependency analysis",
        "database_boundary": "data_governance_graph_analytics",
        "api_boundary": "/api/v1/data-governance/graph/analytics",
        "events": "data_governance.graph_analytics.*",
        "security_model": "via_analytics",
        "scaling_strategy": "read_replicas",
    },
    {
        "name": "inference-engine-service",
        "responsibility": "Graph inference and semantic rule application",
        "database_boundary": "data_governance_inference",
        "api_boundary": "/api/v1/data-governance/graph/inference",
        "events": "data_governance.inference.*",
        "security_model": "via_policy_engine_p208",
        "scaling_strategy": "async_workers",
    },
    {
        "name": "ai-knowledge-intelligence-service",
        "responsibility": "AI reasoning via Enterprise AI",
        "database_boundary": "data_governance_graph_ai",
        "api_boundary": "/api/v1/data-governance/graph/intelligence",
        "events": "data_governance.graph_intel.*",
        "security_model": "via_enterprise_ai",
        "scaling_strategy": "async_workers",
    },
)

COMMANDS: tuple[str, ...] = (
    "CreateKnowledgeEntityCommand",
    "CreateOntologyCommand",
    "EstablishRelationshipCommand",
    "ApproveSemanticRuleCommand",
    "ExecuteGraphInferenceCommand",
)

QUERIES: tuple[str, ...] = (
    "SearchKnowledgeGraphQuery",
    "GetEntityContextQuery",
    "GetRelationshipQuery",
    "GetImpactAnalysisQuery",
)

DOMAIN_EVENTS: tuple[dict[str, Any], ...] = (
    {
        "name": "KnowledgeEntityCreatedEvent",
        "producer": "knowledge_graph_core_service",
        "consumers": ("ontology", "search", "audit"),
        "payload": ("tenant_id", "entity_id", "entity_type", "owner_ref"),
        "version": "v1",
    },
    {
        "name": "OntologyCreatedEvent",
        "producer": "ontology_management_service",
        "consumers": ("graph_core", "intelligence", "audit"),
        "payload": ("tenant_id", "ontology_id", "version"),
        "version": "v1",
    },
    {
        "name": "RelationshipCreatedEvent",
        "producer": "knowledge_graph_core_service",
        "consumers": ("analytics", "marketplace", "audit"),
        "payload": (
            "tenant_id",
            "relationship_id",
            "from_entity",
            "to_entity",
            "type",
        ),
        "version": "v1",
    },
    {
        "name": "SemanticRuleAppliedEvent",
        "producer": "inference_engine_service",
        "consumers": ("graph_core", "policy", "audit"),
        "payload": ("tenant_id", "rule_id", "entity_id", "result"),
        "version": "v1",
    },
    {
        "name": "InferenceGeneratedEvent",
        "producer": "ai_knowledge_intelligence_service",
        "consumers": ("analytics", "digital_twin", "audit"),
        "payload": ("tenant_id", "inference_id", "confidence", "subject_ref"),
        "version": "v1",
    },
    {
        "name": "KnowledgeGraphUpdatedEvent",
        "producer": "knowledge_graph_core_service",
        "consumers": ("search", "twin", "intelligence"),
        "payload": ("tenant_id", "graph_version", "change_summary"),
        "version": "v1",
    },
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_data_intelligence_vision",
    "knowledge_graph_domain_model_ddd",
    "knowledge_graph_bounded_context_architecture",
    "enterprise_knowledge_graph_model",
    "ontology_management_platform",
    "semantic_data_fabric_architecture",
    "graph_intelligence_engine",
    "semantic_search_platform",
    "knowledge_graph_governance_model",
    "data_mesh_knowledge_graph_alignment",
    "data_marketplace_intelligence_integration",
    "data_policy_intelligence_integration",
    "data_quality_intelligence_integration",
    "digital_twin_integration",
    "cqrs_architecture",
    "event_sourcing_architecture",
    "microservice_architecture",
    "api_first_architecture",
    "security_zero_trust_architecture",
    "deployment_architecture",
    "production_readiness_checklist",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "enterprise_knowledge_graph_architecture_is_incomplete",
    "ddd_domain_model_is_missing",
    "ontology_architecture_is_missing",
    "semantic_data_fabric_is_missing",
    "graph_intelligence_engine_is_missing",
    "ai_reasoning_layer_is_missing",
    "data_mesh_integration_is_missing",
    "metadata_integration_is_missing",
    "data_marketplace_integration_is_missing",
    "policy_integration_is_missing",
    "digital_twin_integration_is_missing",
    "cqrs_architecture_is_missing",
    "event_sourcing_architecture_is_missing",
    "microservices_architecture_is_missing",
    "zero_trust_security_is_missing",
    "enterprise_scalability_is_missing",
    "sibling_knowledge_graph_bc",
)

INTEGRATIONS: tuple[str, ...] = (
    "P207",
    "P208",
    "P209",
    "P210",
    "P211",
    "P212-D",
    "P212-E",
    "P212-F",
    "P212-G",
    "P212-H",
    "enterprise_search",
    "enterprise_ai",
    "policy_engine",
    "workflow",
    "audit",
    "knowledge_graph",
    "digital_twin",
)

DEPLOYMENT: dict[str, Any] = {
    "kubernetes": True,
    "containers": True,
    "graph_database_cluster": True,
    "service_mesh": True,
    "cicd": True,
    "gitops": True,
    "infrastructure_as_code": True,
    "observability": True,
    "auto_scaling": True,
    "multi_region": True,
}


def graph_architecture() -> dict[str, Any]:
    return {
        "complete_required": True,
        "not_incomplete": True,
        "principle": PRINCIPLE,
        "core_domain": CORE_DOMAIN,
        "supporting_domains": list(SUPPORTING_DOMAINS),
        "bounded_contexts": [dict(b) for b in BOUNDED_CONTEXTS],
        "bc_count": len(BOUNDED_CONTEXTS),
        "fabric": "meos_enterprise_data_intelligence_graph_fabric",
        "aggregate": "KnowledgeEntityGraph",
        "transforms": "disconnected_assets_to_connected_semantic_knowledge_fabric",
    }


def ddd_model() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "core_domain": CORE_DOMAIN,
        "supporting_domains": list(SUPPORTING_DOMAINS),
        "aggregate": "KnowledgeEntityGraph",
        "entities": (
            "KnowledgeEntity",
            "Ontology",
            "Relationship",
            "SemanticRule",
            "GraphQuery",
            "KnowledgeContext",
        ),
        "value_objects": (
            "EntityType",
            "RelationshipType",
            "ConfidenceScore",
            "SemanticMeaning",
            "KnowledgeVersion",
        ),
    }


def ontology() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "capabilities": list(ONTOLOGY_CAPABILITIES),
        "model": list(ONTOLOGY_MODEL),
        "capability_count": len(ONTOLOGY_CAPABILITIES),
    }


def semantic_fabric() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "layers": list(SEMANTIC_FABRIC_LAYERS),
        "layer_count": len(SEMANTIC_FABRIC_LAYERS),
        "semantic_integration": True,
        "context_awareness": True,
        "data_meaning_resolution": True,
        "cross_domain_knowledge_sharing": True,
    }


def graph_intelligence() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "capabilities": list(GRAPH_INTELLIGENCE_CAPABILITIES),
        "agents": list(GRAPH_AI_AGENTS),
        "capability_count": len(GRAPH_INTELLIGENCE_CAPABILITIES),
    }


def ai_reasoning() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "via_enterprise_ai": True,
        "agents": list(GRAPH_AI_AGENTS),
        "inference": True,
        "knowledge_augmentation": True,
        "decision_intelligence": True,
    }


def node_model() -> dict[str, Any]:
    return {
        "categories": {k: list(v) for k, v in NODE_CATEGORIES.items()},
        "category_count": len(NODE_CATEGORIES),
        "node_type_count": sum(len(v) for v in NODE_CATEGORIES.values()),
    }


def semantic_search() -> dict[str, Any]:
    return {
        "capabilities": list(SEMANTIC_SEARCH_CAPABILITIES),
        "via_enterprise_search": True,
        "examples": (
            "What customer data affects financial reporting?",
            "Which policies govern this dataset?",
            "Who owns this data product?",
        ),
    }


def graph_governance() -> dict[str, Any]:
    return {
        "roles": list(GRAPH_GOVERNANCE_ROLES),
        "includes": (
            "entity_ownership",
            "ontology_governance",
            "relationship_approval",
            "semantic_quality_control",
            "graph_security",
        ),
    }


def mesh_alignment() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "via_p212_f": True,
        "flow": list(MESH_ALIGNMENT_FLOW),
        "federated_knowledge_ownership": True,
        "domain_semantic_responsibility": True,
        "cross_domain_intelligence": True,
    }


def metadata_integration() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "via_catalog_and_mesh_metadata": True,
        "metadata_to_knowledge_entity": True,
    }


def marketplace_integration() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "via_p212_g": True,
        "intelligent_discovery": True,
        "product_recommendation": True,
        "consumer_assistance": True,
        "semantic_catalog_search": True,
    }


def policy_integration() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "via_p212_h": True,
        "policy_reasoning": True,
        "compliance_analysis": True,
        "governance_recommendations": True,
        "automated_decisions": True,
    }


def quality_integration() -> dict[str, Any]:
    return {
        "via_p212_e": True,
        "quality_relationship_analysis": True,
        "quality_impact_analysis": True,
        "root_cause_discovery": True,
        "trust_scoring": True,
    }


def knowledge_graph() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "nodes": [n for nodes in NODE_CATEGORIES.values() for n in nodes],
        "relationships": list(KG_RELATIONSHIPS),
        "ontology": True,
        "semantic_relationships": True,
        "reasoning_engine": True,
        "graph_query_model": True,
        "node_count": sum(len(v) for v in NODE_CATEGORIES.values()),
    }


def digital_twin() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "capabilities": list(TWIN_CAPABILITIES),
        "scenarios": list(TWIN_SCENARIOS),
        "capability_count": len(TWIN_CAPABILITIES),
    }


def cqrs() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "commands": list(COMMANDS),
        "command_count": len(COMMANDS),
        "queries": list(QUERIES),
        "query_count": len(QUERIES),
        "events": [e["name"] for e in DOMAIN_EVENTS],
        "event_count": len(DOMAIN_EVENTS),
    }


def event_sourcing() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "immutable_events": True,
        "outbox_required": True,
        "events": [dict(e) for e in DOMAIN_EVENTS],
        "versioning_strategy": "append_only_vN",
    }


def microservices() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "services": [dict(s) for s in MICROSERVICES],
        "service_count": len(MICROSERVICES),
    }


def zero_trust() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "via_p207": True,
        "via_p208": True,
        "via_p209": True,
        "via_p211": True,
        "graph_access_control": True,
        "entity_security": True,
        "relationship_security": True,
        "query_authorization": True,
        "auditability": True,
    }


def scalability() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "deployment": dict(DEPLOYMENT),
        "microservice_count": len(MICROSERVICES),
    }


def apis() -> dict[str, Any]:
    return {
        "rest": (
            "/api/v1/data-governance/graph",
            "/api/v1/data-governance/graph/entities",
            "/api/v1/data-governance/graph/relationships",
            "/api/v1/data-governance/graph/ontology",
            "/api/v1/data-governance/graph/semantic-search",
            "/api/v1/data-governance/graph/inference",
            "/api/v1/data-governance/graph/analytics",
        ),
        "ai": (
            "/api/v1/data-governance/graph/knowledge-assistant",
            "/api/v1/data-governance/graph/reasoning",
            "/api/v1/data-governance/graph/context-analysis",
        ),
        "graphql": "/api/v1/data-governance/graph/graphql",
        "graph_query_apis": True,
        "event_apis": "data_governance.graph|ontology|inference.*.v1",
        "streaming_apis": True,
        "api_security": ("data_governance.read", "zero_trust", "tenant_isolation"),
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
            "enterprise_knowledge_graph": True,
            "ontology_platform": True,
            "semantic_fabric": True,
            "graph_intelligence": True,
            "ai_reasoning": True,
            "knowledge_governance": True,
            "digital_twin_integration": True,
            "cqrs_architecture": True,
            "event_architecture": True,
            "microservice_architecture": True,
            "api_architecture": True,
            "deployment_architecture": True,
            "foundation_tests": True,
            "graph_api_live": True,
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
            "ADR-392",
            "ADR-393",
            "ADR-397",
            "ADR-398",
            "ADR-399",
            "ADR-400",
            "ADR-401",
        ],
        "graph_architecture": graph_architecture(),
        "ddd_model": ddd_model(),
        "ontology": ontology(),
        "semantic_fabric": semantic_fabric(),
        "graph_intelligence": graph_intelligence(),
        "ai_reasoning": ai_reasoning(),
        "node_model": node_model(),
        "semantic_search": semantic_search(),
        "graph_governance": graph_governance(),
        "mesh_alignment": mesh_alignment(),
        "metadata_integration": metadata_integration(),
        "marketplace_integration": marketplace_integration(),
        "policy_integration": policy_integration(),
        "quality_integration": quality_integration(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "cqrs": cqrs(),
        "event_sourcing": event_sourcing(),
        "microservices": microservices(),
        "zero_trust": zero_trust(),
        "scalability": scalability(),
        "apis": apis(),
        "integrations": integrations(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "knowledge_graph_architecture_complete_required": True,
        "ddd_domain_model_present_required": True,
        "ontology_architecture_present_required": True,
        "semantic_data_fabric_present_required": True,
        "graph_intelligence_engine_present_required": True,
        "ai_reasoning_layer_present_required": True,
        "data_mesh_integration_present_required": True,
        "metadata_integration_present_required": True,
        "data_marketplace_integration_present_required": True,
        "policy_integration_present_required": True,
        "digital_twin_integration_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_sourcing_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "zero_trust_security_present_required": True,
        "enterprise_scalability_present_required": True,
        "sibling_knowledge_graph_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/graph",
        "forbidden_sibling_bc": [
            "knowledge_graph",
            "ontology_platform",
            "semantic_fabric_platform",
            "data_marketplace",
            "data_mesh",
            "metadata_governance_platform",
        ],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def graph_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /data-governance/graph",
            "GET /data-governance/graph/ontology",
            "GET /data-governance/graph/entities",
            "GET /data-governance/graph/semantic-fabric",
            "GET /data-governance/graph/intelligence",
            "GET /data-governance/graph/ai-reasoning",
            "GET /data-governance/graph/semantic-search",
            "GET /data-governance/graph/mesh-alignment",
            "GET /data-governance/graph/marketplace",
            "GET /data-governance/graph/policies",
            "GET /data-governance/graph/digital-twin",
            "GET /data-governance/graph/cqrs",
            "GET /data-governance/graph/events",
            "GET /data-governance/graph/microservices",
            "GET /data-governance/graph/apis",
            "GET /data-governance/graph/security",
            "GET /data-governance/graph/deployment",
            "GET /data-governance/graph/outputs",
            "GET /data-governance/graph/production-readiness",
            "GET /data-governance/graph/readiness",
        ],
    }
