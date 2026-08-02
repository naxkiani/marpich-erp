"""P218-E Enterprise Space Intelligence Space AI Engine — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P218-E"
ADR = 531
SOR = "space"
API_PREFIX = "/api/v1/space"
PRODUCT = "Enterprise Space Intelligence Space AI Engine, Mission Intelligence, Autonomous Decision Systems, Space Cognitive Platform & MEOS Space AI Intelligence Core"
CAPABILITY = "CAP-PLT-SP-001"
SPACE_AI_MISSION = (
    "Build the enterprise cognitive engine capable of understanding, reasoning, predicting and "
    "autonomously supporting every space mission, orbital system and future space civilization ecosystem."
)
SPACE_AI_VISION = (
    "Transform space operations from telemetry-driven control into an intelligence-driven, "
    "explainable, human-supervised cognitive mission ecosystem."
)
FABRIC = "meos_space_ai_intelligence_fabric"
FOUNDATION_GATE = "P218"
MISSION_GATE = "P218-A"
STRATEGY_GATE = "P218-B"
DOMAIN_GATE = "P218-C"
INFRASTRUCTURE_GATE = "P218-D"
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

ARCHITECTURE_LAYERS = (
    {"id": "L01", "name": "Knowledge Layer", "components": ("enterprise_knowledge_graph", "mission_knowledge_base", "scientific_repository", "telemetry_knowledge_store", "orbital_knowledge_graph", "mission_memory", "operational_memory")},
    {"id": "L02", "name": "Foundation Intelligence Layer", "components": ("space_foundation_model", "mission_language_model", "scientific_reasoning_model", "orbital_intelligence_model", "navigation_intelligence_model", "mission_planning_model", "risk_intelligence_model")},
    {"id": "L03", "name": "Cognitive Intelligence Layer", "components": ("reasoning_engine", "decision_engine", "planning_engine", "prediction_engine", "simulation_intelligence", "learning_engine", "optimization_engine")},
    {"id": "L04", "name": "Agent Intelligence Layer", "components": ("mission_agent", "navigation_agent", "scientific_agent", "operations_agent", "security_agent", "infrastructure_agent", "mission_commander_agent", "digital_twin_agent")},
    {"id": "L05", "name": "Execution Layer", "components": ("recommendation_engine", "decision_orchestrator", "mission_automation", "workflow_engine", "mission_command_interface", "human_approval_layer")},
)
FOUNDATION_MODELS = (
    {"id": "MODEL-01", "name": "Mission Foundation Model", "purpose": ("mission_planning", "mission_execution", "mission_optimization"), "training_data": ("mission_history", "telemetry", "procedures", "orbital_knowledge")},
    {"id": "MODEL-02", "name": "Orbital Intelligence Model", "purpose": ("orbital_prediction", "collision_avoidance", "trajectory_optimisation")},
    {"id": "MODEL-03", "name": "Scientific Discovery Model", "purpose": ("pattern_discovery", "scientific_reasoning", "experiment_optimisation")},
    {"id": "MODEL-04", "name": "Space Operations Model", "purpose": ("operations_intelligence", "infrastructure_optimisation", "mission_support")},
    {"id": "MODEL-05", "name": "Space Cognitive Model", "purpose": ("enterprise_reasoning", "long_term_planning", "strategic_intelligence")},
)
SPACE_AI_ENGINE = {
    "present_required": True,
    "engine": "meos_space_ai_engine",
    "components": (
        {"id": "mission_reasoning_engine", "capabilities": ("mission_inference", "procedure_reasoning", "timeline_optimisation")},
        {"id": "orbital_prediction_engine", "capabilities": ("trajectory_forecast", "collision_risk", "fuel_estimation")},
        {"id": "scientific_discovery_engine", "capabilities": ("pattern_discovery", "hypothesis_support", "experiment_planning")},
        {"id": "decision_recommendation_engine", "capabilities": ("risk_scoring", "alternative_strategies", "recovery_planning")},
    ),
}
MISSION_INTELLIGENCE = {
    "present_required": True,
    "platform": "meos_mission_intelligence_platform",
    "capabilities": (
        "mission_planning_intelligence", "mission_risk_assessment", "mission_timeline_optimization",
        "mission_readiness_assessment", "mission_success_prediction", "mission_resource_optimization",
        "mission_cost_optimization", "mission_knowledge_assistance",
    ),
    "decision_services": (
        "mission_approval_recommendation", "risk_scoring", "resource_allocation",
        "crew_support", "mission_recovery_planning", "alternative_strategy_generation",
    ),
}
AUTONOMOUS_DECISION = {
    "present_required": True,
    "platform": "meos_autonomous_decision_system",
    "categories": (
        "strategic", "operational", "scientific", "emergency",
        "navigation", "infrastructure", "resource", "security",
    ),
    "pipeline": ("observe", "understand", "reason", "predict", "recommend", "approve", "execute", "learn"),
    "oversight_modes": (
        "human_approval_required", "human_review_optional", "fully_autonomous_gated",
        "emergency_override", "simulation_only",
    ),
    "never_ungated_autonomous_mission_strategy": True,
    "never_skip_human_mission_oversight_strategy": True,
}
COGNITIVE_PLATFORM = {
    "present_required": True,
    "platform": "meos_space_cognitive_platform",
    "functions": ("reasoning", "memory", "planning", "learning", "reflection", "simulation", "explanation", "adaptation"),
    "reasoning_types": (
        "logical", "scientific", "mission", "probabilistic", "causal", "strategic", "multi_agent",
    ),
}
SPACE_AGENTS = (
    {"id": "mission_planning_agent", "responsibilities": ("plan_generation", "constraint_checking")},
    {"id": "mission_commander_agent", "responsibilities": ("mission_orchestration", "escalation")},
    {"id": "orbital_intelligence_agent", "responsibilities": ("orbit_awareness", "conjunction_support")},
    {"id": "satellite_intelligence_agent", "responsibilities": ("fleet_health", "payload_ops_support")},
    {"id": "scientific_discovery_agent", "responsibilities": ("experiment_support", "pattern_discovery")},
    {"id": "space_weather_agent", "responsibilities": ("weather_risk", "comms_impact")},
    {"id": "navigation_agent", "responsibilities": ("guidance", "trajectory_advice")},
    {"id": "ground_operations_agent", "responsibilities": ("ground_segment_support", "schedule_advice")},
    {"id": "mission_safety_agent", "responsibilities": ("safety_constraints", "safe_mode_advice")},
    {"id": "infrastructure_agent", "responsibilities": ("infra_health", "capacity_advice")},
    {"id": "resource_optimizer_agent", "responsibilities": ("fuel", "power", "bandwidth")},
    {"id": "digital_twin_agent", "responsibilities": ("scenario_sim", "decision_validation")},
)
PREDICTIVE_INTELLIGENCE = {
    "present_required": True,
    "domains": (
        "mission_success", "equipment_failure", "satellite_health", "orbital_collision",
        "mission_duration", "fuel_consumption", "communication_failure", "space_weather",
        "mission_cost", "scientific_opportunity",
    ),
    "outputs": ("confidence_score", "risk_level", "mitigation_plan", "recommended_actions"),
}
BOUNDED_CONTEXTS = (
    {"id": "BC-AI-01", "name": "AI Model Management"},
    {"id": "BC-AI-02", "name": "Inference"},
    {"id": "BC-AI-03", "name": "Mission Intelligence"},
    {"id": "BC-AI-04", "name": "Decision Intelligence"},
    {"id": "BC-AI-05", "name": "Prediction Intelligence"},
    {"id": "BC-AI-06", "name": "Learning Intelligence"},
    {"id": "BC-AI-07", "name": "Agent Management"},
    {"id": "BC-AI-08", "name": "Model Governance"},
)
KNOWLEDGE_GRAPH = {
    "present_required": True,
    "platform": "meos_space_knowledge_graph",
    "capabilities": ("semantic_search", "context_retrieval", "reasoning", "mission_memory", "scientific_knowledge_discovery"),
}
DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_space_digital_twin",
    "capabilities": ("scenario_simulation", "mission_forecasting", "failure_simulation", "decision_validation", "mission_replay"),
}
MODEL_LIFECYCLE = {
    "present_required": True,
    "platform": "meos_space_ai_model_operations_platform",
    "lifecycle": ("model_discovery", "data_preparation", "training", "validation", "deployment", "monitoring", "continuous_learning"),
    "via_p214_z": True,
}
GOVERNANCE = {
    "present_required": True,
    "framework": "meos_responsible_space_ai_framework",
    "areas": ("ai_ethics", "bias_detection", "model_validation", "explainability", "traceability", "human_accountability", "safety_constraints", "alignment_policies"),
    "monitoring": ("model_drift", "prediction_accuracy", "decision_accuracy", "inference_latency", "hallucination_detection", "agent_behaviour", "policy_compliance"),
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "never_opaque_unexplainable_decisions": True,
    "never_ungated_autonomous_mission_strategy": True,
    "never_skip_human_mission_oversight_strategy": True,
}
SECURITY = {
    "present_required": True,
    "domains": ("model_security", "inference_security", "mission_decision_security", "agent_security", "training_data_protection"),
    "controls": ("encryption", "identity_management", "access_policies", "ai_threat_detection", "secure_model_deployment"),
    "zero_trust": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
    "never_opaque_unexplainable_decisions": True,
    "never_replace_p218_foundation": True,
    "never_replace_p218_a_mission": True,
    "never_replace_p218_b_strategy": True,
    "never_replace_p218_c_domain": True,
    "never_replace_p218_d_infrastructure": True,
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
}
INTEGRATION = {
    "present_required": True,
    "targets": ("p214z_ai_master", "p215z_quantum_supreme", "p216z_robotics_supreme", "p217z_bio_nexus", "p218d_space_infrastructure", "meos_knowledge_graph", "meos_digital_twin", "policy_engine", "workflow", "audit"),
    "mechanisms": ("api_gateway", "event_bus", "acl_peer_ids_only", "inference_intents_not_models"),
    "via_p214_z": True, "via_p215_z": True, "via_p216_z": True, "via_p217": True, "via_p218_d": True,
}
DEPLOYMENT = {
    "present_required": True,
    "environments": ("mission_ai_environment", "scientific_ai_environment", "enterprise_space_ai_environment", "simulation_only_environment"),
    "cloud_native": True,
}
ROADMAP_PHASES = (
    {"phase": 1, "name": "AI Foundation", "deliverables": ("foundation_models", "knowledge_graph", "inference_platform", "model_registry")},
    {"phase": 2, "name": "Mission Intelligence", "deliverables": ("mission_ai", "decision_engine", "prediction_services", "optimization_platform")},
    {"phase": 3, "name": "Agentic Intelligence", "deliverables": ("multi_agent_platform", "autonomous_decision_system", "mission_copilot", "digital_twin_intelligence")},
    {"phase": 4, "name": "Space Cognitive Core", "deliverables": ("enterprise_cognitive_platform", "continuous_learning", "civilization_scale_intelligence", "meos_space_ai_intelligence_core")},
)
COMMANDS = (
    "RegisterSpaceFoundationModelCommand", "RequestSpaceInferenceCommand", "GenerateMissionPredictionCommand",
    "ProposeMissionDecisionCommand", "ActivateSpaceAgentCommand", "CompleteLearningCycleCommand",
)
QUERIES = (
    "GetSpaceAiPlatformQuery", "GetFoundationModelQuery", "GetMissionIntelligenceQuery",
    "GetDecisionStatusQuery", "GetAgentStatusQuery",
)
CORE_EVENTS = (
    {"name": "ModelRegisteredEvent", "schema": "space.ai.model.registered.v1", "owner": "BC-AI-01", "consumers": "audit,search,ai"},
    {"name": "ModelTrainedEvent", "schema": "space.ai.model.trained.v1", "owner": "BC-AI-01", "consumers": "audit,mlops"},
    {"name": "InferenceRequestedEvent", "schema": "space.ai.inference.requested.v1", "owner": "BC-AI-02", "consumers": "audit,p214z"},
    {"name": "InferenceCompletedEvent", "schema": "space.ai.inference.completed.v1", "owner": "BC-AI-02", "consumers": "audit,analytics,decision"},
    {"name": "PredictionGeneratedEvent", "schema": "space.ai.prediction.generated.v1", "owner": "BC-AI-05", "consumers": "audit,analytics,notifications"},
    {"name": "RecommendationCreatedEvent", "schema": "space.ai.recommendation.created.v1", "owner": "BC-AI-04", "consumers": "audit,workflow"},
    {"name": "DecisionApprovedEvent", "schema": "space.ai.decision.approved.v1", "owner": "BC-AI-04", "consumers": "audit,workflow,mission"},
    {"name": "DecisionExecutedEvent", "schema": "space.ai.decision.executed.v1", "owner": "BC-AI-04", "consumers": "audit,analytics,mission"},
    {"name": "AgentActivatedEvent", "schema": "space.ai.agent.activated.v1", "owner": "BC-AI-07", "consumers": "audit,workflow"},
    {"name": "LearningCycleCompletedEvent", "schema": "space.ai.learning.completed.v1", "owner": "BC-AI-06", "consumers": "audit,mlops,analytics"},
)
MICROSERVICES = (
    {"id": "space_ai_platform_service", "api": "/space/space-ai", "db": "space_*", "events": ("ModelRegisteredEvent",), "security": ("space.read",), "scaling": "space_ai_replicas"},
    {"id": "foundation_model_service", "api": "/space/space-ai/foundation-models", "db": "space_*", "events": ("ModelRegisteredEvent", "ModelTrainedEvent"), "security": ("space.ai.infer",), "scaling": "model_workers"},
    {"id": "space_ai_engine_service", "api": "/space/space-ai/engine", "db": "space_*", "events": ("InferenceCompletedEvent",), "security": ("space.ai.infer",), "scaling": "engine_workers"},
    {"id": "mission_intelligence_service", "api": "/space/space-ai/mission-intelligence", "db": "space_*", "events": ("PredictionGeneratedEvent",), "security": ("space.ai.infer",), "scaling": "mission_intel_workers"},
    {"id": "decision_service", "api": "/space/space-ai/decision", "db": "space_*", "events": ("RecommendationCreatedEvent", "DecisionApprovedEvent"), "security": ("space.write",), "scaling": "decision_workers"},
    {"id": "agent_service", "api": "/space/space-ai/agents", "db": "space_*", "events": ("AgentActivatedEvent",), "security": ("space.write",), "scaling": "agent_workers"},
    {"id": "knowledge_graph_service", "api": "/space/space-ai/knowledge-graph", "db": "space_*", "events": ("InferenceCompletedEvent",), "security": ("space.read",), "scaling": "kg_workers"},
    {"id": "model_lifecycle_service", "api": "/space/space-ai/lifecycle", "db": "space_*", "events": ("LearningCycleCompletedEvent",), "security": ("space.admin",), "scaling": "mlops_workers"},
    {"id": "space_ai_governance_service", "api": "/space/space-ai/governance", "db": "space_*", "events": ("DecisionApprovedEvent",), "security": ("space.admin",), "scaling": "governance_replicas"},
    {"id": "space_ai_security_service", "api": "/space/space-ai/security", "db": "space_*", "events": ("InferenceRequestedEvent",), "security": ("space.admin",), "scaling": "security_replicas"},
)
TESTING = (
    "ai_model_testing", "mission_accuracy_testing", "prediction_validation",
    "bias_testing", "explainability_testing", "security_testing", "agent_behaviour_testing", "reproducibility_testing",
)
QUALITY_GATES_REJECT_IF = (
    "space_ai_platform_is_missing", "foundation_models_are_missing", "space_ai_engine_is_missing",
    "mission_intelligence_platform_is_missing", "autonomous_decision_platform_is_missing",
    "space_cognitive_platform_is_missing", "multi_agent_architecture_is_missing",
    "knowledge_graph_integration_is_missing", "digital_twin_integration_is_missing",
    "ai_governance_is_missing", "security_architecture_is_missing", "deployment_architecture_is_missing",
    "cqrs_architecture_is_missing", "event_architecture_is_missing", "microservices_architecture_is_missing",
    "sibling_space_bc", "replace_p218_foundation", "replace_p218_d_infrastructure",
    "module_local_llm", "opaque_unexplainable_decisions", "ungated_autonomous_mission_strategy",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Space AI Intelligence Fabric",
        "mission": SPACE_AI_MISSION, "vision": SPACE_AI_VISION,
        "builds_on_p218": True, "builds_on_p218_a": True, "builds_on_p218_b": True,
        "builds_on_p218_c": True, "builds_on_p218_d": True,
        "builds_on_p217_z": True, "builds_on_p216_z": True, "builds_on_p215_z": True, "builds_on_p214_z": True,
        "never_replace_p218_d_infrastructure": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
        "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "infrastructure_gate": INFRASTRUCTURE_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
    }

def architecture() -> dict[str, Any]:
    return {"present_required": True, "layers": [dict(x) for x in ARCHITECTURE_LAYERS], "layer_count": len(ARCHITECTURE_LAYERS)}

def foundation_models() -> dict[str, Any]:
    return {"present_required": True, "models": [dict(m) for m in FOUNDATION_MODELS], "model_count": len(FOUNDATION_MODELS), "via_p214_z": True}

def space_ai_engine() -> dict[str, Any]:
    return dict(SPACE_AI_ENGINE) | {"component_count": len(SPACE_AI_ENGINE["components"])}

def mission_intelligence() -> dict[str, Any]:
    return dict(MISSION_INTELLIGENCE) | {"capability_count": len(MISSION_INTELLIGENCE["capabilities"]), "decision_service_count": len(MISSION_INTELLIGENCE["decision_services"])}

def autonomous_decision() -> dict[str, Any]:
    return dict(AUTONOMOUS_DECISION) | {"category_count": len(AUTONOMOUS_DECISION["categories"]), "pipeline_step_count": len(AUTONOMOUS_DECISION["pipeline"])}

def cognitive_platform() -> dict[str, Any]:
    return dict(COGNITIVE_PLATFORM) | {"function_count": len(COGNITIVE_PLATFORM["functions"]), "reasoning_type_count": len(COGNITIVE_PLATFORM["reasoning_types"])}

def scientific_agents() -> dict[str, Any]:
    return {"present_required": True, "agents": [dict(a) for a in SPACE_AGENTS], "agent_count": len(SPACE_AGENTS)}

def predictive_intelligence() -> dict[str, Any]:
    return dict(PREDICTIVE_INTELLIGENCE) | {"domain_count": len(PREDICTIVE_INTELLIGENCE["domains"])}

def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH)

def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN)

def model_lifecycle() -> dict[str, Any]:
    return dict(MODEL_LIFECYCLE)

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
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p218_f": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "space_ai_mission": SPACE_AI_MISSION, "space_ai_vision": SPACE_AI_VISION, "principle": SPACE_AI_MISSION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE, "infrastructure_gate": INFRASTRUCTURE_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P218", "P218-A", "P218-B", "P218-C", "P218-D", "P217-Z", "P216-Z", "P215-Z", "P214-Z"] + [f"ADR-{i}" for i in range(526, 531)],
        "vision": vision_pack(),
        "architecture": architecture(),
        "foundation_models": foundation_models(),
        "space_ai_engine": space_ai_engine(),
        "mission_intelligence": mission_intelligence(),
        "autonomous_decision": autonomous_decision(),
        "cognitive_platform": cognitive_platform(),
        "scientific_agents": scientific_agents(),
        "predictive_intelligence": predictive_intelligence(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "model_lifecycle": model_lifecycle(),
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
        "space_ai_platform_present_required": True,
        "foundation_models_present_required": True,
        "space_ai_engine_present_required": True,
        "mission_intelligence_platform_present_required": True,
        "autonomous_decision_platform_present_required": True,
        "space_cognitive_platform_present_required": True,
        "multi_agent_architecture_present_required": True,
        "knowledge_graph_integration_present_required": True,
        "digital_twin_integration_present_required": True,
        "ai_governance_present_required": True,
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
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_replace_p216_z": True,
        "never_replace_biotechnology": True,
        "space_ai_via_p214z_acl_only": True,
        "no_module_local_llm": True,
        "never_opaque_unexplainable_decisions": True,
        "never_skip_human_mission_oversight_strategy": True,
        "never_skip_space_cybersecurity_strategy": True,
        "never_skip_space_sustainability_strategy": True,
        "never_opaque_mission_critical_strategy": True,
        "never_ungated_autonomous_mission_strategy": True,
        "api_prefix": f"{API_PREFIX}/space-ai",
        "forbidden_sibling_bc": [
            "space_ai_platform",
            "space_foundation_model_platform",
            "space_cognitive_platform_bc",
        ],
        "foundation_for_p218_f": True,
    }

def space_ai_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /space/space-ai",
        "GET /space/space-ai/vision",
        "GET /space/space-ai/architecture",
        "GET /space/space-ai/foundation-models",
        "GET /space/space-ai/engine",
        "GET /space/space-ai/mission-intelligence",
        "GET /space/space-ai/decision",
        "GET /space/space-ai/agents",
        "GET /space/space-ai/knowledge-graph",
        "GET /space/space-ai/lifecycle",
        "GET /space/space-ai/governance",
        "GET /space/space-ai/security",
        "GET /space/space-ai/integration",
        "GET /space/space-ai/deployment",
        "GET /space/space-ai/testing",
        "GET /space/space-ai/cqrs",
        "GET /space/space-ai/events",
        "GET /space/space-ai/readiness",
    ], "foundation_gate_routes": ["GET /space/foundation"],
       "mission_gate_routes": ["GET /space/mission"],
       "strategy_gate_routes": ["GET /space/strategy"],
       "domain_gate_routes": ["GET /space/domain"],
       "infrastructure_gate_routes": ["GET /space/infrastructure", "GET /space/infrastructure/readiness"]}
