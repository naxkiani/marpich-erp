"""P218-G Enterprise Space Intelligence Orbital Intelligence — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P218-G"
ADR = 533
SOR = "space"
API_PREFIX = "/api/v1/space"
PRODUCT = (
    "Enterprise Space Intelligence Orbital Traffic Management, Space Situational Awareness, "
    "Collision Avoidance, Space Debris Intelligence & MEOS Orbital Intelligence Platform"
)
CAPABILITY = "CAP-PLT-SP-001"
ORBITAL_MISSION = (
    "Provide continuous, global, real-time awareness of all orbital objects and enable intelligent, "
    "autonomous and safe management of orbital traffic for satellites, spacecraft and future space infrastructure."
)
ORBITAL_VISION = (
    "Transform orbital safety from reactive conjunction alerts into a predictive, explainable, "
    "human-supervised planetary-scale traffic and debris intelligence ecosystem."
)
FABRIC = "meos_orbital_intelligence_fabric"
FOUNDATION_GATE = "P218"
MISSION_GATE = "P218-A"
STRATEGY_GATE = "P218-B"
DOMAIN_GATE = "P218-C"
INFRASTRUCTURE_GATE = "P218-D"
SPACE_AI_GATE = "P218-E"
SATELLITE_GATE = "P218-F"
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

ARCHITECTURE_LAYERS = (
    {"id": "L01", "name": "Orbital Observation Layer", "components": ("observation_gateway", "tracking_ingestion", "sensor_fusion", "time_synchronisation", "observation_quality_engine")},
    {"id": "L02", "name": "Orbital Intelligence Layer", "components": ("orbit_determination_engine", "trajectory_propagation_engine", "conjunction_assessment_engine", "debris_classification_engine", "orbital_risk_engine", "space_weather_correlation_engine")},
    {"id": "L03", "name": "Safety Decision Layer", "components": ("collision_avoidance_planner", "maneuver_optimizer", "fuel_impact_analyzer", "mission_impact_analyzer", "human_approval_engine", "emergency_autonomy_engine")},
    {"id": "L04", "name": "Coordination Layer", "components": ("traffic_coordination_platform", "operator_collaboration_hub", "regulatory_interface", "notification_engine", "international_data_exchange")},
    {"id": "L05", "name": "Governance Layer", "components": ("orbital_safety_policies", "risk_threshold_engine", "compliance_intelligence", "audit_traceability", "sustainability_governance")},
)
SSA = {
    "present_required": True,
    "platform": "meos_space_situational_awareness_platform",
    "capabilities": (
        "object_detection", "object_tracking", "orbit_determination", "identity_resolution",
        "behavior_analysis", "threat_classification", "anomaly_detection", "space_weather_correlation",
    ),
    "object_categories": (
        "operational_satellites", "inactive_satellites", "rocket_bodies", "mission_debris",
        "fragmentation_debris", "cubesats", "space_stations", "deep_space_objects",
    ),
    "outputs": (
        "current_orbit", "predicted_orbit", "uncertainty_ellipsoid",
        "threat_score", "behavior_classification", "confidence_level",
    ),
}
OTM = {
    "present_required": True,
    "platform": "meos_orbital_traffic_management_platform",
    "functions": (
        "traffic_registration", "orbit_slot_allocation", "trajectory_coordination", "conjunction_resolution",
        "priority_management", "emergency_coordination", "capacity_management", "traffic_analytics",
    ),
    "traffic_classes": (
        "critical_human_spaceflight", "national_security", "operational_constellations",
        "scientific_missions", "commercial_missions", "experimental_missions", "inactive_objects",
    ),
    "priority_rules": (
        "human_safety", "national_critical_infrastructure", "active_mission_preservation",
        "collision_probability", "debris_generation_potential",
    ),
}
COLLISION_AVOIDANCE = {
    "present_required": True,
    "platform": "meos_collision_avoidance_platform",
    "pipeline": ("observe", "track", "propagate", "assess", "prioritize", "recommend", "approve", "execute", "verify"),
    "maneuver_types": ("in_track", "radial", "cross_track", "combined_vector", "hold_position", "safe_mode"),
    "outputs": (
        "probability_of_collision", "time_of_closest_approach", "miss_distance",
        "recommended_maneuver", "fuel_cost", "mission_impact",
    ),
    "never_ungated_collision_avoidance_maneuver": True,
    "never_disable_human_override": True,
}
DEBRIS = {
    "present_required": True,
    "platform": "meos_space_debris_intelligence_platform",
    "capabilities": (
        "debris_detection", "debris_classification", "fragmentation_analysis", "debris_propagation",
        "reentry_prediction", "debris_risk_mapping", "debris_removal_prioritization", "long_term_environment_simulation",
    ),
    "taxonomy": (
        "mission_related", "explosion_debris", "collision_debris", "paint_flakes",
        "solid_rocket_residue", "fragment_clouds", "micrometeoroid_like_particles",
    ),
    "analytics": (
        "spatial_density", "altitude_density", "collision_cascade_risk",
        "debris_growth_rate", "high_risk_regions", "protected_corridors",
    ),
}
DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_orbital_digital_twin",
    "represents": (
        "earth_orbit_environment", "satellites", "debris_fields", "ground_stations",
        "traffic_corridors", "space_weather", "mission_constraints",
    ),
    "capabilities": (
        "real_time_orbit_visualisation", "future_orbit_simulation", "conjunction_replay",
        "what_if_maneuver_analysis", "debris_evolution_simulation", "traffic_capacity_forecasting",
        "sustainability_impact_assessment",
    ),
}
KNOWLEDGE_GRAPH = {
    "present_required": True,
    "platform": "meos_orbital_knowledge_graph",
    "entities": (
        "OrbitalObject", "Satellite", "DebrisObject", "Launch", "Orbit", "Conjunction",
        "Maneuver", "Operator", "GroundStation", "SpaceWeatherEvent", "RiskAssessment", "Regulation",
    ),
    "relationships": (
        "OBJECT_IN_ORBIT", "OBJECT_OWNED_BY", "OBJECT_TRACKED_BY", "OBJECT_CONJUNCTION_WITH",
        "MANEUVER_AVOIDS", "EVENT_AFFECTS", "POLICY_GOVERNS",
    ),
    "capabilities": (
        "risk_reasoning", "operator_attribution", "debris_lineage",
        "conjunction_correlation", "regulatory_impact_analysis",
    ),
}
AI_AUTONOMY = {
    "present_required": True,
    "platform": "meos_autonomous_orbital_intelligence",
    "capabilities": (
        "conjunction_prioritization", "false_positive_reduction", "maneuver_optimization",
        "fuel_minimal_avoidance", "anomaly_detection", "behavioral_pattern_analysis",
        "debris_evolution_forecasting", "traffic_congestion_prediction",
    ),
    "modes": (
        "advisory_only", "human_approval_required", "conditional_autonomy",
        "fully_autonomous_emergency_response",
    ),
    "human_override": ("always_available", "immediate_abort", "manual_maneuver_injection", "policy_override", "emergency_freeze"),
    "via_p214_z": True,
    "via_p218_e": True,
    "never_disable_human_override": True,
    "never_ungated_collision_avoidance_maneuver": True,
}
OBSERVABILITY = {
    "present_required": True,
    "dashboards": (
        "global_orbit_map", "high_risk_conjunctions", "active_maneuvers", "debris_density_heatmap",
        "traffic_congestion", "sensor_coverage", "operator_coordination", "sustainability_metrics",
    ),
    "kpis": (
        "mean_time_to_detect", "mean_time_to_assess", "mean_time_to_recommend", "mean_time_to_execute",
        "conjunction_prediction_accuracy", "false_positive_rate", "collision_avoidance_success_rate",
        "fuel_efficiency_of_maneuvers", "debris_growth_rate", "orbital_sustainability_index",
    ),
}
BOUNDED_CONTEXTS = (
    {"id": "BC-ORB-01", "name": "Space Situational Awareness"},
    {"id": "BC-ORB-02", "name": "Orbital Traffic Management"},
    {"id": "BC-ORB-03", "name": "Conjunction Assessment"},
    {"id": "BC-ORB-04", "name": "Collision Avoidance"},
    {"id": "BC-ORB-05", "name": "Debris Intelligence"},
    {"id": "BC-ORB-06", "name": "Maneuver Execution"},
    {"id": "BC-ORB-07", "name": "Orbital Governance"},
    {"id": "BC-ORB-08", "name": "Orbital Analytics"},
)
GOVERNANCE = {
    "present_required": True,
    "compliance": (
        "iadc_guidelines", "unoosa_best_practices", "national_licensing_requirements",
        "debris_mitigation_standards", "post_mission_disposal_policies",
    ),
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "never_opaque_unexplainable_decisions": True,
    "never_ungated_autonomous_mission_strategy": True,
    "never_ungated_collision_avoidance_maneuver": True,
    "never_disable_human_override": True,
}
SECURITY = {
    "present_required": True,
    "controls": (
        "authenticated_tracking_feeds", "signed_telemetry", "pki_for_maneuver_commands",
        "role_based_access_control", "multi_party_approval", "immutable_audit_trail", "zero_trust_networking",
    ),
    "trust": ("data_provenance", "source_confidence_scoring", "cross_network_verification", "independent_sensor_validation"),
    "zero_trust": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "via_integration": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
    "no_module_local_telemetry_stack": True,
    "no_module_local_ssa_sensor_stack": True,
    "never_opaque_unexplainable_decisions": True,
    "never_replace_p218_foundation": True,
    "never_replace_p218_a_mission": True,
    "never_replace_p218_b_strategy": True,
    "never_replace_p218_c_domain": True,
    "never_replace_p218_d_infrastructure": True,
    "never_replace_p218_e_space_ai": True,
    "never_replace_p218_f_satellite": True,
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
    "never_disable_human_override": True,
}
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p214z_ai_master", "p215z_quantum_supreme", "p216z_robotics_supreme", "p217z_bio_nexus",
        "p218d_space_infrastructure", "p218e_space_ai", "p218f_satellite", "meos_knowledge_graph",
        "meos_digital_twin", "policy_engine", "workflow", "audit", "integration_platform", "notifications",
    ),
    "mechanisms": ("api_gateway", "event_bus", "acl_peer_ids_only", "inference_intents_not_models", "ssa_feeds_via_integration"),
    "via_p214_z": True, "via_p215_z": True, "via_p216_z": True, "via_p217": True,
    "via_p218_d": True, "via_p218_e": True, "via_p218_f": True,
}
DEPLOYMENT = {
    "present_required": True,
    "environments": (
        "ssa_ops_environment", "conjunction_sim_environment",
        "enterprise_orbital_safety_environment", "simulation_only_environment",
    ),
    "cloud_native": True,
    "planetary_scale": True,
}
ROADMAP_PHASES = (
    {"phase": 1, "name": "SSA Foundation", "deliverables": ("sensor_ingestion", "object_catalog", "orbit_determination", "real_time_tracking")},
    {"phase": 2, "name": "Conjunction Intelligence", "deliverables": ("conjunction_assessment", "risk_scoring", "operator_notifications", "maneuver_planning")},
    {"phase": 3, "name": "Autonomous Orbital Safety", "deliverables": ("ai_prioritization", "conditional_autonomy", "debris_forecasting", "digital_twin_simulation")},
    {"phase": 4, "name": "Planetary Orbital Intelligence Core", "deliverables": ("global_traffic_coordination", "cross_operator_automation", "sustainability_optimization", "meos_orbital_intelligence_core")},
)
COMMANDS = (
    "RegisterOrbitalObjectCommand", "AssessConjunctionCommand", "RecommendAvoidanceManeuverCommand",
    "ApproveManeuverCommand", "ExecuteManeuverCommand", "EscalateConjunctionCommand",
)
QUERIES = (
    "GetOrbitalPlatformQuery", "GetConjunctionQuery", "GetDebrisFieldQuery",
    "GetTrafficPlanQuery", "GetRiskAssessmentQuery",
)
CORE_EVENTS = (
    {"name": "OrbitalObjectDetectedEvent", "schema": "space.orbital.object.detected.v1", "owner": "BC-ORB-01", "consumers": "audit,search,ssa"},
    {"name": "OrbitUpdatedEvent", "schema": "space.orbital.orbit.updated.v1", "owner": "BC-ORB-01", "consumers": "audit,analytics,twin"},
    {"name": "ConjunctionPredictedEvent", "schema": "space.orbital.conjunction.predicted.v1", "owner": "BC-ORB-03", "consumers": "audit,notifications,avoidance"},
    {"name": "ConjunctionEscalatedEvent", "schema": "space.orbital.conjunction.escalated.v1", "owner": "BC-ORB-03", "consumers": "audit,workflow,notifications"},
    {"name": "AvoidanceManeuverRecommendedEvent", "schema": "space.orbital.maneuver.recommended.v1", "owner": "BC-ORB-04", "consumers": "audit,workflow,ai"},
    {"name": "ManeuverApprovedEvent", "schema": "space.orbital.maneuver.approved.v1", "owner": "BC-ORB-06", "consumers": "audit,workflow,fleet"},
    {"name": "ManeuverExecutedEvent", "schema": "space.orbital.maneuver.executed.v1", "owner": "BC-ORB-06", "consumers": "audit,analytics,satellite"},
    {"name": "CollisionAvoidedEvent", "schema": "space.orbital.collision.avoided.v1", "owner": "BC-ORB-04", "consumers": "audit,analytics,compliance"},
    {"name": "DebrisFragmentDetectedEvent", "schema": "space.orbital.debris.fragment.detected.v1", "owner": "BC-ORB-05", "consumers": "audit,search,ssa"},
    {"name": "DebrisCloudGeneratedEvent", "schema": "space.orbital.debris.cloud.generated.v1", "owner": "BC-ORB-05", "consumers": "audit,analytics,notifications"},
    {"name": "ReentryPredictedEvent", "schema": "space.orbital.reentry.predicted.v1", "owner": "BC-ORB-05", "consumers": "audit,notifications,compliance"},
    {"name": "RiskThresholdExceededEvent", "schema": "space.orbital.risk.threshold.exceeded.v1", "owner": "BC-ORB-07", "consumers": "audit,workflow,notifications"},
)
MICROSERVICES = (
    {"id": "orbital_platform_service", "api": "/space/orbital", "db": "space_*", "events": ("OrbitalObjectDetectedEvent",), "security": ("space.read",), "scaling": "orbital_platform_replicas"},
    {"id": "ssa_service", "api": "/space/orbital/ssa", "db": "space_*", "events": ("OrbitUpdatedEvent",), "security": ("space.read",), "scaling": "ssa_workers"},
    {"id": "traffic_service", "api": "/space/orbital/traffic", "db": "space_*", "events": ("ConjunctionPredictedEvent",), "security": ("space.write",), "scaling": "traffic_workers"},
    {"id": "collision_avoidance_service", "api": "/space/orbital/collision-avoidance", "db": "space_*", "events": ("AvoidanceManeuverRecommendedEvent", "ManeuverApprovedEvent"), "security": ("space.write",), "scaling": "avoidance_workers"},
    {"id": "debris_service", "api": "/space/orbital/debris", "db": "space_*", "events": ("DebrisFragmentDetectedEvent",), "security": ("space.read",), "scaling": "debris_workers"},
    {"id": "digital_twin_service", "api": "/space/orbital/digital-twin", "db": "space_*", "events": ("OrbitUpdatedEvent",), "security": ("space.read",), "scaling": "twin_workers"},
    {"id": "knowledge_graph_service", "api": "/space/orbital/knowledge-graph", "db": "space_*", "events": ("ConjunctionPredictedEvent",), "security": ("space.read",), "scaling": "kg_workers"},
    {"id": "ai_autonomy_service", "api": "/space/orbital/ai-autonomy", "db": "space_*", "events": ("AvoidanceManeuverRecommendedEvent",), "security": ("space.ai.infer",), "scaling": "ai_workers"},
    {"id": "orbital_governance_service", "api": "/space/orbital/governance", "db": "space_*", "events": ("RiskThresholdExceededEvent",), "security": ("space.admin",), "scaling": "governance_replicas"},
    {"id": "orbital_security_service", "api": "/space/orbital/security", "db": "space_*", "events": ("ManeuverApprovedEvent",), "security": ("space.admin",), "scaling": "security_replicas"},
)
TESTING = (
    "ssa_tracking_testing", "conjunction_accuracy_testing", "maneuver_approval_testing",
    "debris_forecast_testing", "human_override_testing", "sensor_feed_integrity_testing",
    "digital_twin_replay_testing", "planetary_scale_performance_testing",
)
QUALITY_GATES_REJECT_IF = (
    "space_situational_awareness_is_missing", "orbital_traffic_management_is_missing",
    "collision_avoidance_is_missing", "space_debris_intelligence_is_missing",
    "orbital_digital_twin_is_missing", "orbital_knowledge_graph_is_missing",
    "ai_autonomy_is_missing", "ddd_model_is_missing", "security_architecture_is_missing",
    "deployment_architecture_is_missing", "cqrs_architecture_is_missing",
    "event_architecture_is_missing", "microservices_architecture_is_missing",
    "sibling_space_bc", "replace_p218_foundation", "replace_p218_f_satellite",
    "module_local_llm", "module_local_ssa_sensor_stack", "opaque_unexplainable_decisions",
    "ungated_collision_avoidance_maneuver", "disable_human_override",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Orbital Intelligence Fabric",
        "mission": ORBITAL_MISSION, "vision": ORBITAL_VISION,
        "builds_on_p218": True, "builds_on_p218_a": True, "builds_on_p218_b": True,
        "builds_on_p218_c": True, "builds_on_p218_d": True, "builds_on_p218_e": True, "builds_on_p218_f": True,
        "builds_on_p217_z": True, "builds_on_p216_z": True, "builds_on_p215_z": True, "builds_on_p214_z": True,
        "never_replace_p218_f_satellite": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
        "no_module_local_ssa_sensor_stack": True,
        "never_disable_human_override": True,
        "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "infrastructure_gate": INFRASTRUCTURE_GATE, "space_ai_gate": SPACE_AI_GATE,
        "satellite_gate": SATELLITE_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
    }

def architecture() -> dict[str, Any]:
    return {"present_required": True, "layers": [dict(x) for x in ARCHITECTURE_LAYERS], "layer_count": len(ARCHITECTURE_LAYERS)}

def ssa() -> dict[str, Any]:
    return dict(SSA) | {
        "capability_count": len(SSA["capabilities"]),
        "category_count": len(SSA["object_categories"]),
        "output_count": len(SSA["outputs"]),
    }

def traffic() -> dict[str, Any]:
    return dict(OTM) | {
        "function_count": len(OTM["functions"]),
        "class_count": len(OTM["traffic_classes"]),
        "priority_rule_count": len(OTM["priority_rules"]),
    }

def collision_avoidance() -> dict[str, Any]:
    return dict(COLLISION_AVOIDANCE) | {
        "pipeline_step_count": len(COLLISION_AVOIDANCE["pipeline"]),
        "maneuver_type_count": len(COLLISION_AVOIDANCE["maneuver_types"]),
    }

def debris() -> dict[str, Any]:
    return dict(DEBRIS) | {
        "capability_count": len(DEBRIS["capabilities"]),
        "taxonomy_count": len(DEBRIS["taxonomy"]),
    }

def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN) | {
        "representation_count": len(DIGITAL_TWIN["represents"]),
        "capability_count": len(DIGITAL_TWIN["capabilities"]),
    }

def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH) | {
        "entity_count": len(KNOWLEDGE_GRAPH["entities"]),
        "relationship_count": len(KNOWLEDGE_GRAPH["relationships"]),
    }

def ai_autonomy() -> dict[str, Any]:
    return dict(AI_AUTONOMY) | {
        "capability_count": len(AI_AUTONOMY["capabilities"]),
        "mode_count": len(AI_AUTONOMY["modes"]),
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
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p218_h": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "orbital_mission": ORBITAL_MISSION, "orbital_vision": ORBITAL_VISION, "principle": ORBITAL_MISSION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE, "infrastructure_gate": INFRASTRUCTURE_GATE,
        "space_ai_gate": SPACE_AI_GATE, "satellite_gate": SATELLITE_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P218", "P218-A", "P218-B", "P218-C", "P218-D", "P218-E", "P218-F", "P217-Z", "P216-Z", "P215-Z", "P214-Z"] + [f"ADR-{i}" for i in range(526, 533)],
        "vision": vision_pack(),
        "architecture": architecture(),
        "ssa": ssa(),
        "traffic": traffic(),
        "collision_avoidance": collision_avoidance(),
        "debris": debris(),
        "digital_twin": digital_twin(),
        "knowledge_graph": knowledge_graph(),
        "ai_autonomy": ai_autonomy(),
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
        "space_situational_awareness_present_required": True,
        "orbital_traffic_management_present_required": True,
        "collision_avoidance_present_required": True,
        "space_debris_intelligence_present_required": True,
        "orbital_digital_twin_present_required": True,
        "orbital_knowledge_graph_present_required": True,
        "ai_autonomy_present_required": True,
        "ddd_model_present_required": True,
        "security_architecture_present_required": True,
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
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_replace_p216_z": True,
        "never_replace_biotechnology": True,
        "space_ai_via_p214z_acl_only": True,
        "no_module_local_llm": True,
        "no_module_local_telemetry_stack": True,
        "no_module_local_ssa_sensor_stack": True,
        "never_opaque_unexplainable_decisions": True,
        "never_skip_human_mission_oversight_strategy": True,
        "never_skip_space_cybersecurity_strategy": True,
        "never_skip_space_sustainability_strategy": True,
        "never_opaque_mission_critical_strategy": True,
        "never_ungated_autonomous_mission_strategy": True,
        "never_ungated_satellite_command_uplink": True,
        "never_ungated_collision_avoidance_maneuver": True,
        "never_disable_human_override": True,
        "api_prefix": f"{API_PREFIX}/orbital",
        "forbidden_sibling_bc": [
            "orbital_intelligence_platform",
            "ssa_platform_bc",
            "collision_avoidance_bc",
        ],
        "foundation_for_p218_h": True,
    }

def orbital_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /space/orbital",
        "GET /space/orbital/vision",
        "GET /space/orbital/architecture",
        "GET /space/orbital/ssa",
        "GET /space/orbital/traffic",
        "GET /space/orbital/collision-avoidance",
        "GET /space/orbital/debris",
        "GET /space/orbital/digital-twin",
        "GET /space/orbital/knowledge-graph",
        "GET /space/orbital/ai-autonomy",
        "GET /space/orbital/observability",
        "GET /space/orbital/governance",
        "GET /space/orbital/security",
        "GET /space/orbital/integration",
        "GET /space/orbital/deployment",
        "GET /space/orbital/testing",
        "GET /space/orbital/cqrs",
        "GET /space/orbital/events",
        "GET /space/orbital/readiness",
    ], "foundation_gate_routes": ["GET /space/foundation"],
       "mission_gate_routes": ["GET /space/mission"],
       "strategy_gate_routes": ["GET /space/strategy"],
       "domain_gate_routes": ["GET /space/domain"],
       "infrastructure_gate_routes": ["GET /space/infrastructure", "GET /space/infrastructure/readiness"],
       "space_ai_gate_routes": ["GET /space/space-ai", "GET /space/space-ai/readiness"],
       "satellite_gate_routes": ["GET /space/satellite", "GET /space/satellite/readiness"]}
