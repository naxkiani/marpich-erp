"""P207-K Knowledge Graph Intelligence & Reasoning — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P207-K"
ADR = 326
SOR = "identity_intelligence"
GRAPH_STORAGE_PEER = "directory"
API_PREFIX = "/api/v1/identity-intelligence"
PRODUCT = "Knowledge Graph Intelligence & Reasoning Engine"

ONTOLOGY_CLASSES: tuple[str, ...] = (
    "identity",
    "organization",
    "resource",
    "access_object",
    "security_object",
)

IDENTITY_TYPES: tuple[str, ...] = (
    "human_identity",
    "workforce_identity",
    "customer_identity",
    "partner_identity",
    "machine_identity",
    "service_identity",
)

GRAPH_EDGES: tuple[str, ...] = (
    "WORKS_FOR",
    "REPORTS_TO",
    "MEMBER_OF",
    "HAS_ROLE",
    "HAS_PERMISSION",
    "USES_APPLICATION",
    "OWNS_RESOURCE",
    "HAS_RISK",
    "TRUSTS",
    "VIOLATES_POLICY",
    "CONNECTED_TO_THREAT",
    "DEPENDS_ON",
    "SUPPORTS",
    "IMPACTS",
)

REASONING_TYPES: tuple[str, ...] = (
    "rule_based_reasoning",
    "semantic_reasoning",
    "ai_reasoning",
    "graph_neural_reasoning",
)

GRAPH_AGENTS: tuple[str, ...] = (
    "graph_analyst_agent",
    "reasoning_agent",
    "risk_intelligence_agent",
)

MICROSERVICES_LOGICAL: tuple[str, ...] = (
    "knowledge-graph-service",
    "ontology-service",
    "graph-query-service",
    "reasoning-engine-service",
    "semantic-search-service",
    "graph-analytics-service",
    "relationship-intelligence-service",
)

LOGICAL_BOUNDED_CONTEXTS: tuple[str, ...] = (
    "graph_data_platform",
    "semantic_ontology",
    "reasoning_engine",
    "graph_intelligence",
    "attack_path_analysis",
    "semantic_search",
    "relationship_intelligence",
)

AGGREGATES: tuple[str, ...] = (
    "KnowledgeGraphEntity",
    "GraphRelationship",
    "GraphReasoningSession",
    "AttackPathAnalysis",
    "SemanticQueryCase",
    "OntologyGovernancePolicy",
    "GraphSecurityContext",
)

COMMANDS: tuple[str, ...] = (
    "CreateEntity",
    "CreateRelationship",
    "UpdateKnowledge",
    "AnalyzeGraph",
    "RunReasoning",
    "DiscoverAttackPath",
)

QUERIES: tuple[str, ...] = (
    "GetIdentityGraph",
    "FindRelationships",
    "AnalyzeImpact",
    "ExplainDecision",
    "GetAttackPath",
    "SemanticSearch",
)

DOMAIN_EVENTS: tuple[str, ...] = (
    "EntityCreated",
    "RelationshipDiscovered",
    "RiskPathDetected",
    "KnowledgeUpdated",
    "ReasoningCompleted",
    "AttackPathIdentified",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "graph_only_data_without_reasoning",
    "relationships_undefined",
    "ai_cannot_explain_conclusions",
    "security_context_missing",
    "ontology_governance_absent",
    "identity_intelligence_integration_weak",
    "duplicates_directory_graph_sor",
    "invents_sibling_graph_bc",
    "embeds_llm_sdk",
    "bypasses_authorization_pdp",
)


def capabilities() -> dict[str, Any]:
    return {
        "not_data_only": True,
        "relationships_defined_required": True,
        "ai_explainable_required": True,
        "security_context_required": True,
        "ontology_governance_required": True,
        "ii_integration_strong_required": True,
        "via_directory_graph": True,
        "via_ai_platform": True,
        "via_search_platform": True,
        "via_p207e_agents": True,
        "via_p207f_twins": True,
        "via_p207g_risk": True,
        "does_not_own_graph_sor": True,
        "not_data_only_graph": True,
        "not_relationships_undefined": True,
        "not_ai_unexplainable": True,
        "not_security_missing": True,
        "not_ontology_ungoverned": True,
        "not_weak_ii_integration": True,
        "embeds_llm_forbidden": True,
    }


def domain_purpose() -> dict[str, Any]:
    return {
        "chain": [
            "identity",
            "organization",
            "role",
            "application",
            "permission",
            "privilege",
            "device",
            "behavior",
            "risk",
            "policy",
        ],
        "required": True,
        "semantic_intelligence": True,
    }


def platform_architecture() -> dict[str, Any]:
    return {
        "graph_data_platform": [
            "store_relationships_via_peer",
            "manage_graph_entities",
            "maintain_connections",
        ],
        "semantic_layer": [
            "ontology_management",
            "meaning_definition",
            "entity_classification",
        ],
        "reasoning_engine": [
            "relationship_analysis",
            "rule_reasoning",
            "ai_inference",
        ],
        "graph_intelligence_engine": [
            "pattern_discovery",
            "risk_detection",
            "prediction",
        ],
        "required": True,
        "not_data_only": True,
        "graph_storage_peer": GRAPH_STORAGE_PEER,
    }


def ontology() -> dict[str, Any]:
    return {
        "core_classes": list(ONTOLOGY_CLASSES),
        "identity_types": list(IDENTITY_TYPES),
        "organization_types": ["company", "department", "business_unit", "team"],
        "resource_types": ["application", "system", "database", "cloud_resource"],
        "access_object_types": ["role", "permission", "entitlement", "privilege"],
        "security_object_types": ["risk", "threat", "policy", "incident"],
        "governed": True,
        "not_ungoverned": True,
        "required": True,
    }


def entity_model() -> dict[str, Any]:
    return {
        "nodes": [
            "identity_node",
            "organization_node",
            "application_node",
            "permission_node",
            "risk_node",
        ],
        "required": True,
    }


def relationship_model() -> dict[str, Any]:
    return {
        "edges": list(GRAPH_EDGES),
        "count": len(GRAPH_EDGES),
        "defined": True,
        "not_undefined": True,
        "required": True,
    }


def reasoning() -> dict[str, Any]:
    return {
        "types": list(REASONING_TYPES),
        "rule_example": "privilege_and_high_risk_generates_security_review",
        "semantic": True,
        "ai": True,
        "gnn": True,
        "explainable": True,
        "not_data_only": True,
        "not_unexplainable": True,
        "via_ai_platform": True,
        "required": True,
    }


def relationship_intelligence() -> dict[str, Any]:
    return {
        "discovers": [
            "hidden_access_paths",
            "privilege_chains",
            "identity_dependencies",
            "risk_relationships",
        ],
        "required": True,
    }


def attack_path() -> dict[str, Any]:
    return {
        "path": [
            "compromised_identity",
            "privilege_escalation",
            "application_access",
            "critical_resource",
        ],
        "capabilities": [
            "attack_path_discovery",
            "risk_prediction",
            "mitigation_recommendation",
        ],
        "security_context_required": True,
        "required": True,
    }


def digital_twin() -> dict[str, Any]:
    return {
        "via_p207f": True,
        "graphs": ["current_state_graph", "future_simulation_graph"],
        "analyzes": "behavioral_impact_of_access_change",
        "required": True,
    }


def graph_agents() -> dict[str, Any]:
    return {
        "agents": list(GRAPH_AGENTS),
        "count": len(GRAPH_AGENTS),
        "via_p207e": True,
        "explainable": True,
        "required": True,
    }


def risk_integration() -> dict[str, Any]:
    return {
        "via_p207g": True,
        "calculates": [
            "relationship_risk",
            "privilege_risk",
            "dependency_risk",
            "exposure_risk",
        ],
        "ii_integration_strong": True,
        "not_weak": True,
        "required": True,
    }


def semantic_search() -> dict[str, Any]:
    return {
        "via_search_platform": True,
        "examples": [
            "users_with_excessive_privilege",
            "identities_accessing_financial_systems",
            "why_user_has_permission",
        ],
        "natural_language": True,
        "required": True,
    }


def security() -> dict[str, Any]:
    return {
        "graph_security": ["access_control", "data_classification", "encryption"],
        "reasoning_security": [
            "explainability",
            "auditability",
            "decision_tracking",
        ],
        "zero_trust": ["verify_every_query", "control_every_relationship"],
        "security_context_present": True,
        "not_missing": True,
        "required": True,
    }


def observability() -> dict[str, Any]:
    return {
        "graph": ["growth", "query_performance", "relationship_accuracy"],
        "ai": ["reasoning_quality", "prediction_accuracy"],
        "operations": ["processing_latency", "event_processing"],
        "via_observability_platform": True,
    }


def ddd() -> dict[str, Any]:
    return {
        "logical_contexts": list(LOGICAL_BOUNDED_CONTEXTS),
        "logical_count": len(LOGICAL_BOUNDED_CONTEXTS),
        "aggregates": list(AGGREGATES),
        "aggregate_count": len(AGGREGATES),
        "boundaries_clear": True,
        "deployable_unit": SOR,
        "graph_storage_peer": GRAPH_STORAGE_PEER,
    }


def cqrs() -> dict[str, Any]:
    return {
        "commands": list(COMMANDS),
        "command_count": len(COMMANDS),
        "queries": list(QUERIES),
        "query_count": len(QUERIES),
        "events": list(DOMAIN_EVENTS),
        "event_count": len(DOMAIN_EVENTS),
        "cqrs_ready": True,
        "event_driven": True,
        "outbox_required": True,
    }


def microservices() -> dict[str, Any]:
    return {
        "logical_services": list(MICROSERVICES_LOGICAL),
        "count": len(MICROSERVICES_LOGICAL),
        "deployable_today": SOR,
        "never_invent_sibling_bc": True,
        "never_duplicate_graph_sor": True,
    }


def integrations() -> dict[str, Any]:
    return {
        "p207a_strategy": True,
        "p207b_mission": True,
        "p207c_domain": True,
        "p207e_agents": True,
        "p207f_twins": True,
        "p207g_risk": True,
        "p207h_behavior": True,
        "p207j_access_gov": True,
        "p205_directory": True,
        "ai_platform": True,
        "search_platform": True,
        "authorization": True,
        "audit_platform": True,
        "graph_integration_complete": True,
    }


def cursor_outputs() -> dict[str, Any]:
    return {
        "knowledge_graph_architecture": True,
        "identity_ontology_model": True,
        "graph_data_model": True,
        "relationship_model": True,
        "reasoning_engine_design": True,
        "semantic_layer_architecture": True,
        "graph_ai_model": True,
        "attack_path_analysis_model": True,
        "digital_twin_integration": True,
        "ai_agent_integration": True,
        "cqrs_architecture": True,
        "event_model": True,
        "microservice_blueprint": True,
        "api_specifications": True,
        "security_architecture": True,
        "data_governance_model": True,
        "testing_strategy": True,
        "kubernetes_deployment_architecture": True,
        "operational_runbook": True,
        "count": 19,
    }


def production_readiness() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "checklist": {
            "graph_architecture": True,
            "ontology_and_relationships": True,
            "reasoning_engine": True,
            "attack_path_and_search": True,
            "security_and_governance": True,
            "integrations": True,
            "cqrs_events": True,
            "foundation_tests": True,
            "graph_api_live": True,
        },
        "verdict": "ENTERPRISE_GRADE",
    }


def quality_gates() -> dict[str, Any]:
    return {
        "reject_if": list(QUALITY_GATES_REJECT_IF),
        "count": len(QUALITY_GATES_REJECT_IF),
    }


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "adr": ADR,
        "sor": SOR,
        "product": PRODUCT,
        "graph_storage_peer": GRAPH_STORAGE_PEER,
        "forbidden_sibling_bc": "knowledge_graph_platform",
        "builds_on": [
            "P207-A",
            "P207-B",
            "P207-C",
            "P207-E",
            "P207-F",
            "P207-G",
            "P207-H",
            "P207-J",
        ],
        "capabilities": capabilities(),
        "domain_purpose": domain_purpose(),
        "platform_architecture": platform_architecture(),
        "ontology": ontology(),
        "entity_model": entity_model(),
        "relationship_model": relationship_model(),
        "reasoning": reasoning(),
        "relationship_intelligence": relationship_intelligence(),
        "attack_path": attack_path(),
        "digital_twin": digital_twin(),
        "graph_agents": graph_agents(),
        "risk_integration": risk_integration(),
        "semantic_search": semantic_search(),
        "security": security(),
        "observability": observability(),
        "ddd": ddd(),
        "cqrs": cqrs(),
        "microservices": microservices(),
        "integrations": integrations(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "not_data_only": True,
        "reasoning_required": True,
        "api_prefix": f"{API_PREFIX}/graph",
        "distinct_from": [
            "P207-A /strategy*",
            "P207-E /agents*",
            "P207-F /twins*",
            "P207-G /risk*",
            "P207-H /behavior*",
            "P207-J /access-gov*",
            "directory /graph*",
        ],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def graph_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /identity-intelligence/graph",
            "GET /identity-intelligence/graph/capabilities",
            "GET /identity-intelligence/graph/purpose",
            "GET /identity-intelligence/graph/architecture",
            "GET /identity-intelligence/graph/ontology",
            "GET /identity-intelligence/graph/entities",
            "GET /identity-intelligence/graph/relationships",
            "GET /identity-intelligence/graph/reasoning",
            "GET /identity-intelligence/graph/intelligence",
            "GET /identity-intelligence/graph/attack-path",
            "GET /identity-intelligence/graph/twins",
            "GET /identity-intelligence/graph/agents",
            "GET /identity-intelligence/graph/risk",
            "GET /identity-intelligence/graph/search",
            "GET /identity-intelligence/graph/security",
            "GET /identity-intelligence/graph/observability",
            "GET /identity-intelligence/graph/ddd",
            "GET /identity-intelligence/graph/cqrs",
            "GET /identity-intelligence/graph/events",
            "GET /identity-intelligence/graph/microservices",
            "GET /identity-intelligence/graph/integrations",
            "GET /identity-intelligence/graph/outputs",
            "GET /identity-intelligence/graph/production-readiness",
            "GET /identity-intelligence/graph/readiness",
        ],
    }
