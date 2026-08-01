"""P216-K Enterprise Construction Intelligence — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P216-K"
ADR = 483
SOR = "robotics"
API_PREFIX = "/api/v1/robotics"
PRODUCT = (
    "Enterprise Robotics Construction Robotics, Smart Infrastructure, "
    "Autonomous Building Systems & Digital Construction Intelligence Platform"
)
CAPABILITY = "CAP-PLT-RB-001"
CONSTRUCTION_VISION = (
    "MEOS Construction Intelligence Platform SHALL unify construction robotics, "
    "smart infrastructure, autonomous building systems and digital twins as "
    "intelligent participants within the MEOS cyber-physical ecosystem."
)
MISSION = (
    "Build autonomous, AI-native, robotics-enabled construction ecosystems "
    "capable of planning, building, monitoring, operating and continuously "
    "improving physical infrastructure."
)
VISION = (
    "Every building, bridge, road, facility, construction robot and "
    "infrastructure asset shall become an intelligent, connected participant "
    "within MEOS."
)
FABRIC = "meos_construction_intelligence_fabric"
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
SUPREME_GATE = "P215-Z"
AI_GATE = "P214-Z"
CORE_DOMAIN = "enterprise_construction_intelligence"
AGGREGATE = "ConstructionAggregate"

SUPPORTING_DOMAINS = (
    "construction_planning",
    "bim",
    "construction_robotics",
    "heavy_equipment",
    "smart_buildings",
    "infrastructure_monitoring",
    "facility_management",
    "asset_lifecycle",
    "safety_intelligence",
    "sustainability",
    "digital_twin",
    "smart_city_integration",
)
ENTITIES = (
    "ConstructionProject",
    "ConstructionSite",
    "Building",
    "Bridge",
    "Tunnel",
    "Road",
    "InfrastructureAsset",
    "ConstructionRobot",
    "AutonomousExcavator",
    "AutonomousCrane",
    "AutonomousBulldozer",
    "InspectionDrone",
    "Worker",
    "Contractor",
    "Facility",
    "BuildingDigitalTwin",
)
VALUE_OBJECTS = (
    "ProjectSchedule",
    "ConstructionPhase",
    "SafetyScore",
    "EquipmentHealth",
    "InspectionScore",
    "AssetCondition",
    "BuildingLocation",
    "EnergyRating",
    "CarbonScore",
)
BOUNDED_CONTEXTS = (
    {"id": "BC-01", "name": "Construction Management Context", "responsibilities": ("project_lifecycle", "scheduling", "phase_governance", "contractor_coordination"), "aggregates": ("ConstructionProject",), "services": ("construction_management_service",), "domain_events": ("ConstructionStartedEvent", "PhaseCompletedEvent"), "policies": ("phase_approval_required",)},
    {"id": "BC-02", "name": "BIM Management Context", "responsibilities": ("bim_models", "iso_19650", "model_federation", "design_coordination"), "aggregates": ("Building",), "services": ("bim_service",), "domain_events": ("InfrastructureUpdatedEvent",), "policies": ("bim_via_integration_platform",)},
    {"id": "BC-03", "name": "Construction Robotics Context", "responsibilities": ("robot_missions", "heavy_equipment", "site_orchestration", "fleet_control"), "aggregates": ("ConstructionRobot",), "services": ("construction_robotics_service",), "domain_events": ("RobotMissionAssignedEvent", "RobotMissionCompletedEvent"), "policies": ("mission_authorisation_required",)},
    {"id": "BC-04", "name": "Infrastructure Monitoring Context", "responsibilities": ("bridge_road_tunnel_monitoring", "pipeline_rail_airports", "condition_assessment"), "aggregates": ("InfrastructureAsset",), "services": ("infrastructure_monitoring_service",), "domain_events": ("InfrastructureIssueDetectedEvent", "InspectionCompletedEvent"), "policies": ("inspection_sla",)},
    {"id": "BC-05", "name": "Smart Building Operations Context", "responsibilities": ("building_automation", "hvac_lighting", "energy_optimisation", "facility_ops"), "aggregates": ("Facility",), "services": ("smart_building_service",), "domain_events": ("BuildingOperationalEvent", "BuildingCommissionedEvent"), "policies": ("energy_optimisation_targets",)},
    {"id": "BC-06", "name": "Asset Lifecycle Management Context", "responsibilities": ("asset_register", "maintenance", "lifecycle_cost", "decommissioning"), "aggregates": ("InfrastructureAsset",), "services": ("asset_lifecycle_service",), "domain_events": ("MaintenanceRequiredEvent",), "policies": ("predictive_maintenance",)},
    {"id": "BC-07", "name": "Construction Digital Twin Context", "responsibilities": ("simulation", "replay", "forecasting", "lifecycle_intelligence"), "aggregates": ("BuildingDigitalTwin",), "services": ("digital_twin_service",), "domain_events": ("InfrastructureUpdatedEvent",), "policies": ("twin_sync_integrity",)},
    {"id": "BC-08", "name": "Safety & Compliance Context", "responsibilities": ("site_safety", "incident_detection", "compliance", "audit"), "aggregates": ("ConstructionSite",), "services": ("safety_service",), "domain_events": ("SafetyIncidentDetectedEvent",), "policies": ("zero_trust_site_access",)},
)
CONSTRUCTION_ROBOTICS = {
    "present_required": True,
    "platform": "meos_construction_robotics_platform",
    "components": (
        "construction_robot_registry",
        "heavy_equipment_controller",
        "mission_planner",
        "site_orchestrator",
        "robot_fleet_manager",
        "construction_workflow_engine",
    ),
    "capabilities": (
        "autonomous_excavation",
        "autonomous_earthmoving",
        "bricklaying_robots",
        "concrete_printing",
        "steel_assembly",
        "structural_inspection",
        "construction_drones",
        "autonomous_surveying",
    ),
}
SMART_INFRASTRUCTURE = {
    "present_required": True,
    "platform": "meos_smart_infrastructure_platform",
    "capabilities": (
        "bridge_monitoring",
        "road_monitoring",
        "tunnel_monitoring",
        "pipeline_monitoring",
        "rail_infrastructure",
        "airport_infrastructure",
        "port_infrastructure",
        "power_infrastructure",
        "water_infrastructure",
        "public_infrastructure",
    ),
}
AUTONOMOUS_BUILDING = {
    "present_required": True,
    "platform": "meos_autonomous_building_systems",
    "capabilities": (
        "building_automation",
        "hvac_optimisation",
        "lighting_intelligence",
        "occupancy_intelligence",
        "energy_optimisation",
        "predictive_maintenance",
        "access_control",
        "fire_intelligence",
        "emergency_evacuation",
        "facility_optimisation",
    ),
}
CONSTRUCTION_AI = {
    "present_required": True,
    "engine": "meos_digital_construction_ai",
    "capabilities": (
        "schedule_optimisation",
        "construction_risk_prediction",
        "cost_optimisation",
        "progress_analytics",
        "delay_prediction",
        "safety_prediction",
        "equipment_optimisation",
        "construction_quality_intelligence",
        "carbon_optimisation",
    ),
    "via_p214_z": True,
}
CONSTRUCTION_DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_construction_digital_twin",
    "represents": (
        "buildings", "infrastructure", "construction_sites", "equipment",
        "workers", "robots", "utilities", "assets", "materials",
    ),
    "capabilities": (
        "simulation",
        "operational_replay",
        "scenario_analysis",
        "construction_forecasting",
        "infrastructure_optimisation",
        "lifecycle_intelligence",
    ),
}
CONSTRUCTION_KG = {
    "present_required": True,
    "graph": "meos_construction_knowledge_graph",
    "nodes": (
        "projects", "buildings", "infrastructure", "assets", "materials",
        "robots", "equipment", "workers", "contractors", "suppliers",
    ),
    "relationships": (
        "builds", "maintains", "constructs", "inspects", "depends_on",
        "supplied_by", "installed_at", "optimises",
    ),
    "enables": (
        "construction_reasoning",
        "infrastructure_intelligence",
        "asset_lifecycle_analytics",
    ),
}
SECURITY = {
    "present_required": True,
    "framework": "meos_construction_zero_trust_framework",
    "includes": (
        "robot_identity",
        "worker_identity",
        "equipment_identity",
        "building_identity",
        "infrastructure_identity",
        "mission_authorisation",
        "operational_safety",
        "edge_security",
        "threat_detection",
    ),
    "zero_trust": True,
    "iso_19650_bim_native": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "via_integration_platform": True,
    "bim_gis_scada_via_integration_platform_only": True,
    "never_direct_bim_gis_scada_bypass": True,
    "never_duplicate_construction_core_logic": True,
    "no_module_local_llm": True,
    "physical_ai_via_p214z_acl_only": True,
    "never_replace_p216_foundation": True,
    "never_replace_p216_i_healthcare": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "ungated_physical_autonomy_strategy_forbidden": True,
    "opaque_safety_strategy_forbidden": True,
}
COMMANDS = (
    "CreateConstructionProjectCommand",
    "AssignRobotMissionCommand",
    "ApproveConstructionPhaseCommand",
    "UpdateDigitalTwinCommand",
    "ScheduleInspectionCommand",
)
QUERIES = (
    "GetProjectStatusQuery",
    "GetBuildingStatusQuery",
    "GetInfrastructureHealthQuery",
    "GetRobotFleetQuery",
)
CORE_EVENTS = (
    {"name": "ConstructionStartedEvent", "schema": "robotics.construction.started.v1", "owner": "BC-01", "consumers": "robotics,twin,audit"},
    {"name": "PhaseCompletedEvent", "schema": "robotics.construction.phase.completed.v1", "owner": "BC-01", "consumers": "bim,analytics,audit"},
    {"name": "RobotMissionCompletedEvent", "schema": "robotics.construction.robot.mission.completed.v1", "owner": "BC-03", "consumers": "runtime,safety,audit"},
    {"name": "InspectionPassedEvent", "schema": "robotics.construction.inspection.passed.v1", "owner": "BC-04", "consumers": "asset,twin,audit"},
    {"name": "InfrastructureIssueDetectedEvent", "schema": "robotics.construction.infrastructure.issue.detected.v1", "owner": "BC-04", "consumers": "safety,asset,audit"},
    {"name": "BuildingOperationalEvent", "schema": "robotics.construction.building.operational.v1", "owner": "BC-05", "consumers": "facility,twin,audit"},
)
MICROSERVICES = (
    {"id": "construction_management_service", "bc": "BC-01", "api": "/robotics/construction/projects", "db": "robotics_*", "events": ("ConstructionStartedEvent", "PhaseCompletedEvent"), "security": ("robotics.write",), "scaling": "project_replicas", "responsibility": "Construction project and phase governance"},
    {"id": "construction_robotics_service", "bc": "BC-03", "api": "/robotics/construction/robots", "db": "robotics_*", "events": ("RobotMissionCompletedEvent",), "security": ("robotics.write",), "scaling": "robot_workers", "responsibility": "Construction robot and heavy equipment missions"},
    {"id": "bim_service", "bc": "BC-02", "api": "/robotics/construction/bim", "db": "robotics_*", "events": ("PhaseCompletedEvent",), "security": ("robotics.read",), "scaling": "bim_workers", "responsibility": "BIM projections via Integration Platform"},
    {"id": "infrastructure_monitoring_service", "bc": "BC-04", "api": "/robotics/construction/infrastructure", "db": "robotics_*", "events": ("InspectionPassedEvent", "InfrastructureIssueDetectedEvent"), "security": ("robotics.write",), "scaling": "infra_workers", "responsibility": "Infrastructure health monitoring"},
    {"id": "smart_building_service", "bc": "BC-05", "api": "/robotics/construction/buildings", "db": "robotics_*", "events": ("BuildingOperationalEvent",), "security": ("robotics.write",), "scaling": "building_workers", "responsibility": "Autonomous building systems operations"},
    {"id": "asset_lifecycle_service", "bc": "BC-06", "api": "/robotics/construction/assets", "db": "robotics_*", "events": ("InfrastructureIssueDetectedEvent",), "security": ("robotics.write",), "scaling": "asset_workers", "responsibility": "Asset lifecycle projections"},
    {"id": "digital_twin_service", "bc": "BC-07", "api": "/robotics/construction/digital-twin", "db": "robotics_*", "events": ("BuildingOperationalEvent", "PhaseCompletedEvent"), "security": ("robotics.read",), "scaling": "twin_workers", "responsibility": "Construction digital twin sync"},
    {"id": "knowledge_graph_service", "bc": "BC-07", "api": "/robotics/construction/knowledge-graph", "db": "robotics_*", "events": ("ConstructionStartedEvent",), "security": ("robotics.read",), "scaling": "kg_workers", "responsibility": "Construction knowledge graph projections"},
    {"id": "safety_service", "bc": "BC-08", "api": "/robotics/construction/safety", "db": "robotics_*", "events": ("InfrastructureIssueDetectedEvent",), "security": ("robotics.write",), "scaling": "safety_workers", "responsibility": "Site safety and compliance"},
    {"id": "construction_analytics_service", "bc": "BC-01", "api": "/robotics/construction/analytics", "db": "robotics_*", "events": ("PhaseCompletedEvent", "RobotMissionCompletedEvent"), "security": ("robotics.read",), "scaling": "analytics_workers", "responsibility": "Construction analytics facets"},
)
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p216d_robotics_os",
        "p216e_physical_ai",
        "p216i_healthcare",
        "p214z_ai_master",
        "p215z_quantum_supreme",
        "erp",
        "bim_platforms",
        "gis",
        "iot",
        "scada",
        "smart_city_platform",
        "facility_management",
        "asset_management",
        "integration_platform",
    ),
    "mechanisms": (
        "construction_apis",
        "robot_mission_interfaces",
        "bim_via_integration_connectors",
        "gis_via_integration_connectors",
        "scada_via_integration_connectors",
        "construction_event_contracts",
    ),
    "via_p216_d": True,
    "via_p216_e": True,
    "via_p216_i": True,
    "via_p214_z": True,
    "via_p215_z": True,
    "via_p213": True,
    "via_integration_platform": True,
    "never_direct_bim_gis_scada_bypass": True,
    "never_duplicate_construction_core_logic": True,
}
DEPLOYMENT = {
    "present_required": True,
    "model": "hybrid_construction_intelligence_infrastructure",
    "includes": (
        "construction_edge_cluster",
        "cloud_platform",
        "robot_runtime",
        "digital_twin_cluster",
        "knowledge_graph_cluster",
        "ai_cluster",
        "observability_platform",
        "disaster_recovery",
    ),
    "deployment_models": (
        "construction_site",
        "enterprise_builder",
        "infrastructure_authority",
        "smart_city",
        "global_infrastructure_network",
    ),
    "cloud_native": True,
    "edge_native": True,
}
TESTING = (
    "construction_workflow_testing",
    "robot_coordination_testing",
    "bim_validation",
    "digital_twin_testing",
    "infrastructure_simulation",
    "performance_testing",
    "security_testing",
    "resilience_testing",
)
API_SURFACES = (
    "/api/v1/robotics/construction",
    "/api/v1/robotics/construction/vision",
    "/api/v1/robotics/construction/domain",
    "/api/v1/robotics/construction/bounded-contexts",
    "/api/v1/robotics/construction/robotics",
    "/api/v1/robotics/construction/infrastructure",
    "/api/v1/robotics/construction/buildings",
    "/api/v1/robotics/construction/ai",
    "/api/v1/robotics/construction/digital-twin",
    "/api/v1/robotics/construction/knowledge-graph",
    "/api/v1/robotics/construction/security",
    "/api/v1/robotics/construction/cqrs",
    "/api/v1/robotics/construction/events",
    "/api/v1/robotics/construction/microservices",
    "/api/v1/robotics/construction/integration",
    "/api/v1/robotics/construction/deployment",
    "/api/v1/robotics/construction/testing",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
QUALITY_GATES_REJECT_IF = (
    "construction_robotics_platform_is_missing",
    "smart_infrastructure_platform_is_missing",
    "autonomous_building_systems_are_missing",
    "construction_ai_is_missing",
    "construction_digital_twin_is_missing",
    "construction_knowledge_graph_is_missing",
    "safety_compliance_architecture_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "cloud_edge_deployment_is_missing",
    "enterprise_construction_integration_is_missing",
    "testing_architecture_is_missing",
    "sibling_robotics_bc",
    "replace_p216_i_healthcare",
    "direct_bim_gis_scada_bypass",
    "duplicate_construction_core_logic",
    "module_local_llm",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Construction Intelligence Fabric",
        "construction_vision": CONSTRUCTION_VISION,
        "mission": MISSION,
        "vision": VISION,
        "builds_on_p216": True,
        "builds_on_p216_i": True,
        "builds_on_p216_h": True,
        "builds_on_p216_e": True,
        "builds_on_p216_d": True,
        "builds_on_p215_z": True,
        "builds_on_p214_z": True,
        "never_replace_p216_i_healthcare": True,
        "foundation_gate": FOUNDATION_GATE,
        "healthcare_gate": HEALTHCARE_GATE,
        "mobility_gate": MOBILITY_GATE,
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
    return dict(CONSTRUCTION_ROBOTICS)

def infrastructure() -> dict[str, Any]:
    return dict(SMART_INFRASTRUCTURE)

def buildings() -> dict[str, Any]:
    return dict(AUTONOMOUS_BUILDING)

def construction_ai() -> dict[str, Any]:
    return dict(CONSTRUCTION_AI)

def digital_twin() -> dict[str, Any]:
    return dict(CONSTRUCTION_DIGITAL_TWIN)

def knowledge_graph() -> dict[str, Any]:
    return dict(CONSTRUCTION_KG)

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
        "healthcare_gate_api": "/api/v1/robotics/healthcare",
        "runtime_gate_api": "/api/v1/robotics/runtime",
    }

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p216_l": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "construction_vision": CONSTRUCTION_VISION, "mission": MISSION, "vision": VISION, "principle": CONSTRUCTION_VISION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE, "runtime_gate": RUNTIME_GATE,
        "physical_ai_gate": PHYSICAL_AI_GATE, "industrial_gate": INDUSTRIAL_GATE,
        "logistics_gate": LOGISTICS_GATE, "mobility_gate": MOBILITY_GATE, "healthcare_gate": HEALTHCARE_GATE,
        "supreme_gate": SUPREME_GATE, "ai_gate": AI_GATE,
        "builds_on": [
            "P216", "P216-A", "P216-B", "P216-C", "P216-D", "P216-E", "P216-F", "P216-G", "P216-H", "P216-I",
            "P215-Z", "P214-Z", "P213",
            "ADR-472", "ADR-473", "ADR-474", "ADR-475", "ADR-476", "ADR-477", "ADR-478", "ADR-479", "ADR-480", "ADR-481",
        ],
        "vision_pack": vision_pack(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "robotics_platform": robotics_platform(),
        "infrastructure": infrastructure(),
        "buildings": buildings(),
        "construction_ai": construction_ai(),
        "digital_twin": digital_twin(),
        "knowledge_graph": knowledge_graph(),
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
        "construction_robotics_platform_present_required": True,
        "smart_infrastructure_platform_present_required": True,
        "autonomous_building_systems_present_required": True,
        "construction_ai_present_required": True,
        "construction_digital_twin_present_required": True,
        "construction_knowledge_graph_present_required": True,
        "safety_compliance_architecture_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "cloud_edge_deployment_present_required": True,
        "enterprise_construction_integration_present_required": True,
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
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_direct_bim_gis_scada_bypass": True,
        "bim_gis_scada_via_integration_platform_only": True,
        "never_duplicate_construction_core_logic": True,
        "no_module_local_llm": True,
        "physical_ai_via_p214z_acl_only": True,
        "ungated_physical_autonomy_strategy_forbidden": True,
        "opaque_safety_strategy_forbidden": True,
        "builds_on_p216": True, "builds_on_p216_i": True, "builds_on_p216_h": True,
        "builds_on_p216_e": True, "builds_on_p216_d": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p216_d": True, "via_p216_e": True, "via_p216_i": True,
        "via_p215_z": True, "via_p214_z": True, "via_p213": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "via_integration_platform": True,
        "api_prefix": f"{API_PREFIX}/construction",
        "forbidden_sibling_bc": [
            "construction_robotics_platform",
            "smart_infrastructure_platform",
            "autonomous_building_systems_platform",
            "digital_construction_intelligence_platform",
        ],
        "foundation_for_p216_l": True,
        "p216_j_agriculture_planned": True,
    }

def construction_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /robotics/construction",
        "GET /robotics/construction/vision",
        "GET /robotics/construction/domain",
        "GET /robotics/construction/bounded-contexts",
        "GET /robotics/construction/robotics",
        "GET /robotics/construction/infrastructure",
        "GET /robotics/construction/buildings",
        "GET /robotics/construction/ai",
        "GET /robotics/construction/digital-twin",
        "GET /robotics/construction/knowledge-graph",
        "GET /robotics/construction/security",
        "GET /robotics/construction/cqrs",
        "GET /robotics/construction/events",
        "GET /robotics/construction/microservices",
        "GET /robotics/construction/integration",
        "GET /robotics/construction/deployment",
        "GET /robotics/construction/testing",
        "GET /robotics/construction/readiness",
    ], "healthcare_gate_routes": ["GET /robotics/healthcare", "GET /robotics/healthcare/readiness"]}
