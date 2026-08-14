"""P218-D Enterprise Space Intelligence Space Infrastructure — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P218-D"
ADR = 530
SOR = "space"
API_PREFIX = "/api/v1/space"
PRODUCT = "Enterprise Space Intelligence Space Infrastructure, Ground Segment, Mission Control, Space Cloud & MEOS Space Infrastructure Platform"
CAPABILITY = "CAP-PLT-SP-001"
INFRA_MISSION = (
    "Provide a secure, resilient, autonomous and globally distributed infrastructure capable of "
    "supporting continuous enterprise space operations across Earth, orbit and future planetary environments."
)
INFRA_VISION = (
    "Every mission control surface, ground station, space cloud workload, telemetry stream and "
    "infrastructure digital twin shall operate on a unified enterprise space infrastructure platform."
)
FABRIC = "meos_space_intelligence_infrastructure_fabric"
FOUNDATION_GATE = "P218"
MISSION_GATE = "P218-A"
STRATEGY_GATE = "P218-B"
DOMAIN_GATE = "P218-C"
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

INFRA_LAYERS = (
    {"id": "L01", "name": "Space Physical Infrastructure", "components": ("launch_facilities", "ground_stations", "mission_control_centres", "satellite_constellations", "tracking_stations", "observatories", "edge_processing_sites", "regional_data_centres")},
    {"id": "L02", "name": "Connectivity Layer", "components": ("satellite_links", "deep_space_network", "rf_communications", "laser_communications", "inter_satellite_links", "ground_fibre_backbone", "secure_wan", "mission_vpn")},
    {"id": "L03", "name": "Space Cloud Platform", "components": ("private_cloud", "hybrid_cloud", "edge_cloud", "mission_cloud", "scientific_compute_cluster", "gpu_cluster", "ai_cluster", "quantum_integration_gateway")},
    {"id": "L04", "name": "Platform Services", "components": ("container_platform", "kubernetes", "service_mesh", "api_gateway", "event_bus", "workflow_engine", "identity_platform", "secrets_platform", "configuration_platform", "observability_platform")},
    {"id": "L05", "name": "Mission Services", "components": ("mission_control", "telemetry_platform", "command_platform", "tracking_platform", "scheduling_platform", "simulation_platform", "mission_analytics", "digital_twin_platform")},
)
GROUND_SEGMENT = {
    "present_required": True,
    "components": (
        "mission_operations_centre", "ground_station_network", "tracking_network", "command_network",
        "telemetry_reception", "mission_planning_centre", "satellite_operations_centre",
        "network_operations_centre", "security_operations_centre",
    ),
    "capabilities": (
        "mission_scheduling", "command_uplink", "telemetry_downlink", "orbit_determination",
        "health_monitoring", "ground_asset_management", "network_optimisation", "mission_recovery",
    ),
    "via_integration_platform": True,
    "never_direct_ground_station_bypass_of_integration_platform": True,
}
MISSION_CONTROL = {
    "present_required": True,
    "core_services": (
        "mission_planning_service", "mission_execution_service", "mission_monitoring_service",
        "mission_timeline_service", "command_authorization_service", "emergency_operations_service",
        "incident_management_service", "decision_support_service",
    ),
    "dashboards": (
        "mission_status", "spacecraft_status", "orbit_status", "telemetry_status",
        "ground_station_status", "communications_health", "infrastructure_health", "mission_risk",
    ),
    "modes": ("nominal", "safe_mode", "recovery", "emergency", "maintenance", "simulation", "training"),
    "human_oversight_required": True,
}
SPACE_CLOUD = {
    "present_required": True,
    "deployment_models": ("private_cloud", "public_cloud", "hybrid_cloud", "mission_cloud", "edge_cloud", "disconnected_operations"),
    "platform_services": (
        "virtual_machines", "containers", "functions", "object_storage", "block_storage",
        "distributed_database", "streaming_platform", "message_broker", "ai_runtime", "digital_twin_runtime",
    ),
    "operational_capabilities": (
        "auto_scaling", "auto_healing", "workload_placement", "policy_based_scheduling",
        "disaster_recovery", "continuous_deployment", "blue_green_deployment", "canary_releases",
    ),
}
SPACE_NETWORK = {
    "present_required": True,
    "domains": (
        "ground_network", "mission_network", "satellite_network", "deep_space_network",
        "operations_network", "management_network", "security_network", "research_network",
    ),
    "services": (
        "routing", "time_synchronization", "qos", "bandwidth_optimisation",
        "traffic_engineering", "network_encryption", "certificate_management", "network_monitoring",
    ),
}
DATA_PLATFORM = {
    "present_required": True,
    "sources": (
        "telemetry", "sensor_data", "satellite_imagery", "scientific_payloads", "ground_systems",
        "mission_logs", "weather_systems", "space_weather", "ai_models", "digital_twins",
    ),
    "components": (
        "streaming_platform", "operational_data_store", "data_lake", "data_warehouse",
        "feature_store", "knowledge_graph", "metadata_repository", "data_catalog",
        "data_governance", "data_lineage",
    ),
    "domains": (
        {"id": "telemetry_data_domain", "includes": ("realtime_telemetry", "health_packets", "command_acks")},
        {"id": "orbital_data_domain", "includes": ("ephemeris", "conjunction_data", "debris_catalogues")},
        {"id": "scientific_data_domain", "includes": ("payload_products", "observations", "research_datasets")},
        {"id": "mission_ops_data_domain", "includes": ("mission_logs", "schedules", "incident_records")},
    ),
}
INFRA_DIGITAL_TWIN = {
    "present_required": True,
    "represents": (
        "ground_stations", "networks", "mission_control", "cloud_resources",
        "satellite_infrastructure", "communication_links", "data_centres", "operational_services",
    ),
    "capabilities": (
        "infrastructure_simulation", "capacity_forecasting", "failure_simulation", "maintenance_planning",
        "recovery_validation", "performance_optimisation", "energy_optimisation", "mission_readiness_assessment",
    ),
}
CONTAINER_PLATFORM = {
    "present_required": True,
    "components": ("container_platform", "kubernetes", "service_mesh", "api_gateway", "event_bus", "workflow_runtime"),
    "supports": ("microservices", "mission_services", "ai_runtime", "digital_twin_runtime"),
    "cloud_native": True,
}
OBSERVABILITY = {
    "present_required": True,
    "components": (
        "metrics", "distributed_tracing", "central_logging", "event_correlation",
        "mission_health", "infrastructure_health", "synthetic_monitoring",
        "telemetry_analytics", "capacity_monitoring", "ai_observability",
    ),
    "kpis": (
        "platform_availability", "mission_availability", "mttr", "mttd",
        "latency", "packet_loss", "infrastructure_utilisation", "mission_success_rate",
    ),
    "via_platform_observability": True,
    "module_local_observability_store_forbidden": True,
}
RESILIENCE = {
    "present_required": True,
    "framework": "meos_space_infrastructure_resilience_framework",
    "capabilities": ("backup_management", "data_replication", "mission_continuity", "auto_healing", "disaster_recovery"),
    "strategies": ("multi_region_deployment", "disconnected_operations", "immutable_backup", "recovery_automation"),
}
SECURITY = {
    "present_required": True,
    "framework": "meos_space_infrastructure_zero_trust_security",
    "domains": (
        "identity_security", "network_security", "infrastructure_security", "platform_security",
        "mission_security", "data_security", "communication_security", "operational_security",
    ),
    "services": (
        "zero_trust_access", "pki", "hsm", "secrets_management", "key_management",
        "runtime_protection", "threat_detection", "soar", "siem", "policy_enforcement",
    ),
    "zero_trust": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "never_replace_p218_foundation": True,
    "never_replace_p218_a_mission": True,
    "never_replace_p218_b_strategy": True,
    "never_replace_p218_c_domain": True,
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
    "module_local_observability_store_forbidden": True,
    "never_direct_ground_station_bypass_of_integration_platform": True,
    "module_local_llm_forbidden": True,
}
BOUNDED_CONTEXTS = (
    {"id": "BC-INFRA-01", "name": "Infrastructure Management"},
    {"id": "BC-INFRA-02", "name": "Ground Segment"},
    {"id": "BC-INFRA-03", "name": "Mission Control"},
    {"id": "BC-INFRA-04", "name": "Cloud Operations"},
    {"id": "BC-INFRA-05", "name": "Network Operations"},
    {"id": "BC-INFRA-06", "name": "Infrastructure Security"},
    {"id": "BC-INFRA-07", "name": "Infrastructure Monitoring"},
    {"id": "BC-INFRA-08", "name": "Capacity Management"},
)
AGGREGATES = (
    {"id": "GroundStationAggregate", "bc": "BC-INFRA-02"},
    {"id": "MissionControlAggregate", "bc": "BC-INFRA-03"},
    {"id": "CloudClusterAggregate", "bc": "BC-INFRA-04"},
    {"id": "NetworkAggregate", "bc": "BC-INFRA-05"},
    {"id": "InfrastructureHealthAggregate", "bc": "BC-INFRA-07"},
    {"id": "TelemetryGatewayAggregate", "bc": "BC-INFRA-02"},
)
ROADMAP_PHASES = (
    {"phase": 1, "name": "Ground Infrastructure Foundation", "deliverables": ("ground_stations", "mission_control", "core_networks", "telemetry_platform")},
    {"phase": 2, "name": "Space Cloud Platform", "deliverables": ("hybrid_cloud", "container_platform", "event_platform", "mission_services")},
    {"phase": 3, "name": "Autonomous Infrastructure", "deliverables": ("ai_operations", "infrastructure_digital_twin", "self_healing_platform", "predictive_maintenance")},
    {"phase": 4, "name": "Planetary Infrastructure", "deliverables": ("deep_space_infrastructure", "planetary_operations_support", "orbital_infrastructure_federation", "meos_space_infrastructure_core")},
)
COMMANDS = (
    "ActivateGroundStationCommand", "InitializeMissionControlCommand", "DispatchMissionCommand",
    "ScaleCloudClusterCommand", "UpdateNetworkPathCommand", "DeclareInfrastructureReadyCommand",
)
QUERIES = (
    "GetGroundStationStatusQuery", "GetMissionControlStateQuery", "GetCloudClusterCapacityQuery",
    "GetNetworkHealthQuery", "GetInfrastructureTwinStateQuery",
)
CORE_EVENTS = (
    {"name": "GroundStationActivatedEvent", "schema": "space.infra.ground_station.activated.v1", "owner": "BC-INFRA-02", "consumers": "audit,mission,observability"},
    {"name": "GroundStationOfflineEvent", "schema": "space.infra.ground_station.offline.v1", "owner": "BC-INFRA-02", "consumers": "audit,notifications,noc"},
    {"name": "MissionControlInitializedEvent", "schema": "space.infra.mission_control.initialized.v1", "owner": "BC-INFRA-03", "consumers": "audit,workflow,analytics"},
    {"name": "MissionCommandDispatchedEvent", "schema": "space.infra.mission_command.dispatched.v1", "owner": "BC-INFRA-03", "consumers": "audit,integration,satellite"},
    {"name": "TelemetryReceivedEvent", "schema": "space.infra.telemetry.received.v1", "owner": "BC-INFRA-02", "consumers": "analytics,twin,ai"},
    {"name": "CloudClusterScaledEvent", "schema": "space.infra.cloud.scaled.v1", "owner": "BC-INFRA-04", "consumers": "audit,observability,capacity"},
    {"name": "NetworkPathUpdatedEvent", "schema": "space.infra.network.path.updated.v1", "owner": "BC-INFRA-05", "consumers": "audit,mission,security"},
    {"name": "InfrastructureFailureDetectedEvent", "schema": "space.infra.failure.detected.v1", "owner": "BC-INFRA-07", "consumers": "audit,notifications,soc"},
    {"name": "InfrastructureRecoveredEvent", "schema": "space.infra.recovered.v1", "owner": "BC-INFRA-07", "consumers": "audit,analytics,mission"},
    {"name": "MissionInfrastructureReadyEvent", "schema": "space.infra.mission.ready.v1", "owner": "BC-INFRA-01", "consumers": "workflow,audit,mission"},
)
MICROSERVICES = (
    {"id": "ground_segment_service", "bc": "BC-INFRA-02", "api": "/space/infrastructure/ground-segment", "db": "space_*", "events": ("GroundStationActivatedEvent",), "security": ("space.write",), "scaling": "ground_workers"},
    {"id": "mission_control_service", "bc": "BC-INFRA-03", "api": "/space/infrastructure/mission-control", "db": "space_*", "events": ("MissionControlInitializedEvent",), "security": ("space.write",), "scaling": "moc_workers"},
    {"id": "space_cloud_service", "bc": "BC-INFRA-04", "api": "/space/infrastructure/cloud", "db": "space_*", "events": ("CloudClusterScaledEvent",), "security": ("space.admin",), "scaling": "cloud_ops_workers"},
    {"id": "space_network_service", "bc": "BC-INFRA-05", "api": "/space/infrastructure/network", "db": "space_*", "events": ("NetworkPathUpdatedEvent",), "security": ("space.admin",), "scaling": "network_workers"},
    {"id": "space_data_platform_service", "bc": "BC-INFRA-01", "api": "/space/infrastructure/data", "db": "space_*", "events": ("TelemetryReceivedEvent",), "security": ("space.read",), "scaling": "data_workers"},
    {"id": "infra_digital_twin_service", "bc": "BC-INFRA-01", "api": "/space/infrastructure/digital-twin", "db": "space_*", "events": ("MissionInfrastructureReadyEvent",), "security": ("space.read",), "scaling": "twin_workers"},
    {"id": "infra_security_service", "bc": "BC-INFRA-06", "api": "/space/infrastructure/security", "db": "space_*", "events": ("InfrastructureFailureDetectedEvent",), "security": ("space.admin",), "scaling": "security_replicas"},
    {"id": "infra_observability_service", "bc": "BC-INFRA-07", "api": "/space/infrastructure/observability", "db": "space_*", "events": ("InfrastructureRecoveredEvent",), "security": ("space.read",), "scaling": "observability_replicas"},
    {"id": "capacity_management_service", "bc": "BC-INFRA-08", "api": "/space/infrastructure/platform", "db": "space_*", "events": ("CloudClusterScaledEvent",), "security": ("space.admin",), "scaling": "capacity_workers"},
    {"id": "telemetry_gateway_service", "bc": "BC-INFRA-02", "api": "/space/infrastructure/ground-segment", "db": "space_*", "events": ("TelemetryReceivedEvent",), "security": ("space.write",), "scaling": "telemetry_workers"},
)
INTEGRATION = {
    "present_required": True,
    "targets": ("p214z_ai_master", "p215z_quantum_supreme", "p216z_robotics_supreme", "p217z_bio_nexus", "meos_knowledge_graph", "meos_digital_twin", "policy_engine", "workflow", "audit", "integration_platform", "observability_platform"),
    "mechanisms": ("api_gateway", "event_bus", "streaming_platform", "acl_peer_ids_only", "iac"),
    "via_p214_z": True, "via_p215_z": True, "via_p216_z": True, "via_p217": True,
    "via_integration_platform": True, "via_observability_platform": True,
}
DEPLOYMENT = {
    "present_required": True,
    "cloud_native": True,
    "models": ("private", "hybrid", "mission_cloud", "edge", "disconnected"),
    "components": ("infra_services_cluster", "ground_workers", "mission_control_plane", "space_cloud_control", "infra_observability"),
    "iac": True,
}
TESTING = (
    "infrastructure_architecture_testing", "ground_segment_testing", "mission_control_testing",
    "space_cloud_testing", "network_architecture_testing", "data_platform_testing",
    "infra_twin_testing", "security_architecture_testing", "observability_testing", "resilience_testing",
)
QUALITY_GATES_REJECT_IF = (
    "space_infrastructure_architecture_is_missing", "ground_segment_platform_is_missing",
    "mission_control_platform_is_missing", "space_cloud_platform_is_missing",
    "space_network_architecture_is_missing", "space_data_platform_is_missing",
    "infrastructure_digital_twin_is_missing", "infrastructure_security_is_missing",
    "observability_architecture_is_missing", "disaster_recovery_is_missing",
    "container_platform_architecture_is_missing", "deployment_model_is_missing",
    "testing_architecture_is_missing", "cqrs_architecture_is_missing",
    "event_architecture_is_missing", "microservices_architecture_is_missing",
    "sibling_space_bc", "replace_p218_foundation", "replace_p218_c_domain",
    "module_local_observability_store", "direct_ground_station_bypass_of_integration_platform",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Space Intelligence Infrastructure Fabric",
        "infra_mission": INFRA_MISSION, "infra_vision": INFRA_VISION,
        "builds_on_p218": True, "builds_on_p218_a": True, "builds_on_p218_b": True, "builds_on_p218_c": True,
        "builds_on_p217_z": True, "builds_on_p216_z": True, "builds_on_p215_z": True, "builds_on_p214_z": True,
        "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
    }

def infrastructure_layers() -> dict[str, Any]:
    return {"present_required": True, "layers": [dict(x) for x in INFRA_LAYERS], "layer_count": len(INFRA_LAYERS)}

def ground_segment() -> dict[str, Any]:
    return dict(GROUND_SEGMENT) | {"component_count": len(GROUND_SEGMENT["components"]), "capability_count": len(GROUND_SEGMENT["capabilities"])}

def mission_control() -> dict[str, Any]:
    return dict(MISSION_CONTROL) | {"service_count": len(MISSION_CONTROL["core_services"]), "mode_count": len(MISSION_CONTROL["modes"])}

def space_cloud() -> dict[str, Any]:
    return dict(SPACE_CLOUD) | {"component_count": len(SPACE_CLOUD["deployment_models"]), "platform_service_count": len(SPACE_CLOUD["platform_services"])}

def space_network() -> dict[str, Any]:
    return dict(SPACE_NETWORK) | {"domain_count": len(SPACE_NETWORK["domains"]), "service_count": len(SPACE_NETWORK["services"])}

def data_infrastructure() -> dict[str, Any]:
    return dict(DATA_PLATFORM) | {"domain_count": len(DATA_PLATFORM["domains"]), "component_count": len(DATA_PLATFORM["components"]), "source_count": len(DATA_PLATFORM["sources"])}

def storage_architecture() -> dict[str, Any]:
    types = ("object_storage", "block_storage", "streaming_store", "secure_mission_vault")
    return {"present_required": True, "types": list(types), "type_count": len(types)}

def infrastructure_digital_twin() -> dict[str, Any]:
    return dict(INFRA_DIGITAL_TWIN) | {"representation_count": len(INFRA_DIGITAL_TWIN["represents"]), "capability_count": len(INFRA_DIGITAL_TWIN["capabilities"])}

def container_platform() -> dict[str, Any]:
    return dict(CONTAINER_PLATFORM)

def observability() -> dict[str, Any]:
    return dict(OBSERVABILITY)

def resilience() -> dict[str, Any]:
    return dict(RESILIENCE)

def security() -> dict[str, Any]:
    return dict(SECURITY)

def bounded_contexts() -> dict[str, Any]:
    return {"present_required": True, "contexts": [dict(c) for c in BOUNDED_CONTEXTS], "context_count": len(BOUNDED_CONTEXTS), "aggregates": [dict(a) for a in AGGREGATES]}

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

def api() -> dict[str, Any]:
    return {"api_first_present_required": True, "prefix": f"{API_PREFIX}/infrastructure"}

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p218_e": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "infra_mission": INFRA_MISSION, "infra_vision": INFRA_VISION, "principle": INFRA_MISSION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE, "bio_gate": BIO_GATE,
        "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P218", "P218-A", "P218-B", "P218-C", "P217-Z", "P216-Z", "P215-Z", "P214-Z", "ADR-526", "ADR-527", "ADR-528", "ADR-529"],
        "vision": vision_pack(),
        "infrastructure_layers": infrastructure_layers(),
        "ground_segment": ground_segment(),
        "mission_control": mission_control(),
        "space_cloud": space_cloud(),
        "space_network": space_network(),
        "data_infrastructure": data_infrastructure(),
        "storage_architecture": storage_architecture(),
        "infrastructure_digital_twin": infrastructure_digital_twin(),
        "container_platform": container_platform(),
        "observability": observability(),
        "resilience": resilience(),
        "security": security(),
        "bounded_contexts": bounded_contexts(),
        "integration": integration(),
        "deployment": deployment(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "testing": testing(),
        "roadmap": roadmap(),
        "api": api(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "space_infrastructure_architecture_present_required": True,
        "ground_segment_platform_present_required": True,
        "mission_control_platform_present_required": True,
        "space_cloud_platform_present_required": True,
        "space_network_architecture_present_required": True,
        "space_data_platform_present_required": True,
        "infrastructure_digital_twin_present_required": True,
        "security_architecture_present_required": True,
        "observability_architecture_present_required": True,
        "disaster_recovery_present_required": True,
        "container_platform_architecture_present_required": True,
        "deployment_model_present_required": True,
        "testing_architecture_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "sibling_space_bc_forbidden": True,
        "never_replace_p218_foundation": True,
        "never_replace_p218_a_mission": True,
        "never_replace_p218_b_strategy": True,
        "never_replace_p218_c_domain": True,
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
        "module_local_observability_store_forbidden": True,
        "never_direct_ground_station_bypass_of_integration_platform": True,
        "module_local_llm_forbidden": True,
        "api_prefix": f"{API_PREFIX}/infrastructure",
        "forbidden_sibling_bc": [
            "space_infrastructure_platform",
            "space_cloud_platform",
            "ground_segment_platform_bc",
        ],
        "foundation_for_p218_e": True,
    }

def infrastructure_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /space/infrastructure",
        "GET /space/infrastructure/layers",
        "GET /space/infrastructure/ground-segment",
        "GET /space/infrastructure/mission-control",
        "GET /space/infrastructure/cloud",
        "GET /space/infrastructure/network",
        "GET /space/infrastructure/data",
        "GET /space/infrastructure/digital-twin",
        "GET /space/infrastructure/security",
        "GET /space/infrastructure/platform",
        "GET /space/infrastructure/observability",
        "GET /space/infrastructure/resilience",
        "GET /space/infrastructure/integration",
        "GET /space/infrastructure/deployment",
        "GET /space/infrastructure/testing",
        "GET /space/infrastructure/cqrs",
        "GET /space/infrastructure/events",
        "GET /space/infrastructure/readiness",
    ], "foundation_gate_routes": ["GET /space/foundation", "GET /space/foundation/readiness"],
       "mission_gate_routes": ["GET /space/mission", "GET /space/mission/readiness"],
       "strategy_gate_routes": ["GET /space/strategy", "GET /space/strategy/readiness"],
       "domain_gate_routes": ["GET /space/domain", "GET /space/domain/readiness"]}
