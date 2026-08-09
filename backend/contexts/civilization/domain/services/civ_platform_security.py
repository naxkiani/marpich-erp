"""P219-M Civilization Security Intelligence Core — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P219-M"
ADR = 566
SOR = "civilization"
API_PREFIX = "/api/v1/civilization"
PRODUCT = (
    "Enterprise Civilization Operating System Civilization Security Intelligence, "
    "Global Risk Intelligence, Resilience Intelligence, Adaptive Security Architecture "
    "& MEOS Civilization Security Intelligence Core"
)
CAPABILITY = "CAP-PLT-CIV-001"
PRIMARY_CAPABILITY = (
    "Create a civilization-scale security intelligence platform capable of "
    "protecting planetary infrastructure, human civilization, critical knowledge "
    "and autonomous systems through predictive intelligence, adaptive defense and "
    "continuous resilience optimization."
)
FABRIC = "meos_civilization_os_civilization_security_intelligence_framework"
FOUNDATION_GATE = "P219"
MISSION_GATE = "P219-A"
STRATEGY_GATE = "P219-B"
DOMAIN_GATE = "P219-C"
PLANETARY_GATE = "P219-D"
AI_OS_GATE = "P219-E"
SIMULATION_GATE = "P219-F"
RESOURCES_GATE = "P219-G"
ECONOMY_GATE = "P219-H"
KNOWLEDGE_GATE = "P219-I"
HUMAN_GATE = "P219-J"
GOVERNANCE_GATE = "P219-K"
INNOVATION_GATE = "P219-L"
INTELLIGENCE_NEXUS_GATE = "P218-Z"
SPACE_GATE = "P218"
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

EVOLUTION = (
    "Reactive Security", "Preventive Security", "Predictive Security",
    "Adaptive Security", "Autonomous Security Intelligence", "Civilization Security Intelligence",
)
LAYERS = (
    {"id": "L01", "name": "Civilization Security Domain"},
    {"id": "L02", "name": "Threat Observation Layer"},
    {"id": "L03", "name": "Risk Intelligence Layer"},
    {"id": "L04", "name": "Security Digital Twin Layer"},
    {"id": "L05", "name": "Adaptive Security Intelligence Layer"},
    {"id": "L06", "name": "Autonomous Security Operations"},
)
RISK_DOMAINS = (
    "cyber", "infrastructure", "economic", "environmental", "geopolitical",
    "technology", "supply_chain", "health", "space", "ai",
)
THREAT_CATEGORIES = (
    "cyber_threats", "infrastructure_threats", "natural_hazards", "supply_chain_disruptions",
    "space_threats", "biological_threats", "ai_threats", "information_threats",
)
RESILIENCE_DOMAINS = (
    "infrastructure", "economic", "social", "energy", "water",
    "food", "knowledge", "ai", "space",
)
RESILIENCE_LIFECYCLE = (
    "Prepare", "Monitor", "Detect", "Respond", "Recover", "Adapt", "Improve",
)
SECURITY_AGENTS = (
    "Threat Intelligence Agent", "Risk Intelligence Agent", "Response Intelligence Agent",
    "Resilience Intelligence Agent", "Governance Security Agent",
)
KG_ENTITIES = (
    "Threat", "Risk", "Attack", "Incident", "Infrastructure",
    "Asset", "Policy", "Vulnerability", "Response", "RecoveryPlan",
)
KG_RELATIONSHIPS = (
    "TARGETS", "AFFECTS", "EXPLOITS", "PROTECTS",
    "DEPENDS_ON", "MITIGATES", "RECOVERS", "ESCALATES",
)
DIGITAL_TWINS = (
    "Security Operations Twin", "Critical Infrastructure Twin", "Threat Twin",
    "Incident Twin", "Recovery Twin",
)
BOUNDED_CONTEXTS = (
    {
        "id": "BC-SEC-01", "name": "Security Intelligence Core", "type": "CORE",
        "aggregate": "SecurityAggregate",
        "entities": ("SecurityModel", "ProtectedAsset", "SecurityControl"),
        "value_objects": ("SecurityId", "ProtectionLevel", "ThreatScore"),
        "services": ("SecurityManagementService", "ThreatAnalysisService"),
        "events": ("SecurityInitializedEvent", "ThreatDetectedEvent", "ProtectionUpdatedEvent"),
    },
    {
        "id": "BC-SEC-02", "name": "Risk Intelligence Context", "type": "CORE",
        "aggregate": "RiskAggregate",
        "entities": ("Risk", "RiskScenario", "RiskAssessment"),
        "value_objects": ("RiskLevel", "ProbabilityScore", "ImpactScore"),
        "services": ("RiskEvaluationService", "RiskForecastService"),
        "events": ("RiskCreatedEvent", "RiskEscalatedEvent", "RiskMitigatedEvent"),
    },
    {
        "id": "BC-SEC-03", "name": "Incident Response Context", "type": "CORE",
        "aggregate": "IncidentAggregate",
        "entities": ("Incident", "ResponsePlan", "RecoveryOperation"),
        "value_objects": ("IncidentSeverity", "RecoveryTimeObjective", "ResponsePriority"),
        "services": ("IncidentResponseService", "RecoveryManagementService"),
        "events": ("IncidentOpenedEvent", "ResponseActivatedEvent", "RecoveryCompletedEvent"),
    },
    {
        "id": "BC-SEC-04", "name": "Resilience Intelligence Context", "type": "SUPPORTING",
        "aggregate": "ResilienceAggregate",
        "entities": ("ResilienceModel", "ContinuityPlan", "RecoveryCapability"),
        "value_objects": ("ResilienceIndex", "ContinuityScore", "RecoveryScore"),
        "services": ("ResilienceOptimizationService", "ContinuityPlanningService"),
        "events": ("ResilienceEvaluatedEvent", "ContinuityValidatedEvent", "ResilienceImprovedEvent"),
    },
)
PRIMARY_AGGREGATES = (
    "SecurityAggregate", "SecurityStateAggregate", "RiskAggregate",
    "IncidentAggregate", "ResilienceAggregate",
)
COMMANDS = (
    "RegisterThreatCommand", "CreateRiskAssessmentCommand", "ActivateIncidentResponseCommand",
    "RunSecuritySimulationCommand", "UpdateSecurityPolicyCommand", "OptimizeResilienceCommand",
)
QUERIES = (
    "GetThreatStatusQuery", "GetRiskDashboardQuery", "GetIncidentTimelineQuery",
    "GetResilienceIndexQuery", "GetRecoveryStatusQuery", "GetSecurityForecastQuery",
)
CORE_EVENTS = (
    {"name": "ThreatDetectedEvent", "owner": "BC-SEC-01"},
    {"name": "ThreatNeutralizedEvent", "owner": "BC-SEC-01"},
    {"name": "SecurityControlUpdatedEvent", "owner": "BC-SEC-01"},
    {"name": "RiskIdentifiedEvent", "owner": "BC-SEC-02"},
    {"name": "RiskForecastGeneratedEvent", "owner": "BC-SEC-02"},
    {"name": "RiskMitigatedEvent", "owner": "BC-SEC-02"},
    {"name": "IncidentCreatedEvent", "owner": "BC-SEC-03"},
    {"name": "IncidentContainedEvent", "owner": "BC-SEC-03"},
    {"name": "IncidentResolvedEvent", "owner": "BC-SEC-03"},
    {"name": "RecoveryStartedEvent", "owner": "BC-SEC-03"},
    {"name": "RecoveryCompletedEvent", "owner": "BC-SEC-03"},
    {"name": "ContinuityRestoredEvent", "owner": "BC-SEC-04"},
)
KNOWLEDGE_GRAPH = {
    "present_required": True,
    "entities": KG_ENTITIES,
    "relationships": KG_RELATIONSHIPS,
    "capabilities": ("threat_reasoning", "attack_path_analysis", "risk_propagation_modeling", "security_recommendation"),
}
DIGITAL_TWIN = {
    "present_required": True,
    "twins": DIGITAL_TWINS,
    "capabilities": (
        "attack_simulation", "resilience_simulation", "recovery_validation",
        "policy_testing", "future_threat_modeling",
    ),
}
INTEGRATION = {
    "present_required": True,
    "peers": (
        "P214-Z", "P215-Z", "P216-Z", "P217-Z", "P218", "P218-Z",
        "P219", "P219-A", "P219-B", "P219-C", "P219-D", "P219-E", "P219-F",
        "P219-G", "P219-H", "P219-I", "P219-J", "P219-K", "P219-L",
        "Identity", "Policy Engine", "Workflow", "Audit", "MEOS Core",
    ),
    "integrations": (
        {"peer": "P214-Z", "provides": ("security_intelligence_models",)},
        {"peer": "P215-Z", "provides": ("advanced_threat_computation",)},
        {"peer": "P216-Z", "provides": ("autonomous_physical_security",)},
        {"peer": "P217-Z", "provides": ("biosecurity_intelligence",)},
        {"peer": "P218", "provides": ("space_security_intelligence",)},
        {"peer": "P218-Z", "provides": ("civilization_security_coordination",)},
        {"peer": "P219-D", "provides": ("critical_infrastructure_protection",)},
        {"peer": "P219-E", "provides": ("adaptive_security_reasoning",)},
        {"peer": "P219-F", "provides": ("global_security_simulation",)},
        {"peer": "P219-G", "provides": ("resource_protection_intelligence",)},
        {"peer": "P219-H", "provides": ("economic_risk_intelligence",)},
        {"peer": "P219-K", "provides": ("security_governance",)},
        {"peer": "Identity", "provides": ("authz_and_identity_controls",)},
    ),
}
ROADMAP = {
    "phases": (
        {"id": "P01", "name": "Security Intelligence Foundation"},
        {"id": "P02", "name": "Adaptive Security Platform"},
        {"id": "P03", "name": "Autonomous Security Operations"},
        {"id": "P04", "name": "Civilization Security Intelligence"},
    ),
}
MICROSERVICES = (
    {"id": "security_intelligence_service", "api": "/civilization/security", "bc": "BC-SEC-01"},
    {"id": "risk_intelligence_service", "api": "/civilization/security/risk", "bc": "BC-SEC-02"},
    {"id": "threat_intelligence_service", "api": "/civilization/security/threat", "bc": "BC-SEC-01"},
    {"id": "resilience_intelligence_service", "api": "/civilization/security/resilience", "bc": "BC-SEC-04"},
    {"id": "adaptive_security_service", "api": "/civilization/security/adaptive", "bc": "BC-SEC-01"},
    {"id": "security_twin_service", "api": "/civilization/security/digital-twin", "bc": "BC-SEC-01"},
    {"id": "security_kg_service", "api": "/civilization/security/knowledge-graph", "bc": "BC-SEC-02"},
    {"id": "security_agents_service", "api": "/civilization/security/agents", "bc": "BC-SEC-01"},
    {"id": "security_events_service", "api": "/civilization/security/events", "bc": "BC-SEC-03"},
    {"id": "security_integration_service", "api": "/civilization/security/integration", "bc": "BC-SEC-01"},
)


def vision_pack() -> dict[str, Any]:
    return {
        "primary_capability": PRIMARY_CAPABILITY,
        "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "planetary_gate": PLANETARY_GATE, "ai_os_gate": AI_OS_GATE,
        "simulation_gate": SIMULATION_GATE, "resources_gate": RESOURCES_GATE,
        "economy_gate": ECONOMY_GATE, "knowledge_gate": KNOWLEDGE_GATE,
        "human_gate": HUMAN_GATE, "governance_gate": GOVERNANCE_GATE,
        "innovation_gate": INNOVATION_GATE,
        "intelligence_nexus_gate": INTELLIGENCE_NEXUS_GATE, "space_gate": SPACE_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "never_replace_p219_l_innovation": True,
        "never_replace_identity": True,
        "never_ungated_autonomous_security_response": True,
        "never_bypass_zero_trust_controls": True,
        "foundation_for_p219_n": True,
    }


def architecture() -> dict[str, Any]:
    return {
        "present_required": True,
        "evolution": list(EVOLUTION),
        "evolution_stage_count": len(EVOLUTION),
        "layers": [dict(l) for l in LAYERS],
        "layer_count": len(LAYERS),
        "risk_domains": list(RISK_DOMAINS),
        "risk_domain_count": len(RISK_DOMAINS),
        "threat_categories": list(THREAT_CATEGORIES),
        "threat_category_count": len(THREAT_CATEGORIES),
        "resilience_domains": list(RESILIENCE_DOMAINS),
        "resilience_domain_count": len(RESILIENCE_DOMAINS),
        "resilience_lifecycle": list(RESILIENCE_LIFECYCLE),
        "resilience_lifecycle_step_count": len(RESILIENCE_LIFECYCLE),
    }


def risk() -> dict[str, Any]:
    return {
        "present_required": True,
        "domains": list(RISK_DOMAINS),
        "domain_count": len(RISK_DOMAINS),
        "capabilities": (
            "risk_identification", "risk_quantification", "risk_prediction",
            "risk_prioritization", "risk_correlation", "risk_forecasting",
        ),
    }


def threat() -> dict[str, Any]:
    return {
        "present_required": True,
        "categories": list(THREAT_CATEGORIES),
        "category_count": len(THREAT_CATEGORIES),
        "capabilities": (
            "threat_hunting", "threat_attribution", "threat_evolution_modeling",
            "threat_simulation", "threat_intelligence_sharing",
        ),
    }


def resilience() -> dict[str, Any]:
    return {
        "present_required": True,
        "domains": list(RESILIENCE_DOMAINS),
        "domain_count": len(RESILIENCE_DOMAINS),
        "lifecycle": list(RESILIENCE_LIFECYCLE),
        "lifecycle_step_count": len(RESILIENCE_LIFECYCLE),
    }


def adaptive() -> dict[str, Any]:
    return {
        "present_required": True,
        "components": (
            "behavior_analytics", "policy_adaptation", "threat_prediction",
            "security_optimization", "recovery_intelligence", "learning_engine",
        ),
        "never_ungated_autonomous_security_response": True,
        "never_bypass_zero_trust_controls": True,
    }


def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN) | {
        "twin_count": len(DIGITAL_TWINS),
        "capability_count": len(DIGITAL_TWIN["capabilities"]),
    }


def agents() -> dict[str, Any]:
    return {
        "present_required": True,
        "agents": list(SECURITY_AGENTS),
        "agent_count": len(SECURITY_AGENTS),
    }


def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH) | {
        "entity_count": len(KG_ENTITIES),
        "relationship_count": len(KG_RELATIONSHIPS),
        "capability_count": len(KNOWLEDGE_GRAPH["capabilities"]),
    }


def bounded_contexts() -> dict[str, Any]:
    return {
        "present_required": True,
        "contexts": [dict(c) for c in BOUNDED_CONTEXTS],
        "context_count": len(BOUNDED_CONTEXTS),
    }


def aggregates() -> dict[str, Any]:
    return {
        "present_required": True,
        "primary_aggregates": list(PRIMARY_AGGREGATES),
        "aggregate_count": len(PRIMARY_AGGREGATES),
    }


def events() -> dict[str, Any]:
    return {
        "present_required": True,
        "core_events": [dict(e) for e in CORE_EVENTS],
        "core_event_count": len(CORE_EVENTS),
    }


def cqrs() -> dict[str, Any]:
    return {
        "present_required": True,
        "commands": list(COMMANDS), "command_count": len(COMMANDS),
        "queries": list(QUERIES), "query_count": len(QUERIES),
    }


def integration() -> dict[str, Any]:
    return dict(INTEGRATION)


def microservices() -> dict[str, Any]:
    return {
        "present_required": True,
        "services": [dict(s) for s in MICROSERVICES],
        "service_count": len(MICROSERVICES),
    }


def roadmap() -> dict[str, Any]:
    return dict(ROADMAP) | {"phase_count": len(ROADMAP["phases"])}


def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p219_n": True}


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "primary_capability": PRIMARY_CAPABILITY, "principle": PRIMARY_CAPABILITY, "fabric": FABRIC,
        "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "planetary_gate": PLANETARY_GATE, "ai_os_gate": AI_OS_GATE,
        "simulation_gate": SIMULATION_GATE, "resources_gate": RESOURCES_GATE,
        "economy_gate": ECONOMY_GATE, "knowledge_gate": KNOWLEDGE_GATE,
        "human_gate": HUMAN_GATE, "governance_gate": GOVERNANCE_GATE,
        "innovation_gate": INNOVATION_GATE,
        "intelligence_nexus_gate": INTELLIGENCE_NEXUS_GATE, "space_gate": SPACE_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": [
            "P219-L", "P219-K", "P219-J", "P219-I", "P219-H", "P219-G", "P219-F", "P219-E", "P219-D",
            "P219-C", "P219-B", "P219-A", "P219",
            "P218-Z", "P218", "P217-Z", "P216-Z", "P215-Z", "P214-Z", "ADR-565",
        ],
        "vision": vision_pack(),
        "architecture": architecture(),
        "risk": risk(),
        "threat": threat(),
        "resilience": resilience(),
        "adaptive": adaptive(),
        "digital_twin": digital_twin(),
        "agents": agents(),
        "knowledge_graph": knowledge_graph(),
        "bounded_contexts": bounded_contexts(),
        "aggregates": aggregates(),
        "events": events(),
        "cqrs": cqrs(),
        "integration": integration(),
        "microservices": microservices(),
        "roadmap": roadmap(),
        "production_readiness": production_readiness(),
        "civilization_security_intelligence_platform_present_required": True,
        "global_risk_intelligence_platform_present_required": True,
        "threat_intelligence_network_present_required": True,
        "adaptive_security_architecture_present_required": True,
        "civilization_resilience_platform_present_required": True,
        "security_digital_twin_present_required": True,
        "meos_civilization_security_intelligence_core_present_required": True,
        "security_knowledge_graph_present_required": True,
        "security_event_architecture_present_required": True,
        "security_cqrs_model_present_required": True,
        "meos_security_integration_map_present_required": True,
        "never_replace_p219_foundation": True,
        "never_replace_p219_a_mission": True,
        "never_replace_p219_b_strategy": True,
        "never_replace_p219_c_domain": True,
        "never_replace_p219_d_planetary": True,
        "never_replace_p219_e_ai_os": True,
        "never_replace_p219_f_simulation": True,
        "never_replace_p219_g_resources": True,
        "never_replace_p219_h_economy": True,
        "never_replace_p219_i_knowledge": True,
        "never_replace_p219_j_human": True,
        "never_replace_p219_k_governance": True,
        "never_replace_p219_l_innovation": True,
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_identity": True,
        "never_replace_policy_engine": True,
        "never_replace_workflow": True,
        "never_replace_audit": True,
        "never_replace_p215_z": True,
        "never_replace_p216_z": True,
        "never_replace_biotechnology": True,
        "never_replace_space": True,
        "never_replace_p218_z_intelligence_nexus": True,
        "never_merge_p218_t_space_civilization": True,
        "never_cross_context_aggregate_imports": True,
        "never_opaque_unexplainable_security_decisions": True,
        "never_ungated_autonomous_security_response": True,
        "never_skip_human_authority_security": True,
        "never_skip_ethical_security_governance": True,
        "never_violate_human_sovereignty_security": True,
        "never_bypass_trusted_security_validation": True,
        "never_bypass_zero_trust_controls": True,
        "no_module_local_llm": True,
        "sibling_civilization_security_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/security",
        "forbidden_sibling_bc": [
            "civilization_security_intelligence_platform",
            "global_risk_intelligence_bc",
            "adaptive_security_architecture_bc",
        ],
        "foundation_for_p219_n": True,
    }


def security_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /civilization/security",
        "GET /civilization/security/architecture",
        "GET /civilization/security/risk",
        "GET /civilization/security/threat",
        "GET /civilization/security/resilience",
        "GET /civilization/security/adaptive",
        "GET /civilization/security/digital-twin",
        "GET /civilization/security/knowledge-graph",
        "GET /civilization/security/agents",
        "GET /civilization/security/bounded-contexts",
        "GET /civilization/security/aggregates",
        "GET /civilization/security/events",
        "GET /civilization/security/cqrs",
        "GET /civilization/security/integration",
        "GET /civilization/security/readiness",
    ]}
