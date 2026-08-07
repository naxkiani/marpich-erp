"""P218-L Enterprise Space Intelligence Exploration Intelligence — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P218-L"
ADR = 538
SOR = "space"
API_PREFIX = "/api/v1/space"
PRODUCT = "Enterprise Space Intelligence Exploration Intelligence & MEOS Space Exploration Intelligence Platform"
CAPABILITY = "CAP-PLT-SP-001"
EXPLORATION_MISSION = (
    "Provide an enterprise platform enabling autonomous, resilient and continuously learning "
    "exploration across the Moon, Mars, asteroids, outer planets and deep space."
)
EXPLORATION_VISION = (
    "Transform planetary exploration from isolated expeditions into an explainable, human-supervised, "
    "planetary-protection-compliant exploration intelligence fabric spanning lunar bases through deep-space expeditions."
)
FABRIC = "meos_space_exploration_intelligence_fabric"
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
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

ARCHITECTURE_LAYERS = (
    {"id": "L01", "name": "Exploration Assets", "components": ("crewed_vehicles", "rovers", "landers", "habitats")},
    {"id": "L02", "name": "Planetary Infrastructure", "components": ("landing_zones", "power", "comms_relays", "logistics_nodes")},
    {"id": "L03", "name": "Exploration Intelligence", "components": ("exploration_ai", "terrain", "hazard", "mission_recovery")},
    {"id": "L04", "name": "Operations Layer", "components": ("surface_ops", "crew_ops", "robot_ops", "emergency_response")},
    {"id": "L05", "name": "Knowledge Layer", "components": ("knowledge_graph", "planetary_atlas", "lessons_learned", "discovery_kb")},
)
LIFECYCLE_STAGES = (
    "mission_definition", "destination_selection", "landing_site_selection", "landing_authorization",
    "landing", "surface_deployment", "surface_operations", "scientific_campaign",
    "infrastructure_expansion", "mission_completion",
)
LUNAR = {
    "present_required": True,
    "platform": "meos_lunar_operations_platform",
    "capabilities": (
        "lunar_landing", "surface_mobility", "habitat_operations", "power_management", "isru",
        "scientific_campaigns", "crew_logistics", "surface_communications", "emergency_operations", "base_planning",
    ),
    "operational_zones": (
        "landing_area", "habitat_zone", "scientific_zone", "industrial_zone",
        "power_zone", "exploration_zone", "protected_heritage_zone",
    ),
}
MARS = {
    "present_required": True,
    "platform": "meos_mars_operations_platform",
    "capabilities": (
        "edl", "surface_navigation", "habitat_management", "life_support", "scientific_operations",
        "autonomous_logistics", "dust_storm_response", "emergency_recovery", "long_duration_support", "resource_extraction",
    ),
    "mission_types": (
        "human_exploration", "robotic_exploration", "cargo", "scientific", "infrastructure", "settlement_preparation",
    ),
}
DEEP_SPACE = {
    "present_required": True,
    "platform": "meos_deep_space_exploration_platform",
    "destinations": (
        "asteroids", "comets", "outer_planets", "moons", "lagrange_points", "interstellar_precursors",
    ),
    "capabilities": (
        "long_duration_planning", "comms_delay_management", "autonomous_mission_control", "radiation_risk",
        "scientific_prioritisation", "resource_optimisation", "mission_adaptation", "crew_autonomy",
    ),
}
EXPLORATION_AI = {
    "present_required": True,
    "platform": "meos_planetary_exploration_ai_platform",
    "capabilities": (
        "terrain_classification", "landing_site_selection", "path_planning", "scientific_target_ranking",
        "hazard_prediction", "mission_replanning", "resource_optimisation", "crew_decision_support",
        "robot_coordination", "environmental_forecasting",
    ),
    "models": (
        {"id": "MODEL-01", "name": "Exploration Foundation Model"},
        {"id": "MODEL-02", "name": "Planetary Terrain Model"},
        {"id": "MODEL-03", "name": "Hazard Intelligence Model"},
        {"id": "MODEL-04", "name": "Scientific Discovery Model"},
        {"id": "MODEL-05", "name": "Mission Adaptation Model"},
        {"id": "MODEL-06", "name": "Resource Optimisation Model"},
    ),
    "via_p214_z": True,
    "via_p218_e": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
}
AUTONOMY = {
    "present_required": True,
    "platform": "meos_autonomous_exploration_platform",
    "functions": (
        "navigation", "scientific_survey", "resource_mapping", "sample_collection",
        "infrastructure_inspection", "mission_adaptation", "fault_recovery", "collaborative_exploration",
    ),
    "agents": (
        "mission_commander", "lunar_operations", "mars_operations", "rover",
        "habitat", "scientific", "resource", "emergency",
    ),
    "via_p216_z": True,
    "never_disable_human_override": True,
}
DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_exploration_digital_twin",
    "represents": ("planetary_terrain", "habitats", "rovers", "crew", "infrastructure", "mission_timeline", "environment", "scientific_assets"),
    "capabilities": ("mission_simulation", "surface_simulation", "hazard_simulation", "mission_replay", "scenario_planning", "landing_validation", "expansion_planning", "infrastructure_forecasting"),
}
GOVERNANCE = {
    "present_required": True,
    "domains": (
        "mission_governance", "planetary_protection", "crew_safety", "scientific_integrity",
        "environmental_stewardship", "infrastructure_governance", "resource_governance", "exploration_ethics",
    ),
    "approval_gates": (
        "mission_review", "planetary_protection_compliance", "landing_authorization",
        "crew_safety_validation", "surface_ops_authorization", "hazard_response_authorization", "mission_closure",
    ),
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "never_skip_planetary_protection_compliance": True,
    "never_ungated_planetary_landing_authorization": True,
    "never_ungated_surface_hazard_response": True,
    "never_skip_crew_safety_validation": True,
}
OBSERVABILITY = {
    "present_required": True,
    "dashboards": (
        "mission_progress", "surface_operations", "crew_health", "robot_fleet",
        "habitat_status", "scientific_campaign", "resource_extraction", "environmental_monitoring", "exploration_ai",
    ),
    "kpis": (
        "mission_success_rate", "surface_coverage", "scientific_yield", "crew_safety_index",
        "autonomous_task_completion", "resource_recovery_rate", "mission_duration_efficiency",
        "infrastructure_availability", "operational_readiness", "exploration_productivity",
    ),
}
BOUNDED_CONTEXTS = (
    {"id": "BC-EX-01", "name": "Exploration Management"},
    {"id": "BC-EX-02", "name": "Lunar Operations"},
    {"id": "BC-EX-03", "name": "Mars Operations"},
    {"id": "BC-EX-04", "name": "Deep Space Operations"},
    {"id": "BC-EX-05", "name": "Planetary Infrastructure"},
    {"id": "BC-EX-06", "name": "Surface Mobility"},
    {"id": "BC-EX-07", "name": "Scientific Exploration"},
    {"id": "BC-EX-08", "name": "Exploration Governance"},
)
SECURITY = {
    "present_required": True,
    "controls": (
        "zero_trust", "exploration_authentication", "exploration_authorization", "landing_integrity",
        "planetary_protection", "human_override", "crew_safety", "hazard_response",
    ),
    "via_identity": True, "via_policy_engine": True, "via_workflow": True,
    "via_audit": True, "via_integration": True,
    "never_ungated_planetary_landing_authorization": True,
    "never_skip_planetary_protection_compliance": True,
    "never_ungated_surface_hazard_response": True,
    "never_skip_crew_safety_validation": True,
    "never_replace_p218_k_scientific": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
}
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p218_foundation", "p218a_mission", "p218b_strategy", "p218c_domain",
        "p218d_infrastructure", "p218e_space_ai", "p218f_satellite", "p218g_orbital",
        "p218h_communications", "p218i_navigation", "p218j_mission_intel", "p218k_scientific",
        "p217z_bio_nexus", "p216z_robotics_supreme", "p215z_quantum_supreme", "p214z_ai_master",
        "policy_engine", "workflow", "audit", "identity", "integration_platform",
        "knowledge_graph", "digital_twin",
    ),
    "mechanisms": ("api_gateway", "event_bus", "acl_peer_ids_only", "outbox", "versioned_contracts"),
}
DEPLOYMENT = {
    "present_required": True,
    "environments": ("exploration_planning", "surface_simulation", "planetary_operations", "exploration_archive"),
    "cloud_native": True,
    "safety_critical": True,
}
COMMANDS = (
    "CreateExplorationMissionCommand", "SelectLandingSiteCommand", "AuthorizePlanetaryLandingCommand",
    "StartSurfaceOperationsCommand", "ActivateHabitatCommand", "ReplanExplorationMissionCommand",
    "DeclareHazardResponseCommand", "CompleteExplorationMissionCommand",
)
QUERIES = (
    "GetExplorationMissionQuery", "GetLandingSiteQuery", "GetHabitatStatusQuery",
    "GetRoverFleetQuery", "GetScientificCampaignQuery", "GetTerrainRiskQuery",
)
CORE_EVENTS = (
    {"name": "ExplorationMissionCreatedEvent", "schema": "space.exploration.mission.created.v1", "owner": "BC-EX-01"},
    {"name": "LandingCompletedEvent", "schema": "space.exploration.landing.completed.v1", "owner": "BC-EX-02"},
    {"name": "SurfaceMissionStartedEvent", "schema": "space.exploration.surface.started.v1", "owner": "BC-EX-06"},
    {"name": "ScientificTargetIdentifiedEvent", "schema": "space.exploration.scientific.target.identified.v1", "owner": "BC-EX-07"},
    {"name": "SampleCollectedEvent", "schema": "space.exploration.sample.collected.v1", "owner": "BC-EX-07"},
    {"name": "HabitatActivatedEvent", "schema": "space.exploration.habitat.activated.v1", "owner": "BC-EX-05"},
    {"name": "HazardDetectedEvent", "schema": "space.exploration.hazard.detected.v1", "owner": "BC-EX-08"},
    {"name": "MissionReplannedEvent", "schema": "space.exploration.mission.replanned.v1", "owner": "BC-EX-01"},
    {"name": "ResourceConfirmedEvent", "schema": "space.exploration.resource.confirmed.v1", "owner": "BC-EX-05"},
    {"name": "ExplorationMissionCompletedEvent", "schema": "space.exploration.mission.completed.v1", "owner": "BC-EX-01"},
)
MICROSERVICES = (
    {"id": "exploration_intel_service", "api": "/space/exploration", "events": ("ExplorationMissionCreatedEvent",)},
    {"id": "lunar_ops_service", "api": "/space/exploration/lunar", "events": ("LandingCompletedEvent",)},
    {"id": "mars_ops_service", "api": "/space/exploration/mars", "events": ("SurfaceMissionStartedEvent",)},
    {"id": "deep_space_service", "api": "/space/exploration/deep-space", "events": ("MissionReplannedEvent",)},
    {"id": "exploration_ai_service", "api": "/space/exploration/exploration-ai", "events": ("HazardDetectedEvent",)},
    {"id": "autonomy_service", "api": "/space/exploration/autonomy", "events": ("SampleCollectedEvent",)},
    {"id": "exploration_twin_service", "api": "/space/exploration/digital-twin", "events": ("HabitatActivatedEvent",)},
    {"id": "exploration_observability_service", "api": "/space/exploration/observability", "events": ("ResourceConfirmedEvent",)},
    {"id": "exploration_governance_service", "api": "/space/exploration/governance", "events": ("ExplorationMissionCompletedEvent",)},
    {"id": "exploration_security_service", "api": "/space/exploration/security", "events": ("ScientificTargetIdentifiedEvent",)},
)
TESTING = (
    "exploration_lifecycle_testing", "lunar_operations_testing", "mars_operations_testing",
    "deep_space_delay_testing", "exploration_ai_explainability_testing", "autonomy_override_testing",
    "planetary_protection_gate_testing", "landing_authorization_gate_testing",
)
ROADMAP_PHASES = (
    {"phase": 1, "name": "Exploration Foundation"},
    {"phase": 2, "name": "Planetary Operations"},
    {"phase": 3, "name": "Autonomous Exploration"},
    {"phase": 4, "name": "Interplanetary Exploration Intelligence"},
)
QUALITY_GATES_REJECT_IF = (
    "space_exploration_platform_is_missing", "lunar_operations_platform_is_missing",
    "mars_operations_platform_is_missing", "deep_space_exploration_platform_is_missing",
    "exploration_ai_is_missing", "autonomous_exploration_is_missing",
    "exploration_digital_twin_is_missing", "governance_and_safety_is_missing",
    "security_architecture_is_missing", "observability_is_missing",
    "ungated_planetary_landing_authorization", "skip_planetary_protection_compliance",
    "ungated_surface_hazard_response", "skip_crew_safety_validation",
    "replace_p218_k_scientific", "module_local_llm", "sibling_space_bc",
)


def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Space Exploration Intelligence Fabric", "mission": EXPLORATION_MISSION,
        "vision": EXPLORATION_VISION, "builds_on_p218": True,
        **{f"builds_on_p218_{x.lower()}": True for x in "ABCDEFGHIJK"},
        "builds_on_p217_z": True, "builds_on_p216_z": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "never_replace_p218_k_scientific": True,
        "never_ungated_planetary_landing_authorization": True,
        "never_skip_planetary_protection_compliance": True,
        "never_ungated_surface_hazard_response": True,
        "never_skip_crew_safety_validation": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
    }


def architecture() -> dict[str, Any]:
    return {"present_required": True, "layers": [dict(x) for x in ARCHITECTURE_LAYERS], "layer_count": len(ARCHITECTURE_LAYERS)}


def lifecycle() -> dict[str, Any]:
    return {
        "present_required": True, "stages": list(LIFECYCLE_STAGES), "stage_count": len(LIFECYCLE_STAGES),
        "planetary_protection_required": True, "landing_authorization_gated": True,
        "crew_safety_validation_required": True,
    }


def lunar() -> dict[str, Any]:
    return dict(LUNAR) | {"capability_count": len(LUNAR["capabilities"]), "zone_count": len(LUNAR["operational_zones"])}


def mars() -> dict[str, Any]:
    return dict(MARS) | {"capability_count": len(MARS["capabilities"]), "mission_type_count": len(MARS["mission_types"])}


def deep_space() -> dict[str, Any]:
    return dict(DEEP_SPACE) | {"destination_count": len(DEEP_SPACE["destinations"]), "capability_count": len(DEEP_SPACE["capabilities"])}


def exploration_ai() -> dict[str, Any]:
    return dict(EXPLORATION_AI) | {"capability_count": len(EXPLORATION_AI["capabilities"]), "model_count": len(EXPLORATION_AI["models"])}


def autonomy() -> dict[str, Any]:
    return dict(AUTONOMY) | {"function_count": len(AUTONOMY["functions"]), "agent_count": len(AUTONOMY["agents"])}


def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN) | {"representation_count": len(DIGITAL_TWIN["represents"]), "capability_count": len(DIGITAL_TWIN["capabilities"])}


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
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p218_m": True}


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT,
        "capability": CAPABILITY, "exploration_mission": EXPLORATION_MISSION,
        "exploration_vision": EXPLORATION_VISION, "principle": EXPLORATION_MISSION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "infrastructure_gate": INFRASTRUCTURE_GATE, "space_ai_gate": SPACE_AI_GATE,
        "satellite_gate": SATELLITE_GATE, "orbital_gate": ORBITAL_GATE,
        "communications_gate": COMMUNICATIONS_GATE, "navigation_gate": NAVIGATION_GATE,
        "mission_intel_gate": MISSION_INTEL_GATE, "scientific_gate": SCIENTIFIC_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P218"] + [f"P218-{x}" for x in "ABCDEFGHIJK"] + ["P217-Z", "P216-Z", "P215-Z", "P214-Z"] + [f"ADR-{i}" for i in range(526, 538)],
        "vision": vision_pack(), "architecture": architecture(), "lifecycle": lifecycle(),
        "lunar": lunar(), "mars": mars(), "deep_space": deep_space(),
        "exploration_ai": exploration_ai(), "autonomy": autonomy(),
        "digital_twin": digital_twin(),
        "governance": governance(), "observability": observability(), "security": security(),
        "bounded_contexts": bounded_contexts(), "integration": integration(),
        "deployment": deployment(), "cqrs": cqrs(), "events": events(),
        "microservices": microservices(), "testing": testing(), "roadmap": roadmap(),
        "quality_gates": quality_gates(), "production_readiness": production_readiness(),
        "space_exploration_platform_present_required": True,
        "lunar_operations_platform_present_required": True,
        "mars_operations_platform_present_required": True,
        "deep_space_exploration_platform_present_required": True,
        "exploration_ai_present_required": True,
        "autonomous_exploration_present_required": True,
        "exploration_digital_twin_present_required": True,
        "ddd_model_present_required": True, "governance_and_safety_present_required": True,
        "security_architecture_present_required": True, "observability_present_required": True,
        "deployment_architecture_present_required": True, "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True, "microservices_architecture_present_required": True,
        "sibling_space_bc_forbidden": True,
        "never_replace_p218_k_scientific": True,
        "never_ungated_planetary_landing_authorization": True,
        "never_skip_planetary_protection_compliance": True,
        "never_ungated_surface_hazard_response": True,
        "never_skip_crew_safety_validation": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
        "api_prefix": f"{API_PREFIX}/exploration",
        "forbidden_sibling_bc": ["space_exploration_platform", "lunar_operations_bc", "mars_operations_bc"],
        "foundation_for_p218_m": True,
    }


def exploration_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /space/exploration", "GET /space/exploration/vision",
        "GET /space/exploration/architecture", "GET /space/exploration/lifecycle",
        "GET /space/exploration/lunar", "GET /space/exploration/mars",
        "GET /space/exploration/deep-space", "GET /space/exploration/exploration-ai",
        "GET /space/exploration/autonomy", "GET /space/exploration/digital-twin",
        "GET /space/exploration/observability", "GET /space/exploration/governance",
        "GET /space/exploration/security", "GET /space/exploration/integration",
        "GET /space/exploration/deployment", "GET /space/exploration/testing",
        "GET /space/exploration/cqrs", "GET /space/exploration/events",
        "GET /space/exploration/readiness",
    ]}
