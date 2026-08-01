"""P216-C Enterprise Robotics Domain Architecture (DDD) — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P216-C"
ADR = 475
SOR = "robotics"
API_PREFIX = "/api/v1/robotics"
PRODUCT = "Enterprise Robotics Domain Architecture (DDD), Bounded Contexts, Aggregates & Domain Model"
CAPABILITY = "CAP-PLT-RB-001"
PRIMARY_CAPABILITY = (
    "Enable intelligent physical execution of enterprise operations through autonomous cyber-physical systems."
)
CORE_DOMAIN_NAME = "Enterprise Cyber-Physical Intelligence Domain"
FABRIC = "meos_robotics_domain_architecture_framework"
FOUNDATION_GATE = "P216"
MISSION_GATE = "P216-A"
STRATEGY_GATE = "P216-B"
SUPREME_GATE = "P215-Z"
AI_GATE = "P214-Z"

SUPPORTING_DOMAINS = (
    {"id": "robotics_lifecycle_management", "purpose": "Robot creation, registration, deployment, maintenance, retirement."},
    {"id": "autonomous_machine_intelligence", "purpose": "Machine reasoning, autonomous behaviour, decision execution."},
    {"id": "physical_ai_intelligence", "purpose": "Perception, environment understanding, physical reasoning, motion intelligence."},
    {"id": "robot_fleet_intelligence", "purpose": "Multi-robot coordination, fleet optimization, mission scheduling."},
    {"id": "robotics_digital_twin", "purpose": "Virtual representation, simulation, prediction, optimization."},
    {"id": "human_robot_collaboration", "purpose": "Human interaction, safety collaboration, workforce augmentation."},
    {"id": "robotics_safety_governance", "purpose": "Safety policies, operational constraints, compliance."},
)
GENERIC_DOMAINS = (
    "identity_management",
    "authorization",
    "audit_logging",
    "notification",
    "workflow_engine",
    "messaging_infrastructure",
    "observability",
    "configuration_management",
)
BOUNDED_CONTEXTS = (
    {"id": "BC-01", "name": "Robot Identity Context", "aggregate": "RobotIdentityAggregate", "purpose": "Manage identity and lifecycle identity of robots.", "dependencies": ("security_platform", "identity_platform")},
    {"id": "BC-02", "name": "Robot Lifecycle Context", "aggregate": "RobotLifecycleAggregate", "purpose": "Manage complete robot lifecycle.", "dependencies": ("BC-01",)},
    {"id": "BC-03", "name": "Autonomous Machine Intelligence Context", "aggregate": "AutonomousMachineAggregate", "purpose": "Manage autonomous machine behaviour.", "dependencies": ("BC-02", "BC-04")},
    {"id": "BC-04", "name": "Physical AI Context", "aggregate": "PhysicalAIModelAggregate", "purpose": "Manage intelligence models operating in physical environments.", "dependencies": ("p214_z",)},
    {"id": "BC-05", "name": "Robot Mission Management Context", "aggregate": "RobotMissionAggregate", "purpose": "Manage autonomous tasks and missions.", "dependencies": ("BC-02", "BC-09")},
    {"id": "BC-06", "name": "Robot Fleet Intelligence Context", "aggregate": "RobotFleetAggregate", "purpose": "Coordinate multiple autonomous systems.", "dependencies": ("BC-02", "BC-05")},
    {"id": "BC-07", "name": "Robotics Digital Twin Context", "aggregate": "RoboticsDigitalTwinAggregate", "purpose": "Create virtual representation of physical systems.", "dependencies": ("BC-02", "BC-05")},
    {"id": "BC-08", "name": "Human Robot Collaboration Context", "aggregate": "HumanRobotCollaborationAggregate", "purpose": "Manage interaction between humans and machines.", "dependencies": ("BC-02", "BC-09")},
    {"id": "BC-09", "name": "Robotics Safety Governance Context", "aggregate": "RoboticsSafetyAggregate", "purpose": "Manage robotics safety and compliance.", "dependencies": ("policy_engine", "workflow")},
)
AGGREGATE_CATALOG = (
    {
        "id": "RobotIdentityAggregate",
        "bc": "BC-01",
        "entities": ("RobotIdentity",),
        "value_objects": ("RobotSerialNumber", "OwnershipRef", "IdentityVerificationStatus"),
        "commands": ("RegisterRobotIdentity", "VerifyRobotIdentity"),
        "events": ("RobotRegisteredEvent",),
    },
    {
        "id": "RobotLifecycleAggregate",
        "bc": "BC-02",
        "entities": ("Robot", "RobotVersion", "RobotConfiguration", "RobotDeployment"),
        "value_objects": ("RobotSerialNumber", "RobotType", "RobotCapabilityProfile", "LifecycleStatus"),
        "commands": ("RegisterRobot", "DeployRobot", "UpgradeRobot", "RetireRobot"),
        "events": ("RobotRegisteredEvent", "RobotDeployedEvent", "RobotUpgradedEvent", "RobotRetiredEvent"),
    },
    {
        "id": "AutonomousMachineAggregate",
        "bc": "BC-03",
        "entities": ("MachineAgent", "DecisionEngine", "LearningModel", "MachineCapability"),
        "value_objects": ("AutonomyLevel", "DecisionConfidence", "LearningState"),
        "commands": ("ActivateAutonomy", "ExecuteDecision", "UpdateCapability"),
        "events": ("AutonomyActivatedEvent", "DecisionExecutedEvent", "CapabilityImprovedEvent"),
    },
    {
        "id": "PhysicalAIModelAggregate",
        "bc": "BC-04",
        "entities": ("AIModel", "VisionModel", "MotionModel", "SensorModel"),
        "value_objects": ("ModelVersion", "AccuracyScore", "InferenceLatency", "ConfidenceLevel"),
        "commands": ("DeployModel", "EvaluateModel", "UpdateModel"),
        "events": ("PhysicalAIModelDeployedEvent", "ModelPerformanceChangedEvent"),
    },
    {
        "id": "RobotMissionAggregate",
        "bc": "BC-05",
        "entities": ("Mission", "Task", "Objective", "ExecutionPlan"),
        "value_objects": ("MissionPriority", "MissionStatus", "ExecutionTime", "SuccessRate"),
        "commands": ("CreateMission", "AssignMission", "ExecuteMission", "CancelMission"),
        "events": ("MissionCreatedEvent", "MissionStartedEvent", "MissionCompletedEvent", "MissionFailedEvent"),
    },
    {
        "id": "RobotFleetAggregate",
        "bc": "BC-06",
        "entities": ("Fleet", "RobotGroup", "FleetStrategy"),
        "value_objects": ("FleetCapacity", "OptimizationScore", "CoordinationLevel"),
        "commands": ("CreateFleet", "OptimizeFleet", "CoordinateRobots"),
        "events": ("FleetCreatedEvent", "FleetOptimizedEvent", "FleetCoordinationCompletedEvent"),
    },
    {
        "id": "RoboticsDigitalTwinAggregate",
        "bc": "BC-07",
        "entities": ("DigitalTwin", "SimulationModel", "PhysicalState", "VirtualState"),
        "value_objects": ("TwinAccuracy", "SimulationConfidence", "SynchronizationLevel"),
        "commands": ("CreateDigitalTwin", "SynchronizeTwin", "RunSimulation"),
        "events": ("DigitalTwinCreatedEvent", "StateSynchronizedEvent", "SimulationCompletedEvent"),
    },
    {
        "id": "HumanRobotCollaborationAggregate",
        "bc": "BC-08",
        "entities": ("HumanOperator", "InteractionSession", "CollaborationWorkflow"),
        "value_objects": ("SafetyDistance", "InteractionMode", "TrustLevel"),
        "commands": ("StartCollaboration", "CompleteSafetyCheck"),
        "events": ("CollaborationStartedEvent", "SafetyCheckCompletedEvent"),
    },
    {
        "id": "RoboticsSafetyAggregate",
        "bc": "BC-09",
        "entities": ("SafetyPolicy", "SafetyRule", "RiskAssessment"),
        "value_objects": ("RiskLevel", "SafetyScore", "ComplianceStatus"),
        "commands": ("CreateSafetyPolicy", "AssessRisk", "ApproveSafety"),
        "events": ("SafetyPolicyCreatedEvent", "RiskDetectedEvent", "SafetyApprovedEvent"),
    },
)
DOMAIN_RELATIONSHIPS = (
    {"from": "Robot", "relation": "owns", "to": "RobotIdentity"},
    {"from": "Robot", "relation": "executes", "to": "Mission"},
    {"from": "Robot", "relation": "belongsTo", "to": "Fleet"},
    {"from": "Robot", "relation": "uses", "to": "PhysicalAIModel"},
    {"from": "Robot", "relation": "synchronizedWith", "to": "DigitalTwin"},
    {"from": "HumanOperator", "relation": "collaboratesWith", "to": "Robot"},
    {"from": "SafetyPolicy", "relation": "governs", "to": "RobotOperation"},
)
AGGREGATE_RULES = (
    "one_aggregate_one_consistency_boundary",
    "external_communication_via_domain_events",
    "cross_context_updates_asynchronous",
    "transaction_consistency_within_aggregate",
    "domain_ownership_per_bc",
    "independent_evolution",
    "event_publishing_required",
    "microservice_isolation",
    "never_cross_context_aggregate_mutation",
)
DOMAIN_SERVICES = (
    {"id": "RobotCapabilityEvaluationService", "responsibility": "Evaluate robot capability profiles against mission requirements", "inputs": ("robot_id", "capability_profile"), "outputs": ("capability_score",), "dependencies": ("BC-02",), "events": ("RobotCapabilityImprovedEvent",)},
    {"id": "MissionPlanningService", "responsibility": "Plan mission objectives and execution plans", "inputs": ("mission_intent", "fleet_capacity"), "outputs": ("execution_plan",), "dependencies": ("BC-05", "BC-06"), "events": ("MissionCreatedEvent",)},
    {"id": "FleetOptimizationService", "responsibility": "Optimize multi-robot coordination and scheduling", "inputs": ("fleet_id", "constraints"), "outputs": ("optimization_score",), "dependencies": ("BC-06",), "events": ("FleetOptimizedEvent",)},
    {"id": "PhysicalAIInferenceService", "responsibility": "Request physical AI inference via P214-Z ACL only", "inputs": ("model_ref", "sensor_context"), "outputs": ("inference_result",), "dependencies": ("BC-04", "p214_z"), "events": ("PhysicalAIUpdatedEvent",)},
    {"id": "SafetyValidationService", "responsibility": "Validate operations against safety policies", "inputs": ("operation", "safety_policy_id"), "outputs": ("safety_decision",), "dependencies": ("BC-09", "policy_engine"), "events": ("SafetyViolationDetectedEvent", "SafetyApprovedEvent")},
    {"id": "DigitalTwinSynchronizationService", "responsibility": "Synchronize physical and virtual robot state", "inputs": ("twin_id", "physical_state"), "outputs": ("sync_level",), "dependencies": ("BC-07",), "events": ("DigitalTwinSynchronizedEvent",)},
    {"id": "AutonomousDecisionService", "responsibility": "Execute gated autonomous decisions", "inputs": ("agent_id", "decision_context"), "outputs": ("decision_result",), "dependencies": ("BC-03", "BC-09"), "events": ("AutonomousDecisionExecutedEvent",)},
)
REPOSITORIES = (
    {"id": "RobotRepository", "aggregate": "RobotLifecycleAggregate", "responsibilities": ("aggregate_persistence", "state_reconstruction", "event_sourcing_support")},
    {"id": "MissionRepository", "aggregate": "RobotMissionAggregate", "responsibilities": ("aggregate_persistence", "state_reconstruction", "event_sourcing_support")},
    {"id": "FleetRepository", "aggregate": "RobotFleetAggregate", "responsibilities": ("aggregate_persistence", "state_reconstruction", "event_sourcing_support")},
    {"id": "PhysicalAIRepository", "aggregate": "PhysicalAIModelAggregate", "responsibilities": ("aggregate_persistence", "state_reconstruction", "event_sourcing_support")},
    {"id": "DigitalTwinRepository", "aggregate": "RoboticsDigitalTwinAggregate", "responsibilities": ("aggregate_persistence", "state_reconstruction", "event_sourcing_support")},
    {"id": "SafetyPolicyRepository", "aggregate": "RoboticsSafetyAggregate", "responsibilities": ("aggregate_persistence", "state_reconstruction", "event_sourcing_support")},
)
CORE_EVENTS = (
    {"name": "RobotRegisteredEvent", "schema": "robotics.robot.registered.v1", "owner": "BC-01", "consumers": "audit,search,lifecycle"},
    {"name": "RobotActivatedEvent", "schema": "robotics.robot.activated.v1", "owner": "BC-02", "consumers": "audit,fleet,notifications"},
    {"name": "MissionCreatedEvent", "schema": "robotics.mission.created.v1", "owner": "BC-05", "consumers": "audit,fleet,workflow"},
    {"name": "MissionCompletedEvent", "schema": "robotics.mission.completed.v1", "owner": "BC-05", "consumers": "audit,analytics,workflow"},
    {"name": "AutonomousDecisionExecutedEvent", "schema": "robotics.autonomous.decision.executed.v1", "owner": "BC-03", "consumers": "audit,analytics,safety"},
    {"name": "FleetOptimizedEvent", "schema": "robotics.fleet.optimized.v1", "owner": "BC-06", "consumers": "analytics,ai,twin"},
    {"name": "PhysicalAIUpdatedEvent", "schema": "robotics.physical_ai.updated.v1", "owner": "BC-04", "consumers": "ai,analytics"},
    {"name": "DigitalTwinSynchronizedEvent", "schema": "robotics.digital_twin.synchronized.v1", "owner": "BC-07", "consumers": "analytics,mission"},
    {"name": "SafetyViolationDetectedEvent", "schema": "robotics.safety.violation.detected.v1", "owner": "BC-09", "consumers": "notifications,audit,compliance"},
    {"name": "RobotCapabilityImprovedEvent", "schema": "robotics.robot.capability.improved.v1", "owner": "BC-03", "consumers": "analytics,lifecycle"},
)
COMMANDS = (
    "RegisterRobotCommand",
    "DeployRobotCommand",
    "CreateMissionCommand",
    "ExecuteAutonomousTaskCommand",
    "OptimizeFleetCommand",
    "SynchronizeDigitalTwinCommand",
)
QUERIES = (
    "GetRobotStatusQuery",
    "GetMissionStateQuery",
    "GetFleetPerformanceQuery",
    "GetPhysicalAIModelQuery",
    "GetSafetyStatusQuery",
)
MICROSERVICES = (
    {"id": "robot_identity_service", "bc": "BC-01", "api": "/robotics/domain/identity", "db": "robotics_*", "events": ("RobotRegisteredEvent",), "security": ("robotics.read",), "scaling": "identity_replicas"},
    {"id": "robot_lifecycle_service", "bc": "BC-02", "api": "/robotics/domain/lifecycle", "db": "robotics_*", "events": ("RobotActivatedEvent",), "security": ("robotics.write",), "scaling": "lifecycle_workers"},
    {"id": "autonomous_machine_service", "bc": "BC-03", "api": "/robotics/domain/autonomy", "db": "robotics_*", "events": ("AutonomousDecisionExecutedEvent",), "security": ("robotics.write",), "scaling": "autonomy_workers"},
    {"id": "physical_ai_service", "bc": "BC-04", "api": "/robotics/domain/physical-ai", "db": "robotics_*", "events": ("PhysicalAIUpdatedEvent",), "security": ("robotics.ai.infer",), "scaling": "physical_ai_workers"},
    {"id": "mission_service", "bc": "BC-05", "api": "/robotics/domain/missions", "db": "robotics_*", "events": ("MissionCompletedEvent",), "security": ("robotics.write",), "scaling": "mission_workers"},
    {"id": "fleet_intelligence_service", "bc": "BC-06", "api": "/robotics/domain/fleet", "db": "robotics_*", "events": ("FleetOptimizedEvent",), "security": ("robotics.write",), "scaling": "fleet_workers"},
    {"id": "digital_twin_service", "bc": "BC-07", "api": "/robotics/domain/twins", "db": "robotics_*", "events": ("DigitalTwinSynchronizedEvent",), "security": ("robotics.read",), "scaling": "twin_workers"},
    {"id": "human_collaboration_service", "bc": "BC-08", "api": "/robotics/domain/collaboration", "db": "robotics_*", "events": ("CollaborationStartedEvent",), "security": ("robotics.read",), "scaling": "hri_replicas"},
    {"id": "safety_governance_service", "bc": "BC-09", "api": "/robotics/domain/safety", "db": "robotics_*", "events": ("SafetyViolationDetectedEvent",), "security": ("robotics.admin",), "scaling": "safety_replicas"},
)
API_SURFACES = (
    "/api/v1/robotics/domain",
    "/api/v1/robotics/domain/strategy",
    "/api/v1/robotics/domain/bounded-contexts",
    "/api/v1/robotics/domain/aggregates",
    "/api/v1/robotics/domain/entities",
    "/api/v1/robotics/domain/value-objects",
    "/api/v1/robotics/domain/services",
    "/api/v1/robotics/domain/repositories",
    "/api/v1/robotics/domain/events",
    "/api/v1/robotics/domain/cqrs",
    "/api/v1/robotics/domain/microservices",
    "/api/v1/robotics/domain/integration",
    "/api/v1/robotics/domain/relationships",
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
    "never_replace_p216_b_strategy": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "ungated_physical_autonomy_strategy_forbidden": True,
    "opaque_safety_strategy_forbidden": True,
    "never_cross_context_aggregate_mutation": True,
    "never_peer_domain_imports": True,
}
INTEGRATION = {
    "present_required": True,
    "targets": ("p215z_quantum_master", "p214z_ai_master", "p213_analytics", "erp_platforms", "iot_platforms", "industrial_systems", "cloud_platforms"),
    "mechanisms": ("api_gateway", "event_bus", "streaming_platform", "knowledge_graph", "digital_twin_synchronization"),
    "via_p215_z": True,
    "via_p214_z": True,
    "via_p213": True,
}
DEPLOYMENT = {"present_required": True, "cloud_native": True, "components": ("domain_services_cluster", "bc_workers", "event_outbox", "domain_observability")}
TESTING = (
    "domain_strategy_testing",
    "bounded_context_isolation_testing",
    "aggregate_invariant_testing",
    "domain_service_testing",
    "repository_boundary_testing",
    "event_contract_testing",
    "cqrs_alignment_testing",
    "microservice_boundary_testing",
)
QUALITY_GATES_REJECT_IF = (
    "robotics_core_domain_is_missing",
    "supporting_domains_are_missing",
    "generic_domains_are_missing",
    "bounded_context_map_is_missing",
    "aggregates_are_missing",
    "entities_are_missing",
    "value_objects_are_missing",
    "domain_services_are_missing",
    "repository_boundaries_are_missing",
    "domain_events_are_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "api_first_architecture_is_missing",
    "cloud_native_deployment_is_missing",
    "sibling_robotics_bc",
    "replace_p216_foundation",
    "replace_p216_a_mission",
    "replace_p216_b_strategy",
    "cross_context_aggregate_mutation",
    "peer_domain_imports",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Robotics Domain Architecture Framework",
        "primary_capability": PRIMARY_CAPABILITY,
        "core_domain": CORE_DOMAIN_NAME,
        "builds_on_p216": True,
        "builds_on_p216_a": True,
        "builds_on_p216_b": True,
        "builds_on_p215_z": True,
        "builds_on_p214_z": True,
        "never_replace_p216_foundation": True,
        "never_replace_p216_a_mission": True,
        "never_replace_p216_b_strategy": True,
        "foundation_gate": FOUNDATION_GATE,
        "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE,
        "supreme_gate": SUPREME_GATE,
        "ai_gate": AI_GATE,
    }

def domain_strategy() -> dict[str, Any]:
    return {
        "present_required": True,
        "core_domain": CORE_DOMAIN_NAME,
        "primary_capability": PRIMARY_CAPABILITY,
        "supporting_domains": [dict(d) for d in SUPPORTING_DOMAINS],
        "supporting_count": len(SUPPORTING_DOMAINS),
        "generic_domains": list(GENERIC_DOMAINS),
        "generic_count": len(GENERIC_DOMAINS),
        "generic_reuse_core_only": True,
    }

def bounded_contexts() -> dict[str, Any]:
    return {"present_required": True, "contexts": [dict(c) for c in BOUNDED_CONTEXTS], "context_count": len(BOUNDED_CONTEXTS)}

def aggregates() -> dict[str, Any]:
    return {
        "present_required": True,
        "aggregates": [dict(a) for a in AGGREGATE_CATALOG],
        "aggregate_count": len(AGGREGATE_CATALOG),
        "rules": list(AGGREGATE_RULES),
    }

def entities() -> dict[str, Any]:
    items = sorted({e for a in AGGREGATE_CATALOG for e in a["entities"]})
    return {"present_required": True, "entities": items, "entity_count": len(items)}

def value_objects() -> dict[str, Any]:
    items = sorted({v for a in AGGREGATE_CATALOG for v in a["value_objects"]})
    return {"present_required": True, "value_objects": items, "value_object_count": len(items)}

def domain_services() -> dict[str, Any]:
    return {"present_required": True, "services": [dict(s) for s in DOMAIN_SERVICES], "service_count": len(DOMAIN_SERVICES)}

def repositories() -> dict[str, Any]:
    return {"present_required": True, "repositories": [dict(r) for r in REPOSITORIES], "repository_count": len(REPOSITORIES)}

def relationships() -> dict[str, Any]:
    return {"present_required": True, "relationships": [dict(r) for r in DOMAIN_RELATIONSHIPS], "relationship_count": len(DOMAIN_RELATIONSHIPS)}

def cqrs() -> dict[str, Any]:
    return {"commands": list(COMMANDS), "command_count": len(COMMANDS), "queries": list(QUERIES), "query_count": len(QUERIES)}

def events() -> dict[str, Any]:
    return {"core_events": [dict(e) for e in CORE_EVENTS], "core_event_count": len(CORE_EVENTS)}

def microservices() -> dict[str, Any]:
    return {"services": [dict(s) for s in MICROSERVICES], "service_count": len(MICROSERVICES)}

def integration() -> dict[str, Any]:
    return dict(INTEGRATION)

def api() -> dict[str, Any]:
    return {
        "surfaces": list(API_SURFACES),
        "styles": list(API_STYLES),
        "api_first_present_required": True,
        "foundation_gate_api": "/api/v1/robotics/foundation",
        "mission_gate_api": "/api/v1/robotics/mission",
        "strategy_gate_api": "/api/v1/robotics/strategy",
    }

def security() -> dict[str, Any]:
    return dict(SECURITY)

def deployment() -> dict[str, Any]:
    return dict(DEPLOYMENT)

def testing() -> dict[str, Any]:
    return {"suites": list(TESTING), "suite_count": len(TESTING)}

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p216_d": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "primary_capability": PRIMARY_CAPABILITY, "principle": PRIMARY_CAPABILITY,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "supreme_gate": SUPREME_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P216", "P216-A", "P216-B", "P215-Z", "P214-Z", "P213", "ADR-472", "ADR-473", "ADR-474"],
        "vision": vision_pack(),
        "domain_strategy": domain_strategy(),
        "bounded_contexts": bounded_contexts(),
        "aggregates": aggregates(),
        "entities": entities(),
        "value_objects": value_objects(),
        "domain_services": domain_services(),
        "repositories": repositories(),
        "relationships": relationships(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "integration": integration(),
        "api": api(),
        "security": security(),
        "deployment": deployment(),
        "testing": testing(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "robotics_core_domain_present_required": True,
        "supporting_domains_present_required": True,
        "generic_domains_present_required": True,
        "bounded_context_map_present_required": True,
        "aggregates_present_required": True,
        "entities_present_required": True,
        "value_objects_present_required": True,
        "domain_services_present_required": True,
        "repository_boundaries_present_required": True,
        "domain_events_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "cloud_native_deployment_present_required": True,
        "sibling_robotics_bc_forbidden": True,
        "never_replace_p216_foundation": True,
        "never_replace_p216_a_mission": True,
        "never_replace_p216_b_strategy": True,
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "ungated_physical_autonomy_strategy_forbidden": True,
        "opaque_safety_strategy_forbidden": True,
        "never_cross_context_aggregate_mutation": True,
        "never_peer_domain_imports": True,
        "builds_on_p216": True, "builds_on_p216_a": True, "builds_on_p216_b": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p215_z": True, "via_p214_z": True, "via_p213": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "api_prefix": f"{API_PREFIX}/domain",
        "forbidden_sibling_bc": [
            "robotics_domain_platform",
            "robotics_ddd_platform",
            "cyber_physical_domain_platform",
        ],
        "foundation_for_p216_d": True,
    }

def domain_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /robotics/domain",
        "GET /robotics/domain/strategy",
        "GET /robotics/domain/bounded-contexts",
        "GET /robotics/domain/aggregates",
        "GET /robotics/domain/entities",
        "GET /robotics/domain/value-objects",
        "GET /robotics/domain/services",
        "GET /robotics/domain/repositories",
        "GET /robotics/domain/events",
        "GET /robotics/domain/cqrs",
        "GET /robotics/domain/microservices",
        "GET /robotics/domain/integration",
        "GET /robotics/domain/relationships",
        "GET /robotics/domain/readiness",
    ], "foundation_gate_routes": ["GET /robotics/foundation", "GET /robotics/foundation/readiness"],
       "mission_gate_routes": ["GET /robotics/mission", "GET /robotics/mission/readiness"],
       "strategy_gate_routes": ["GET /robotics/strategy", "GET /robotics/strategy/readiness"]}
