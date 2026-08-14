"""P216-B Enterprise Robotics Strategic Architecture — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P216-B"
ADR = 474
SOR = "robotics"
API_PREFIX = "/api/v1/robotics"
PRODUCT = "Enterprise Robotics Strategic Architecture, Capability Model & Robotics Operating Framework"
CAPABILITY = "CAP-PLT-RB-001"
ARCHITECTURE_VISION = (
    "MEOS Robotics Architecture SHALL provide a unified enterprise framework where robots, "
    "autonomous machines, physical AI systems and human operators operate as an integrated "
    "intelligent cyber-physical ecosystem."
)
FABRIC = "meos_robotics_strategic_architecture_framework"
FOUNDATION_GATE = "P216"
MISSION_GATE = "P216-A"
SUPREME_GATE = "P215-Z"
AI_GATE = "P214-Z"
CORE_DOMAIN = "enterprise_robotics_strategic_architecture"
SUPPORTING_DOMAINS = (
    {"id": "architecture_layers", "purpose": "Five-layer robotics architecture model."},
    {"id": "capability_model", "purpose": "Seven capability domains taxonomy."},
    {"id": "operating_framework", "purpose": "Five-layer operating model."},
    {"id": "service_model", "purpose": "Core robotics enterprise services."},
    {"id": "organizational_coe", "purpose": "Robotics Center of Excellence."},
    {"id": "governance_board", "purpose": "Robotics governance areas and decision rights."},
    {"id": "data_architecture", "purpose": "Robotics data sources and platforms."},
    {"id": "integration_architecture", "purpose": "MEOS and industrial integration patterns."},
    {"id": "security_architecture", "purpose": "Cyber-physical robotics security framework."},
    {"id": "scalability_maturity", "purpose": "Scale dimensions and maturity levels."},
)
LOGICAL_BOUNDED_CONTEXTS = (
    {"id": "strategy_architecture", "bc": "BC-01", "name": "Robotics Strategic Architecture Context", "purpose": "Five architecture layers and vision."},
    {"id": "capability_model", "bc": "BC-02", "name": "Robotics Capability Model Context", "purpose": "Seven capability domains."},
    {"id": "operating_framework", "bc": "BC-03", "name": "Robotics Operating Framework Context", "purpose": "Strategy through innovation layers."},
    {"id": "service_model", "bc": "BC-04", "name": "Robotics Service Model Context", "purpose": "Core enterprise robotics services."},
    {"id": "organization_governance", "bc": "BC-05", "name": "Robotics Org and Governance Context", "purpose": "CoE and governance board."},
    {"id": "data_integration", "bc": "BC-06", "name": "Robotics Data and Integration Context", "purpose": "Data platforms and peer integration."},
    {"id": "security_scale_maturity", "bc": "BC-07", "name": "Robotics Security Scale Maturity Context", "purpose": "Security, scale, maturity, CQRS, events."},
)
ARCHITECTURE_GOALS = (
    "standardized_robotics_capabilities",
    "enterprise_scalability",
    "autonomous_operations",
    "secure_machine_intelligence",
    "cross_domain_integration",
    "continuous_improvement",
)
ARCHITECTURE_LAYERS = (
    {"id": "L01", "name": "Physical Intelligence Layer", "responsibilities": ("physical_machines", "robots", "sensors", "actuators", "industrial_equipment", "autonomous_devices"), "components": ("industrial_robots", "mobile_robots", "collaborative_robots", "autonomous_vehicles", "drones", "smart_machines")},
    {"id": "L02", "name": "Edge Robotics Intelligence Layer", "responsibilities": ("real_time_processing", "local_intelligence", "machine_control", "sensor_processing"), "components": ("edge_ai_runtime", "robot_controllers", "sensor_fusion_engine", "real_time_decision_engine")},
    {"id": "L03", "name": "Robotics Platform Layer", "responsibilities": ("robot_management", "fleet_orchestration", "mission_control", "device_lifecycle"), "components": ("robot_management_platform", "fleet_management_platform", "mission_platform", "robot_registry")},
    {"id": "L04", "name": "Enterprise Intelligence Layer", "responsibilities": ("ai_reasoning", "analytics", "optimization", "decision_intelligence"), "components": ("ai_models_via_p214", "digital_twins", "knowledge_graphs", "optimization_engines")},
    {"id": "L05", "name": "MEOS Intelligence Control Layer", "responsibilities": ("enterprise_orchestration", "autonomous_governance", "strategic_intelligence"), "components": ("p215z_quantum_supreme_intelligence_core", "p214_ai_intelligence_layer", "enterprise_control_plane")},
)
CAPABILITY_DOMAINS = (
    {"id": "CD01", "name": "Robot Lifecycle Management", "capabilities": ("robot_registration", "robot_identity", "robot_configuration", "robot_deployment", "robot_monitoring", "robot_retirement", "robot_upgrade")},
    {"id": "CD02", "name": "Autonomous Machine Management", "capabilities": ("machine_intelligence", "machine_decision_making", "machine_learning", "machine_adaptation", "machine_optimization")},
    {"id": "CD03", "name": "Robot Fleet Intelligence", "capabilities": ("fleet_monitoring", "fleet_coordination", "fleet_scheduling", "fleet_optimization", "multi_robot_collaboration")},
    {"id": "CD04", "name": "Physical AI Intelligence", "capabilities": ("computer_vision", "sensor_intelligence", "spatial_understanding", "motion_planning", "environment_awareness", "physical_reasoning")},
    {"id": "CD05", "name": "Robotics Operations Management", "capabilities": ("mission_management", "task_scheduling", "operational_monitoring", "performance_analysis", "failure_management")},
    {"id": "CD06", "name": "Human-Robot Collaboration", "capabilities": ("human_interaction", "safety_collaboration", "workforce_augmentation", "collaborative_workflows")},
    {"id": "CD07", "name": "Robotics Knowledge Management", "capabilities": ("robot_knowledge_graph", "operational_memory", "machine_learning_repository", "experience_management")},
)
OPERATING_MODEL_LAYERS = (
    {"id": "OM01", "name": "Strategy Layer", "responsibilities": ("robotics_roadmap", "investment_planning", "capability_evolution", "business_alignment")},
    {"id": "OM02", "name": "Governance Layer", "responsibilities": ("policies", "standards", "safety", "compliance", "risk_management")},
    {"id": "OM03", "name": "Platform Layer", "responsibilities": ("robotics_services", "apis", "infrastructure", "runtime_platforms")},
    {"id": "OM04", "name": "Operations Layer", "responsibilities": ("robot_operations", "monitoring", "maintenance", "optimization")},
    {"id": "OM05", "name": "Innovation Layer", "responsibilities": ("robotics_research", "new_capabilities", "future_automation")},
)
CORE_SERVICES = (
    {"id": "robot_identity", "purpose": "Authenticate and identify robots and autonomous machines", "ownership": "robotics", "apis": ("/api/v1/robotics/identity",), "events": ("robotics.robot.identity.issued.v1",), "data_responsibility": "robot_identity_records", "security_boundary": "device_mtls_and_jwt"},
    {"id": "robot_registry", "purpose": "Canonical registry of robot assets and capabilities", "ownership": "robotics", "apis": ("/api/v1/robotics/registry",), "events": ("robotics.robot.registered.v1",), "data_responsibility": "robot_registry", "security_boundary": "tenant_scoped_rbac"},
    {"id": "robot_lifecycle", "purpose": "Deploy, upgrade, retire robots under governance", "ownership": "robotics", "apis": ("/api/v1/robotics/lifecycle",), "events": ("robotics.robot.activated.v1", "robotics.robot.retired.v1"), "data_responsibility": "lifecycle_state", "security_boundary": "workflow_gated_mutations"},
    {"id": "mission_management", "purpose": "Plan and execute robot missions safely", "ownership": "robotics", "apis": ("/api/v1/robotics/missions",), "events": ("robotics.mission.completed.v1",), "data_responsibility": "mission_plans_and_results", "security_boundary": "command_authorization"},
    {"id": "fleet_intelligence", "purpose": "Coordinate and optimize multi-robot fleets", "ownership": "robotics", "apis": ("/api/v1/robotics/fleet",), "events": ("robotics.fleet.intelligence.updated.v1",), "data_responsibility": "fleet_projections", "security_boundary": "fleet_operator_roles"},
    {"id": "physical_ai", "purpose": "Physical AI surfaces via P214-Z ACL only", "ownership": "robotics_acl_to_ai", "apis": ("/api/v1/ai",), "events": ("ai.insight.generated.v1",), "data_responsibility": "inference_intents_not_models", "security_boundary": "ai_infer_permissions"},
    {"id": "robot_analytics", "purpose": "Operational analytics via Analytics Platform", "ownership": "analytics_with_robotics_facets", "apis": ("/api/v1/analytics",), "events": ("analytics.metric.recorded.v1",), "data_responsibility": "metric_facets", "security_boundary": "analytics_read_scopes"},
    {"id": "digital_twin", "purpose": "Digital twin synchronization for robots and sites", "ownership": "robotics", "apis": ("/api/v1/robotics/twins",), "events": ("robotics.twin.synchronized.v1",), "data_responsibility": "twin_state_refs", "security_boundary": "twin_access_policies"},
    {"id": "safety_management", "purpose": "Safety policies, alerts, and collaborative safety", "ownership": "robotics", "apis": ("/api/v1/robotics/safety",), "events": ("robotics.safety.alert.generated.v1",), "data_responsibility": "safety_incidents_and_policies", "security_boundary": "safety_critical_roles"},
    {"id": "maintenance_intelligence", "purpose": "Predictive and planned maintenance intelligence", "ownership": "robotics", "apis": ("/api/v1/robotics/maintenance",), "events": ("robotics.maintenance.recommended.v1",), "data_responsibility": "maintenance_plans", "security_boundary": "maintenance_operator_roles"},
)
ORGANIZATIONAL_COE = (
    "robotics_architecture_team",
    "physical_ai_team",
    "robot_operations_team",
    "safety_engineering_team",
    "robot_data_team",
    "digital_twin_team",
    "security_team",
    "research_innovation_team",
)
GOVERNANCE_AREAS = (
    "architecture_governance",
    "safety_governance",
    "security_governance",
    "machine_governance",
    "ai_model_governance",
    "operational_governance",
)
DATA_SOURCES = ("robot_telemetry", "sensor_data", "mission_data", "machine_events", "operational_data", "environmental_data")
DATA_PLATFORMS = ("robot_data_lake", "industrial_data_platform", "knowledge_graph", "digital_twin_data_platform")
INTEGRATION_TARGETS = ("p215z_quantum_master", "p214_ai_intelligence", "p213_enterprise_analytics", "erp_systems", "iot_platforms", "manufacturing_systems", "cloud_platforms", "edge_platforms")
INTEGRATION_PATTERNS = ("api_first", "event_driven", "streaming_intelligence", "digital_twin_synchronization", "command_and_control_interfaces")
SECURITY_DOMAINS = ("robot_identity_security", "device_authentication", "command_authorization", "communication_security", "firmware_security", "ai_model_security", "physical_security")
SECURITY_PRINCIPLES = ("zero_trust", "least_privilege", "continuous_verification", "threat_intelligence")
SCALE_DIMENSIONS = ("number_of_robots", "geographic_expansion", "operational_complexity", "data_volume", "ai_model_growth")
SCALE_REQUIREMENTS = ("multi_tenant_support", "edge_scaling", "cloud_scaling", "fleet_scaling", "global_deployment")
MATURITY_LEVELS = (
    {"level": 1, "name": "Manual Operations"},
    {"level": 2, "name": "Connected Machines"},
    {"level": 3, "name": "Intelligent Automation"},
    {"level": 4, "name": "Autonomous Robotics"},
    {"level": 5, "name": "Cyber-Physical Autonomous Enterprise"},
    {"level": 6, "name": "Self-Optimizing Intelligence Ecosystem"},
)
COMMANDS = ("RegisterRobotCommand", "DeployRobotCommand", "ExecuteMissionCommand", "OptimizeFleetCommand", "UpdateRobotCapabilityCommand")
QUERIES = ("GetRobotStateQuery", "GetFleetStatusQuery", "GetMissionPerformanceQuery", "GetMachineHealthQuery")
CORE_EVENTS = (
    {"name": "RobotRegisteredEvent", "schema": "robotics.robot.registered.v1", "owner": "robot_registry", "consumers": "audit,search,analytics"},
    {"name": "RobotActivatedEvent", "schema": "robotics.robot.activated.v1", "owner": "robot_lifecycle", "consumers": "audit,fleet,notifications"},
    {"name": "MissionCompletedEvent", "schema": "robotics.mission.completed.v1", "owner": "mission_management", "consumers": "audit,analytics,workflow"},
    {"name": "MachineOptimizationCompletedEvent", "schema": "robotics.machine.optimization.completed.v1", "owner": "fleet_intelligence", "consumers": "analytics,ai"},
    {"name": "SafetyAlertGeneratedEvent", "schema": "robotics.safety.alert.generated.v1", "owner": "safety_management", "consumers": "notifications,audit,compliance"},
    {"name": "FleetIntelligenceUpdatedEvent", "schema": "robotics.fleet.intelligence.updated.v1", "owner": "fleet_intelligence", "consumers": "analytics,ai,digital_twin"},
)
MICROSERVICES = (
    {"id": "robotics_strategy_architecture_service", "bc": "BC-01", "api": "/robotics/strategy", "db": "robotics_*", "events": ("RobotRegisteredEvent",), "security": ("robotics.read",), "scaling": "strategy_replicas"},
    {"id": "capability_model_service", "bc": "BC-02", "api": "/robotics/strategy/capabilities", "db": "robotics_*", "events": ("FleetIntelligenceUpdatedEvent",), "security": ("robotics.read",), "scaling": "capability_workers"},
    {"id": "operating_framework_service", "bc": "BC-03", "api": "/robotics/strategy/operating-model", "db": "robotics_*", "events": ("MissionCompletedEvent",), "security": ("robotics.read",), "scaling": "ops_model_replicas"},
    {"id": "service_model_service", "bc": "BC-04", "api": "/robotics/strategy/services", "db": "robotics_*", "events": ("RobotActivatedEvent",), "security": ("robotics.read",), "scaling": "service_catalog_replicas"},
    {"id": "organization_governance_service", "bc": "BC-05", "api": "/robotics/strategy/governance", "db": "robotics_*", "events": ("SafetyAlertGeneratedEvent",), "security": ("robotics.admin",), "scaling": "governance_replicas"},
    {"id": "data_integration_service", "bc": "BC-06", "api": "/robotics/strategy/data", "db": "robotics_*", "events": ("FleetIntelligenceUpdatedEvent",), "security": ("robotics.read",), "scaling": "data_workers"},
    {"id": "security_architecture_service", "bc": "BC-07", "api": "/robotics/strategy/security", "db": "robotics_*", "events": ("SafetyAlertGeneratedEvent",), "security": ("robotics.admin",), "scaling": "security_replicas"},
    {"id": "maturity_scale_service", "bc": "BC-07", "api": "/robotics/strategy/maturity", "db": "robotics_*", "events": ("MachineOptimizationCompletedEvent",), "security": ("robotics.read",), "scaling": "maturity_replicas"},
)
API_SURFACES = (
    "/api/v1/robotics/strategy",
    "/api/v1/robotics/strategy/layers",
    "/api/v1/robotics/strategy/capabilities",
    "/api/v1/robotics/strategy/operating-model",
    "/api/v1/robotics/strategy/services",
    "/api/v1/robotics/strategy/organization",
    "/api/v1/robotics/strategy/governance",
    "/api/v1/robotics/strategy/data",
    "/api/v1/robotics/strategy/integration",
    "/api/v1/robotics/strategy/security",
    "/api/v1/robotics/strategy/scalability",
    "/api/v1/robotics/strategy/maturity",
    "/api/v1/robotics/strategy/cqrs",
    "/api/v1/robotics/strategy/events",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
SECURITY = {
    "present_required": True,
    "zero_trust": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "never_replace_p216_foundation": True,
    "never_replace_p216_a_mission": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "ungated_physical_autonomy_strategy_forbidden": True,
    "opaque_safety_strategy_forbidden": True,
    "domains": list(SECURITY_DOMAINS),
    "principles": list(SECURITY_PRINCIPLES),
}
DEPLOYMENT = {"present_required": True, "cloud_native": True, "components": ("strategy_services_cluster", "capability_model_service", "fleet_intelligence_plane", "strategic_observability")}
TESTING = (
    "strategy_architecture_testing",
    "capability_model_testing",
    "operating_framework_testing",
    "service_model_testing",
    "governance_testing",
    "security_architecture_testing",
    "maturity_model_testing",
)
QUALITY_GATES_REJECT_IF = (
    "robotics_strategic_architecture_is_missing",
    "capability_model_is_missing",
    "operating_framework_is_missing",
    "service_model_is_missing",
    "organizational_model_is_missing",
    "governance_model_is_missing",
    "security_model_is_missing",
    "data_architecture_is_missing",
    "integration_architecture_is_missing",
    "scalability_model_is_missing",
    "maturity_model_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "api_first_architecture_is_missing",
    "cloud_native_deployment_is_missing",
    "sibling_robotics_bc",
    "replace_p216_foundation",
    "replace_p216_a_mission",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Robotics Strategic Architecture Framework",
        "architecture_vision": ARCHITECTURE_VISION,
        "goals": list(ARCHITECTURE_GOALS),
        "builds_on_p216": True,
        "builds_on_p216_a": True,
        "builds_on_p215_z": True,
        "builds_on_p214_z": True,
        "never_replace_p216_foundation": True,
        "never_replace_p216_a_mission": True,
        "foundation_gate": FOUNDATION_GATE,
        "mission_gate": MISSION_GATE,
        "supreme_gate": SUPREME_GATE,
        "ai_gate": AI_GATE,
    }

def domain_model() -> dict[str, Any]:
    return {"core_domain": CORE_DOMAIN, "supporting_domains": [dict(d) for d in SUPPORTING_DOMAINS], "supporting_count": len(SUPPORTING_DOMAINS)}

def bounded_contexts() -> dict[str, Any]:
    return {"contexts": [dict(c) for c in LOGICAL_BOUNDED_CONTEXTS], "context_count": len(LOGICAL_BOUNDED_CONTEXTS)}

def architecture_layers() -> dict[str, Any]:
    return {"present_required": True, "layers": [dict(x) for x in ARCHITECTURE_LAYERS], "layer_count": len(ARCHITECTURE_LAYERS)}

def capability_model() -> dict[str, Any]:
    return {"present_required": True, "domains": [dict(d) for d in CAPABILITY_DOMAINS], "domain_count": len(CAPABILITY_DOMAINS)}

def operating_framework() -> dict[str, Any]:
    return {"present_required": True, "model": "meos_robotics_operating_framework", "layers": [dict(x) for x in OPERATING_MODEL_LAYERS], "layer_count": len(OPERATING_MODEL_LAYERS)}

def service_model() -> dict[str, Any]:
    return {"present_required": True, "services": [dict(s) for s in CORE_SERVICES], "service_count": len(CORE_SERVICES)}

def organizational_model() -> dict[str, Any]:
    return {"present_required": True, "coe": "meos_robotics_center_of_excellence", "functions": list(ORGANIZATIONAL_COE)}

def governance_model() -> dict[str, Any]:
    return {
        "present_required": True,
        "board": "meos_robotics_governance_board",
        "areas": list(GOVERNANCE_AREAS),
        "decision_rights": True,
        "approval_processes_via_workflow": True,
        "policy_management_via_policy_engine": True,
        "risk_management": True,
        "via_policy_engine": True,
        "via_workflow": True,
        "opaque_safety_strategy_forbidden": True,
        "ungated_physical_autonomy_strategy_forbidden": True,
    }

def data_architecture() -> dict[str, Any]:
    return {"present_required": True, "sources": list(DATA_SOURCES), "platforms": list(DATA_PLATFORMS)}

def integration_architecture() -> dict[str, Any]:
    return {
        "present_required": True,
        "targets": list(INTEGRATION_TARGETS),
        "patterns": list(INTEGRATION_PATTERNS),
        "via_p215_z": True,
        "via_p214_z": True,
        "via_p213": True,
    }

def security_architecture() -> dict[str, Any]:
    return dict(SECURITY)

def scalability_model() -> dict[str, Any]:
    return {"present_required": True, "dimensions": list(SCALE_DIMENSIONS), "requirements": list(SCALE_REQUIREMENTS)}

def maturity_model() -> dict[str, Any]:
    return {"present_required": True, "levels": [dict(x) for x in MATURITY_LEVELS], "level_count": len(MATURITY_LEVELS)}

def cqrs() -> dict[str, Any]:
    return {"commands": list(COMMANDS), "command_count": len(COMMANDS), "queries": list(QUERIES), "query_count": len(QUERIES)}

def events() -> dict[str, Any]:
    return {"core_events": [dict(e) for e in CORE_EVENTS], "core_event_count": len(CORE_EVENTS)}

def microservices() -> dict[str, Any]:
    return {"services": [dict(s) for s in MICROSERVICES], "service_count": len(MICROSERVICES)}

def api() -> dict[str, Any]:
    return {
        "surfaces": list(API_SURFACES),
        "styles": list(API_STYLES),
        "api_first_present_required": True,
        "foundation_gate_api": "/api/v1/robotics/foundation",
        "mission_gate_api": "/api/v1/robotics/mission",
    }

def deployment() -> dict[str, Any]:
    return dict(DEPLOYMENT)

def testing() -> dict[str, Any]:
    return {"suites": list(TESTING), "suite_count": len(TESTING)}

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p216_c": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "architecture_vision": ARCHITECTURE_VISION, "principle": ARCHITECTURE_VISION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "supreme_gate": SUPREME_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P216", "P216-A", "P215-Z", "P214-Z", "P213", "ADR-472", "ADR-473"],
        "vision": vision_pack(), "domain_model": domain_model(), "bounded_contexts": bounded_contexts(),
        "architecture_layers": architecture_layers(), "capability_model": capability_model(),
        "operating_framework": operating_framework(), "service_model": service_model(),
        "organizational_model": organizational_model(), "governance_model": governance_model(),
        "data_architecture": data_architecture(), "integration_architecture": integration_architecture(),
        "security_architecture": security_architecture(), "scalability_model": scalability_model(),
        "maturity_model": maturity_model(), "cqrs": cqrs(), "events": events(),
        "microservices": microservices(), "api": api(), "security": security_architecture(),
        "deployment": deployment(), "testing": testing(), "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "robotics_strategic_architecture_present_required": True,
        "capability_model_present_required": True,
        "operating_framework_present_required": True,
        "service_model_present_required": True,
        "organizational_model_present_required": True,
        "governance_model_present_required": True,
        "security_model_present_required": True,
        "data_architecture_present_required": True,
        "integration_architecture_present_required": True,
        "scalability_model_present_required": True,
        "maturity_model_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "cloud_native_deployment_present_required": True,
        "sibling_robotics_bc_forbidden": True,
        "never_replace_p216_foundation": True,
        "never_replace_p216_a_mission": True,
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "ungated_physical_autonomy_strategy_forbidden": True,
        "opaque_safety_strategy_forbidden": True,
        "builds_on_p216": True, "builds_on_p216_a": True, "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p215_z": True, "via_p214_z": True, "via_p213": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "api_prefix": f"{API_PREFIX}/strategy",
        "forbidden_sibling_bc": [
            "robotics_strategy_platform",
            "robotics_capability_platform",
            "robotics_operating_framework_platform",
        ],
        "foundation_for_p216_c": True,
    }

def strategy_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /robotics/strategy",
        "GET /robotics/strategy/layers",
        "GET /robotics/strategy/capabilities",
        "GET /robotics/strategy/operating-model",
        "GET /robotics/strategy/services",
        "GET /robotics/strategy/organization",
        "GET /robotics/strategy/governance",
        "GET /robotics/strategy/data",
        "GET /robotics/strategy/integration",
        "GET /robotics/strategy/security",
        "GET /robotics/strategy/scalability",
        "GET /robotics/strategy/maturity",
        "GET /robotics/strategy/cqrs",
        "GET /robotics/strategy/events",
        "GET /robotics/strategy/readiness",
    ], "foundation_gate_routes": ["GET /robotics/foundation", "GET /robotics/foundation/readiness"],
       "mission_gate_routes": ["GET /robotics/mission", "GET /robotics/mission/readiness"]}
