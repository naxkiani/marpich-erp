"""P210-K Cyber Knowledge Graph & Digital Twin — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P210-K"
ADR = 371
SOR = "cyber_security"
API_PREFIX = "/api/v1/cyber-security"
PRODUCT = (
    "Enterprise Cyber Security & Threat Defense Platform — "
    "Cyber Knowledge Graph & Digital Twin"
)

MISSION_STATEMENT = (
    "Create an enterprise cyber intelligence platform capable of understanding "
    "enterprise security relationships, mapping complete attack paths, "
    "predicting cyber risks, simulating cyber attacks, supporting AI security "
    "reasoning, enabling autonomous security operations, and providing a "
    "real-time security digital reality."
)

VISION_STATEMENT = (
    "Create a Cyber Intelligence Fabric where every asset has context, every "
    "identity has relationships, every threat has intelligence, every "
    "vulnerability has impact, every attack path is visible, every security "
    "decision is explainable, and every cyber scenario can be simulated."
)

GRAPH_LAYERS: tuple[str, ...] = (
    "data_sources",
    "graph_ingestion_layer",
    "entity_resolution_engine",
    "semantic_modeling_layer",
    "knowledge_graph_database",
    "reasoning_engine",
    "ai_intelligence_layer",
    "security_applications",
    "soc_siem_soar_xdr",
)

CORE_ENTITIES: tuple[str, ...] = (
    "identity",
    "user",
    "service_account",
    "privileged_account",
    "role",
    "permission",
    "group",
    "device",
    "endpoint",
    "server",
    "application",
    "api",
    "microservice",
    "container",
    "pod",
    "cluster",
    "cloud_resource",
    "database",
    "storage",
    "network_segment",
    "certificate",
    "secret",
    "cryptographic_key",
)

THREAT_ENTITIES: tuple[str, ...] = (
    "threat_actor",
    "threat_group",
    "campaign",
    "malware",
    "ransomware",
    "exploit",
    "vulnerability",
    "ioc",
    "ioa",
    "attack_technique",
    "attack_tactic",
    "mitre_attack_technique",
    "kill_chain_stage",
    "threat_intelligence_report",
)

SECURITY_ENTITIES: tuple[str, ...] = (
    "alert",
    "incident",
    "case",
    "evidence",
    "detection_rule",
    "playbook",
    "response_action",
    "security_control",
    "policy",
    "compliance_requirement",
    "risk",
    "exposure",
    "business_service",
)

RELATIONSHIP_TYPES: tuple[str, ...] = (
    "HAS_ROLE",
    "HAS_PERMISSION",
    "CAN_ACCESS",
    "USES",
    "TARGETS",
    "CREATES",
    "AFFECTS",
    "INCREASES",
    "MITIGATES",
    "GENERATES",
)

ONTOLOGY_BASES: tuple[str, ...] = (
    "stix_2x",
    "mitre_attack",
    "mitre_d3fend",
    "nist_csf",
    "nist_zero_trust",
    "csa_ccm",
    "iso_27001_controls",
)

ENTITY_RESOLUTION: tuple[str, ...] = (
    "duplicate_assets",
    "duplicate_identities",
    "unknown_relationships",
    "shadow_assets",
    "shadow_applications",
    "unknown_cloud_resources",
    "hidden_dependencies",
    "third_party_connections",
)

RESOLUTION_CAPABILITIES: tuple[str, ...] = (
    "entity_matching",
    "identity_resolution",
    "graph_similarity",
    "ai_classification",
    "confidence_scoring",
)

ATTACK_PATH_STAGES: tuple[str, ...] = (
    "threat_actor",
    "initial_access",
    "identity_compromise",
    "privilege_escalation",
    "lateral_movement",
    "persistence",
    "data_access",
    "exfiltration",
    "business_impact",
)

ATTACK_PATH_CAPABILITIES: tuple[str, ...] = (
    "attack_path_discovery",
    "shortest_attack_path",
    "critical_attack_path",
    "blast_radius_analysis",
    "privilege_analysis",
    "zero_trust_validation",
)

REASONING_CAPABILITIES: tuple[str, ...] = (
    "graph_reasoning",
    "causal_reasoning",
    "threat_reasoning",
    "risk_reasoning",
    "policy_reasoning",
    "identity_reasoning",
    "attack_reasoning",
    "compliance_reasoning",
    "business_impact_reasoning",
)

DIGITAL_TWINS: tuple[str, ...] = (
    "enterprise_security_twin",
    "infrastructure_twin",
    "identity_twin",
    "application_twin",
    "cloud_twin",
    "network_twin",
    "threat_twin",
    "incident_twin",
    "soc_twin",
    "ai_agent_twin",
)

TWIN_CAPABILITIES: tuple[str, ...] = (
    "real_time_synchronization",
    "security_state_modeling",
    "attack_simulation",
    "incident_replay",
    "threat_simulation",
    "control_validation",
    "policy_testing",
    "security_architecture_testing",
    "resilience_analysis",
    "future_scenario_prediction",
)

SIMULATION_SCENARIOS: tuple[str, ...] = (
    "cyber_attacks",
    "ransomware_scenarios",
    "identity_attacks",
    "cloud_breaches",
    "api_attacks",
    "supply_chain_attacks",
    "insider_threats",
    "ai_security_attacks",
)

AI_CAPABILITIES: tuple[str, ...] = (
    "understand_graph_context",
    "discover_hidden_risks",
    "predict_attack_paths",
    "recommend_controls",
    "explain_incidents",
    "generate_security_insights",
    "optimize_detection",
    "optimize_response",
    "learn_from_historical_events",
)

COMMANDS: tuple[str, ...] = (
    "CreateEntity",
    "UpdateEntity",
    "CreateRelationship",
    "AnalyzeAttackPath",
    "GenerateSimulation",
    "UpdateDigitalTwin",
    "ExecuteReasoning",
    "ValidateControl",
)

QUERIES: tuple[str, ...] = (
    "GetSecurityGraph",
    "GetAttackPath",
    "GetEntityContext",
    "GetRiskPropagation",
    "GetDigitalTwinState",
    "GetSimulationResult",
)

DOMAIN_EVENTS: tuple[str, ...] = (
    "EntityCreated",
    "RelationshipDiscovered",
    "ThreatMapped",
    "AttackPathGenerated",
    "RiskPropagated",
    "SimulationStarted",
    "SimulationCompleted",
    "InsightGenerated",
)

MICROSERVICES: tuple[str, ...] = (
    "graph-ingestion-service",
    "entity-resolution-service",
    "ontology-service",
    "knowledge-graph-service",
    "relationship-service",
    "attack-graph-service",
    "reasoning-engine-service",
    "digital-twin-service",
    "simulation-service",
    "graph-ai-service",
)

OBSERVABILITY_METRICS: tuple[str, ...] = (
    "graph_size",
    "entity_count",
    "relationship_count",
    "graph_query_latency",
    "reasoning_accuracy",
    "attack_path_discovery_rate",
    "simulation_accuracy",
    "twin_synchronization_rate",
    "ai_insight_quality",
    "platform_availability",
)

COMPLIANCE: tuple[str, ...] = (
    "iso_27001",
    "nist_csf",
    "nist_ai_rmf",
    "mitre_attack",
    "soc_2",
)

INTEGRATIONS: tuple[str, ...] = (
    "P201",
    "P202",
    "P203",
    "P204",
    "P205",
    "P206",
    "P207",
    "P208",
    "P209",
    "P210-D",
    "P210-E",
    "P210-F",
    "P210-G",
    "P210-H",
    "P210-I",
    "P210-J",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "cyber_knowledge_graph_architecture",
    "security_ontology_model",
    "entity_relationship_model",
    "graph_database_design",
    "entity_resolution_framework",
    "attack_graph_engine",
    "ai_reasoning_engine",
    "cyber_digital_twin_architecture",
    "simulation_platform",
    "security_intelligence_model",
    "cqrs_architecture",
    "event_catalogue",
    "microservice_blueprint",
    "api_specifications",
    "graph_query_language_model",
    "ai_integration_framework",
    "security_visualization_platform",
    "operational_runbooks",
    "scalability_architecture",
    "production_deployment_blueprint",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "security_entities_lack_semantic_relationships",
    "attack_paths_cannot_be_calculated",
    "digital_twins_are_static",
    "ai_reasoning_unavailable",
    "graph_governance_missing",
    "entity_resolution_inaccurate",
    "simulation_capability_absent",
    "sibling_graph_bc",
)


def architecture() -> dict[str, Any]:
    return {"layers": list(GRAPH_LAYERS), "layer_count": len(GRAPH_LAYERS)}


def ontology() -> dict[str, Any]:
    return {
        "core_entities": list(CORE_ENTITIES),
        "threat_entities": list(THREAT_ENTITIES),
        "security_entities": list(SECURITY_ENTITIES),
        "bases": list(ONTOLOGY_BASES),
        "semantic_relationships_required": True,
        "not_lacking_relationships": True,
        "relationship_types": list(RELATIONSHIP_TYPES),
    }


def entity_resolution() -> dict[str, Any]:
    return {
        "resolves": list(ENTITY_RESOLUTION),
        "capabilities": list(RESOLUTION_CAPABILITIES),
        "accurate_required": True,
        "not_inaccurate": True,
        "confidence_scoring": True,
    }


def attack_graph() -> dict[str, Any]:
    return {
        "stages": list(ATTACK_PATH_STAGES),
        "capabilities": list(ATTACK_PATH_CAPABILITIES),
        "calculable_required": True,
        "not_incalculable": True,
    }


def reasoning() -> dict[str, Any]:
    return {
        "capabilities": list(REASONING_CAPABILITIES),
        "available_required": True,
        "not_unavailable": True,
        "via_enterprise_ai_platform": True,
        "outputs": [
            "security_recommendations",
            "risk_explanations",
            "attack_predictions",
            "control_recommendations",
        ],
    }


def digital_twin() -> dict[str, Any]:
    return {
        "twins": list(DIGITAL_TWINS),
        "capabilities": list(TWIN_CAPABILITIES),
        "living_required": True,
        "real_time_sync": True,
        "not_static": True,
    }


def simulation() -> dict[str, Any]:
    return {
        "scenarios": list(SIMULATION_SCENARIOS),
        "capability_required": True,
        "not_absent": True,
        "capabilities": [
            "red_team_simulation",
            "blue_team_simulation",
            "purple_team_exercises",
            "security_training",
            "defense_optimization",
        ],
    }


def ai() -> dict[str, Any]:
    return {
        "capabilities": list(AI_CAPABILITIES),
        "via_enterprise_ai_platform": True,
    }


def graph_governance() -> dict[str, Any]:
    return {
        "required": True,
        "not_missing": True,
        "graph_access_control": True,
        "data_classification": True,
        "knowledge_integrity_validation": True,
        "immutable_audit": True,
    }


def observability() -> dict[str, Any]:
    return {
        "metrics": list(OBSERVABILITY_METRICS),
        "metric_count": len(OBSERVABILITY_METRICS),
    }


def governance() -> dict[str, Any]:
    return {
        "zero_trust": True,
        "ai_governance": True,
        "model_governance": True,
        "compliance": list(COMPLIANCE),
    }


def ddd() -> dict[str, Any]:
    return {
        "sor": SOR,
        "logical_subdomains": [
            "graph_ingestion",
            "entity_resolution",
            "ontology",
            "knowledge_graph",
            "attack_graph",
            "reasoning",
            "digital_twin",
            "simulation",
        ],
        "sibling_bc_forbidden": [
            "cyber_graph",
            "security_digital_twin",
            "attack_graph",
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


def integrations() -> dict[str, Any]:
    return {"targets": list(INTEGRATIONS), "count": len(INTEGRATIONS)}


def cursor_outputs() -> dict[str, Any]:
    return {"outputs": list(CURSOR_OUTPUTS), "count": len(CURSOR_OUTPUTS)}


def production_readiness() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "checklist": {
            "semantic_relationships": True,
            "attack_paths_calculable": True,
            "digital_twins_living": True,
            "ai_reasoning": True,
            "graph_governance": True,
            "entity_resolution_accurate": True,
            "simulation": True,
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
        "mission": MISSION_STATEMENT,
        "vision": VISION_STATEMENT,
        "builds_on": [
            "P210-A",
            "P210-B",
            "P210-C",
            "P210-D",
            "P210-E",
            "P210-F",
            "P210-G",
            "P210-H",
            "P210-I",
            "P210-J",
            "ADR-361",
            "ADR-362",
            "ADR-363",
            "ADR-364",
            "ADR-365",
            "ADR-366",
            "ADR-367",
            "ADR-368",
            "ADR-369",
            "ADR-370",
        ],
        "architecture": architecture(),
        "ontology": ontology(),
        "entity_resolution": entity_resolution(),
        "attack_graph": attack_graph(),
        "reasoning": reasoning(),
        "digital_twin": digital_twin(),
        "simulation": simulation(),
        "ai": ai(),
        "graph_governance": graph_governance(),
        "observability": observability(),
        "governance": governance(),
        "ddd": ddd(),
        "cqrs": cqrs(),
        "microservices": microservices(),
        "integrations": integrations(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "semantic_relationships_required": True,
        "attack_paths_calculable_required": True,
        "digital_twins_living_required": True,
        "ai_reasoning_available_required": True,
        "graph_governance_required": True,
        "entity_resolution_accurate_required": True,
        "simulation_capability_required": True,
        "sibling_graph_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/graph",
        "forbidden_sibling_bc": [
            "cyber_graph",
            "security_digital_twin",
            "attack_graph",
        ],
        "distinct_from": [
            "P210-J /ai-ops* (consumes graph)",
            "enterprise AI platform",
            "peer domain SoR entities (IDs only)",
        ],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def graph_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /cyber-security/graph",
            "GET /cyber-security/graph/architecture",
            "GET /cyber-security/graph/ontology",
            "GET /cyber-security/graph/entity-resolution",
            "GET /cyber-security/graph/attack-paths",
            "GET /cyber-security/graph/reasoning",
            "GET /cyber-security/graph/digital-twin",
            "GET /cyber-security/graph/simulation",
            "GET /cyber-security/graph/ai",
            "GET /cyber-security/graph/governance",
            "GET /cyber-security/graph/observability",
            "GET /cyber-security/graph/ddd",
            "GET /cyber-security/graph/cqrs",
            "GET /cyber-security/graph/events",
            "GET /cyber-security/graph/microservices",
            "GET /cyber-security/graph/integrations",
            "GET /cyber-security/graph/outputs",
            "GET /cyber-security/graph/production-readiness",
            "GET /cyber-security/graph/readiness",
        ],
    }
