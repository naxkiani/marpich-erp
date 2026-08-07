"""P218-I Enterprise Space Intelligence Space Navigation — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P218-I"
ADR = 535
SOR = "space"
API_PREFIX = "/api/v1/space"
PRODUCT = (
    "Enterprise Space Intelligence Space Navigation Intelligence, GNSS, Autonomous Navigation, "
    "Space Positioning Platform, Trajectory Optimization, Guidance & Control & MEOS Space Navigation Intelligence Platform"
)
CAPABILITY = "CAP-PLT-SP-001"
NAV_MISSION = (
    "Deliver a unified navigation intelligence platform capable of autonomously determining, predicting and "
    "optimising the position, attitude and trajectory of every spacecraft, satellite and planetary vehicle "
    "across Earth orbit and deep space."
)
NAV_VISION = (
    "Transform spaceflight navigation from ground-loop GNC into an explainable, sensor-fused, "
    "human-supervised autonomous navigation fabric spanning GNSS, deep space and planetary operations."
)
FABRIC = "meos_space_navigation_intelligence_fabric"
FOUNDATION_GATE = "P218"
MISSION_GATE = "P218-A"
STRATEGY_GATE = "P218-B"
DOMAIN_GATE = "P218-C"
INFRASTRUCTURE_GATE = "P218-D"
SPACE_AI_GATE = "P218-E"
SATELLITE_GATE = "P218-F"
ORBITAL_GATE = "P218-G"
COMMUNICATIONS_GATE = "P218-H"
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

ARCHITECTURE_LAYERS = (
    {"id": "L01", "name": "Navigation Sensor Layer", "components": ("gnss_receivers", "star_trackers", "sun_sensors", "imus", "gyroscopes", "accelerometers", "optical_navigation_cameras", "radar", "lidar", "planetary_landmark_sensors")},
    {"id": "L02", "name": "Navigation Processing Layer", "components": ("sensor_fusion_engine", "orbit_determination_engine", "state_estimation_engine", "attitude_determination_engine", "ephemeris_engine", "clock_synchronisation", "navigation_filtering", "kalman_filter_services")},
    {"id": "L03", "name": "Navigation Intelligence Layer", "components": ("trajectory_optimizer", "navigation_ai", "collision_aware_routing", "mission_path_planner", "gravity_assist_planner", "fuel_optimizer", "navigation_predictor", "uncertainty_analysis_engine")},
    {"id": "L04", "name": "Guidance & Control Layer", "components": ("guidance_engine", "attitude_control", "thruster_control", "reaction_wheel_controller", "autonomous_maneuver_planner", "docking_controller", "landing_controller", "formation_flying_controller")},
    {"id": "L05", "name": "Mission Navigation Services", "components": ("mission_route_planning", "launch_navigation", "orbit_transfer", "planetary_descent", "landing_support", "return_navigation", "formation_coordination", "emergency_navigation")},
)
GNSS = {
    "present_required": True,
    "platform": "meos_gnss_intelligence_platform",
    "supported_systems": (
        "gps", "galileo", "glonass", "beidou",
        "regional_navigation_systems", "future_lunar_pnt", "planetary_navigation_networks",
    ),
    "capabilities": (
        "position_determination", "time_synchronisation", "velocity_estimation", "integrity_monitoring",
        "signal_quality_analysis", "multi_gnss_fusion", "fallback_navigation", "spoofing_detection",
    ),
    "never_skip_gnss_spoofing_detection": True,
}
AUTONOMOUS_NAV = {
    "present_required": True,
    "platform": "meos_autonomous_navigation_platform",
    "capabilities": (
        "self_localization", "autonomous_guidance", "dynamic_replanning", "safe_route_selection",
        "obstacle_avoidance", "formation_navigation", "docking_navigation", "planetary_surface_navigation",
        "deep_space_navigation",
    ),
    "modes": ("ground_controlled", "ai_assisted", "semi_autonomous", "fully_autonomous", "emergency_safe_mode"),
    "never_disable_human_override": True,
}
TRAJECTORY = {
    "present_required": True,
    "platform": "meos_trajectory_optimization_platform",
    "objectives": (
        "minimum_fuel", "minimum_time", "maximum_safety", "maximum_scientific_value",
        "collision_avoidance", "communication_visibility", "energy_efficiency", "mission_success_probability",
    ),
    "maneuvers": (
        "orbit_raising", "orbit_lowering", "plane_change", "rendezvous", "docking",
        "gravity_assist", "station_keeping", "reentry", "planetary_transfer",
    ),
    "via_p215_z": True,
}
GNC = {
    "present_required": True,
    "platform": "meos_guidance_navigation_control_platform",
    "components": (
        "guidance_computer", "navigation_computer", "flight_dynamics_engine", "attitude_controller",
        "thruster_manager", "reaction_wheel_controller", "momentum_management", "fault_detection",
    ),
    "control_algorithms": ("pid", "lqr", "mpc", "adaptive_control", "robust_control", "ai_assisted_control"),
    "never_ungated_guidance_command": True,
}
NAVIGATION_AI = {
    "present_required": True,
    "platform": "meos_navigation_ai_platform",
    "capabilities": (
        "trajectory_prediction", "anomaly_detection", "fuel_prediction", "autonomous_replanning",
        "sensor_health_assessment", "navigation_confidence_estimation", "landing_optimization", "formation_optimization",
    ),
    "models": (
        {"id": "MODEL-01", "name": "Navigation Foundation Model"},
        {"id": "MODEL-02", "name": "Trajectory Intelligence Model"},
        {"id": "MODEL-03", "name": "Landing Intelligence Model"},
        {"id": "MODEL-04", "name": "Flight Dynamics Model"},
        {"id": "MODEL-05", "name": "Mission Route Model"},
    ),
    "via_p214_z": True,
    "via_p218_e": True,
}
DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_space_navigation_digital_twin",
    "represents": (
        "spacecraft", "satellite", "orbit", "trajectory", "attitude",
        "thrusters", "sensors", "planetary_terrain", "navigation_environment",
    ),
    "capabilities": (
        "trajectory_simulation", "landing_simulation", "orbit_forecasting", "sensor_simulation",
        "mission_replay", "failure_simulation", "navigation_validation", "fuel_optimization",
    ),
}
OBSERVABILITY = {
    "present_required": True,
    "dashboards": (
        "navigation_status", "trajectory_map", "mission_route", "fuel_projection",
        "attitude_status", "sensor_health", "landing_readiness", "formation_status",
    ),
    "kpis": (
        "navigation_accuracy", "trajectory_deviation", "fuel_efficiency", "mission_route_efficiency",
        "autonomous_navigation_success_rate", "docking_accuracy", "landing_accuracy",
        "position_integrity", "control_latency", "mission_completion_rate",
    ),
}
BOUNDED_CONTEXTS = (
    {"id": "BC-NAV-01", "name": "Navigation Management"},
    {"id": "BC-NAV-02", "name": "GNSS Services"},
    {"id": "BC-NAV-03", "name": "Trajectory Planning"},
    {"id": "BC-NAV-04", "name": "Guidance & Control"},
    {"id": "BC-NAV-05", "name": "Attitude Determination"},
    {"id": "BC-NAV-06", "name": "Navigation AI"},
    {"id": "BC-NAV-07", "name": "Formation Navigation"},
    {"id": "BC-NAV-08", "name": "Landing Operations"},
)
GOVERNANCE = {
    "present_required": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "never_opaque_unexplainable_decisions": True,
    "never_ungated_guidance_command": True,
    "never_skip_gnss_spoofing_detection": True,
    "never_disable_human_override": True,
}
SECURITY = {
    "present_required": True,
    "controls": (
        "navigation_authentication", "gnss_spoofing_detection", "signal_integrity_monitoring",
        "command_authentication", "secure_guidance_commands", "redundant_navigation_paths",
        "fault_isolation", "safe_mode_navigation",
    ),
    "resilience": (
        "sensor_redundancy", "navigation_failover", "autonomous_recovery",
        "emergency_return_planning", "mission_continuity",
    ),
    "zero_trust": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "via_integration": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
    "no_module_local_telemetry_stack": True,
    "no_module_local_communications_radio_stack": True,
    "no_module_local_gnss_receiver_stack": True,
    "never_opaque_unexplainable_decisions": True,
    "never_replace_p218_foundation": True,
    "never_replace_p218_a_mission": True,
    "never_replace_p218_b_strategy": True,
    "never_replace_p218_c_domain": True,
    "never_replace_p218_d_infrastructure": True,
    "never_replace_p218_e_space_ai": True,
    "never_replace_p218_f_satellite": True,
    "never_replace_p218_g_orbital": True,
    "never_replace_p218_h_communications": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "never_replace_p216_z": True,
    "never_replace_biotechnology": True,
    "never_skip_human_mission_oversight_strategy": True,
    "never_skip_space_cybersecurity_strategy": True,
    "never_skip_space_sustainability_strategy": True,
    "never_opaque_mission_critical_strategy": True,
    "never_ungated_autonomous_mission_strategy": True,
    "never_ungated_satellite_command_uplink": True,
    "never_ungated_collision_avoidance_maneuver": True,
    "never_ungated_command_transport": True,
    "never_ungated_guidance_command": True,
    "never_disable_human_override": True,
    "never_skip_delay_tolerant_networking": True,
    "never_skip_gnss_spoofing_detection": True,
}
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p214z_ai_master", "p215z_quantum_supreme", "p216z_robotics_supreme", "p217z_bio_nexus",
        "p218d_space_infrastructure", "p218e_space_ai", "p218f_satellite", "p218g_orbital",
        "p218h_communications", "meos_knowledge_graph", "meos_digital_twin", "policy_engine",
        "workflow", "audit", "integration_platform", "notifications",
    ),
    "mechanisms": ("api_gateway", "event_bus", "acl_peer_ids_only", "inference_intents_not_models", "sensors_via_integration", "trajectory_via_quantum"),
    "via_p214_z": True, "via_p215_z": True, "via_p216_z": True, "via_p217": True,
    "via_p218_d": True, "via_p218_e": True, "via_p218_f": True, "via_p218_g": True, "via_p218_h": True,
}
DEPLOYMENT = {
    "present_required": True,
    "environments": (
        "gnss_ops_environment", "gnc_sim_environment",
        "deep_space_nav_environment", "simulation_only_environment",
    ),
    "cloud_native": True,
    "safety_critical": True,
}
ROADMAP_PHASES = (
    {"phase": 1, "name": "Navigation Foundation", "deliverables": ("gnss_platform", "sensor_fusion", "trajectory_engine", "navigation_dashboard")},
    {"phase": 2, "name": "Mission Navigation", "deliverables": ("autonomous_guidance", "trajectory_optimizer", "mission_route_planner", "navigation_ai")},
    {"phase": 3, "name": "Advanced Space Navigation", "deliverables": ("deep_space_navigation", "planetary_navigation", "formation_flying", "digital_twin")},
    {"phase": 4, "name": "Enterprise Navigation Intelligence", "deliverables": ("fully_autonomous_navigation", "self_optimising_guidance", "civilisation_scale_navigation_platform", "meos_space_navigation_intelligence_core")},
)
COMMANDS = (
    "InitializeNavigationCommand", "OptimizeTrajectoryCommand", "IssueControlCommand",
    "InitiateDockingCommand", "StartLandingSequenceCommand", "ExecuteOrbitTransferCommand",
)
QUERIES = (
    "GetNavigationPlatformQuery", "GetTrajectoryQuery", "GetAttitudeStateQuery",
    "GetGnssIntegrityQuery", "GetLandingReadinessQuery",
)
CORE_EVENTS = (
    {"name": "NavigationInitializedEvent", "schema": "space.navigation.initialized.v1", "owner": "BC-NAV-01", "consumers": "audit,search,mission"},
    {"name": "NavigationUpdatedEvent", "schema": "space.navigation.updated.v1", "owner": "BC-NAV-01", "consumers": "audit,analytics,twin"},
    {"name": "TrajectoryGeneratedEvent", "schema": "space.navigation.trajectory.generated.v1", "owner": "BC-NAV-03", "consumers": "audit,ai,mission"},
    {"name": "TrajectoryOptimizedEvent", "schema": "space.navigation.trajectory.optimized.v1", "owner": "BC-NAV-03", "consumers": "audit,analytics,quantum"},
    {"name": "ControlCommandIssuedEvent", "schema": "space.navigation.control.issued.v1", "owner": "BC-NAV-04", "consumers": "audit,workflow,satellite"},
    {"name": "DockingInitiatedEvent", "schema": "space.navigation.docking.initiated.v1", "owner": "BC-NAV-07", "consumers": "audit,workflow,robotics"},
    {"name": "LandingSequenceStartedEvent", "schema": "space.navigation.landing.started.v1", "owner": "BC-NAV-08", "consumers": "audit,workflow,notifications"},
    {"name": "LandingCompletedEvent", "schema": "space.navigation.landing.completed.v1", "owner": "BC-NAV-08", "consumers": "audit,analytics,compliance"},
    {"name": "OrbitTransferExecutedEvent", "schema": "space.navigation.orbit.transfer.executed.v1", "owner": "BC-NAV-03", "consumers": "audit,orbital,satellite"},
    {"name": "FormationReconfiguredEvent", "schema": "space.navigation.formation.reconfigured.v1", "owner": "BC-NAV-07", "consumers": "audit,analytics,fleet"},
)
MICROSERVICES = (
    {"id": "navigation_platform_service", "api": "/space/navigation", "db": "space_*", "events": ("NavigationInitializedEvent",), "security": ("space.read",), "scaling": "nav_platform_replicas"},
    {"id": "gnss_service", "api": "/space/navigation/gnss", "db": "space_*", "events": ("NavigationUpdatedEvent",), "security": ("space.read",), "scaling": "gnss_workers"},
    {"id": "autonomous_nav_service", "api": "/space/navigation/autonomous", "db": "space_*", "events": ("TrajectoryGeneratedEvent",), "security": ("space.write",), "scaling": "autonav_workers"},
    {"id": "trajectory_service", "api": "/space/navigation/trajectory", "db": "space_*", "events": ("TrajectoryOptimizedEvent",), "security": ("space.write",), "scaling": "trajectory_workers"},
    {"id": "gnc_service", "api": "/space/navigation/gnc", "db": "space_*", "events": ("ControlCommandIssuedEvent",), "security": ("space.write",), "scaling": "gnc_workers"},
    {"id": "navigation_ai_service", "api": "/space/navigation/navigation-ai", "db": "space_*", "events": ("TrajectoryOptimizedEvent",), "security": ("space.ai.infer",), "scaling": "nav_ai_workers"},
    {"id": "digital_twin_service", "api": "/space/navigation/digital-twin", "db": "space_*", "events": ("NavigationUpdatedEvent",), "security": ("space.read",), "scaling": "twin_workers"},
    {"id": "observability_service", "api": "/space/navigation/observability", "db": "space_*", "events": ("LandingCompletedEvent",), "security": ("space.read",), "scaling": "obs_replicas"},
    {"id": "nav_governance_service", "api": "/space/navigation/governance", "db": "space_*", "events": ("ControlCommandIssuedEvent",), "security": ("space.admin",), "scaling": "governance_replicas"},
    {"id": "nav_security_service", "api": "/space/navigation/security", "db": "space_*", "events": ("NavigationUpdatedEvent",), "security": ("space.admin",), "scaling": "security_replicas"},
)
TESTING = (
    "gnss_integrity_testing", "spoofing_detection_testing", "trajectory_optimization_testing",
    "guidance_command_gate_testing", "sensor_fusion_testing", "landing_sequence_testing",
    "formation_control_testing", "navigation_ai_confidence_testing",
)
QUALITY_GATES_REJECT_IF = (
    "space_navigation_platform_is_missing", "gnss_intelligence_is_missing",
    "autonomous_navigation_is_missing", "trajectory_optimization_is_missing",
    "guidance_and_control_is_missing", "navigation_ai_is_missing",
    "navigation_digital_twin_is_missing", "ddd_model_is_missing",
    "security_architecture_is_missing", "observability_is_missing",
    "deployment_architecture_is_missing", "cqrs_architecture_is_missing",
    "event_architecture_is_missing", "microservices_architecture_is_missing",
    "sibling_space_bc", "replace_p218_foundation", "replace_p218_h_communications",
    "module_local_llm", "module_local_gnss_receiver_stack",
    "ungated_guidance_command", "skip_gnss_spoofing_detection",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Space Navigation Intelligence Fabric",
        "mission": NAV_MISSION, "vision": NAV_VISION,
        "builds_on_p218": True, "builds_on_p218_a": True, "builds_on_p218_b": True,
        "builds_on_p218_c": True, "builds_on_p218_d": True, "builds_on_p218_e": True,
        "builds_on_p218_f": True, "builds_on_p218_g": True, "builds_on_p218_h": True,
        "builds_on_p217_z": True, "builds_on_p216_z": True, "builds_on_p215_z": True, "builds_on_p214_z": True,
        "never_replace_p218_h_communications": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
        "no_module_local_gnss_receiver_stack": True,
        "never_skip_gnss_spoofing_detection": True,
        "never_ungated_guidance_command": True,
        "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "infrastructure_gate": INFRASTRUCTURE_GATE, "space_ai_gate": SPACE_AI_GATE,
        "satellite_gate": SATELLITE_GATE, "orbital_gate": ORBITAL_GATE,
        "communications_gate": COMMUNICATIONS_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
    }

def architecture() -> dict[str, Any]:
    return {"present_required": True, "layers": [dict(x) for x in ARCHITECTURE_LAYERS], "layer_count": len(ARCHITECTURE_LAYERS)}

def gnss() -> dict[str, Any]:
    return dict(GNSS) | {
        "system_count": len(GNSS["supported_systems"]),
        "capability_count": len(GNSS["capabilities"]),
    }

def autonomous() -> dict[str, Any]:
    return dict(AUTONOMOUS_NAV) | {
        "capability_count": len(AUTONOMOUS_NAV["capabilities"]),
        "mode_count": len(AUTONOMOUS_NAV["modes"]),
    }

def trajectory() -> dict[str, Any]:
    return dict(TRAJECTORY) | {
        "objective_count": len(TRAJECTORY["objectives"]),
        "maneuver_count": len(TRAJECTORY["maneuvers"]),
    }

def gnc() -> dict[str, Any]:
    return dict(GNC) | {
        "component_count": len(GNC["components"]),
        "algorithm_count": len(GNC["control_algorithms"]),
    }

def navigation_ai() -> dict[str, Any]:
    return dict(NAVIGATION_AI) | {
        "capability_count": len(NAVIGATION_AI["capabilities"]),
        "model_count": len(NAVIGATION_AI["models"]),
    }

def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN) | {
        "representation_count": len(DIGITAL_TWIN["represents"]),
        "capability_count": len(DIGITAL_TWIN["capabilities"]),
    }

def observability() -> dict[str, Any]:
    return dict(OBSERVABILITY) | {
        "dashboard_count": len(OBSERVABILITY["dashboards"]),
        "kpi_count": len(OBSERVABILITY["kpis"]),
    }

def governance() -> dict[str, Any]:
    return dict(GOVERNANCE)

def security() -> dict[str, Any]:
    return dict(SECURITY)

def bounded_contexts() -> dict[str, Any]:
    return {"present_required": True, "contexts": [dict(c) for c in BOUNDED_CONTEXTS], "context_count": len(BOUNDED_CONTEXTS)}

def integration() -> dict[str, Any]:
    return dict(INTEGRATION)

def deployment() -> dict[str, Any]:
    return dict(DEPLOYMENT)

def cqrs() -> dict[str, Any]:
    return {"present_required": True, "commands": list(COMMANDS), "queries": list(QUERIES)}

def events() -> dict[str, Any]:
    return {"present_required": True, "core_events": [dict(e) for e in CORE_EVENTS], "core_event_count": len(CORE_EVENTS)}

def microservices() -> dict[str, Any]:
    return {"present_required": True, "services": [dict(s) for s in MICROSERVICES], "service_count": len(MICROSERVICES)}

def testing() -> dict[str, Any]:
    return {"present_required": True, "suites": list(TESTING)}

def roadmap() -> dict[str, Any]:
    return {"present_required": True, "phases": [dict(p) for p in ROADMAP_PHASES], "phase_count": len(ROADMAP_PHASES)}

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p218_j": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "nav_mission": NAV_MISSION, "nav_vision": NAV_VISION, "principle": NAV_MISSION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE, "infrastructure_gate": INFRASTRUCTURE_GATE,
        "space_ai_gate": SPACE_AI_GATE, "satellite_gate": SATELLITE_GATE, "orbital_gate": ORBITAL_GATE,
        "communications_gate": COMMUNICATIONS_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P218", "P218-A", "P218-B", "P218-C", "P218-D", "P218-E", "P218-F", "P218-G", "P218-H", "P217-Z", "P216-Z", "P215-Z", "P214-Z"] + [f"ADR-{i}" for i in range(526, 535)],
        "vision": vision_pack(),
        "architecture": architecture(),
        "gnss": gnss(),
        "autonomous": autonomous(),
        "trajectory": trajectory(),
        "gnc": gnc(),
        "navigation_ai": navigation_ai(),
        "digital_twin": digital_twin(),
        "observability": observability(),
        "governance": governance(),
        "security": security(),
        "bounded_contexts": bounded_contexts(),
        "integration": integration(),
        "deployment": deployment(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "testing": testing(),
        "roadmap": roadmap(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "space_navigation_platform_present_required": True,
        "gnss_intelligence_present_required": True,
        "autonomous_navigation_present_required": True,
        "trajectory_optimization_present_required": True,
        "guidance_and_control_present_required": True,
        "navigation_ai_present_required": True,
        "navigation_digital_twin_present_required": True,
        "ddd_model_present_required": True,
        "security_architecture_present_required": True,
        "observability_present_required": True,
        "deployment_architecture_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "sibling_space_bc_forbidden": True,
        "never_replace_p218_foundation": True,
        "never_replace_p218_a_mission": True,
        "never_replace_p218_b_strategy": True,
        "never_replace_p218_c_domain": True,
        "never_replace_p218_d_infrastructure": True,
        "never_replace_p218_e_space_ai": True,
        "never_replace_p218_f_satellite": True,
        "never_replace_p218_g_orbital": True,
        "never_replace_p218_h_communications": True,
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_replace_p216_z": True,
        "never_replace_biotechnology": True,
        "space_ai_via_p214z_acl_only": True,
        "no_module_local_llm": True,
        "no_module_local_telemetry_stack": True,
        "no_module_local_communications_radio_stack": True,
        "no_module_local_gnss_receiver_stack": True,
        "never_opaque_unexplainable_decisions": True,
        "never_skip_human_mission_oversight_strategy": True,
        "never_skip_space_cybersecurity_strategy": True,
        "never_skip_space_sustainability_strategy": True,
        "never_opaque_mission_critical_strategy": True,
        "never_ungated_autonomous_mission_strategy": True,
        "never_ungated_satellite_command_uplink": True,
        "never_ungated_collision_avoidance_maneuver": True,
        "never_ungated_command_transport": True,
        "never_ungated_guidance_command": True,
        "never_disable_human_override": True,
        "never_skip_delay_tolerant_networking": True,
        "never_skip_gnss_spoofing_detection": True,
        "api_prefix": f"{API_PREFIX}/navigation",
        "forbidden_sibling_bc": [
            "space_navigation_platform",
            "gnss_intelligence_bc",
            "gnc_platform_bc",
        ],
        "foundation_for_p218_j": True,
    }

def navigation_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /space/navigation",
        "GET /space/navigation/vision",
        "GET /space/navigation/architecture",
        "GET /space/navigation/gnss",
        "GET /space/navigation/autonomous",
        "GET /space/navigation/trajectory",
        "GET /space/navigation/gnc",
        "GET /space/navigation/navigation-ai",
        "GET /space/navigation/digital-twin",
        "GET /space/navigation/observability",
        "GET /space/navigation/governance",
        "GET /space/navigation/security",
        "GET /space/navigation/integration",
        "GET /space/navigation/deployment",
        "GET /space/navigation/testing",
        "GET /space/navigation/cqrs",
        "GET /space/navigation/events",
        "GET /space/navigation/readiness",
    ], "foundation_gate_routes": ["GET /space/foundation"],
       "mission_gate_routes": ["GET /space/mission"],
       "strategy_gate_routes": ["GET /space/strategy"],
       "domain_gate_routes": ["GET /space/domain"],
       "infrastructure_gate_routes": ["GET /space/infrastructure", "GET /space/infrastructure/readiness"],
       "space_ai_gate_routes": ["GET /space/space-ai", "GET /space/space-ai/readiness"],
       "satellite_gate_routes": ["GET /space/satellite", "GET /space/satellite/readiness"],
       "orbital_gate_routes": ["GET /space/orbital", "GET /space/orbital/readiness"],
       "communications_gate_routes": ["GET /space/communications", "GET /space/communications/readiness"]}
