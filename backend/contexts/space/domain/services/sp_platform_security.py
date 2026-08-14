"""P218-P Enterprise Space Intelligence Security Intelligence — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P218-P"
ADR = 542
SOR = "space"
API_PREFIX = "/api/v1/space"
PRODUCT = "Enterprise Space Intelligence Security Intelligence & MEOS Space Security Intelligence Platform"
CAPABILITY = "CAP-PLT-SP-001"
SECURITY_MISSION = (
    "Create an intelligent security ecosystem capable of detecting, preventing, responding to "
    "and recovering from cyber, physical, operational and strategic threats against space assets and infrastructure."
)
SECURITY_VISION = (
    "Transform fragmented space asset protection into an explainable, human-supervised, zero-trust "
    "security intelligence fabric spanning cyber defense, satellite protection, orbital threat intelligence "
    "and civilization-scale resilience."
)
FABRIC = "meos_space_security_intelligence_fabric"
FOUNDATION_GATE = "P218"
MISSION_GATE = "P218-A"
STRATEGY_GATE = "P218-B"
DOMAIN_GATE = "P218-C"
INFRASTRUCTURE_GATE = "P218-D"
SPACE_AI_GATE = "P218-E"
SATELLITE_GATE = "P218-F"
ORBITAL_GATE = "P218-G"
COMMUNICATIONS_GATE = "P218-H"
NAVIGATION_GATE = "P218-I"
MISSION_INTEL_GATE = "P218-J"
SCIENTIFIC_GATE = "P218-K"
EXPLORATION_GATE = "P218-L"
MANUFACTURING_GATE = "P218-M"
RESOURCES_GATE = "P218-N"
LOGISTICS_GATE = "P218-O"
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

ARCHITECTURE_LAYERS = (
    {"id": "L01", "name": "Space Asset Protection Layer", "components": ("satellites", "stations", "factories", "comms_nodes")},
    {"id": "L02", "name": "Cybersecurity Layer", "components": ("cyber_defense", "network_security", "command_security", "identity")},
    {"id": "L03", "name": "Threat Intelligence Layer", "components": ("detection", "prediction", "anomaly", "threat_kg")},
    {"id": "L04", "name": "Autonomous Defense Layer", "components": ("security_agents", "containment", "recovery", "decision_engine")},
    {"id": "L05", "name": "Strategic Resilience Layer", "components": ("continuity", "redundancy", "hardening", "governance")},
)
LIFECYCLE_STAGES = (
    "asset_registration", "identity_verification", "threat_monitoring", "threat_detection",
    "risk_assessment", "response_authorization", "response_execution", "containment",
    "recovery", "post_incident_review",
)
CYBERSECURITY = {
    "present_required": True,
    "platform": "meos_space_cybersecurity_platform",
    "domains": (
        "satellite_cybersecurity", "ground_station_security", "mission_control_security",
        "space_network_security", "communication_security", "navigation_security",
        "ai_system_security", "robotics_security",
    ),
    "capabilities": (
        "cyber_threat_detection", "intrusion_detection", "secure_command", "encrypted_communication",
        "identity_verification", "vulnerability_management", "security_monitoring", "incident_response",
    ),
}
SATELLITE_SECURITY = {
    "present_required": True,
    "platform": "meos_satellite_security_platform",
    "protected_assets": (
        "communication", "navigation", "earth_observation", "scientific", "industrial", "defense",
    ),
    "capabilities": (
        "satellite_identity", "secure_firmware", "secure_software_updates", "command_authentication",
        "telemetry_protection", "anomaly_detection", "autonomous_recovery",
    ),
}
ORBITAL_DEFENSE = {
    "present_required": True,
    "platform": "meos_orbital_defense_intelligence_platform",
    "domains": (
        "orbital_asset_protection", "space_situational_security", "collision_risk_management",
        "unauthorized_object_detection", "operational_threat_monitoring",
    ),
    "capabilities": (
        "threat_classification", "risk_prediction", "asset_protection",
        "security_coordination", "emergency_maneuver_support", "autonomous_response",
    ),
    "via_p218_g": True,
}
THREAT_INTEL = {
    "present_required": True,
    "platform": "meos_space_threat_intelligence_platform",
    "threat_categories": (
        "cyber", "physical", "operational_failures", "communication_disruption",
        "navigation_attacks", "ai_system_attacks", "infrastructure_failures",
    ),
    "ai_capabilities": (
        "threat_prediction", "attack_pattern_recognition", "behavior_analysis",
        "risk_scoring", "security_recommendations", "autonomous_detection",
    ),
}
SECURITY_AI = {
    "present_required": True,
    "platform": "meos_space_security_ai_platform",
    "capabilities": (
        "threat_prediction", "attack_pattern_recognition", "behavior_analysis", "risk_scoring",
        "security_recommendations", "autonomous_detection", "incident_correlation", "response_planning",
    ),
    "models": (
        {"id": "MODEL-01", "name": "Space Security Foundation Model"},
        {"id": "MODEL-02", "name": "Threat Intelligence Model"},
        {"id": "MODEL-03", "name": "Anomaly Detection Model"},
        {"id": "MODEL-04", "name": "Risk Prediction Model"},
        {"id": "MODEL-05", "name": "Security Response Model"},
    ),
    "via_p214_z": True,
    "via_p218_e": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
}
AUTONOMY = {
    "present_required": True,
    "platform": "meos_autonomous_security_operations_platform",
    "agents": (
        "threat_detection", "cyber_defense", "mission_protection", "satellite_protection",
        "recovery", "compliance", "risk_analysis",
    ),
    "functions": (
        "continuous_monitoring", "threat_assessment", "automated_response",
        "security_optimization", "incident_management", "recovery_coordination",
    ),
    "never_ungated_autonomous_security_response": True,
    "never_disable_human_override": True,
}
DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_space_security_digital_twin",
    "represents": ("satellites", "networks", "ground_systems", "stations", "factories", "communication_links", "mission_systems", "threat_scenarios"),
    "capabilities": ("security_simulation", "attack_simulation", "risk_analysis", "defense_testing", "recovery_validation", "resilience_planning", "security_forecasting"),
}
KNOWLEDGE_GRAPH = {
    "present_required": True,
    "platform": "meos_space_security_knowledge_graph",
    "entities": ("space_asset", "threat", "vulnerability", "security_policy", "incident", "attack_pattern", "response_action", "mission", "security_control"),
    "relationships": (
        "THREAT_TARGETS_ASSET", "ASSET_PROTECTED_BY_POLICY", "INCIDENT_TRIGGERED_RESPONSE",
        "VULNERABILITY_AFFECTS_SYSTEM", "SECURITY_CONTROL_MITIGATES_RISK",
    ),
    "capabilities": ("threat_reasoning", "risk_intelligence", "security_prediction", "attack_correlation", "defense_optimization"),
}
GOVERNANCE = {
    "present_required": True,
    "domains": (
        "space_security_governance", "cybersecurity_governance", "mission_protection_governance",
        "ai_security_governance", "data_security_governance", "infrastructure_security_governance",
        "access_governance", "incident_reviews",
    ),
    "approval_gates": (
        "policy_activation", "response_authorization", "recovery_authorization",
        "security_certification", "incident_closure", "compliance_attestation", "post_incident_review",
    ),
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "never_ungated_autonomous_security_response": True,
    "never_skip_command_authentication": True,
    "never_skip_satellite_identity_verification": True,
    "never_opaque_unexplainable_security_decisions": True,
}
OBSERVABILITY = {
    "present_required": True,
    "dashboards": (
        "threat_landscape", "asset_protection", "incident_pipeline", "cyber_posture",
        "satellite_security", "resilience", "security_ai", "compliance",
    ),
    "kpis": (
        "mean_time_to_detect", "mean_time_to_respond", "threat_neutralization_rate",
        "false_positive_rate", "asset_protection_coverage", "recovery_time_objective",
        "command_auth_success_rate", "human_override_rate", "compliance_score", "resilience_index",
    ),
}
BOUNDED_CONTEXTS = (
    {"id": "BC-SEC-01", "name": "Space Security Management"},
    {"id": "BC-SEC-02", "name": "Cyber Defense"},
    {"id": "BC-SEC-03", "name": "Threat Intelligence"},
    {"id": "BC-SEC-04", "name": "Satellite Protection"},
    {"id": "BC-SEC-05", "name": "Mission Security"},
    {"id": "BC-SEC-06", "name": "Incident Management"},
    {"id": "BC-SEC-07", "name": "Security Governance"},
    {"id": "BC-SEC-08", "name": "Resilience Management"},
)
SECURITY = {
    "present_required": True,
    "controls": (
        "zero_trust_space", "command_authentication", "satellite_identity", "encrypted_comms",
        "human_override", "audit_trail", "quantum_ready_crypto", "defense_in_depth",
    ),
    "via_identity": True, "via_policy_engine": True, "via_workflow": True,
    "via_audit": True, "via_integration": True,
    "via_p215_z": True,
    "never_ungated_autonomous_security_response": True,
    "never_skip_command_authentication": True,
    "never_skip_satellite_identity_verification": True,
    "never_opaque_unexplainable_security_decisions": True,
    "never_replace_p218_o_logistics": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
}
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p218_foundation", "p218a_mission", "p218b_strategy", "p218c_domain",
        "p218d_infrastructure", "p218e_space_ai", "p218f_satellite", "p218g_orbital",
        "p218h_communications", "p218i_navigation", "p218j_mission_intel", "p218k_scientific",
        "p218l_exploration", "p218m_manufacturing", "p218n_resources", "p218o_logistics",
        "p217z_bio_nexus", "p216z_robotics_supreme", "p215z_quantum_supreme", "p214z_ai_master",
        "policy_engine", "workflow", "audit", "identity", "integration_platform",
        "knowledge_graph", "digital_twin", "security_fabric",
    ),
    "mechanisms": ("api_gateway", "event_bus", "acl_peer_ids_only", "outbox", "versioned_contracts"),
}
DEPLOYMENT = {
    "present_required": True,
    "environments": ("security_ops", "threat_simulation", "incident_response", "security_archive"),
    "cloud_native": True,
    "safety_critical": True,
    "quantum_ready": True,
}
COMMANDS = (
    "RegisterSpaceAssetCommand", "VerifySatelliteIdentityCommand", "DetectThreatCommand",
    "AuthorizeSecurityResponseCommand", "ExecuteIncidentResponseCommand", "ActivateRecoveryCommand",
    "NeutralizeThreatCommand", "CloseSecurityIncidentCommand",
)
QUERIES = (
    "GetSpaceAssetQuery", "GetThreatEventQuery", "GetSecurityIncidentQuery",
    "GetSecurityPolicyQuery", "GetRiskScoreQuery", "GetRecoveryPlanQuery",
)
CORE_EVENTS = (
    {"name": "ThreatDetectedEvent", "schema": "space.security.threat.detected.v1", "owner": "BC-SEC-03"},
    {"name": "CyberAttackIdentifiedEvent", "schema": "space.security.cyber.attack.identified.v1", "owner": "BC-SEC-02"},
    {"name": "SecurityPolicyActivatedEvent", "schema": "space.security.policy.activated.v1", "owner": "BC-SEC-07"},
    {"name": "IncidentCreatedEvent", "schema": "space.security.incident.created.v1", "owner": "BC-SEC-06"},
    {"name": "ResponseExecutedEvent", "schema": "space.security.response.executed.v1", "owner": "BC-SEC-06"},
    {"name": "AssetProtectedEvent", "schema": "space.security.asset.protected.v1", "owner": "BC-SEC-04"},
    {"name": "RecoveryStartedEvent", "schema": "space.security.recovery.started.v1", "owner": "BC-SEC-08"},
    {"name": "ThreatNeutralizedEvent", "schema": "space.security.threat.neutralized.v1", "owner": "BC-SEC-03"},
    {"name": "MissionSecurityRestoredEvent", "schema": "space.security.mission.restored.v1", "owner": "BC-SEC-05"},
    {"name": "SatelliteIdentityVerifiedEvent", "schema": "space.security.satellite.identity.verified.v1", "owner": "BC-SEC-04"},
)
MICROSERVICES = (
    {"id": "security_intel_service", "api": "/space/security", "events": ("ThreatDetectedEvent",)},
    {"id": "cybersecurity_service", "api": "/space/security/cybersecurity", "events": ("CyberAttackIdentifiedEvent",)},
    {"id": "satellite_security_service", "api": "/space/security/satellite", "events": ("SatelliteIdentityVerifiedEvent",)},
    {"id": "orbital_defense_service", "api": "/space/security/orbital-defense", "events": ("AssetProtectedEvent",)},
    {"id": "threat_intel_service", "api": "/space/security/threat-intelligence", "events": ("ThreatNeutralizedEvent",)},
    {"id": "security_ai_service", "api": "/space/security/security-ai", "events": ("IncidentCreatedEvent",)},
    {"id": "security_twin_service", "api": "/space/security/digital-twin", "events": ("RecoveryStartedEvent",)},
    {"id": "security_observability_service", "api": "/space/security/observability", "events": ("MissionSecurityRestoredEvent",)},
    {"id": "security_governance_service", "api": "/space/security/governance", "events": ("SecurityPolicyActivatedEvent",)},
    {"id": "security_controls_service", "api": "/space/security/controls", "events": ("ResponseExecutedEvent",)},
)
TESTING = (
    "security_lifecycle_testing", "cyber_defense_testing", "satellite_identity_testing",
    "threat_intelligence_testing", "security_ai_explainability_testing", "digital_twin_attack_sim_testing",
    "autonomous_response_gate_testing", "command_authentication_gate_testing",
)
ROADMAP_PHASES = (
    {"phase": 1, "name": "Space Security Foundation"},
    {"phase": 2, "name": "Autonomous Cyber Defense"},
    {"phase": 3, "name": "Space Resilience"},
    {"phase": 4, "name": "Space Civilization Security Network"},
)
QUALITY_GATES_REJECT_IF = (
    "space_security_platform_is_missing", "space_cybersecurity_is_missing",
    "satellite_security_is_missing", "space_defense_intelligence_is_missing",
    "threat_intelligence_is_missing", "autonomous_security_operations_is_missing",
    "security_digital_twin_is_missing", "knowledge_graph_is_missing",
    "governance_is_missing", "security_architecture_is_missing",
    "ungated_autonomous_security_response", "skip_command_authentication",
    "skip_satellite_identity_verification", "opaque_unexplainable_security_decisions",
    "replace_p218_o_logistics", "module_local_llm", "sibling_space_bc",
)


def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Space Security Intelligence Fabric", "mission": SECURITY_MISSION,
        "vision": SECURITY_VISION, "builds_on_p218": True,
        **{f"builds_on_p218_{x.lower()}": True for x in "ABCDEFGHIJKLMNO"},
        "builds_on_p217_z": True, "builds_on_p216_z": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "never_replace_p218_o_logistics": True,
        "never_ungated_autonomous_security_response": True,
        "never_skip_command_authentication": True,
        "never_skip_satellite_identity_verification": True,
        "never_opaque_unexplainable_security_decisions": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
    }


def architecture() -> dict[str, Any]:
    return {"present_required": True, "layers": [dict(x) for x in ARCHITECTURE_LAYERS], "layer_count": len(ARCHITECTURE_LAYERS)}


def lifecycle() -> dict[str, Any]:
    return {
        "present_required": True, "stages": list(LIFECYCLE_STAGES), "stage_count": len(LIFECYCLE_STAGES),
        "autonomous_security_response_gated": True, "command_authentication_required": True,
        "satellite_identity_verification_required": True, "human_override_required": True,
    }


def cybersecurity() -> dict[str, Any]:
    return dict(CYBERSECURITY) | {"domain_count": len(CYBERSECURITY["domains"]), "capability_count": len(CYBERSECURITY["capabilities"])}


def satellite_security() -> dict[str, Any]:
    return dict(SATELLITE_SECURITY) | {"protected_asset_count": len(SATELLITE_SECURITY["protected_assets"]), "capability_count": len(SATELLITE_SECURITY["capabilities"])}


def orbital_defense() -> dict[str, Any]:
    return dict(ORBITAL_DEFENSE) | {"domain_count": len(ORBITAL_DEFENSE["domains"]), "capability_count": len(ORBITAL_DEFENSE["capabilities"])}


def threat_intelligence() -> dict[str, Any]:
    return dict(THREAT_INTEL) | {"threat_category_count": len(THREAT_INTEL["threat_categories"]), "ai_capability_count": len(THREAT_INTEL["ai_capabilities"])}


def security_ai() -> dict[str, Any]:
    return dict(SECURITY_AI) | {"capability_count": len(SECURITY_AI["capabilities"]), "model_count": len(SECURITY_AI["models"])}


def autonomy() -> dict[str, Any]:
    return dict(AUTONOMY) | {"agent_count": len(AUTONOMY["agents"]), "function_count": len(AUTONOMY["functions"])}


def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN) | {"representation_count": len(DIGITAL_TWIN["represents"]), "capability_count": len(DIGITAL_TWIN["capabilities"])}


def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH) | {"entity_count": len(KNOWLEDGE_GRAPH["entities"]), "relationship_count": len(KNOWLEDGE_GRAPH["relationships"]), "capability_count": len(KNOWLEDGE_GRAPH["capabilities"])}


def governance() -> dict[str, Any]:
    return dict(GOVERNANCE) | {"domain_count": len(GOVERNANCE["domains"]), "approval_gate_count": len(GOVERNANCE["approval_gates"])}


def observability() -> dict[str, Any]:
    return dict(OBSERVABILITY) | {"dashboard_count": len(OBSERVABILITY["dashboards"]), "kpi_count": len(OBSERVABILITY["kpis"])}


def security() -> dict[str, Any]:
    return dict(SECURITY)


def bounded_contexts() -> dict[str, Any]:
    return {"present_required": True, "contexts": [dict(x) for x in BOUNDED_CONTEXTS], "context_count": len(BOUNDED_CONTEXTS)}


def integration() -> dict[str, Any]:
    return dict(INTEGRATION)


def deployment() -> dict[str, Any]:
    return dict(DEPLOYMENT)


def cqrs() -> dict[str, Any]:
    return {"present_required": True, "commands": list(COMMANDS), "queries": list(QUERIES)}


def events() -> dict[str, Any]:
    return {"present_required": True, "core_events": [dict(x) for x in CORE_EVENTS], "core_event_count": len(CORE_EVENTS)}


def microservices() -> dict[str, Any]:
    return {"present_required": True, "services": [dict(x) for x in MICROSERVICES], "service_count": len(MICROSERVICES)}


def testing() -> dict[str, Any]:
    return {"present_required": True, "suites": list(TESTING)}


def roadmap() -> dict[str, Any]:
    return {"present_required": True, "phases": [dict(x) for x in ROADMAP_PHASES], "phase_count": len(ROADMAP_PHASES)}


def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF)}


def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p218_q": True}


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT,
        "capability": CAPABILITY, "security_mission": SECURITY_MISSION,
        "security_vision": SECURITY_VISION, "principle": SECURITY_MISSION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "infrastructure_gate": INFRASTRUCTURE_GATE, "space_ai_gate": SPACE_AI_GATE,
        "satellite_gate": SATELLITE_GATE, "orbital_gate": ORBITAL_GATE,
        "communications_gate": COMMUNICATIONS_GATE, "navigation_gate": NAVIGATION_GATE,
        "mission_intel_gate": MISSION_INTEL_GATE, "scientific_gate": SCIENTIFIC_GATE,
        "exploration_gate": EXPLORATION_GATE, "manufacturing_gate": MANUFACTURING_GATE,
        "resources_gate": RESOURCES_GATE, "logistics_gate": LOGISTICS_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P218"] + [f"P218-{x}" for x in "ABCDEFGHIJKLMNO"] + ["P217-Z", "P216-Z", "P215-Z", "P214-Z"] + [f"ADR-{i}" for i in range(526, 542)],
        "vision": vision_pack(), "architecture": architecture(), "lifecycle": lifecycle(),
        "cybersecurity": cybersecurity(), "satellite_security": satellite_security(),
        "orbital_defense": orbital_defense(), "threat_intelligence": threat_intelligence(),
        "security_ai": security_ai(), "autonomy": autonomy(),
        "digital_twin": digital_twin(), "knowledge_graph": knowledge_graph(),
        "governance": governance(), "observability": observability(), "security": security(),
        "bounded_contexts": bounded_contexts(), "integration": integration(),
        "deployment": deployment(), "cqrs": cqrs(), "events": events(),
        "microservices": microservices(), "testing": testing(), "roadmap": roadmap(),
        "quality_gates": quality_gates(), "production_readiness": production_readiness(),
        "space_security_platform_present_required": True,
        "space_cybersecurity_present_required": True,
        "satellite_security_present_required": True,
        "space_defense_intelligence_present_required": True,
        "threat_intelligence_present_required": True,
        "autonomous_security_operations_present_required": True,
        "security_digital_twin_present_required": True,
        "knowledge_graph_present_required": True,
        "ddd_model_present_required": True, "governance_present_required": True,
        "security_architecture_present_required": True, "observability_present_required": True,
        "deployment_architecture_present_required": True, "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True, "microservices_architecture_present_required": True,
        "sibling_space_bc_forbidden": True,
        "never_replace_p218_o_logistics": True,
        "never_ungated_autonomous_security_response": True,
        "never_skip_command_authentication": True,
        "never_skip_satellite_identity_verification": True,
        "never_opaque_unexplainable_security_decisions": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
        "api_prefix": f"{API_PREFIX}/security",
        "forbidden_sibling_bc": ["space_security_platform", "space_cybersecurity_bc", "orbital_defense_bc"],
        "foundation_for_p218_q": True,
    }


def security_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /space/security", "GET /space/security/vision",
        "GET /space/security/architecture", "GET /space/security/lifecycle",
        "GET /space/security/cybersecurity", "GET /space/security/satellite",
        "GET /space/security/orbital-defense", "GET /space/security/threat-intelligence",
        "GET /space/security/security-ai", "GET /space/security/autonomy",
        "GET /space/security/digital-twin", "GET /space/security/knowledge-graph",
        "GET /space/security/observability", "GET /space/security/governance",
        "GET /space/security/controls", "GET /space/security/integration",
        "GET /space/security/deployment", "GET /space/security/testing",
        "GET /space/security/cqrs", "GET /space/security/events",
        "GET /space/security/readiness",
    ]}
