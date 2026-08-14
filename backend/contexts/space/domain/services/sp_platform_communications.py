"""P218-H Enterprise Space Intelligence Space Communications — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P218-H"
ADR = 534
SOR = "space"
API_PREFIX = "/api/v1/space"
PRODUCT = (
    "Enterprise Space Intelligence Space Communications, Deep Space Network, "
    "Inter-Satellite Networking, Laser Communications & MEOS Space Communications Platform"
)
CAPABILITY = "CAP-PLT-SP-001"
COMMS_MISSION = (
    "Provide secure, resilient, autonomous, high-bandwidth communications connecting Earth, "
    "orbit, lunar infrastructure, planetary missions and future interplanetary networks."
)
COMMS_VISION = (
    "Transform space connectivity from ground-station windows into a delay-tolerant, "
    "AI-optimized, quantum-ready, human-supervised interplanetary communications fabric."
)
FABRIC = "meos_space_communications_fabric"
FOUNDATION_GATE = "P218"
MISSION_GATE = "P218-A"
STRATEGY_GATE = "P218-B"
DOMAIN_GATE = "P218-C"
INFRASTRUCTURE_GATE = "P218-D"
SPACE_AI_GATE = "P218-E"
SATELLITE_GATE = "P218-F"
ORBITAL_GATE = "P218-G"
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

ARCHITECTURE_LAYERS = (
    {"id": "L01", "name": "Physical Communication Layer", "components": ("ground_stations", "tracking_stations", "relay_satellites", "optical_terminals", "rf_antennas", "laser_terminals", "mission_communication_nodes", "planetary_gateways")},
    {"id": "L02", "name": "Network Layer", "components": ("delay_tolerant_network", "inter_satellite_mesh", "mission_wan", "ground_backbone", "deep_space_network", "optical_backbone", "mission_vpn", "routing_platform")},
    {"id": "L03", "name": "Communication Services Layer", "components": ("telemetry_transport", "command_transport", "video_streaming", "scientific_data_transport", "payload_communications", "emergency_communications", "mission_messaging", "synchronization_services")},
    {"id": "L04", "name": "Communication Intelligence Layer", "components": ("traffic_optimization", "adaptive_routing", "bandwidth_intelligence", "signal_prediction", "network_ai", "qos_optimization", "failure_prediction", "autonomous_recovery")},
    {"id": "L05", "name": "Business & Mission Layer", "components": ("mission_communications", "fleet_coordination", "research_collaboration", "scientific_exchange", "commercial_services", "emergency_operations", "mission_analytics")},
)
DSN = {
    "present_required": True,
    "platform": "meos_deep_space_network_platform",
    "infrastructure": (
        "earth_stations", "lunar_relay", "mars_relay", "planetary_relay",
        "deep_space_antennas", "optical_relays", "mission_gateways",
    ),
    "capabilities": (
        "long_distance_communications", "store_and_forward_routing", "autonomous_scheduling",
        "adaptive_bandwidth_allocation", "deep_space_synchronization", "mission_prioritization",
        "communication_recovery", "autonomous_fault_handling",
    ),
}
ISN = {
    "present_required": True,
    "platform": "meos_inter_satellite_networking_platform",
    "architectures": ("satellite_mesh", "optical_mesh", "hybrid_mesh", "multi_orbit_network", "constellation_backbone", "mission_cluster_network"),
    "capabilities": (
        "dynamic_routing", "peer_discovery", "network_healing", "traffic_balancing",
        "load_distribution", "route_optimization", "qos_management", "network_segmentation",
    ),
}
LASER = {
    "present_required": True,
    "platform": "meos_laser_communications_platform",
    "capabilities": (
        "optical_links", "point_to_point_laser_links", "inter_satellite_optical_links",
        "ground_optical_links", "adaptive_beam_steering", "optical_encryption",
        "weather_aware_routing", "bandwidth_optimization",
    ),
    "metrics": (
        "throughput", "bit_error_rate", "signal_stability", "link_availability",
        "latency", "packet_loss", "alignment_accuracy",
    ),
}
MISSION_SERVICES = {
    "present_required": True,
    "platform": "meos_mission_communication_services",
    "services": (
        "telemetry_delivery", "command_delivery", "mission_broadcast", "scientific_data_streaming",
        "mission_messaging", "emergency_alerting", "payload_data_transfer", "synchronization_services",
    ),
    "classes": (
        "real_time", "near_real_time", "delay_tolerant", "bulk_transfer",
        "emergency_priority", "scientific_transfer",
    ),
    "never_ungated_command_transport": True,
    "never_skip_delay_tolerant_networking": True,
}
NETWORK_AI = {
    "present_required": True,
    "platform": "meos_network_ai_platform",
    "capabilities": (
        "adaptive_routing", "congestion_prediction", "bandwidth_forecasting", "signal_quality_prediction",
        "interference_detection", "failure_prediction", "autonomous_recovery", "communication_optimization",
    ),
    "models": (
        {"id": "MODEL-01", "name": "Network Foundation Model"},
        {"id": "MODEL-02", "name": "Routing Intelligence Model"},
        {"id": "MODEL-03", "name": "Signal Prediction Model"},
        {"id": "MODEL-04", "name": "Traffic Optimization Model"},
        {"id": "MODEL-05", "name": "Communication Health Model"},
    ),
    "via_p214_z": True,
    "via_p218_e": True,
}
DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_space_communication_digital_twin",
    "represents": (
        "ground_stations", "relay_satellites", "communication_links", "laser_networks",
        "rf_networks", "mission_traffic", "bandwidth_usage", "deep_space_links",
    ),
    "capabilities": (
        "traffic_simulation", "failure_simulation", "capacity_forecasting", "coverage_analysis",
        "mission_readiness", "recovery_simulation", "optimization_analysis",
    ),
}
OBSERVABILITY = {
    "present_required": True,
    "dashboards": (
        "global_communication_map", "ground_station_status", "optical_link_status", "satellite_mesh_health",
        "bandwidth_utilization", "communication_latency", "deep_space_windows", "network_ai_recommendations",
    ),
    "kpis": (
        "network_availability", "mission_communication_success_rate", "average_latency", "packet_delivery_ratio",
        "optical_link_availability", "bandwidth_utilization", "autonomous_recovery_success", "mttr", "mttd",
    ),
}
BOUNDED_CONTEXTS = (
    {"id": "BC-COM-01", "name": "Ground Communications"},
    {"id": "BC-COM-02", "name": "Deep Space Network"},
    {"id": "BC-COM-03", "name": "Inter-Satellite Networking"},
    {"id": "BC-COM-04", "name": "Laser Communications"},
    {"id": "BC-COM-05", "name": "Mission Communications"},
    {"id": "BC-COM-06", "name": "Network Intelligence"},
    {"id": "BC-COM-07", "name": "Bandwidth Management"},
    {"id": "BC-COM-08", "name": "Communication Security"},
)
GOVERNANCE = {
    "present_required": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "never_opaque_unexplainable_decisions": True,
    "never_ungated_command_transport": True,
    "never_skip_delay_tolerant_networking": True,
}
SECURITY = {
    "present_required": True,
    "domains": (
        "identity_security", "network_security", "optical_security", "mission_security",
        "command_security", "ground_security", "key_management", "communication_integrity",
    ),
    "controls": (
        "zero_trust_network_access", "pki", "mutual_tls", "quantum_ready_cryptography",
        "secure_routing", "command_authentication", "tamper_detection", "policy_enforcement",
    ),
    "zero_trust": True,
    "quantum_ready": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "via_integration": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
    "no_module_local_telemetry_stack": True,
    "no_module_local_communications_radio_stack": True,
    "never_opaque_unexplainable_decisions": True,
    "never_replace_p218_foundation": True,
    "never_replace_p218_a_mission": True,
    "never_replace_p218_b_strategy": True,
    "never_replace_p218_c_domain": True,
    "never_replace_p218_d_infrastructure": True,
    "never_replace_p218_e_space_ai": True,
    "never_replace_p218_f_satellite": True,
    "never_replace_p218_g_orbital": True,
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
    "never_disable_human_override": True,
    "never_skip_delay_tolerant_networking": True,
}
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p214z_ai_master", "p215z_quantum_supreme", "p216z_robotics_supreme", "p217z_bio_nexus",
        "p218d_space_infrastructure", "p218e_space_ai", "p218f_satellite", "p218g_orbital",
        "meos_knowledge_graph", "meos_digital_twin", "policy_engine", "workflow", "audit",
        "integration_platform", "notifications",
    ),
    "mechanisms": ("api_gateway", "event_bus", "acl_peer_ids_only", "inference_intents_not_models", "radios_via_integration", "dtn_routing"),
    "via_p214_z": True, "via_p215_z": True, "via_p216_z": True, "via_p217": True,
    "via_p218_d": True, "via_p218_e": True, "via_p218_f": True, "via_p218_g": True,
}
DEPLOYMENT = {
    "present_required": True,
    "environments": (
        "ground_comms_environment", "orbital_mesh_environment",
        "deep_space_network_environment", "simulation_only_environment",
    ),
    "cloud_native": True,
    "dtn_native": True,
    "quantum_ready": True,
}
ROADMAP_PHASES = (
    {"phase": 1, "name": "Communication Foundation", "deliverables": ("ground_communication_network", "mission_backbone", "telemetry_platform", "secure_communication_services")},
    {"phase": 2, "name": "Orbital Communication", "deliverables": ("inter_satellite_mesh", "laser_communications", "bandwidth_intelligence", "network_ai")},
    {"phase": 3, "name": "Deep Space Networking", "deliverables": ("deep_space_network", "delay_tolerant_networking", "planetary_relay_platform", "communication_digital_twin")},
    {"phase": 4, "name": "Autonomous Space Communications", "deliverables": ("ai_autonomous_communications", "self_healing_network", "planetary_internet_foundation", "meos_space_communications_intelligence_core")},
)
COMMANDS = (
    "RegisterGroundStationCommand", "EstablishCommunicationCommand", "AllocateBandwidthCommand",
    "ActivateLaserLinkCommand", "OptimizeRouteCommand", "ActivateEmergencyChannelCommand",
)
QUERIES = (
    "GetCommunicationsPlatformQuery", "GetDeepSpaceWindowQuery", "GetOpticalLinkQuery",
    "GetMeshHealthQuery", "GetBandwidthAllocationQuery",
)
CORE_EVENTS = (
    {"name": "GroundStationOnlineEvent", "schema": "space.communications.ground.online.v1", "owner": "BC-COM-01", "consumers": "audit,search,mesh"},
    {"name": "CommunicationEstablishedEvent", "schema": "space.communications.link.established.v1", "owner": "BC-COM-01", "consumers": "audit,analytics,mission"},
    {"name": "CommunicationLostEvent", "schema": "space.communications.link.lost.v1", "owner": "BC-COM-01", "consumers": "audit,notifications,recovery"},
    {"name": "LaserLinkActivatedEvent", "schema": "space.communications.laser.activated.v1", "owner": "BC-COM-04", "consumers": "audit,analytics,mesh"},
    {"name": "BandwidthAllocatedEvent", "schema": "space.communications.bandwidth.allocated.v1", "owner": "BC-COM-07", "consumers": "audit,qos,mission"},
    {"name": "RouteOptimizedEvent", "schema": "space.communications.route.optimized.v1", "owner": "BC-COM-06", "consumers": "audit,analytics,ai"},
    {"name": "NetworkCongestionDetectedEvent", "schema": "space.communications.congestion.detected.v1", "owner": "BC-COM-06", "consumers": "audit,notifications,ai"},
    {"name": "DeepSpaceWindowOpenedEvent", "schema": "space.communications.dsn.window.opened.v1", "owner": "BC-COM-02", "consumers": "audit,scheduler,mission"},
    {"name": "MissionCommunicationCompletedEvent", "schema": "space.communications.mission.completed.v1", "owner": "BC-COM-05", "consumers": "audit,analytics,compliance"},
    {"name": "EmergencyChannelActivatedEvent", "schema": "space.communications.emergency.activated.v1", "owner": "BC-COM-05", "consumers": "audit,workflow,notifications"},
)
MICROSERVICES = (
    {"id": "communications_platform_service", "api": "/space/communications", "db": "space_*", "events": ("GroundStationOnlineEvent",), "security": ("space.read",), "scaling": "comms_platform_replicas"},
    {"id": "dsn_service", "api": "/space/communications/dsn", "db": "space_*", "events": ("DeepSpaceWindowOpenedEvent",), "security": ("space.write",), "scaling": "dsn_workers"},
    {"id": "isn_service", "api": "/space/communications/inter-satellite", "db": "space_*", "events": ("RouteOptimizedEvent",), "security": ("space.write",), "scaling": "isn_workers"},
    {"id": "laser_service", "api": "/space/communications/laser", "db": "space_*", "events": ("LaserLinkActivatedEvent",), "security": ("space.write",), "scaling": "laser_workers"},
    {"id": "mission_comms_service", "api": "/space/communications/mission-services", "db": "space_*", "events": ("MissionCommunicationCompletedEvent",), "security": ("space.write",), "scaling": "mission_comms_workers"},
    {"id": "network_ai_service", "api": "/space/communications/network-ai", "db": "space_*", "events": ("NetworkCongestionDetectedEvent",), "security": ("space.ai.infer",), "scaling": "network_ai_workers"},
    {"id": "digital_twin_service", "api": "/space/communications/digital-twin", "db": "space_*", "events": ("CommunicationEstablishedEvent",), "security": ("space.read",), "scaling": "twin_workers"},
    {"id": "observability_service", "api": "/space/communications/observability", "db": "space_*", "events": ("CommunicationLostEvent",), "security": ("space.read",), "scaling": "obs_replicas"},
    {"id": "comms_governance_service", "api": "/space/communications/governance", "db": "space_*", "events": ("EmergencyChannelActivatedEvent",), "security": ("space.admin",), "scaling": "governance_replicas"},
    {"id": "comms_security_service", "api": "/space/communications/security", "db": "space_*", "events": ("BandwidthAllocatedEvent",), "security": ("space.admin",), "scaling": "security_replicas"},
)
TESTING = (
    "ground_station_failover_testing", "dtn_routing_testing", "laser_link_alignment_testing",
    "command_transport_gate_testing", "mesh_healing_testing", "deep_space_window_testing",
    "network_ai_prediction_testing", "quantum_ready_crypto_testing",
)
QUALITY_GATES_REJECT_IF = (
    "space_communications_platform_is_missing", "deep_space_network_is_missing",
    "inter_satellite_networking_is_missing", "laser_communications_is_missing",
    "communication_ai_platform_is_missing", "communication_digital_twin_is_missing",
    "ddd_model_is_missing", "security_architecture_is_missing", "observability_is_missing",
    "deployment_architecture_is_missing", "cqrs_architecture_is_missing",
    "event_architecture_is_missing", "microservices_architecture_is_missing",
    "sibling_space_bc", "replace_p218_foundation", "replace_p218_g_orbital",
    "module_local_llm", "module_local_communications_radio_stack",
    "ungated_command_transport", "skip_delay_tolerant_networking",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Space Communications Fabric",
        "mission": COMMS_MISSION, "vision": COMMS_VISION,
        "builds_on_p218": True, "builds_on_p218_a": True, "builds_on_p218_b": True,
        "builds_on_p218_c": True, "builds_on_p218_d": True, "builds_on_p218_e": True,
        "builds_on_p218_f": True, "builds_on_p218_g": True,
        "builds_on_p217_z": True, "builds_on_p216_z": True, "builds_on_p215_z": True, "builds_on_p214_z": True,
        "never_replace_p218_g_orbital": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
        "no_module_local_communications_radio_stack": True,
        "never_skip_delay_tolerant_networking": True,
        "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "infrastructure_gate": INFRASTRUCTURE_GATE, "space_ai_gate": SPACE_AI_GATE,
        "satellite_gate": SATELLITE_GATE, "orbital_gate": ORBITAL_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
    }

def architecture() -> dict[str, Any]:
    return {"present_required": True, "layers": [dict(x) for x in ARCHITECTURE_LAYERS], "layer_count": len(ARCHITECTURE_LAYERS), "dtn_native": True}

def dsn() -> dict[str, Any]:
    return dict(DSN) | {
        "infrastructure_count": len(DSN["infrastructure"]),
        "capability_count": len(DSN["capabilities"]),
    }

def inter_satellite() -> dict[str, Any]:
    return dict(ISN) | {
        "architecture_count": len(ISN["architectures"]),
        "capability_count": len(ISN["capabilities"]),
    }

def laser() -> dict[str, Any]:
    return dict(LASER) | {
        "capability_count": len(LASER["capabilities"]),
        "metric_count": len(LASER["metrics"]),
    }

def mission_services() -> dict[str, Any]:
    return dict(MISSION_SERVICES) | {
        "service_count": len(MISSION_SERVICES["services"]),
        "class_count": len(MISSION_SERVICES["classes"]),
    }

def network_ai() -> dict[str, Any]:
    return dict(NETWORK_AI) | {
        "capability_count": len(NETWORK_AI["capabilities"]),
        "model_count": len(NETWORK_AI["models"]),
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
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p218_i": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "comms_mission": COMMS_MISSION, "comms_vision": COMMS_VISION, "principle": COMMS_MISSION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE, "infrastructure_gate": INFRASTRUCTURE_GATE,
        "space_ai_gate": SPACE_AI_GATE, "satellite_gate": SATELLITE_GATE, "orbital_gate": ORBITAL_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P218", "P218-A", "P218-B", "P218-C", "P218-D", "P218-E", "P218-F", "P218-G", "P217-Z", "P216-Z", "P215-Z", "P214-Z"] + [f"ADR-{i}" for i in range(526, 534)],
        "vision": vision_pack(),
        "architecture": architecture(),
        "dsn": dsn(),
        "inter_satellite": inter_satellite(),
        "laser": laser(),
        "mission_services": mission_services(),
        "network_ai": network_ai(),
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
        "space_communications_platform_present_required": True,
        "deep_space_network_present_required": True,
        "inter_satellite_networking_present_required": True,
        "laser_communications_present_required": True,
        "communication_ai_platform_present_required": True,
        "communication_digital_twin_present_required": True,
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
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_replace_p216_z": True,
        "never_replace_biotechnology": True,
        "space_ai_via_p214z_acl_only": True,
        "no_module_local_llm": True,
        "no_module_local_telemetry_stack": True,
        "no_module_local_communications_radio_stack": True,
        "never_opaque_unexplainable_decisions": True,
        "never_skip_human_mission_oversight_strategy": True,
        "never_skip_space_cybersecurity_strategy": True,
        "never_skip_space_sustainability_strategy": True,
        "never_opaque_mission_critical_strategy": True,
        "never_ungated_autonomous_mission_strategy": True,
        "never_ungated_satellite_command_uplink": True,
        "never_ungated_collision_avoidance_maneuver": True,
        "never_ungated_command_transport": True,
        "never_disable_human_override": True,
        "never_skip_delay_tolerant_networking": True,
        "api_prefix": f"{API_PREFIX}/communications",
        "forbidden_sibling_bc": [
            "space_communications_platform",
            "deep_space_network_bc",
            "laser_communications_bc",
        ],
        "foundation_for_p218_i": True,
    }

def communications_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /space/communications",
        "GET /space/communications/vision",
        "GET /space/communications/architecture",
        "GET /space/communications/dsn",
        "GET /space/communications/inter-satellite",
        "GET /space/communications/laser",
        "GET /space/communications/mission-services",
        "GET /space/communications/network-ai",
        "GET /space/communications/digital-twin",
        "GET /space/communications/observability",
        "GET /space/communications/governance",
        "GET /space/communications/security",
        "GET /space/communications/integration",
        "GET /space/communications/deployment",
        "GET /space/communications/testing",
        "GET /space/communications/cqrs",
        "GET /space/communications/events",
        "GET /space/communications/readiness",
    ], "foundation_gate_routes": ["GET /space/foundation"],
       "mission_gate_routes": ["GET /space/mission"],
       "strategy_gate_routes": ["GET /space/strategy"],
       "domain_gate_routes": ["GET /space/domain"],
       "infrastructure_gate_routes": ["GET /space/infrastructure", "GET /space/infrastructure/readiness"],
       "space_ai_gate_routes": ["GET /space/space-ai", "GET /space/space-ai/readiness"],
       "satellite_gate_routes": ["GET /space/satellite", "GET /space/satellite/readiness"],
       "orbital_gate_routes": ["GET /space/orbital", "GET /space/orbital/readiness"]}
