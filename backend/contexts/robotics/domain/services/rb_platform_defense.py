"""P216-U Enterprise Defense Intelligence — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P216-U"
ADR = 493
SOR = "robotics"
API_PREFIX = "/api/v1/robotics"
PRODUCT = (
    "Enterprise Robotics Military Robotics, Autonomous Defense Systems, "
    "Strategic Security Intelligence & National Defense AI Platform"
)
CAPABILITY = "CAP-PLT-RB-001"
DEFENSE_VISION = (
    "MEOS Defense Intelligence Platform SHALL unify military robotics management, "
    "strategic security intelligence, autonomous system governance and defense digital twins as "
    "intelligent participants within the MEOS Defense Intelligence Ecosystem."
)
MISSION = (
    "Create a secure, responsible, AI-enabled defense intelligence ecosystem "
    "that improves strategic awareness, supports human decision-making, "
    "enhances resilience and manages complex cyber-physical environments."
)
VISION = (
    "Every security asset, operational process, intelligence source, infrastructure element, "
    "defense system and strategic scenario shall become an intelligent participant "
    "inside the MEOS Defense Intelligence Ecosystem."
)
FABRIC = "meos_defense_intelligence_fabric"
FOUNDATION_GATE = "P216"
MISSION_GATE = "P216-A"
STRATEGY_GATE = "P216-B"
DOMAIN_GATE = "P216-C"
RUNTIME_GATE = "P216-D"
PHYSICAL_AI_GATE = "P216-E"
INDUSTRIAL_GATE = "P216-F"
LOGISTICS_GATE = "P216-G"
MOBILITY_GATE = "P216-H"
HEALTHCARE_GATE = "P216-I"
CONSTRUCTION_GATE = "P216-K"
PUBLIC_SAFETY_GATE = "P216-L"
RETAIL_GATE = "P216-O"
HOSPITALITY_GATE = "P216-P"
EDUCATION_GATE = "P216-Q"
FINANCE_GATE = "P216-R"
GOVERNMENT_GATE = "P216-T"
SUPREME_GATE = "P215-Z"
AI_GATE = "P214-Z"
CORE_DOMAIN = "enterprise_defense_intelligence"
AGGREGATE = "DefenseIntelligenceAggregate"

SUPPORTING_DOMAINS = (
    "strategic_intelligence",
    "defense_operations",
    "security_intelligence",
    "defense_robotics",
    "cyber_defense_intelligence",
    "infrastructure_protection",
    "risk_analysis",
    "resilience_management",
    "defense_analytics",
    "defense_digital_twin",
    "knowledge_intelligence",
    "governance_oversight",
)
ENTITIES = (
    "DefenseOrganization",
    "SecurityCommand",
    "MissionProfile",
    "DefenseAsset",
    "AutonomousSystem",
    "IntelligenceSource",
    "SecurityEvent",
    "RiskScenario",
    "DefenseRobot",
    "DefenseDigitalTwin",
    "StrategicPlan",
)
VALUE_OBJECTS = (
    "ThreatAssessment",
    "RiskLevel",
    "MissionPriority",
    "ReadinessScore",
    "SecurityStatus",
    "OperationalCapability",
    "ResilienceScore",
    "ComplianceStatus",
    "TrustLevel",
)
BOUNDED_CONTEXTS = (
    {"id": "BC-01", "name": "Strategic Intelligence Context", "responsibilities": ("intelligence_analysis", "strategic_assessment", "decision_support")},
    {"id": "BC-02", "name": "Defense Robotics Context", "responsibilities": ("autonomous_system_management", "robotics_lifecycle", "asset_intelligence")},
    {"id": "BC-03", "name": "Security Operations Context", "responsibilities": ("security_monitoring", "risk_analysis", "operational_awareness")},
    {"id": "BC-04", "name": "Cyber Defense Intelligence Context", "responsibilities": ("cyber_risk_analysis", "digital_infrastructure_protection", "threat_intelligence")},
    {"id": "BC-05", "name": "Mission Intelligence Context", "responsibilities": ("scenario_analysis", "operational_planning", "simulation_intelligence")},
    {"id": "BC-06", "name": "Defense Asset Intelligence Context", "responsibilities": ("asset_management", "capability_analysis", "lifecycle_intelligence")},
    {"id": "BC-07", "name": "Defense Digital Twin Context", "responsibilities": ("strategic_simulation", "infrastructure_modelling", "scenario_evaluation")},
    {"id": "BC-08", "name": "Defense Governance Context", "responsibilities": ("responsible_ai", "oversight", "compliance", "human_accountability")},
)
DEFENSE_ROBOTICS = {
    "present_required": True,
    "platform": "meos_defense_robotics_platform",
    "components": (
        "defense_robotics_registry",
        "autonomous_system_manager",
        "robotics_lifecycle_controller",
        "mission_intelligence_engine",
        "asset_monitoring_platform",
        "defense_operations_dashboard",
    ),
    "supported_systems": (
        "ground_robotics_systems",
        "aerial_robotics_systems",
        "maritime_robotics_systems",
        "inspection_robotics_systems",
        "infrastructure_monitoring_systems",
    ),
    "capabilities": (
        "asset_intelligence",
        "autonomous_monitoring",
        "operational_analytics",
        "system_coordination",
        "lifecycle_management",
    ),
}
STRATEGIC_INTELLIGENCE = {
    "present_required": True,
    "engine": "meos_strategic_intelligence_engine",
    "capabilities": (
        "data_fusion",
        "pattern_analysis",
        "scenario_modelling",
        "risk_assessment",
        "strategic_forecasting",
        "decision_intelligence",
    ),
    "models": (
        "strategic_intelligence_models",
        "risk_prediction_models",
        "scenario_analysis_models",
        "knowledge_reasoning_models",
        "anomaly_detection_models",
    ),
    "via_p214_z": True,
    "explainable_ai": True,
    "responsible_ai": True,
    "human_authorization_control": True,
}
AUTONOMOUS_GOVERNANCE = {
    "present_required": True,
    "platform": "meos_autonomous_system_governance_platform",
    "capabilities": (
        "system_monitoring",
        "operational_readiness_analysis",
        "lifecycle_management",
        "safety_validation",
        "human_authorization_workflows",
        "performance_optimisation",
    ),
    "human_authorization_required": True,
    "via_workflow": True,
}
DEFENSE_AI = {
    "present_required": True,
    "platform": "meos_defense_ai_platform",
    "capabilities": (
        "decision_support",
        "threat_intelligence",
        "anomaly_detection",
        "strategic_forecasting",
    ),
    "via_p214_z": True,
    "explainable_ai": True,
    "responsible_ai": True,
}
DEFENSE_DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_defense_digital_twin_platform",
    "represents": (
        "defense_infrastructure", "security_assets", "operational_environment",
        "communication_systems", "logistics_networks", "risk_scenarios", "strategic_models",
    ),
    "capabilities": (
        "scenario_simulation",
        "readiness_analysis",
        "resource_optimisation",
        "risk_modelling",
        "strategic_planning",
    ),
}
DEFENSE_KG = {
    "present_required": True,
    "graph": "meos_defense_knowledge_graph",
    "nodes": (
        "security_assets", "infrastructure", "organizations", "risks",
        "events", "policies", "intelligence_sources", "autonomous_systems",
    ),
    "relationships": (
        "depends_on", "protects", "impacts", "connected_to",
        "managed_by", "analysed_by", "governed_by",
    ),
    "enables": (
        "strategic_reasoning",
        "risk_intelligence",
        "security_analysis",
        "decision_support",
    ),
}
MISSION_INTELLIGENCE = {
    "present_required": True,
    "platform": "meos_mission_intelligence_platform",
    "capabilities": (
        "scenario_analysis",
        "operational_planning",
        "simulation_intelligence",
    ),
}
NATIONAL_RESILIENCE = {
    "present_required": True,
    "layer": "meos_national_resilience_intelligence_layer",
    "capabilities": (
        "resilience_planning",
        "readiness_tracking",
        "critical_infrastructure_awareness",
    ),
}
OBSERVABILITY = {
    "present_required": True,
    "platform": "meos_defense_observability_platform",
    "monitors": (
        "system_readiness",
        "security_events",
        "ai_performance",
        "asset_intelligence",
        "digital_twin_accuracy",
        "operational_reliability",
        "governance_compliance",
    ),
    "via_platform_observability": True,
}
SECURITY = {
    "present_required": True,
    "framework": "meos_defense_zero_trust_framework",
    "domains": (
        "identity_security",
        "system_integrity",
        "data_protection",
        "ai_model_security",
        "operational_security",
        "audit_governance",
        "human_oversight",
    ),
    "controls": (
        "strong_authentication",
        "encryption",
        "policy_enforcement",
        "continuous_monitoring",
        "ai_transparency",
        "access_governance",
    ),
    "zero_trust": True,
    "human_authorization_control": True,
    "responsible_ai_governance": True,
    "explainable_ai": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "via_integration_platform": True,
    "never_duplicate_public_safety_core_logic": True,
    "no_module_local_llm": True,
    "physical_ai_via_p214z_acl_only": True,
    "never_replace_p216_foundation": True,
    "never_replace_p216_t_government": True,
    "never_replace_p216_l_public_safety": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "ungated_physical_autonomy_strategy_forbidden": True,
    "opaque_safety_strategy_forbidden": True,
}
COMMANDS = (
    "RegisterDefenseAssetCommand",
    "AnalyseSecurityScenarioCommand",
    "ActivateAutonomousSystemCommand",
    "GenerateStrategicAssessmentCommand",
    "UpdateDefenseTwinCommand",
)
QUERIES = (
    "GetAssetStatusQuery",
    "GetSecurityAssessmentQuery",
    "GetRiskScenarioQuery",
    "GetStrategicAnalysisQuery",
    "GetDefenseTwinQuery",
)
CORE_EVENTS = (
    {"name": "SecurityEventDetectedEvent", "schema": "robotics.defense.security.event.detected.v1", "owner": "BC-03", "consumers": "risk,governance,audit"},
    {"name": "IntelligenceUpdatedEvent", "schema": "robotics.defense.intelligence.updated.v1", "owner": "BC-01", "consumers": "mission,twin,audit"},
    {"name": "AssetStatusChangedEvent", "schema": "robotics.defense.asset.status.changed.v1", "owner": "BC-06", "consumers": "robotics,twin,audit"},
    {"name": "ScenarioCompletedEvent", "schema": "robotics.defense.scenario.completed.v1", "owner": "BC-05", "consumers": "twin,analytics,audit"},
    {"name": "RiskAssessmentGeneratedEvent", "schema": "robotics.defense.risk.assessment.generated.v1", "owner": "BC-03", "consumers": "governance,workflow,audit"},
    {"name": "SystemReadinessUpdatedEvent", "schema": "robotics.defense.system.readiness.updated.v1", "owner": "BC-02", "consumers": "operations,twin,audit"},
)
MICROSERVICES = (
    {"id": "defense_intelligence_service", "bc": "BC-01", "api": "/robotics/defense/intelligence", "db": "robotics_*", "events": ("IntelligenceUpdatedEvent",), "security": ("robotics.write",), "scaling": "intel_workers", "responsibility": "Strategic intelligence projections via P214-Z"},
    {"id": "robotics_management_service", "bc": "BC-02", "api": "/robotics/defense/robots", "db": "robotics_*", "events": ("SystemReadinessUpdatedEvent", "AssetStatusChangedEvent"), "security": ("robotics.write",), "scaling": "robot_workers", "responsibility": "Defense robotics lifecycle and readiness"},
    {"id": "security_analytics_service", "bc": "BC-03", "api": "/robotics/defense/security", "db": "robotics_*", "events": ("SecurityEventDetectedEvent", "RiskAssessmentGeneratedEvent"), "security": ("robotics.write",), "scaling": "security_workers", "responsibility": "Security operations analytics"},
    {"id": "risk_intelligence_service", "bc": "BC-03", "api": "/robotics/defense/risk", "db": "robotics_*", "events": ("RiskAssessmentGeneratedEvent",), "security": ("robotics.write",), "scaling": "risk_workers", "responsibility": "Risk intelligence facets"},
    {"id": "scenario_simulation_service", "bc": "BC-05", "api": "/robotics/defense/scenarios", "db": "robotics_*", "events": ("ScenarioCompletedEvent",), "security": ("robotics.write",), "scaling": "scenario_workers", "responsibility": "Mission scenario simulation"},
    {"id": "asset_intelligence_service", "bc": "BC-06", "api": "/robotics/defense/assets", "db": "robotics_*", "events": ("AssetStatusChangedEvent",), "security": ("robotics.write",), "scaling": "asset_workers", "responsibility": "Defense asset intelligence"},
    {"id": "digital_twin_service", "bc": "BC-07", "api": "/robotics/defense/digital-twin", "db": "robotics_*", "events": ("ScenarioCompletedEvent", "SystemReadinessUpdatedEvent"), "security": ("robotics.read",), "scaling": "twin_workers", "responsibility": "Defense digital twin sync"},
    {"id": "knowledge_graph_service", "bc": "BC-07", "api": "/robotics/defense/knowledge-graph", "db": "robotics_*", "events": ("IntelligenceUpdatedEvent", "RiskAssessmentGeneratedEvent"), "security": ("robotics.read",), "scaling": "kg_workers", "responsibility": "Defense knowledge graph projections"},
    {"id": "governance_service", "bc": "BC-08", "api": "/robotics/defense/governance", "db": "robotics_*", "events": ("RiskAssessmentGeneratedEvent", "SecurityEventDetectedEvent"), "security": ("robotics.write",), "scaling": "governance_workers", "responsibility": "Human oversight and responsible AI governance"},
    {"id": "observability_service", "bc": "BC-08", "api": "/robotics/defense/observability", "db": "robotics_*", "events": ("SystemReadinessUpdatedEvent",), "security": ("robotics.read",), "scaling": "obs_workers", "responsibility": "Defense observability facets"},
)
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p216d_robotics_os",
        "p216e_physical_ai",
        "p216l_public_safety",
        "p216t_government",
        "p214z_ai_master",
        "p215z_quantum_supreme",
        "cybersecurity_platforms",
        "critical_infrastructure_platforms",
        "communication_platforms",
        "emergency_management_platforms",
        "enterprise_governance_platforms",
        "integration_platform",
    ),
    "mechanisms": (
        "defense_apis",
        "robot_mission_interfaces",
        "public_safety_via_peer_api",
        "government_via_peer_api",
        "cyber_via_integration_connectors",
        "defense_event_contracts",
    ),
    "via_p216_d": True,
    "via_p216_e": True,
    "via_p216_l": True,
    "via_p216_t": True,
    "via_p214_z": True,
    "via_p215_z": True,
    "via_p213": True,
    "via_integration_platform": True,
    "never_duplicate_public_safety_core_logic": True,
    "human_authorization_via_workflow": True,
}
DEPLOYMENT = {
    "present_required": True,
    "model": "hybrid_defense_intelligence_infrastructure",
    "includes": (
        "secure_edge_platform",
        "mission_computing_platform",
        "defense_cloud_platform",
        "ai_compute_infrastructure",
        "robotics_runtime_platform",
        "digital_twin_platform",
        "knowledge_graph_platform",
        "security_operations_platform",
    ),
    "deployment_models": (
        "enterprise_security_organization",
        "critical_infrastructure_network",
        "national_resilience_platform",
        "strategic_intelligence_ecosystem",
    ),
    "cloud_native": True,
    "edge_native": True,
}
TESTING = (
    "ai_validation_testing",
    "robotics_system_testing",
    "digital_twin_validation",
    "security_testing",
    "reliability_testing",
    "resilience_testing",
    "governance_testing",
    "human_oversight_testing",
)
API_SURFACES = (
    "/api/v1/robotics/defense",
    "/api/v1/robotics/defense/vision",
    "/api/v1/robotics/defense/domain",
    "/api/v1/robotics/defense/bounded-contexts",
    "/api/v1/robotics/defense/robotics",
    "/api/v1/robotics/defense/strategic-intelligence",
    "/api/v1/robotics/defense/autonomous-governance",
    "/api/v1/robotics/defense/ai",
    "/api/v1/robotics/defense/mission-intelligence",
    "/api/v1/robotics/defense/resilience",
    "/api/v1/robotics/defense/digital-twin",
    "/api/v1/robotics/defense/knowledge-graph",
    "/api/v1/robotics/defense/observability",
    "/api/v1/robotics/defense/security",
    "/api/v1/robotics/defense/cqrs",
    "/api/v1/robotics/defense/events",
    "/api/v1/robotics/defense/microservices",
    "/api/v1/robotics/defense/integration",
    "/api/v1/robotics/defense/deployment",
    "/api/v1/robotics/defense/testing",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
QUALITY_GATES_REJECT_IF = (
    "military_robotics_platform_is_missing",
    "strategic_intelligence_platform_is_missing",
    "autonomous_system_governance_is_missing",
    "defense_ai_platform_is_missing",
    "defense_digital_twin_is_missing",
    "security_knowledge_graph_is_missing",
    "security_architecture_is_missing",
    "human_oversight_architecture_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "cloud_edge_deployment_is_missing",
    "enterprise_defense_integration_is_missing",
    "testing_architecture_is_missing",
    "sibling_robotics_bc",
    "replace_p216_t_government",
    "replace_p216_l_public_safety",
    "duplicate_public_safety_core_logic",
    "module_local_llm",
    "ungated_physical_autonomy",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Defense Intelligence Fabric",
        "defense_vision": DEFENSE_VISION,
        "mission": MISSION,
        "vision": VISION,
        "builds_on_p216": True,
        "builds_on_p216_t": True,
        "builds_on_p216_l": True,
        "builds_on_p216_e": True,
        "builds_on_p216_d": True,
        "builds_on_p215_z": True,
        "builds_on_p214_z": True,
        "never_replace_p216_t_government": True,
        "never_replace_p216_l_public_safety": True,
        "foundation_gate": FOUNDATION_GATE,
        "government_gate": GOVERNMENT_GATE,
        "public_safety_gate": PUBLIC_SAFETY_GATE,
        "physical_ai_gate": PHYSICAL_AI_GATE,
        "runtime_gate": RUNTIME_GATE,
        "supreme_gate": SUPREME_GATE,
        "ai_gate": AI_GATE,
    }

def domain_model() -> dict[str, Any]:
    return {
        "present_required": True,
        "core_domain": CORE_DOMAIN,
        "aggregate": AGGREGATE,
        "supporting_domains": list(SUPPORTING_DOMAINS),
        "supporting_count": len(SUPPORTING_DOMAINS),
        "entities": list(ENTITIES),
        "entity_count": len(ENTITIES),
        "value_objects": list(VALUE_OBJECTS),
        "value_object_count": len(VALUE_OBJECTS),
    }

def bounded_contexts() -> dict[str, Any]:
    return {"present_required": True, "contexts": [dict(c) for c in BOUNDED_CONTEXTS], "context_count": len(BOUNDED_CONTEXTS)}

def robotics_platform() -> dict[str, Any]:
    return dict(DEFENSE_ROBOTICS)

def strategic_intelligence() -> dict[str, Any]:
    return dict(STRATEGIC_INTELLIGENCE)

def autonomous_governance() -> dict[str, Any]:
    return dict(AUTONOMOUS_GOVERNANCE)

def defense_ai() -> dict[str, Any]:
    return dict(DEFENSE_AI)

def mission_intelligence() -> dict[str, Any]:
    return dict(MISSION_INTELLIGENCE)

def resilience() -> dict[str, Any]:
    return dict(NATIONAL_RESILIENCE)

def digital_twin() -> dict[str, Any]:
    return dict(DEFENSE_DIGITAL_TWIN)

def knowledge_graph() -> dict[str, Any]:
    return dict(DEFENSE_KG)

def observability() -> dict[str, Any]:
    return dict(OBSERVABILITY)

def security() -> dict[str, Any]:
    return dict(SECURITY)

def cqrs() -> dict[str, Any]:
    return {"commands": list(COMMANDS), "command_count": len(COMMANDS), "queries": list(QUERIES), "query_count": len(QUERIES)}

def events() -> dict[str, Any]:
    return {"core_events": [dict(e) for e in CORE_EVENTS], "core_event_count": len(CORE_EVENTS)}

def microservices() -> dict[str, Any]:
    return {"services": [dict(s) for s in MICROSERVICES], "service_count": len(MICROSERVICES)}

def integration() -> dict[str, Any]:
    return dict(INTEGRATION)

def deployment() -> dict[str, Any]:
    return dict(DEPLOYMENT)

def testing() -> dict[str, Any]:
    return {"present_required": True, "suites": list(TESTING), "suite_count": len(TESTING)}

def api() -> dict[str, Any]:
    return {
        "surfaces": list(API_SURFACES),
        "styles": list(API_STYLES),
        "api_first_present_required": True,
        "government_gate_api": "/api/v1/robotics/government",
        "runtime_gate_api": "/api/v1/robotics/runtime",
    }

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p216_v": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "defense_vision": DEFENSE_VISION, "mission": MISSION, "vision": VISION, "principle": DEFENSE_VISION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE, "runtime_gate": RUNTIME_GATE,
        "physical_ai_gate": PHYSICAL_AI_GATE, "industrial_gate": INDUSTRIAL_GATE,
        "logistics_gate": LOGISTICS_GATE, "mobility_gate": MOBILITY_GATE,
        "healthcare_gate": HEALTHCARE_GATE, "construction_gate": CONSTRUCTION_GATE,
        "public_safety_gate": PUBLIC_SAFETY_GATE, "retail_gate": RETAIL_GATE,
        "hospitality_gate": HOSPITALITY_GATE, "education_gate": EDUCATION_GATE,
        "finance_gate": FINANCE_GATE, "government_gate": GOVERNMENT_GATE,
        "supreme_gate": SUPREME_GATE, "ai_gate": AI_GATE,
        "builds_on": [
            "P216", "P216-A", "P216-B", "P216-C", "P216-D", "P216-E", "P216-F", "P216-G", "P216-H",
            "P216-I", "P216-K", "P216-L", "P216-O", "P216-P", "P216-Q", "P216-R", "P216-T",
            "P215-Z", "P214-Z", "P213",
            "ADR-472", "ADR-473", "ADR-474", "ADR-475", "ADR-476", "ADR-477", "ADR-478", "ADR-479",
            "ADR-480", "ADR-481", "ADR-483", "ADR-484", "ADR-487", "ADR-488", "ADR-489", "ADR-490", "ADR-492",
        ],
        "vision_pack": vision_pack(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "robotics_platform": robotics_platform(),
        "strategic_intelligence": strategic_intelligence(),
        "autonomous_governance": autonomous_governance(),
        "defense_ai": defense_ai(),
        "mission_intelligence": mission_intelligence(),
        "resilience": resilience(),
        "digital_twin": digital_twin(),
        "knowledge_graph": knowledge_graph(),
        "observability": observability(),
        "security": security(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "integration": integration(),
        "deployment": deployment(),
        "testing": testing(),
        "api": api(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "military_robotics_platform_present_required": True,
        "strategic_intelligence_platform_present_required": True,
        "autonomous_system_governance_present_required": True,
        "defense_ai_platform_present_required": True,
        "defense_digital_twin_present_required": True,
        "security_knowledge_graph_present_required": True,
        "security_architecture_present_required": True,
        "human_oversight_architecture_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "cloud_edge_deployment_present_required": True,
        "enterprise_defense_integration_present_required": True,
        "testing_architecture_present_required": True,
        "sibling_robotics_bc_forbidden": True,
        "never_replace_p216_foundation": True,
        "never_replace_p216_a_mission": True,
        "never_replace_p216_b_strategy": True,
        "never_replace_p216_c_domain": True,
        "never_replace_p216_d_runtime": True,
        "never_replace_p216_e_physical_ai": True,
        "never_replace_p216_f_industrial": True,
        "never_replace_p216_g_logistics": True,
        "never_replace_p216_h_mobility": True,
        "never_replace_p216_i_healthcare": True,
        "never_replace_p216_k_construction": True,
        "never_replace_p216_l_public_safety": True,
        "never_replace_p216_o_retail": True,
        "never_replace_p216_p_hospitality": True,
        "never_replace_p216_q_education": True,
        "never_replace_p216_r_finance": True,
        "never_replace_p216_t_government": True,
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_duplicate_public_safety_core_logic": True,
        "no_module_local_llm": True,
        "physical_ai_via_p214z_acl_only": True,
        "human_authorization_control_required": True,
        "responsible_ai_governance_required": True,
        "explainable_ai_required": True,
        "ungated_physical_autonomy_strategy_forbidden": True,
        "opaque_safety_strategy_forbidden": True,
        "builds_on_p216": True, "builds_on_p216_t": True, "builds_on_p216_l": True,
        "builds_on_p216_e": True, "builds_on_p216_d": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p216_d": True, "via_p216_e": True, "via_p216_l": True, "via_p216_t": True,
        "via_p215_z": True, "via_p214_z": True, "via_p213": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "via_integration_platform": True,
        "api_prefix": f"{API_PREFIX}/defense",
        "forbidden_sibling_bc": [
            "military_robotics_platform",
            "autonomous_defense_intelligence_platform",
            "strategic_security_intelligence_platform",
            "defense_ai_operations_platform",
        ],
        "foundation_for_p216_v": True,
        "p216_s_legal_planned": True,
        "p216_j_agriculture_planned": True,
        "p216_m_space_planned": True,
        "p216_n_environmental_planned": True,
    }

def defense_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /robotics/defense",
        "GET /robotics/defense/vision",
        "GET /robotics/defense/domain",
        "GET /robotics/defense/bounded-contexts",
        "GET /robotics/defense/robotics",
        "GET /robotics/defense/strategic-intelligence",
        "GET /robotics/defense/autonomous-governance",
        "GET /robotics/defense/ai",
        "GET /robotics/defense/mission-intelligence",
        "GET /robotics/defense/resilience",
        "GET /robotics/defense/digital-twin",
        "GET /robotics/defense/knowledge-graph",
        "GET /robotics/defense/observability",
        "GET /robotics/defense/security",
        "GET /robotics/defense/cqrs",
        "GET /robotics/defense/events",
        "GET /robotics/defense/microservices",
        "GET /robotics/defense/integration",
        "GET /robotics/defense/deployment",
        "GET /robotics/defense/testing",
        "GET /robotics/defense/readiness",
    ], "government_gate_routes": ["GET /robotics/government", "GET /robotics/government/readiness"]}
