"""P218-Q Enterprise Space Intelligence Sustainability Intelligence — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P218-Q"
ADR = 543
SOR = "space"
API_PREFIX = "/api/v1/space"
PRODUCT = "Enterprise Space Intelligence Sustainability Intelligence & MEOS Space Sustainability Intelligence Platform"
CAPABILITY = "CAP-PLT-SP-001"
SUSTAINABILITY_MISSION = (
    "Create an intelligent sustainability platform capable of monitoring, protecting, governing and "
    "optimizing the long-term health of orbital, lunar, planetary and deep-space environments."
)
SUSTAINABILITY_VISION = (
    "Transform fragmented orbital and planetary environmental stewardship into an explainable, "
    "human-supervised sustainability intelligence fabric spanning debris management, space governance "
    "and intergenerational responsibility."
)
FABRIC = "meos_space_sustainability_intelligence_fabric"
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
SECURITY_GATE = "P218-P"
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

ARCHITECTURE_LAYERS = (
    {"id": "L01", "name": "Space Environment Observation Layer", "components": ("orbital_sensors", "telescopes", "env_satellites", "planetary_sensors")},
    {"id": "L02", "name": "Environmental Intelligence Layer", "components": ("env_ai", "debris_detection", "risk_prediction", "impact_assessment")},
    {"id": "L03", "name": "Sustainability Operations Layer", "components": ("debris_mgmt", "cleanup", "mission_sustainability", "lifecycle")},
    {"id": "L04", "name": "Governance Intelligence Layer", "components": ("policy_engine", "compliance", "standards", "coordination")},
    {"id": "L05", "name": "Civilization Sustainability Layer", "components": ("long_term_planning", "heritage", "intergenerational_gov")},
)
LIFECYCLE_STAGES = (
    "environment_registration", "orbital_monitoring", "debris_detection", "risk_assessment",
    "impact_assessment", "governance_review", "cleanup_authorization", "remediation_execution",
    "compliance_validation", "sustainability_reporting",
)
ORBITAL_ENVIRONMENT = {
    "present_required": True,
    "platform": "meos_orbital_environment_protection_platform",
    "protected_domains": ("leo", "meo", "geo", "lunar_orbit", "interplanetary_routes"),
    "capabilities": (
        "orbital_monitoring", "satellite_density_analysis", "collision_risk_assessment",
        "orbital_congestion_analysis", "environmental_impact_prediction", "operational_recommendations",
    ),
    "intelligence_functions": (
        "orbit_health_monitoring", "risk_forecasting", "operational_optimization", "sustainable_orbit_allocation",
    ),
}
DEBRIS_MANAGEMENT = {
    "present_required": True,
    "platform": "meos_space_debris_management_platform",
    "domains": (
        "inactive_satellites", "rocket_stages", "fragments", "micro_debris",
        "collision_risks", "abandoned_infrastructure",
    ),
    "capabilities": (
        "debris_detection", "object_tracking", "risk_classification",
        "collision_prediction", "removal_planning", "cleanup_coordination",
    ),
    "autonomous_functions": (
        "debris_identification_agent", "collision_prediction_agent",
        "cleanup_planning_agent", "risk_mitigation_agent",
    ),
}
AUTONOMY = {
    "present_required": True,
    "platform": "meos_autonomous_orbital_management_platform",
    "agents": (
        "orbital_guardian", "environment_monitoring", "debris_management",
        "sustainability_advisor", "governance_compliance",
    ),
    "capabilities": (
        "autonomous_maneuver_recommendations", "collision_avoidance", "orbit_optimization",
        "traffic_coordination", "resource_sharing", "mission_adaptation",
    ),
    "never_ungated_debris_cleanup_mission": True,
    "never_disable_human_override": True,
}
SUSTAINABILITY_AI = {
    "present_required": True,
    "platform": "meos_space_sustainability_ai_platform",
    "capabilities": (
        "environmental_prediction", "debris_forecasting", "risk_modeling",
        "sustainability_optimization", "policy_analysis", "mission_impact_assessment",
    ),
    "models": (
        {"id": "MODEL-01", "name": "Space Sustainability Foundation Model"},
        {"id": "MODEL-02", "name": "Orbital Environment Model"},
        {"id": "MODEL-03", "name": "Debris Prediction Model"},
        {"id": "MODEL-04", "name": "Policy Intelligence Model"},
        {"id": "MODEL-05", "name": "Environmental Impact Model"},
        {"id": "MODEL-06", "name": "Governance Reasoning Model"},
    ),
    "via_p214_z": True,
    "via_p218_e": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
}
SPACE_GOVERNANCE = {
    "present_required": True,
    "platform": "meos_space_governance_intelligence_platform",
    "domains": (
        "orbital_resource_governance", "space_traffic_governance", "mission_authorization",
        "environmental_compliance", "commercial_space_governance", "planetary_protection",
    ),
    "capabilities": (
        "policy_monitoring", "compliance_automation", "regulation_analysis",
        "risk_governance", "international_coordination", "decision_support",
    ),
}
PLANETARY_PROTECTION = {
    "present_required": True,
    "platform": "meos_planetary_protection_intelligence_platform",
    "protected_environments": ("moon", "mars", "asteroids", "outer_planet_moons", "scientific_exploration_zones"),
    "capabilities": (
        "contamination_prevention", "scientific_preservation", "environmental_assessment",
        "mission_impact_analysis", "exploration_governance",
    ),
    "never_skip_planetary_protection_compliance": True,
}
DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_space_sustainability_digital_twin",
    "represents": (
        "orbital_environment", "space_objects", "debris_population", "missions",
        "satellites", "industrial_assets", "planetary_environments", "governance_policies",
    ),
    "capabilities": (
        "environmental_simulation", "debris_scenario_modeling", "collision_simulation",
        "policy_simulation", "sustainability_forecasting", "long_term_impact_analysis",
    ),
}
KNOWLEDGE_GRAPH = {
    "present_required": True,
    "platform": "meos_space_sustainability_knowledge_graph",
    "entities": (
        "space_object", "debris_object", "orbit", "mission", "policy",
        "regulation", "environmental_risk", "sustainability_metric", "governance_decision",
    ),
    "relationships": (
        "OBJECT_ORBITS_IN", "OBJECT_CREATES_RISK", "MISSION_IMPACTS_ENVIRONMENT",
        "POLICY_GOVERNS_OPERATION", "RISK_REQUIRES_ACTION", "DECISION_AFFECTS_SUSTAINABILITY",
    ),
    "capabilities": (
        "environmental_reasoning", "policy_intelligence", "risk_discovery", "governance_optimization",
    ),
}
GOVERNANCE = {
    "present_required": True,
    "domains": (
        "space_sustainability_governance", "orbital_environment_governance", "debris_governance",
        "planetary_protection_governance", "ai_sustainability_governance", "data_governance",
        "compliance_governance", "intergenerational_governance",
    ),
    "approval_gates": (
        "cleanup_authorization", "impact_assessment_approval", "policy_activation",
        "planetary_protection_validation", "sustainable_operation_approval",
        "compliance_attestation", "sustainability_reporting",
    ),
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "never_ungated_debris_cleanup_mission": True,
    "never_skip_planetary_protection_compliance": True,
    "never_skip_environmental_impact_assessment": True,
    "never_opaque_unexplainable_sustainability_decisions": True,
}
OBSERVABILITY = {
    "present_required": True,
    "dashboards": (
        "orbital_environment_health", "debris_population", "collision_risk_map",
        "sustainability_score", "mission_impact", "governance_status", "compliance_status",
    ),
    "kpis": (
        "orbital_sustainability_index", "debris_reduction_rate", "collision_risk_reduction",
        "mission_sustainability_score", "compliance_rate", "environmental_impact_score",
        "space_traffic_efficiency", "long_term_sustainability_forecast",
    ),
}
BOUNDED_CONTEXTS = (
    {"id": "BC-SUS-01", "name": "Space Environment Management"},
    {"id": "BC-SUS-02", "name": "Debris Management"},
    {"id": "BC-SUS-03", "name": "Orbital Governance"},
    {"id": "BC-SUS-04", "name": "Sustainability Analytics"},
    {"id": "BC-SUS-05", "name": "Planetary Protection"},
    {"id": "BC-SUS-06", "name": "Policy Management"},
    {"id": "BC-SUS-07", "name": "Compliance Management"},
)
SECURITY = {
    "present_required": True,
    "controls": (
        "data_provenance", "policy_validation", "secure_governance_workflows",
        "audit_trails", "transparent_decision_records", "planetary_protection_gates",
        "environmental_impact_assessment", "human_override",
    ),
    "via_identity": True, "via_policy_engine": True, "via_workflow": True,
    "via_audit": True, "via_integration": True, "via_p218_p": True,
    "never_ungated_debris_cleanup_mission": True,
    "never_skip_planetary_protection_compliance": True,
    "never_skip_environmental_impact_assessment": True,
    "never_opaque_unexplainable_sustainability_decisions": True,
    "never_replace_p218_p_security": True,
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
        "p218p_security", "p217z_bio_nexus", "p216z_robotics_supreme", "p215z_quantum_supreme",
        "p214z_ai_master", "policy_engine", "workflow", "audit", "identity",
        "integration_platform", "knowledge_graph", "digital_twin", "governance_fabric",
    ),
    "mechanisms": ("api_gateway", "event_bus", "acl_peer_ids_only", "outbox", "versioned_contracts"),
}
DEPLOYMENT = {
    "present_required": True,
    "environments": ("sustainability_ops", "debris_simulation", "governance_review", "sustainability_archive"),
    "cloud_native": True,
    "safety_critical": True,
    "quantum_ready": True,
}
COMMANDS = (
    "RegisterSpaceObjectCommand", "DetectDebrisCommand", "AssessCollisionRiskCommand",
    "AuthorizeCleanupMissionCommand", "ValidatePlanetaryProtectionCommand",
    "ApproveSustainableOperationCommand", "UpdateSustainabilityPolicyCommand",
    "CloseSustainabilityAssessmentCommand",
)
QUERIES = (
    "GetSpaceObjectQuery", "GetDebrisObjectQuery", "GetOrbitHealthQuery",
    "GetSustainabilityIndexQuery", "GetPolicyStatusQuery", "GetComplianceLevelQuery",
)
CORE_EVENTS = (
    {"name": "SpaceObjectDetectedEvent", "schema": "space.sustainability.object.detected.v1", "owner": "BC-SUS-01"},
    {"name": "DebrisIdentifiedEvent", "schema": "space.sustainability.debris.identified.v1", "owner": "BC-SUS-02"},
    {"name": "CollisionRiskDetectedEvent", "schema": "space.sustainability.collision.risk.detected.v1", "owner": "BC-SUS-02"},
    {"name": "SustainabilityAssessmentCompletedEvent", "schema": "space.sustainability.assessment.completed.v1", "owner": "BC-SUS-04"},
    {"name": "PolicyUpdatedEvent", "schema": "space.sustainability.policy.updated.v1", "owner": "BC-SUS-06"},
    {"name": "ComplianceValidatedEvent", "schema": "space.sustainability.compliance.validated.v1", "owner": "BC-SUS-07"},
    {"name": "CleanupMissionScheduledEvent", "schema": "space.sustainability.cleanup.scheduled.v1", "owner": "BC-SUS-02"},
    {"name": "EnvironmentalRiskReducedEvent", "schema": "space.sustainability.risk.reduced.v1", "owner": "BC-SUS-01"},
    {"name": "SustainableOperationApprovedEvent", "schema": "space.sustainability.operation.approved.v1", "owner": "BC-SUS-03"},
    {"name": "PlanetaryProtectionValidatedEvent", "schema": "space.sustainability.planetary.protection.validated.v1", "owner": "BC-SUS-05"},
)
MICROSERVICES = (
    {"id": "sustainability_intel_service", "api": "/space/sustainability", "events": ("SpaceObjectDetectedEvent",)},
    {"id": "orbital_environment_service", "api": "/space/sustainability/orbital-environment", "events": ("EnvironmentalRiskReducedEvent",)},
    {"id": "debris_service", "api": "/space/sustainability/debris", "events": ("DebrisIdentifiedEvent",)},
    {"id": "autonomy_service", "api": "/space/sustainability/autonomy", "events": ("CollisionRiskDetectedEvent",)},
    {"id": "sustainability_ai_service", "api": "/space/sustainability/sustainability-ai", "events": ("SustainabilityAssessmentCompletedEvent",)},
    {"id": "governance_service", "api": "/space/sustainability/governance", "events": ("PolicyUpdatedEvent",)},
    {"id": "planetary_protection_service", "api": "/space/sustainability/planetary-protection", "events": ("PlanetaryProtectionValidatedEvent",)},
    {"id": "sustainability_twin_service", "api": "/space/sustainability/digital-twin", "events": ("CleanupMissionScheduledEvent",)},
    {"id": "sustainability_observability_service", "api": "/space/sustainability/observability", "events": ("ComplianceValidatedEvent",)},
    {"id": "sustainability_security_service", "api": "/space/sustainability/security", "events": ("SustainableOperationApprovedEvent",)},
)
TESTING = (
    "sustainability_lifecycle_testing", "orbital_environment_testing", "debris_detection_testing",
    "planetary_protection_testing", "sustainability_ai_explainability_testing",
    "digital_twin_debris_sim_testing", "debris_cleanup_gate_testing", "impact_assessment_gate_testing",
)
ROADMAP_PHASES = (
    {"phase": 1, "name": "Sustainability Foundation"},
    {"phase": 2, "name": "Autonomous Sustainability Operations"},
    {"phase": 3, "name": "Space Governance Intelligence"},
    {"phase": 4, "name": "Sustainable Space Civilization Layer"},
)
QUALITY_GATES_REJECT_IF = (
    "space_sustainability_platform_is_missing", "orbital_environment_protection_is_missing",
    "space_debris_management_is_missing", "space_governance_is_missing",
    "sustainability_ai_is_missing", "planetary_protection_is_missing",
    "digital_twin_is_missing", "knowledge_graph_is_missing",
    "governance_framework_is_missing", "sustainability_architecture_is_missing",
    "ungated_debris_cleanup_mission", "skip_planetary_protection_compliance",
    "skip_environmental_impact_assessment", "opaque_unexplainable_sustainability_decisions",
    "replace_p218_p_security", "module_local_llm", "sibling_space_bc",
)


def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Space Sustainability Intelligence Fabric", "mission": SUSTAINABILITY_MISSION,
        "vision": SUSTAINABILITY_VISION, "builds_on_p218": True,
        **{f"builds_on_p218_{x.lower()}": True for x in "ABCDEFGHIJKLMNOP"},
        "builds_on_p217_z": True, "builds_on_p216_z": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "never_replace_p218_p_security": True,
        "never_ungated_debris_cleanup_mission": True,
        "never_skip_planetary_protection_compliance": True,
        "never_skip_environmental_impact_assessment": True,
        "never_opaque_unexplainable_sustainability_decisions": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
    }


def architecture() -> dict[str, Any]:
    return {"present_required": True, "layers": [dict(x) for x in ARCHITECTURE_LAYERS], "layer_count": len(ARCHITECTURE_LAYERS)}


def lifecycle() -> dict[str, Any]:
    return {
        "present_required": True, "stages": list(LIFECYCLE_STAGES), "stage_count": len(LIFECYCLE_STAGES),
        "debris_cleanup_gated": True, "planetary_protection_required": True,
        "environmental_impact_assessment_required": True, "human_override_required": True,
    }


def orbital_environment() -> dict[str, Any]:
    return dict(ORBITAL_ENVIRONMENT) | {
        "protected_domain_count": len(ORBITAL_ENVIRONMENT["protected_domains"]),
        "capability_count": len(ORBITAL_ENVIRONMENT["capabilities"]),
        "intelligence_function_count": len(ORBITAL_ENVIRONMENT["intelligence_functions"]),
    }


def debris() -> dict[str, Any]:
    return dict(DEBRIS_MANAGEMENT) | {
        "domain_count": len(DEBRIS_MANAGEMENT["domains"]),
        "capability_count": len(DEBRIS_MANAGEMENT["capabilities"]),
        "autonomous_function_count": len(DEBRIS_MANAGEMENT["autonomous_functions"]),
    }


def autonomy() -> dict[str, Any]:
    return dict(AUTONOMY) | {"agent_count": len(AUTONOMY["agents"]), "capability_count": len(AUTONOMY["capabilities"])}


def sustainability_ai() -> dict[str, Any]:
    return dict(SUSTAINABILITY_AI) | {"capability_count": len(SUSTAINABILITY_AI["capabilities"]), "model_count": len(SUSTAINABILITY_AI["models"])}


def space_governance() -> dict[str, Any]:
    return dict(SPACE_GOVERNANCE) | {"domain_count": len(SPACE_GOVERNANCE["domains"]), "capability_count": len(SPACE_GOVERNANCE["capabilities"])}


def planetary_protection() -> dict[str, Any]:
    return dict(PLANETARY_PROTECTION) | {
        "protected_environment_count": len(PLANETARY_PROTECTION["protected_environments"]),
        "capability_count": len(PLANETARY_PROTECTION["capabilities"]),
    }


def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN) | {"representation_count": len(DIGITAL_TWIN["represents"]), "capability_count": len(DIGITAL_TWIN["capabilities"])}


def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH) | {
        "entity_count": len(KNOWLEDGE_GRAPH["entities"]),
        "relationship_count": len(KNOWLEDGE_GRAPH["relationships"]),
        "capability_count": len(KNOWLEDGE_GRAPH["capabilities"]),
    }


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
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p218_r": True}


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT,
        "capability": CAPABILITY, "sustainability_mission": SUSTAINABILITY_MISSION,
        "sustainability_vision": SUSTAINABILITY_VISION, "principle": SUSTAINABILITY_MISSION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "infrastructure_gate": INFRASTRUCTURE_GATE, "space_ai_gate": SPACE_AI_GATE,
        "satellite_gate": SATELLITE_GATE, "orbital_gate": ORBITAL_GATE,
        "communications_gate": COMMUNICATIONS_GATE, "navigation_gate": NAVIGATION_GATE,
        "mission_intel_gate": MISSION_INTEL_GATE, "scientific_gate": SCIENTIFIC_GATE,
        "exploration_gate": EXPLORATION_GATE, "manufacturing_gate": MANUFACTURING_GATE,
        "resources_gate": RESOURCES_GATE, "logistics_gate": LOGISTICS_GATE,
        "security_gate": SECURITY_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P218"] + [f"P218-{x}" for x in "ABCDEFGHIJKLMNOP"] + ["P217-Z", "P216-Z", "P215-Z", "P214-Z"] + [f"ADR-{i}" for i in range(526, 543)],
        "vision": vision_pack(), "architecture": architecture(), "lifecycle": lifecycle(),
        "orbital_environment": orbital_environment(), "debris": debris(),
        "autonomy": autonomy(), "sustainability_ai": sustainability_ai(),
        "space_governance": space_governance(), "planetary_protection": planetary_protection(),
        "digital_twin": digital_twin(), "knowledge_graph": knowledge_graph(),
        "governance": governance(), "observability": observability(), "security": security(),
        "bounded_contexts": bounded_contexts(), "integration": integration(),
        "deployment": deployment(), "cqrs": cqrs(), "events": events(),
        "microservices": microservices(), "testing": testing(), "roadmap": roadmap(),
        "quality_gates": quality_gates(), "production_readiness": production_readiness(),
        "space_sustainability_platform_present_required": True,
        "orbital_environment_protection_present_required": True,
        "space_debris_management_present_required": True,
        "space_governance_present_required": True,
        "sustainability_ai_present_required": True,
        "planetary_protection_present_required": True,
        "sustainability_digital_twin_present_required": True,
        "knowledge_graph_present_required": True,
        "ddd_model_present_required": True, "governance_framework_present_required": True,
        "sustainability_architecture_present_required": True, "observability_present_required": True,
        "deployment_architecture_present_required": True, "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True, "microservices_architecture_present_required": True,
        "sibling_space_bc_forbidden": True,
        "never_replace_p218_p_security": True,
        "never_ungated_debris_cleanup_mission": True,
        "never_skip_planetary_protection_compliance": True,
        "never_skip_environmental_impact_assessment": True,
        "never_opaque_unexplainable_sustainability_decisions": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
        "api_prefix": f"{API_PREFIX}/sustainability",
        "forbidden_sibling_bc": ["space_sustainability_platform", "space_debris_bc", "orbital_environment_bc"],
        "foundation_for_p218_r": True,
    }


def sustainability_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /space/sustainability", "GET /space/sustainability/vision",
        "GET /space/sustainability/architecture", "GET /space/sustainability/lifecycle",
        "GET /space/sustainability/orbital-environment", "GET /space/sustainability/debris",
        "GET /space/sustainability/autonomy", "GET /space/sustainability/sustainability-ai",
        "GET /space/sustainability/governance", "GET /space/sustainability/planetary-protection",
        "GET /space/sustainability/digital-twin", "GET /space/sustainability/knowledge-graph",
        "GET /space/sustainability/observability", "GET /space/sustainability/security",
        "GET /space/sustainability/integration", "GET /space/sustainability/deployment",
        "GET /space/sustainability/testing", "GET /space/sustainability/cqrs",
        "GET /space/sustainability/events", "GET /space/sustainability/readiness",
    ]}
