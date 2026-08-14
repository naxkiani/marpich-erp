"""P216-E Enterprise Physical AI Engine — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P216-E"
ADR = 477
SOR = "robotics"
API_PREFIX = "/api/v1/robotics"
PRODUCT = "Enterprise Robotics Physical AI Engine, Robot Perception, Cognitive Robotics & Autonomous Decision Platform"
CAPABILITY = "CAP-PLT-RB-001"
PHYSICAL_AI_VISION = (
    "Physical AI enables robots to perceive, understand, reason, decide and safely act "
    "within dynamic real-world environments."
)
MISSION = (
    "Provide every autonomous machine with human-level environmental understanding, "
    "context awareness and safe autonomous behaviour."
)
FABRIC = "meos_physical_ai_intelligence_fabric"
FOUNDATION_GATE = "P216"
MISSION_GATE = "P216-A"
STRATEGY_GATE = "P216-B"
DOMAIN_GATE = "P216-C"
RUNTIME_GATE = "P216-D"
SUPREME_GATE = "P215-Z"
AI_GATE = "P214-Z"
CORE_DOMAIN = "physical_ai_intelligence_management"
AGGREGATE = "PhysicalAIAggregate"

SUPPORTING_DOMAINS = (
    "robot_perception",
    "cognitive_robotics",
    "spatial_intelligence",
    "world_modeling",
    "motion_intelligence",
    "robot_memory",
    "decision_intelligence",
    "learning_intelligence",
    "safety_intelligence",
    "human_collaboration",
)
ENTITIES = (
    "RobotBrain",
    "PerceptionModel",
    "WorldModel",
    "DecisionModel",
    "MotionPlanner",
    "RobotMemory",
    "LearningPolicy",
    "ReasoningSession",
    "SafetyController",
    "ContextState",
)
VALUE_OBJECTS = (
    "PerceptionConfidence",
    "SpatialLocation",
    "EnvironmentState",
    "DecisionConfidence",
    "RiskLevel",
    "MissionContext",
    "LearningScore",
    "SafetyMargin",
    "InferenceLatency",
)
BOUNDED_CONTEXTS = (
    {"id": "BC-01", "name": "Robot Perception Context", "responsibilities": ("sensor_fusion", "object_detection", "scene_understanding", "environmental_perception")},
    {"id": "BC-02", "name": "Spatial Intelligence Context", "responsibilities": ("mapping", "localization", "navigation", "spatial_reasoning")},
    {"id": "BC-03", "name": "Physical AI Context", "responsibilities": ("physical_reasoning", "environmental_intelligence", "context_understanding", "behaviour_planning")},
    {"id": "BC-04", "name": "Cognitive Robotics Context", "responsibilities": ("goal_reasoning", "task_planning", "symbolic_reasoning", "neuro_symbolic_ai")},
    {"id": "BC-05", "name": "Autonomous Decision Context", "responsibilities": ("decision_generation", "policy_execution", "action_prioritization", "safe_execution")},
    {"id": "BC-06", "name": "Robot Learning Context", "responsibilities": ("online_learning", "reinforcement_learning", "behaviour_optimisation", "experience_replay")},
    {"id": "BC-07", "name": "Robot Memory Context", "responsibilities": ("episodic_memory", "semantic_memory", "procedural_memory", "long_term_knowledge")},
)
PERCEPTION_PLATFORM = {
    "present_required": True,
    "engine": "meos_robot_perception_engine",
    "components": (
        "vision_intelligence_engine",
        "sensor_fusion_engine",
        "audio_intelligence_engine",
        "lidar_intelligence_engine",
        "radar_intelligence_engine",
        "depth_perception_engine",
        "thermal_perception_engine",
        "environmental_understanding_engine",
    ),
    "capabilities": (
        "multi_modal_perception",
        "object_detection",
        "object_tracking",
        "human_recognition",
        "gesture_recognition",
        "hazard_detection",
        "terrain_understanding",
        "dynamic_environment_modelling",
    ),
}
PHYSICAL_AI_ENGINE = {
    "present_required": True,
    "core": "meos_physical_ai_core",
    "capabilities": (
        "physical_reasoning",
        "object_affordance_understanding",
        "cause_effect_reasoning",
        "physics_awareness",
        "temporal_reasoning",
        "context_understanding",
        "adaptive_behaviour",
        "embodied_intelligence",
    ),
    "ai_models_via_p214z": (
        "foundation_models",
        "vision_language_models",
        "action_models",
        "planning_models",
        "robot_world_models",
        "physics_models",
        "behaviour_models",
    ),
}
COGNITIVE_PLATFORM = {
    "present_required": True,
    "engine": "meos_cognitive_robotics_engine",
    "components": (
        "goal_manager",
        "reasoning_engine",
        "task_planner",
        "policy_engine_port",
        "behaviour_tree_engine",
        "executive_controller",
        "knowledge_integration_engine",
        "decision_validator",
    ),
    "capabilities": (
        "goal_decomposition",
        "multi_step_reasoning",
        "constraint_reasoning",
        "hierarchical_planning",
        "intent_recognition",
        "context_adaptation",
        "autonomous_execution",
    ),
}
DECISION_PLATFORM = {
    "present_required": True,
    "engine": "meos_autonomous_decision_engine",
    "pipeline": (
        "situation_assessment",
        "risk_evaluation",
        "goal_analysis",
        "alternative_generation",
        "policy_validation",
        "action_selection",
        "execution_approval",
        "physical_execution",
        "feedback_learning",
    ),
    "decision_types": ("reactive", "predictive", "collaborative", "strategic", "emergency", "safety_critical"),
}
WORLD_MODEL = {
    "present_required": True,
    "platform": "meos_world_model_platform",
    "components": (
        "semantic_world_model",
        "spatial_world_model",
        "temporal_world_model",
        "operational_world_model",
        "mission_world_model",
        "digital_twin_synchronization",
    ),
}
ROBOT_MEMORY = {
    "present_required": True,
    "types": (
        "working_memory",
        "short_term_memory",
        "long_term_memory",
        "experience_memory",
        "knowledge_memory",
        "mission_memory",
    ),
}
KNOWLEDGE_GRAPH = {
    "present_required": True,
    "graph": "meos_robotics_knowledge_graph",
    "nodes": ("robots", "humans", "objects", "environments", "tasks", "missions", "capabilities", "policies", "sensors", "actions", "world_states"),
    "relationships": ("observes", "interacts_with", "plans", "controls", "learns_from", "depends_on", "avoids", "collaborates_with", "optimizes"),
    "enables": ("contextual_reasoning", "semantic_navigation", "enterprise_cognition", "cross_domain_intelligence"),
}
DIGITAL_TWIN = {
    "present_required": True,
    "platform": "physical_ai_digital_twin_platform",
    "represents": ("robot_state", "ai_state", "perception_state", "decision_state", "environment_state", "mission_state", "learning_state"),
    "capabilities": ("simulation", "scenario_testing", "decision_validation", "predictive_behaviour", "continuous_optimisation"),
}
RESPONSIBLE_AI = {
    "present_required": True,
    "framework": "meos_responsible_physical_ai_framework",
    "includes": (
        "ai_explainability",
        "decision_traceability",
        "safety_envelopes",
        "human_override",
        "ethical_behaviour_policies",
        "operational_constraints",
        "continuous_validation",
        "model_governance",
        "bias_monitoring",
        "risk_scoring",
    ),
    "never_opaque_unexplainable_decisions": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
}
COMMANDS = (
    "StartPerceptionCommand",
    "UpdateWorldModelCommand",
    "GenerateDecisionCommand",
    "ExecuteActionCommand",
    "LearnFromExperienceCommand",
    "ValidateSafetyCommand",
)
QUERIES = (
    "GetRobotPerceptionQuery",
    "GetWorldStateQuery",
    "GetDecisionHistoryQuery",
    "GetLearningStateQuery",
    "GetEnvironmentMapQuery",
    "GetRobotMemoryQuery",
)
CORE_EVENTS = (
    {"name": "PerceptionStartedEvent", "schema": "robotics.physical_ai.perception.started.v1", "owner": "BC-01", "consumers": "audit,world_model,observability"},
    {"name": "ObjectDetectedEvent", "schema": "robotics.physical_ai.object.detected.v1", "owner": "BC-01", "consumers": "spatial,decision,audit"},
    {"name": "EnvironmentMappedEvent", "schema": "robotics.physical_ai.environment.mapped.v1", "owner": "BC-02", "consumers": "world_model,twin,analytics"},
    {"name": "DecisionApprovedEvent", "schema": "robotics.physical_ai.decision.approved.v1", "owner": "BC-05", "consumers": "audit,runtime,workflow"},
    {"name": "ActionExecutedEvent", "schema": "robotics.physical_ai.action.executed.v1", "owner": "BC-05", "consumers": "audit,learning,analytics"},
    {"name": "BehaviourAdaptedEvent", "schema": "robotics.physical_ai.behaviour.adapted.v1", "owner": "BC-06", "consumers": "analytics,memory"},
    {"name": "LearningCompletedEvent", "schema": "robotics.physical_ai.learning.completed.v1", "owner": "BC-06", "consumers": "ai,knowledge_graph,audit"},
    {"name": "SafetyOverrideActivatedEvent", "schema": "robotics.physical_ai.safety.override.activated.v1", "owner": "BC-05", "consumers": "notifications,audit,compliance"},
)
MICROSERVICES = (
    {"id": "robot_perception_service", "bc": "BC-01", "api": "/robotics/physical-ai/perception", "db": "robotics_*", "events": ("PerceptionStartedEvent", "ObjectDetectedEvent"), "security": ("robotics.ai.infer",), "scaling": "perception_workers", "responsibility": "Multi-modal robot perception"},
    {"id": "sensor_fusion_service", "bc": "BC-01", "api": "/robotics/physical-ai/fusion", "db": "robotics_*", "events": ("ObjectDetectedEvent",), "security": ("robotics.ai.infer",), "scaling": "fusion_workers", "responsibility": "Sensor fusion pipelines"},
    {"id": "physical_ai_service", "bc": "BC-03", "api": "/robotics/physical-ai", "db": "robotics_*", "events": ("DecisionApprovedEvent",), "security": ("robotics.ai.infer",), "scaling": "physical_ai_workers", "responsibility": "Physical reasoning via P214-Z ACL"},
    {"id": "world_model_service", "bc": "BC-02", "api": "/robotics/physical-ai/world-model", "db": "robotics_*", "events": ("EnvironmentMappedEvent",), "security": ("robotics.read",), "scaling": "world_model_workers", "responsibility": "Semantic/spatial/temporal world models"},
    {"id": "decision_intelligence_service", "bc": "BC-05", "api": "/robotics/physical-ai/decisions", "db": "robotics_*", "events": ("DecisionApprovedEvent", "ActionExecutedEvent"), "security": ("robotics.write",), "scaling": "decision_workers", "responsibility": "Autonomous decision pipeline"},
    {"id": "motion_planning_service", "bc": "BC-03", "api": "/robotics/physical-ai/motion", "db": "robotics_*", "events": ("ActionExecutedEvent",), "security": ("robotics.write",), "scaling": "motion_workers", "responsibility": "Motion intelligence planning"},
    {"id": "robot_memory_service", "bc": "BC-07", "api": "/robotics/physical-ai/memory", "db": "robotics_*", "events": ("LearningCompletedEvent",), "security": ("robotics.read",), "scaling": "memory_workers", "responsibility": "Episodic/semantic/procedural memory"},
    {"id": "learning_intelligence_service", "bc": "BC-06", "api": "/robotics/physical-ai/learning", "db": "robotics_*", "events": ("BehaviourAdaptedEvent", "LearningCompletedEvent"), "security": ("robotics.ai.infer",), "scaling": "learning_workers", "responsibility": "Online and reinforcement learning intents"},
    {"id": "knowledge_graph_service", "bc": "BC-07", "api": "/robotics/physical-ai/knowledge-graph", "db": "robotics_*", "events": ("LearningCompletedEvent",), "security": ("robotics.read",), "scaling": "kg_workers", "responsibility": "Robotics knowledge graph projections"},
    {"id": "safety_decision_service", "bc": "BC-05", "api": "/robotics/physical-ai/safety", "db": "robotics_*", "events": ("SafetyOverrideActivatedEvent",), "security": ("robotics.admin",), "scaling": "safety_replicas", "responsibility": "Safety envelopes and overrides"},
)
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p214z_ai_master",
        "p215z_quantum_supreme",
        "p216d_robotics_os",
        "enterprise_digital_twin",
        "enterprise_knowledge_graph",
        "enterprise_analytics",
        "industrial_iot",
        "erp_mes",
    ),
    "mechanisms": ("ai_inference_apis", "decision_apis", "event_contracts", "digital_twin_synchronization", "robot_cognition_interfaces"),
    "via_p214_z": True,
    "via_p215_z": True,
    "via_p216_d": True,
    "via_p213": True,
}
DEPLOYMENT = {
    "present_required": True,
    "model": "hybrid_physical_ai_infrastructure",
    "includes": (
        "cloud_ai_cluster",
        "edge_ai_runtime",
        "gpu_infrastructure",
        "robot_ai_runtime",
        "knowledge_graph_cluster",
        "digital_twin_platform",
        "observability_platform",
        "security_infrastructure",
        "inference_gateways",
        "model_registry_via_ai_platform",
    ),
    "cloud_native": True,
    "edge_native": True,
}
TESTING = (
    "perception_testing",
    "object_recognition_testing",
    "spatial_reasoning_testing",
    "decision_accuracy_testing",
    "motion_planning_testing",
    "safety_validation_testing",
    "simulation_testing",
    "digital_twin_testing",
    "learning_validation",
    "stress_testing",
    "latency_testing",
    "explainability_validation",
)
SECURITY = {
    "present_required": True,
    "zero_trust": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "physical_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
    "never_opaque_unexplainable_decisions": True,
    "never_replace_p216_foundation": True,
    "never_replace_p216_a_mission": True,
    "never_replace_p216_b_strategy": True,
    "never_replace_p216_c_domain": True,
    "never_replace_p216_d_runtime": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "ungated_physical_autonomy_strategy_forbidden": True,
    "opaque_safety_strategy_forbidden": True,
}
API_SURFACES = (
    "/api/v1/robotics/physical-ai",
    "/api/v1/robotics/physical-ai/vision",
    "/api/v1/robotics/physical-ai/domain",
    "/api/v1/robotics/physical-ai/bounded-contexts",
    "/api/v1/robotics/physical-ai/perception",
    "/api/v1/robotics/physical-ai/engine",
    "/api/v1/robotics/physical-ai/cognitive",
    "/api/v1/robotics/physical-ai/decisions",
    "/api/v1/robotics/physical-ai/world-model",
    "/api/v1/robotics/physical-ai/memory",
    "/api/v1/robotics/physical-ai/knowledge-graph",
    "/api/v1/robotics/physical-ai/digital-twin",
    "/api/v1/robotics/physical-ai/responsible-ai",
    "/api/v1/robotics/physical-ai/cqrs",
    "/api/v1/robotics/physical-ai/events",
    "/api/v1/robotics/physical-ai/microservices",
    "/api/v1/robotics/physical-ai/integration",
    "/api/v1/robotics/physical-ai/deployment",
    "/api/v1/robotics/physical-ai/testing",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
QUALITY_GATES_REJECT_IF = (
    "physical_ai_engine_is_missing",
    "robot_perception_platform_is_missing",
    "cognitive_robotics_platform_is_missing",
    "autonomous_decision_platform_is_missing",
    "world_model_architecture_is_missing",
    "robot_memory_architecture_is_missing",
    "learning_platform_is_missing",
    "knowledge_graph_integration_is_missing",
    "digital_twin_integration_is_missing",
    "safety_and_responsible_ai_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "cloud_edge_ai_deployment_is_missing",
    "testing_architecture_is_missing",
    "sibling_robotics_bc",
    "replace_p216_d_runtime",
    "module_local_llm",
    "opaque_unexplainable_decisions",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Physical AI Intelligence Fabric",
        "physical_ai_vision": PHYSICAL_AI_VISION,
        "mission": MISSION,
        "builds_on_p216": True,
        "builds_on_p216_a": True,
        "builds_on_p216_b": True,
        "builds_on_p216_c": True,
        "builds_on_p216_d": True,
        "builds_on_p215_z": True,
        "builds_on_p214_z": True,
        "never_replace_p216_d_runtime": True,
        "foundation_gate": FOUNDATION_GATE,
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

def perception() -> dict[str, Any]:
    return dict(PERCEPTION_PLATFORM)

def engine() -> dict[str, Any]:
    return dict(PHYSICAL_AI_ENGINE)

def cognitive() -> dict[str, Any]:
    return dict(COGNITIVE_PLATFORM)

def decisions() -> dict[str, Any]:
    return dict(DECISION_PLATFORM)

def world_model() -> dict[str, Any]:
    return dict(WORLD_MODEL)

def memory() -> dict[str, Any]:
    return dict(ROBOT_MEMORY)

def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH)

def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN)

def responsible_ai() -> dict[str, Any]:
    return dict(RESPONSIBLE_AI)

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

def security() -> dict[str, Any]:
    return dict(SECURITY)

def api() -> dict[str, Any]:
    return {
        "surfaces": list(API_SURFACES),
        "styles": list(API_STYLES),
        "api_first_present_required": True,
        "runtime_gate_api": "/api/v1/robotics/runtime",
        "ai_gate_api": "/api/v1/ai",
    }

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p216_f": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "physical_ai_vision": PHYSICAL_AI_VISION, "mission": MISSION, "principle": PHYSICAL_AI_VISION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE, "runtime_gate": RUNTIME_GATE,
        "supreme_gate": SUPREME_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P216", "P216-A", "P216-B", "P216-C", "P216-D", "P215-Z", "P214-Z", "P213", "ADR-472", "ADR-473", "ADR-474", "ADR-475", "ADR-476"],
        "vision": vision_pack(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "perception": perception(),
        "engine": engine(),
        "cognitive": cognitive(),
        "decisions": decisions(),
        "world_model": world_model(),
        "memory": memory(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "responsible_ai": responsible_ai(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "integration": integration(),
        "deployment": deployment(),
        "testing": testing(),
        "security": security(),
        "api": api(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "physical_ai_engine_present_required": True,
        "robot_perception_platform_present_required": True,
        "cognitive_robotics_platform_present_required": True,
        "autonomous_decision_platform_present_required": True,
        "world_model_architecture_present_required": True,
        "robot_memory_architecture_present_required": True,
        "learning_platform_present_required": True,
        "knowledge_graph_integration_present_required": True,
        "digital_twin_integration_present_required": True,
        "safety_and_responsible_ai_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "cloud_edge_ai_deployment_present_required": True,
        "testing_architecture_present_required": True,
        "sibling_robotics_bc_forbidden": True,
        "never_replace_p216_foundation": True,
        "never_replace_p216_a_mission": True,
        "never_replace_p216_b_strategy": True,
        "never_replace_p216_c_domain": True,
        "never_replace_p216_d_runtime": True,
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "physical_ai_via_p214z_acl_only": True,
        "no_module_local_llm": True,
        "never_opaque_unexplainable_decisions": True,
        "ungated_physical_autonomy_strategy_forbidden": True,
        "opaque_safety_strategy_forbidden": True,
        "builds_on_p216": True, "builds_on_p216_a": True, "builds_on_p216_b": True,
        "builds_on_p216_c": True, "builds_on_p216_d": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p215_z": True, "via_p214_z": True, "via_p213": True, "via_p216_d": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "api_prefix": f"{API_PREFIX}/physical-ai",
        "forbidden_sibling_bc": [
            "physical_ai_platform",
            "robot_perception_platform",
            "cognitive_robotics_platform",
        ],
        "foundation_for_p216_f": True,
    }

def physical_ai_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /robotics/physical-ai",
        "GET /robotics/physical-ai/vision",
        "GET /robotics/physical-ai/domain",
        "GET /robotics/physical-ai/bounded-contexts",
        "GET /robotics/physical-ai/perception",
        "GET /robotics/physical-ai/engine",
        "GET /robotics/physical-ai/cognitive",
        "GET /robotics/physical-ai/decisions",
        "GET /robotics/physical-ai/world-model",
        "GET /robotics/physical-ai/memory",
        "GET /robotics/physical-ai/knowledge-graph",
        "GET /robotics/physical-ai/digital-twin",
        "GET /robotics/physical-ai/responsible-ai",
        "GET /robotics/physical-ai/cqrs",
        "GET /robotics/physical-ai/events",
        "GET /robotics/physical-ai/microservices",
        "GET /robotics/physical-ai/integration",
        "GET /robotics/physical-ai/deployment",
        "GET /robotics/physical-ai/testing",
        "GET /robotics/physical-ai/readiness",
    ], "runtime_gate_routes": ["GET /robotics/runtime", "GET /robotics/runtime/readiness"]}
