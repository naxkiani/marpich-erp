"""P216-L Enterprise Public Safety & Civil Protection — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P216-L"
ADR = 484
SOR = "robotics"
API_PREFIX = "/api/v1/robotics"
PRODUCT = (
    "Enterprise Robotics Public Safety, Emergency Response, "
    "Disaster Recovery & Civil Protection Intelligence Platform"
)
CAPABILITY = "CAP-PLT-RB-001"
PUBLIC_SAFETY_VISION = (
    "MEOS Civil Protection Intelligence Platform SHALL unify public safety robotics, "
    "emergency operations, disaster recovery and community resilience as intelligent "
    "participants within the MEOS cyber-physical ecosystem."
)
MISSION = (
    "Create an intelligent, AI-assisted, robotics-enabled public safety ecosystem "
    "that improves preparedness, response, recovery and resilience for communities."
)
VISION = (
    "Every emergency operation, robot, drone, responder, critical infrastructure "
    "asset and emergency workflow shall become part of the unified MEOS Civil "
    "Protection Ecosystem."
)
FABRIC = "meos_civil_protection_intelligence_fabric"
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
SUPREME_GATE = "P215-Z"
AI_GATE = "P214-Z"
CORE_DOMAIN = "enterprise_emergency_civil_protection_intelligence"
AGGREGATE = "EmergencyManagementAggregate"

SUPPORTING_DOMAINS = (
    "incident_management",
    "emergency_operations",
    "disaster_recovery",
    "public_safety",
    "search_and_rescue",
    "humanitarian_logistics",
    "emergency_healthcare_coordination",
    "infrastructure_recovery",
    "volunteer_coordination",
    "situation_awareness",
    "disaster_digital_twin",
    "community_resilience",
)
ENTITIES = (
    "EmergencyIncident",
    "EmergencyOperation",
    "EmergencyMission",
    "Responder",
    "EmergencyRobot",
    "EmergencyDrone",
    "Shelter",
    "Hospital",
    "ReliefCenter",
    "Volunteer",
    "Victim",
    "CriticalInfrastructure",
    "RecoveryProject",
    "DisasterDigitalTwin",
)
VALUE_OBJECTS = (
    "SeverityLevel",
    "RiskScore",
    "IncidentLocation",
    "ResourcePriority",
    "ResponseTime",
    "SafetyZone",
    "WeatherCondition",
    "EvacuationArea",
    "MissionStatus",
    "RecoveryProgress",
)
BOUNDED_CONTEXTS = (
    {"id": "BC-01", "name": "Incident Management Context", "responsibilities": ("incident_lifecycle", "severity_scoring", "classification", "closure"), "aggregates": ("EmergencyIncident",), "domain_services": ("incident_classification",), "events": ("IncidentReportedEvent",), "policies": ("severity_thresholds",)},
    {"id": "BC-02", "name": "Emergency Operations Context", "responsibilities": ("eoc_command", "multi_agency_coordination", "resource_allocation", "volunteer_coordination"), "aggregates": ("EmergencyOperation",), "domain_services": ("resource_allocator",), "events": ("EmergencyActivatedEvent",), "policies": ("multi_agency_auth",)},
    {"id": "BC-03", "name": "Search & Rescue Context", "responsibilities": ("sar_missions", "victim_location", "field_tasking"), "aggregates": ("EmergencyMission",), "domain_services": ("sar_planner",), "events": ("MissionAssignedEvent",), "policies": ("sar_safety_envelopes",)},
    {"id": "BC-04", "name": "Public Safety Robotics Context", "responsibilities": ("robot_fleet", "drone_survey", "hazard_assessment"), "aggregates": ("EmergencyRobot", "EmergencyDrone"), "domain_services": ("fleet_mission_planner",), "events": ("DroneSurveyCompletedEvent",), "policies": ("mission_authorisation",)},
    {"id": "BC-05", "name": "Disaster Recovery Context", "responsibilities": ("damage_assessment", "restoration_planning", "recovery_kpis"), "aggregates": ("RecoveryProject",), "domain_services": ("recovery_planner",), "events": ("RecoveryInitiatedEvent", "InfrastructureRecoveredEvent"), "policies": ("recovery_prioritisation",)},
    {"id": "BC-06", "name": "Humanitarian Logistics Context", "responsibilities": ("aid_distribution", "shelter_capacity", "relief_tracking"), "aggregates": ("Shelter", "ReliefCenter"), "domain_services": ("relief_orchestrator",), "events": ("EvacuationCompletedEvent",), "policies": ("aid_equity",)},
    {"id": "BC-07", "name": "Disaster Digital Twin Context", "responsibilities": ("scenario_simulation", "impact_modelling", "operational_replay"), "aggregates": ("DisasterDigitalTwin",), "domain_services": ("twin_sync",), "events": ("DroneSurveyCompletedEvent",), "policies": ("twin_integrity",)},
    {"id": "BC-08", "name": "Community Resilience & Governance Context", "responsibilities": ("after_action_review", "compliance", "community_resilience", "audit"), "aggregates": ("EmergencyOperation",), "domain_services": ("governance_review",), "events": ("AfterActionReviewCompletedEvent",), "policies": ("privacy_by_design",)},
)
PUBLIC_SAFETY_ROBOTICS = {
    "present_required": True,
    "platform": "meos_public_safety_robotics_platform",
    "components": (
        "emergency_robot_registry",
        "robot_fleet_manager",
        "mission_planner",
        "responder_coordination_engine",
        "emergency_drone_coordinator",
        "field_operations_console",
    ),
    "capabilities": (
        "search_support",
        "infrastructure_inspection",
        "hazard_assessment",
        "damage_mapping",
        "medical_supply_delivery",
        "environmental_monitoring",
        "remote_communications_support",
    ),
}
EMERGENCY_RESPONSE = {
    "present_required": True,
    "platform": "meos_emergency_operations_platform",
    "capabilities": (
        "incident_lifecycle_management",
        "emergency_command_center",
        "multi_agency_coordination",
        "resource_allocation",
        "volunteer_coordination",
        "shelter_management",
        "evacuation_coordination",
        "relief_distribution",
    ),
}
DISASTER_RECOVERY = {
    "present_required": True,
    "platform": "meos_disaster_recovery_platform",
    "capabilities": (
        "damage_assessment",
        "infrastructure_restoration_planning",
        "recovery_programme_management",
        "aid_distribution_tracking",
        "recovery_kpi_monitoring",
        "community_recovery_analytics",
        "business_continuity_coordination",
    ),
}
CIVIL_PROTECTION = {
    "present_required": True,
    "platform": "meos_civil_protection_platform",
    "capabilities": (
        "preparedness",
        "response",
        "recovery",
        "community_resilience",
        "critical_infrastructure_protection",
    ),
}
SITUATION_INTELLIGENCE = {
    "present_required": True,
    "engine": "meos_ai_situational_intelligence",
    "capabilities": (
        "incident_classification",
        "risk_forecasting",
        "impact_estimation",
        "resource_optimisation",
        "evacuation_recommendations",
        "traffic_impact_prediction",
        "infrastructure_prioritisation",
        "operational_decision_support",
    ),
    "via_p214_z": True,
    "explainable_ai": True,
    "human_centered": True,
}
DISASTER_DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_disaster_digital_twin",
    "represents": (
        "cities", "communities", "roads", "hospitals", "shelters",
        "utilities", "communication_networks", "critical_infrastructure", "emergency_assets",
    ),
    "capabilities": (
        "scenario_simulation",
        "impact_modelling",
        "recovery_simulation",
        "infrastructure_resilience_analysis",
        "capacity_planning",
        "operational_replay",
    ),
}
PUBLIC_SAFETY_KG = {
    "present_required": True,
    "graph": "meos_public_safety_knowledge_graph",
    "nodes": (
        "incidents", "responders", "robots", "drones", "shelters", "hospitals",
        "citizens", "infrastructure", "recovery_projects", "resources", "volunteers",
    ),
    "relationships": (
        "responds_to", "supports", "located_at", "assigned_to", "depends_on",
        "protects", "restores", "coordinates",
    ),
    "enables": (
        "emergency_reasoning",
        "operational_awareness",
        "cross_agency_collaboration",
        "community_resilience_intelligence",
    ),
}
OBSERVABILITY = {
    "present_required": True,
    "platform": "meos_public_safety_observability",
    "monitors": (
        "emergency_kpis",
        "incident_response_time",
        "mission_success_rate",
        "robot_fleet_health",
        "infrastructure_recovery",
        "shelter_capacity",
        "resource_utilisation",
        "digital_twin_synchronisation",
        "ai_recommendation_accuracy",
    ),
    "via_platform_observability": True,
}
SECURITY = {
    "present_required": True,
    "framework": "meos_public_safety_zero_trust_framework",
    "domains": (
        "responder_identity",
        "robot_identity",
        "drone_identity",
        "agency_identity",
        "mission_authorisation",
        "critical_infrastructure_protection",
        "data_privacy",
        "operational_logging",
        "continuous_monitoring",
        "compliance",
        "auditability",
    ),
    "zero_trust": True,
    "privacy_by_design": True,
    "multi_region_resilience": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "via_integration_platform": True,
    "via_notification_platform": True,
    "gis_weather_via_integration_platform_only": True,
    "never_direct_gis_weather_bypass": True,
    "citizen_alerts_via_notification_platform_only": True,
    "never_bypass_notification_platform": True,
    "never_duplicate_hospital_clinic_core_logic": True,
    "no_module_local_llm": True,
    "physical_ai_via_p214z_acl_only": True,
    "human_centered_explainable_ai_required": True,
    "never_replace_p216_foundation": True,
    "never_replace_p216_k_construction": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "ungated_physical_autonomy_strategy_forbidden": True,
    "opaque_safety_strategy_forbidden": True,
}
COMMANDS = (
    "ReportIncidentCommand",
    "DeclareEmergencyCommand",
    "AssignMissionCommand",
    "DispatchResponderCommand",
    "OpenShelterCommand",
    "StartRecoveryCommand",
    "CloseIncidentCommand",
)
QUERIES = (
    "GetIncidentStatusQuery",
    "GetMissionStatusQuery",
    "GetShelterCapacityQuery",
    "GetInfrastructureStatusQuery",
    "GetRecoveryProgressQuery",
    "GetDigitalTwinQuery",
)
CORE_EVENTS = (
    {"name": "IncidentReportedEvent", "schema": "robotics.public_safety.incident.reported.v1", "owner": "BC-01", "consumers": "eoc,analytics,audit"},
    {"name": "EmergencyActivatedEvent", "schema": "robotics.public_safety.emergency.activated.v1", "owner": "BC-02", "consumers": "robotics,notifications,audit"},
    {"name": "MissionAssignedEvent", "schema": "robotics.public_safety.mission.assigned.v1", "owner": "BC-03", "consumers": "runtime,fleet,audit"},
    {"name": "ResponderArrivedEvent", "schema": "robotics.public_safety.responder.arrived.v1", "owner": "BC-02", "consumers": "eoc,twin,audit"},
    {"name": "DroneSurveyCompletedEvent", "schema": "robotics.public_safety.drone.survey.completed.v1", "owner": "BC-04", "consumers": "twin,recovery,audit"},
    {"name": "EvacuationCompletedEvent", "schema": "robotics.public_safety.evacuation.completed.v1", "owner": "BC-06", "consumers": "eoc,analytics,audit"},
    {"name": "RecoveryInitiatedEvent", "schema": "robotics.public_safety.recovery.initiated.v1", "owner": "BC-05", "consumers": "twin,analytics,audit"},
    {"name": "InfrastructureRecoveredEvent", "schema": "robotics.public_safety.infrastructure.recovered.v1", "owner": "BC-05", "consumers": "twin,governance,audit"},
    {"name": "AfterActionReviewCompletedEvent", "schema": "robotics.public_safety.after_action.review.completed.v1", "owner": "BC-08", "consumers": "kg,analytics,audit"},
)
MICROSERVICES = (
    {"id": "incident_management_service", "bc": "BC-01", "api": "/robotics/public-safety/incidents", "db": "robotics_*", "events": ("IncidentReportedEvent",), "security": ("robotics.write",), "scaling": "incident_replicas", "responsibility": "Incident lifecycle and severity"},
    {"id": "emergency_operations_service", "bc": "BC-02", "api": "/robotics/public-safety/operations", "db": "robotics_*", "events": ("EmergencyActivatedEvent", "ResponderArrivedEvent"), "security": ("robotics.write",), "scaling": "eoc_workers", "responsibility": "EOC and multi-agency coordination"},
    {"id": "public_safety_robotics_service", "bc": "BC-04", "api": "/robotics/public-safety/robots", "db": "robotics_*", "events": ("DroneSurveyCompletedEvent", "MissionAssignedEvent"), "security": ("robotics.write",), "scaling": "robot_workers", "responsibility": "Emergency robot and drone fleet"},
    {"id": "search_and_rescue_service", "bc": "BC-03", "api": "/robotics/public-safety/sar", "db": "robotics_*", "events": ("MissionAssignedEvent",), "security": ("robotics.write",), "scaling": "sar_workers", "responsibility": "Search and rescue mission planning"},
    {"id": "shelter_management_service", "bc": "BC-06", "api": "/robotics/public-safety/shelters", "db": "robotics_*", "events": ("EvacuationCompletedEvent",), "security": ("robotics.write",), "scaling": "shelter_workers", "responsibility": "Shelter capacity and relief logistics"},
    {"id": "recovery_management_service", "bc": "BC-05", "api": "/robotics/public-safety/recovery", "db": "robotics_*", "events": ("RecoveryInitiatedEvent", "InfrastructureRecoveredEvent"), "security": ("robotics.write",), "scaling": "recovery_workers", "responsibility": "Disaster recovery programmes"},
    {"id": "digital_twin_service", "bc": "BC-07", "api": "/robotics/public-safety/digital-twin", "db": "robotics_*", "events": ("DroneSurveyCompletedEvent", "InfrastructureRecoveredEvent"), "security": ("robotics.read",), "scaling": "twin_workers", "responsibility": "Disaster digital twin sync"},
    {"id": "knowledge_graph_service", "bc": "BC-08", "api": "/robotics/public-safety/knowledge-graph", "db": "robotics_*", "events": ("AfterActionReviewCompletedEvent",), "security": ("robotics.read",), "scaling": "kg_workers", "responsibility": "Public safety knowledge graph"},
    {"id": "situation_intelligence_service", "bc": "BC-02", "api": "/robotics/public-safety/intelligence", "db": "robotics_*", "events": ("IncidentReportedEvent", "EmergencyActivatedEvent"), "security": ("robotics.read",), "scaling": "intel_workers", "responsibility": "AI situational intelligence via P214-Z"},
    {"id": "emergency_analytics_service", "bc": "BC-08", "api": "/robotics/public-safety/analytics", "db": "robotics_*", "events": ("EvacuationCompletedEvent", "AfterActionReviewCompletedEvent"), "security": ("robotics.read",), "scaling": "analytics_workers", "responsibility": "Emergency analytics facets"},
)
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p216d_robotics_os",
        "p216e_physical_ai",
        "p216k_construction",
        "p214z_ai_master",
        "p215z_quantum_supreme",
        "gis_platform",
        "weather_services",
        "healthcare_systems",
        "transportation_systems",
        "utility_platforms",
        "iot_sensors",
        "digital_twin_platform",
        "citizen_notification_platform",
        "integration_platform",
        "notification_platform",
    ),
    "mechanisms": (
        "incident_apis",
        "robot_mission_interfaces",
        "gis_via_integration_connectors",
        "weather_via_integration_connectors",
        "alerts_via_notification_platform",
        "public_safety_event_contracts",
    ),
    "via_p216_d": True,
    "via_p216_e": True,
    "via_p216_k": True,
    "via_p214_z": True,
    "via_p215_z": True,
    "via_p213": True,
    "via_integration_platform": True,
    "via_notification_platform": True,
    "never_direct_gis_weather_bypass": True,
    "never_bypass_notification_platform": True,
    "never_duplicate_hospital_clinic_core_logic": True,
}
DEPLOYMENT = {
    "present_required": True,
    "model": "hybrid_civil_protection_infrastructure",
    "includes": (
        "emergency_operations_cloud",
        "regional_edge_clusters",
        "robot_runtime_platform",
        "drone_control_platform",
        "digital_twin_cluster",
        "knowledge_graph_cluster",
        "ai_platform",
        "observability_platform",
        "disaster_recovery_region",
    ),
    "deployment_models": (
        "municipality",
        "province",
        "national_civil_protection_agency",
        "international_humanitarian_network",
    ),
    "cloud_native": True,
    "edge_native": True,
    "multi_region_resilience": True,
}
TESTING = (
    "incident_workflow_testing",
    "emergency_coordination_testing",
    "robot_fleet_testing",
    "drone_operations_testing",
    "digital_twin_validation",
    "resilience_testing",
    "performance_testing",
    "security_testing",
    "disaster_recovery_testing",
    "business_continuity_testing",
)
API_SURFACES = (
    "/api/v1/robotics/public-safety",
    "/api/v1/robotics/public-safety/vision",
    "/api/v1/robotics/public-safety/domain",
    "/api/v1/robotics/public-safety/bounded-contexts",
    "/api/v1/robotics/public-safety/robotics",
    "/api/v1/robotics/public-safety/emergency",
    "/api/v1/robotics/public-safety/recovery",
    "/api/v1/robotics/public-safety/civil-protection",
    "/api/v1/robotics/public-safety/intelligence",
    "/api/v1/robotics/public-safety/digital-twin",
    "/api/v1/robotics/public-safety/knowledge-graph",
    "/api/v1/robotics/public-safety/observability",
    "/api/v1/robotics/public-safety/security",
    "/api/v1/robotics/public-safety/cqrs",
    "/api/v1/robotics/public-safety/events",
    "/api/v1/robotics/public-safety/microservices",
    "/api/v1/robotics/public-safety/integration",
    "/api/v1/robotics/public-safety/deployment",
    "/api/v1/robotics/public-safety/testing",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
QUALITY_GATES_REJECT_IF = (
    "public_safety_robotics_platform_is_missing",
    "emergency_response_platform_is_missing",
    "disaster_recovery_platform_is_missing",
    "civil_protection_platform_is_missing",
    "disaster_digital_twin_is_missing",
    "situation_intelligence_platform_is_missing",
    "public_safety_knowledge_graph_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "zero_trust_security_is_missing",
    "multi_region_resilience_is_missing",
    "sibling_robotics_bc",
    "replace_p216_k_construction",
    "direct_gis_weather_bypass",
    "bypass_notification_platform",
    "module_local_llm",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Civil Protection Intelligence Fabric",
        "public_safety_vision": PUBLIC_SAFETY_VISION,
        "mission": MISSION,
        "vision": VISION,
        "builds_on_p216": True,
        "builds_on_p216_k": True,
        "builds_on_p216_i": True,
        "builds_on_p216_e": True,
        "builds_on_p216_d": True,
        "builds_on_p215_z": True,
        "builds_on_p214_z": True,
        "never_replace_p216_k_construction": True,
        "foundation_gate": FOUNDATION_GATE,
        "construction_gate": CONSTRUCTION_GATE,
        "healthcare_gate": HEALTHCARE_GATE,
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
    return dict(PUBLIC_SAFETY_ROBOTICS)

def emergency() -> dict[str, Any]:
    return dict(EMERGENCY_RESPONSE)

def recovery() -> dict[str, Any]:
    return dict(DISASTER_RECOVERY)

def civil_protection() -> dict[str, Any]:
    return dict(CIVIL_PROTECTION)

def intelligence() -> dict[str, Any]:
    return dict(SITUATION_INTELLIGENCE)

def digital_twin() -> dict[str, Any]:
    return dict(DISASTER_DIGITAL_TWIN)

def knowledge_graph() -> dict[str, Any]:
    return dict(PUBLIC_SAFETY_KG)

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
        "construction_gate_api": "/api/v1/robotics/construction",
        "runtime_gate_api": "/api/v1/robotics/runtime",
    }

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p216_m": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "public_safety_vision": PUBLIC_SAFETY_VISION, "mission": MISSION, "vision": VISION, "principle": PUBLIC_SAFETY_VISION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE, "runtime_gate": RUNTIME_GATE,
        "physical_ai_gate": PHYSICAL_AI_GATE, "industrial_gate": INDUSTRIAL_GATE,
        "logistics_gate": LOGISTICS_GATE, "mobility_gate": MOBILITY_GATE,
        "healthcare_gate": HEALTHCARE_GATE, "construction_gate": CONSTRUCTION_GATE,
        "supreme_gate": SUPREME_GATE, "ai_gate": AI_GATE,
        "builds_on": [
            "P216", "P216-A", "P216-B", "P216-C", "P216-D", "P216-E", "P216-F", "P216-G", "P216-H", "P216-I", "P216-K",
            "P215-Z", "P214-Z", "P213",
            "ADR-472", "ADR-473", "ADR-474", "ADR-475", "ADR-476", "ADR-477", "ADR-478", "ADR-479", "ADR-480", "ADR-481", "ADR-483",
        ],
        "vision_pack": vision_pack(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "robotics_platform": robotics_platform(),
        "emergency": emergency(),
        "recovery": recovery(),
        "civil_protection": civil_protection(),
        "intelligence": intelligence(),
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
        "public_safety_robotics_platform_present_required": True,
        "emergency_response_platform_present_required": True,
        "disaster_recovery_platform_present_required": True,
        "civil_protection_platform_present_required": True,
        "disaster_digital_twin_present_required": True,
        "situation_intelligence_platform_present_required": True,
        "public_safety_knowledge_graph_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "zero_trust_security_present_required": True,
        "multi_region_resilience_present_required": True,
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
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_direct_gis_weather_bypass": True,
        "gis_weather_via_integration_platform_only": True,
        "never_bypass_notification_platform": True,
        "citizen_alerts_via_notification_platform_only": True,
        "never_duplicate_hospital_clinic_core_logic": True,
        "no_module_local_llm": True,
        "physical_ai_via_p214z_acl_only": True,
        "human_centered_explainable_ai_required": True,
        "ungated_physical_autonomy_strategy_forbidden": True,
        "opaque_safety_strategy_forbidden": True,
        "builds_on_p216": True, "builds_on_p216_k": True, "builds_on_p216_i": True,
        "builds_on_p216_e": True, "builds_on_p216_d": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p216_d": True, "via_p216_e": True, "via_p216_k": True,
        "via_p215_z": True, "via_p214_z": True, "via_p213": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "via_integration_platform": True, "via_notification_platform": True,
        "api_prefix": f"{API_PREFIX}/public-safety",
        "forbidden_sibling_bc": [
            "public_safety_robotics_platform",
            "emergency_response_platform",
            "disaster_recovery_platform",
            "civil_protection_platform",
        ],
        "foundation_for_p216_m": True,
        "p216_j_agriculture_planned": True,
    }

def public_safety_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /robotics/public-safety",
        "GET /robotics/public-safety/vision",
        "GET /robotics/public-safety/domain",
        "GET /robotics/public-safety/bounded-contexts",
        "GET /robotics/public-safety/robotics",
        "GET /robotics/public-safety/emergency",
        "GET /robotics/public-safety/recovery",
        "GET /robotics/public-safety/civil-protection",
        "GET /robotics/public-safety/intelligence",
        "GET /robotics/public-safety/digital-twin",
        "GET /robotics/public-safety/knowledge-graph",
        "GET /robotics/public-safety/observability",
        "GET /robotics/public-safety/security",
        "GET /robotics/public-safety/cqrs",
        "GET /robotics/public-safety/events",
        "GET /robotics/public-safety/microservices",
        "GET /robotics/public-safety/integration",
        "GET /robotics/public-safety/deployment",
        "GET /robotics/public-safety/testing",
        "GET /robotics/public-safety/readiness",
    ], "construction_gate_routes": ["GET /robotics/construction", "GET /robotics/construction/readiness"]}
