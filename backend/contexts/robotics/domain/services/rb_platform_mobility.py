"""P216-H Enterprise Autonomous Mobility — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P216-H"
ADR = 480
SOR = "robotics"
API_PREFIX = "/api/v1/robotics"
PRODUCT = (
    "Enterprise Robotics Autonomous Mobility, Connected Vehicles, "
    "Drone Intelligence & Smart Transportation Platform"
)
CAPABILITY = "CAP-PLT-RB-001"
MOBILITY_VISION = (
    "MEOS Autonomous Mobility Platform SHALL coordinate vehicles, drones, fleets "
    "and transportation intelligence as intelligent participants within the MEOS "
    "cyber-physical ecosystem."
)
MISSION = (
    "Provide a secure, AI-native, autonomous, connected mobility ecosystem that "
    "coordinates vehicles, robots, drones, operators and enterprise transportation."
)
VISION = (
    "Every enterprise mobility asset shall become an intelligent, autonomous, "
    "self-learning participant within the MEOS cyber-physical ecosystem."
)
FABRIC = "meos_autonomous_mobility_fabric"
FOUNDATION_GATE = "P216"
MISSION_GATE = "P216-A"
STRATEGY_GATE = "P216-B"
DOMAIN_GATE = "P216-C"
RUNTIME_GATE = "P216-D"
PHYSICAL_AI_GATE = "P216-E"
INDUSTRIAL_GATE = "P216-F"
LOGISTICS_GATE = "P216-G"
SUPREME_GATE = "P215-Z"
AI_GATE = "P214-Z"
CORE_DOMAIN = "enterprise_autonomous_mobility_intelligence"
AGGREGATE = "MobilityAggregate"

SUPPORTING_DOMAINS = (
    "connected_vehicles",
    "autonomous_navigation",
    "drone_operations",
    "fleet_operations",
    "route_intelligence",
    "traffic_intelligence",
    "mobility_safety",
    "airspace_management",
    "charging_infrastructure",
    "vehicle_health",
    "mobility_digital_twin",
    "emergency_operations",
)
ENTITIES = (
    "Vehicle",
    "AutonomousVehicle",
    "Drone",
    "ChargingStation",
    "Fleet",
    "Driver",
    "Pilot",
    "NavigationMission",
    "MobilityRoute",
    "TrafficZone",
    "AirCorridor",
    "MissionController",
    "MobilityDigitalTwin",
)
VALUE_OBJECTS = (
    "VehicleIdentity",
    "VehicleLocation",
    "RouteScore",
    "NavigationState",
    "BatteryLevel",
    "PayloadWeight",
    "FlightAltitude",
    "TrafficDensity",
    "WeatherRisk",
    "SafetyStatus",
    "MissionPriority",
)
BOUNDED_CONTEXTS = (
    {"id": "BC-01", "name": "Connected Vehicle Context", "responsibilities": ("vehicle_lifecycle", "connectivity", "identity", "telematics")},
    {"id": "BC-02", "name": "Autonomous Navigation Context", "responsibilities": ("route_planning", "navigation", "obstacle_avoidance", "dynamic_routing")},
    {"id": "BC-03", "name": "Drone Operations Context", "responsibilities": ("flight_planning", "mission_execution", "swarm_coordination", "airspace_compliance")},
    {"id": "BC-04", "name": "Fleet Mobility Context", "responsibilities": ("fleet_orchestration", "vehicle_assignment", "resource_optimization")},
    {"id": "BC-05", "name": "Traffic Intelligence Context", "responsibilities": ("traffic_prediction", "congestion_analysis", "signal_optimization")},
    {"id": "BC-06", "name": "Mobility Safety Context", "responsibilities": ("collision_prevention", "risk_analysis", "emergency_response")},
    {"id": "BC-07", "name": "Mobility Digital Twin Context", "responsibilities": ("simulation", "replay", "prediction", "optimization")},
    {"id": "BC-08", "name": "Vehicle Maintenance Context", "responsibilities": ("predictive_maintenance", "diagnostics", "ota_lifecycle")},
)
CONNECTED_VEHICLE = {
    "present_required": True,
    "platform": "meos_connected_vehicle_platform",
    "components": (
        "vehicle_registry",
        "vehicle_identity_manager",
        "telematics_gateway",
        "v2x_gateway",
        "ota_update_platform",
        "vehicle_edge_runtime",
        "remote_diagnostics",
        "fleet_connectivity_manager",
    ),
    "capabilities": (
        "vehicle_to_vehicle",
        "vehicle_to_infrastructure",
        "vehicle_to_cloud",
        "vehicle_telemetry",
        "remote_configuration",
        "secure_ota_updates",
        "continuous_monitoring",
    ),
    "v2x_via_integration_platform": True,
}
AUTONOMOUS_NAVIGATION = {
    "present_required": True,
    "engine": "meos_autonomous_navigation_engine",
    "capabilities": (
        "localization",
        "hd_mapping",
        "sensor_fusion",
        "trajectory_planning",
        "decision_planning",
        "obstacle_avoidance",
        "adaptive_cruise_intelligence",
        "lane_intelligence",
        "parking_intelligence",
        "emergency_behaviour",
    ),
}
DRONE_INTELLIGENCE = {
    "present_required": True,
    "platform": "meos_drone_intelligence_platform",
    "drone_types": (
        "inspection_drones",
        "delivery_drones",
        "survey_drones",
        "security_drones",
        "industrial_drones",
        "emergency_response_drones",
    ),
    "capabilities": (
        "mission_planning",
        "swarm_coordination",
        "autonomous_flight",
        "payload_optimization",
        "weather_intelligence",
        "geofencing",
        "return_to_base_automation",
    ),
}
FLEET_MOBILITY = {
    "present_required": True,
    "platform": "meos_intelligent_fleet_platform",
    "capabilities": (
        "fleet_orchestration",
        "vehicle_assignment",
        "resource_optimization",
        "fleet_balancing",
        "mission_dispatch",
    ),
}
SMART_TRANSPORTATION = {
    "present_required": True,
    "platform": "meos_transportation_intelligence_platform",
    "capabilities": (
        "traffic_optimization",
        "fleet_dispatch",
        "demand_prediction",
        "dynamic_routing",
        "mobility_scheduling",
        "urban_mobility_coordination",
        "public_transport_integration",
        "smart_parking",
        "carbon_optimization",
        "emergency_routing",
    ),
}
MOBILITY_DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_transportation_digital_twin",
    "represents": (
        "vehicles", "road_networks", "drone_corridors", "traffic_signals",
        "charging_stations", "logistics_hubs", "weather_conditions", "mobility_infrastructure",
    ),
    "capabilities": (
        "simulation",
        "scenario_planning",
        "traffic_replay",
        "capacity_planning",
        "risk_prediction",
        "operational_optimization",
    ),
}
TRANSPORTATION_KG = {
    "present_required": True,
    "graph": "meos_transportation_knowledge_graph",
    "nodes": (
        "vehicles", "drones", "routes", "roads", "intersections", "drivers", "pilots",
        "traffic_events", "infrastructure", "charging_stations", "air_corridors", "maintenance_assets",
    ),
    "relationships": (
        "travels_on", "assigned_to", "operates", "charges_at", "avoids",
        "communicates_with", "depends_on", "optimizes", "maintains", "inspects",
    ),
    "enables": (
        "mobility_reasoning",
        "fleet_intelligence",
        "traffic_prediction",
        "cross_domain_optimization",
    ),
}
OBSERVABILITY = {
    "present_required": True,
    "platform": "meos_mobility_observability_platform",
    "monitors": (
        "fleet_health",
        "vehicle_health",
        "navigation_accuracy",
        "traffic_conditions",
        "mission_success",
        "battery_health",
        "communication_quality",
        "drone_flight_safety",
        "ai_decision_confidence",
    ),
    "via_platform_observability": True,
}
SECURITY = {
    "present_required": True,
    "framework": "meos_mobility_zero_trust_framework",
    "includes": (
        "vehicle_identity",
        "drone_identity",
        "mission_authorization",
        "secure_telemetry",
        "encrypted_v2x",
        "ota_security",
        "edge_security",
        "operational_safety",
        "threat_detection",
        "fleet_isolation",
    ),
    "zero_trust": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "via_integration_platform": True,
    "v2x_via_integration_platform_only": True,
    "never_direct_v2x_bypass": True,
    "no_module_local_llm": True,
    "physical_ai_via_p214z_acl_only": True,
    "never_replace_p216_foundation": True,
    "never_replace_p216_g_logistics": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "ungated_physical_autonomy_strategy_forbidden": True,
    "opaque_safety_strategy_forbidden": True,
}
COMMANDS = (
    "RegisterVehicleCommand",
    "AssignMissionCommand",
    "LaunchDroneCommand",
    "OptimizeRouteCommand",
    "UpdateNavigationCommand",
    "CompleteMissionCommand",
    "ScheduleMaintenanceCommand",
)
QUERIES = (
    "GetVehicleStatusQuery",
    "GetFleetStatusQuery",
    "GetMissionStateQuery",
    "GetTrafficStateQuery",
    "GetDroneStatusQuery",
    "GetDigitalTwinQuery",
)
CORE_EVENTS = (
    {"name": "VehicleConnectedEvent", "schema": "robotics.mobility.vehicle.connected.v1", "owner": "BC-01", "consumers": "fleet,audit,telematics"},
    {"name": "MissionStartedEvent", "schema": "robotics.mobility.mission.started.v1", "owner": "BC-04", "consumers": "navigation,audit,analytics"},
    {"name": "NavigationUpdatedEvent", "schema": "robotics.mobility.navigation.updated.v1", "owner": "BC-02", "consumers": "twin,fleet,audit"},
    {"name": "ObstacleDetectedEvent", "schema": "robotics.mobility.obstacle.detected.v1", "owner": "BC-02", "consumers": "safety,navigation,audit"},
    {"name": "DroneTakeoffEvent", "schema": "robotics.mobility.drone.takeoff.v1", "owner": "BC-03", "consumers": "airspace,fleet,audit"},
    {"name": "DroneLandingEvent", "schema": "robotics.mobility.drone.landing.v1", "owner": "BC-03", "consumers": "fleet,audit,analytics"},
    {"name": "TrafficCongestionDetectedEvent", "schema": "robotics.mobility.traffic.congestion.detected.v1", "owner": "BC-05", "consumers": "routing,fleet,audit"},
    {"name": "EmergencyRouteActivatedEvent", "schema": "robotics.mobility.emergency.route.activated.v1", "owner": "BC-06", "consumers": "fleet,navigation,audit"},
    {"name": "VehicleMaintenanceCompletedEvent", "schema": "robotics.mobility.vehicle.maintenance.completed.v1", "owner": "BC-08", "consumers": "fleet,audit"},
    {"name": "FleetOptimizationCompletedEvent", "schema": "robotics.mobility.fleet.optimization.completed.v1", "owner": "BC-04", "consumers": "analytics,twin,audit"},
)
MICROSERVICES = (
    {"id": "vehicle_service", "bc": "BC-01", "api": "/robotics/mobility/vehicles", "db": "robotics_*", "events": ("VehicleConnectedEvent",), "security": ("robotics.write",), "scaling": "vehicle_replicas", "responsibility": "Vehicle lifecycle and identity"},
    {"id": "navigation_service", "bc": "BC-02", "api": "/robotics/mobility/navigation", "db": "robotics_*", "events": ("NavigationUpdatedEvent", "ObstacleDetectedEvent"), "security": ("robotics.write",), "scaling": "nav_workers", "responsibility": "Autonomous navigation and routing"},
    {"id": "drone_service", "bc": "BC-03", "api": "/robotics/mobility/drones", "db": "robotics_*", "events": ("DroneTakeoffEvent", "DroneLandingEvent"), "security": ("robotics.write",), "scaling": "drone_workers", "responsibility": "Drone mission and swarm coordination"},
    {"id": "fleet_service", "bc": "BC-04", "api": "/robotics/mobility/fleet", "db": "robotics_*", "events": ("MissionStartedEvent", "FleetOptimizationCompletedEvent"), "security": ("robotics.write",), "scaling": "fleet_workers", "responsibility": "Fleet orchestration and assignment"},
    {"id": "traffic_intelligence_service", "bc": "BC-05", "api": "/robotics/mobility/traffic", "db": "robotics_*", "events": ("TrafficCongestionDetectedEvent",), "security": ("robotics.read",), "scaling": "traffic_workers", "responsibility": "Traffic prediction and congestion intelligence"},
    {"id": "digital_twin_service", "bc": "BC-07", "api": "/robotics/mobility/digital-twin", "db": "robotics_*", "events": ("NavigationUpdatedEvent", "FleetOptimizationCompletedEvent"), "security": ("robotics.read",), "scaling": "twin_workers", "responsibility": "Transportation digital twin sync"},
    {"id": "maintenance_service", "bc": "BC-08", "api": "/robotics/mobility/maintenance", "db": "robotics_*", "events": ("VehicleMaintenanceCompletedEvent",), "security": ("robotics.write",), "scaling": "maintenance_workers", "responsibility": "Predictive maintenance and OTA lifecycle projections"},
    {"id": "telematics_service", "bc": "BC-01", "api": "/robotics/mobility/telematics", "db": "robotics_*", "events": ("VehicleConnectedEvent",), "security": ("robotics.read",), "scaling": "telematics_workers", "responsibility": "Telematics projections via Integration Platform"},
    {"id": "mobility_analytics_service", "bc": "BC-05", "api": "/robotics/mobility/analytics", "db": "robotics_*", "events": ("FleetOptimizationCompletedEvent",), "security": ("robotics.read",), "scaling": "analytics_workers", "responsibility": "Mobility analytics facets"},
    {"id": "knowledge_graph_service", "bc": "BC-07", "api": "/robotics/mobility/knowledge-graph", "db": "robotics_*", "events": ("FleetOptimizationCompletedEvent",), "security": ("robotics.read",), "scaling": "kg_workers", "responsibility": "Transportation knowledge graph projections"},
)
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p216d_robotics_os",
        "p216e_physical_ai",
        "p216f_industrial",
        "p216g_autonomous_logistics",
        "p214z_ai_master",
        "p215z_quantum_supreme",
        "enterprise_gis",
        "erp",
        "scm",
        "iot_platform",
        "digital_twin_platform",
        "weather_intelligence_platform",
        "traffic_management_systems",
        "emergency_response_platform",
        "integration_platform",
    ),
    "mechanisms": (
        "vehicle_apis",
        "navigation_apis",
        "drone_mission_interfaces",
        "v2x_via_integration_connectors",
        "mobility_event_contracts",
        "fleet_intelligence_interfaces",
    ),
    "via_p216_d": True,
    "via_p216_e": True,
    "via_p216_f": True,
    "via_p216_g": True,
    "via_p214_z": True,
    "via_p215_z": True,
    "via_p213": True,
    "via_integration_platform": True,
    "never_direct_v2x_bypass": True,
}
DEPLOYMENT = {
    "present_required": True,
    "model": "hybrid_autonomous_mobility_infrastructure",
    "includes": (
        "cloud_mobility_platform",
        "edge_mobility_cluster",
        "vehicle_edge_runtime",
        "drone_runtime_platform",
        "fleet_control_cluster",
        "digital_twin_cluster",
        "knowledge_graph_cluster",
        "ai_compute_cluster",
        "security_platform",
        "global_operations_center",
    ),
    "deployment_models": (
        "single_fleet",
        "multi_fleet",
        "regional_mobility",
        "global_mobility_network",
    ),
    "cloud_native": True,
    "edge_native": True,
}
TESTING = (
    "autonomous_navigation_testing",
    "connected_vehicle_testing",
    "drone_flight_testing",
    "fleet_coordination_testing",
    "traffic_simulation_testing",
    "digital_twin_testing",
    "cybersecurity_testing",
    "safety_validation",
    "scalability_testing",
    "resilience_testing",
    "disaster_recovery_testing",
)
API_SURFACES = (
    "/api/v1/robotics/mobility",
    "/api/v1/robotics/mobility/vision",
    "/api/v1/robotics/mobility/domain",
    "/api/v1/robotics/mobility/bounded-contexts",
    "/api/v1/robotics/mobility/connected-vehicle",
    "/api/v1/robotics/mobility/navigation",
    "/api/v1/robotics/mobility/drones",
    "/api/v1/robotics/mobility/fleet",
    "/api/v1/robotics/mobility/transportation",
    "/api/v1/robotics/mobility/digital-twin",
    "/api/v1/robotics/mobility/knowledge-graph",
    "/api/v1/robotics/mobility/observability",
    "/api/v1/robotics/mobility/security",
    "/api/v1/robotics/mobility/cqrs",
    "/api/v1/robotics/mobility/events",
    "/api/v1/robotics/mobility/microservices",
    "/api/v1/robotics/mobility/integration",
    "/api/v1/robotics/mobility/deployment",
    "/api/v1/robotics/mobility/testing",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
QUALITY_GATES_REJECT_IF = (
    "connected_vehicle_platform_is_missing",
    "autonomous_mobility_platform_is_missing",
    "autonomous_navigation_platform_is_missing",
    "drone_intelligence_platform_is_missing",
    "fleet_mobility_platform_is_missing",
    "smart_transportation_platform_is_missing",
    "mobility_digital_twin_is_missing",
    "transportation_knowledge_graph_is_missing",
    "observability_platform_is_missing",
    "security_architecture_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "cloud_edge_deployment_is_missing",
    "enterprise_mobility_integration_is_missing",
    "testing_architecture_is_missing",
    "sibling_robotics_bc",
    "replace_p216_g_logistics",
    "direct_v2x_bypass",
    "module_local_llm",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Autonomous Mobility Fabric",
        "mobility_vision": MOBILITY_VISION,
        "mission": MISSION,
        "vision": VISION,
        "builds_on_p216": True,
        "builds_on_p216_g": True,
        "builds_on_p216_f": True,
        "builds_on_p216_e": True,
        "builds_on_p216_d": True,
        "builds_on_p215_z": True,
        "builds_on_p214_z": True,
        "never_replace_p216_g_logistics": True,
        "foundation_gate": FOUNDATION_GATE,
        "logistics_gate": LOGISTICS_GATE,
        "industrial_gate": INDUSTRIAL_GATE,
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

def connected_vehicle() -> dict[str, Any]:
    return dict(CONNECTED_VEHICLE)

def navigation() -> dict[str, Any]:
    return dict(AUTONOMOUS_NAVIGATION)

def drones() -> dict[str, Any]:
    return dict(DRONE_INTELLIGENCE)

def fleet() -> dict[str, Any]:
    return dict(FLEET_MOBILITY)

def transportation() -> dict[str, Any]:
    return dict(SMART_TRANSPORTATION)

def digital_twin() -> dict[str, Any]:
    return dict(MOBILITY_DIGITAL_TWIN)

def knowledge_graph() -> dict[str, Any]:
    return dict(TRANSPORTATION_KG)

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
        "logistics_gate_api": "/api/v1/robotics/logistics",
        "industrial_gate_api": "/api/v1/robotics/industrial",
        "runtime_gate_api": "/api/v1/robotics/runtime",
    }

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p216_i": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "mobility_vision": MOBILITY_VISION, "mission": MISSION, "vision": VISION, "principle": MOBILITY_VISION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE, "runtime_gate": RUNTIME_GATE,
        "physical_ai_gate": PHYSICAL_AI_GATE, "industrial_gate": INDUSTRIAL_GATE,
        "logistics_gate": LOGISTICS_GATE, "supreme_gate": SUPREME_GATE, "ai_gate": AI_GATE,
        "builds_on": [
            "P216", "P216-A", "P216-B", "P216-C", "P216-D", "P216-E", "P216-F", "P216-G",
            "P215-Z", "P214-Z", "P213",
            "ADR-472", "ADR-473", "ADR-474", "ADR-475", "ADR-476", "ADR-477", "ADR-478", "ADR-479",
        ],
        "vision_pack": vision_pack(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "connected_vehicle": connected_vehicle(),
        "navigation": navigation(),
        "drones": drones(),
        "fleet": fleet(),
        "transportation": transportation(),
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
        "connected_vehicle_platform_present_required": True,
        "autonomous_mobility_platform_present_required": True,
        "autonomous_navigation_platform_present_required": True,
        "drone_intelligence_platform_present_required": True,
        "fleet_mobility_platform_present_required": True,
        "smart_transportation_platform_present_required": True,
        "mobility_digital_twin_present_required": True,
        "transportation_knowledge_graph_present_required": True,
        "observability_platform_present_required": True,
        "security_architecture_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "cloud_edge_deployment_present_required": True,
        "enterprise_mobility_integration_present_required": True,
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
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_direct_v2x_bypass": True,
        "v2x_via_integration_platform_only": True,
        "no_module_local_llm": True,
        "physical_ai_via_p214z_acl_only": True,
        "ungated_physical_autonomy_strategy_forbidden": True,
        "opaque_safety_strategy_forbidden": True,
        "builds_on_p216": True, "builds_on_p216_g": True, "builds_on_p216_f": True,
        "builds_on_p216_e": True, "builds_on_p216_d": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p216_d": True, "via_p216_e": True, "via_p216_f": True, "via_p216_g": True,
        "via_p215_z": True, "via_p214_z": True, "via_p213": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "via_integration_platform": True,
        "api_prefix": f"{API_PREFIX}/mobility",
        "forbidden_sibling_bc": [
            "autonomous_mobility_platform",
            "connected_vehicle_platform",
            "drone_intelligence_platform",
            "smart_transportation_platform",
        ],
        "foundation_for_p216_i": True,
    }

def mobility_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /robotics/mobility",
        "GET /robotics/mobility/vision",
        "GET /robotics/mobility/domain",
        "GET /robotics/mobility/bounded-contexts",
        "GET /robotics/mobility/connected-vehicle",
        "GET /robotics/mobility/navigation",
        "GET /robotics/mobility/drones",
        "GET /robotics/mobility/fleet",
        "GET /robotics/mobility/transportation",
        "GET /robotics/mobility/digital-twin",
        "GET /robotics/mobility/knowledge-graph",
        "GET /robotics/mobility/observability",
        "GET /robotics/mobility/security",
        "GET /robotics/mobility/cqrs",
        "GET /robotics/mobility/events",
        "GET /robotics/mobility/microservices",
        "GET /robotics/mobility/integration",
        "GET /robotics/mobility/deployment",
        "GET /robotics/mobility/testing",
        "GET /robotics/mobility/readiness",
    ], "logistics_gate_routes": ["GET /robotics/logistics", "GET /robotics/logistics/readiness"]}
