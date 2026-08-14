"""P216-W Enterprise Personal Intelligence — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P216-W"
ADR = 495
SOR = "robotics"
API_PREFIX = "/api/v1/robotics"
PRODUCT = (
    "Enterprise Robotics Personal Robotics, Consumer Autonomous Assistants, "
    "Home Intelligence, Personal AI Robotics & Human Augmentation Platform"
)
CAPABILITY = "CAP-PLT-RB-001"
PERSONAL_VISION = (
    "MEOS Personal Intelligence Platform SHALL unify personal robotics, "
    "consumer AI companions, home intelligence and personal digital twins as "
    "intelligent participants within the MEOS Personal Intelligence Ecosystem."
)
MISSION = (
    "Create a secure, personalised, AI-native ecosystem "
    "where every individual has intelligent assistants, autonomous services "
    "and adaptive robotic support that improve quality of life, "
    "productivity and human capability."
)
VISION = (
    "Every person, device, home, personal activity, knowledge resource, "
    "preference and life objective shall become an intelligent participant "
    "inside the MEOS Personal Intelligence Ecosystem."
)
FABRIC = "meos_personal_intelligence_fabric"
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
PUBLIC_SAFETY_GATE = "P216-L"
RETAIL_GATE = "P216-O"
HOSPITALITY_GATE = "P216-P"
EDUCATION_GATE = "P216-Q"
FINANCE_GATE = "P216-R"
GOVERNMENT_GATE = "P216-T"
DEFENSE_GATE = "P216-U"
SCIENCE_GATE = "P216-V"
SUPREME_GATE = "P215-Z"
AI_GATE = "P214-Z"
CORE_DOMAIN = "personal_intelligence_management"
AGGREGATE = "PersonalIntelligenceAggregate"

SUPPORTING_DOMAINS = (
    "personal_ai_assistant",
    "personal_robotics",
    "smart_home_intelligence",
    "human_interaction",
    "personal_knowledge_management",
    "personal_automation",
    "personal_digital_twin",
    "health_lifestyle_intelligence",
    "personal_security",
    "human_augmentation",
    "consumer_device_intelligence",
    "personal_analytics",
)
ENTITIES = (
    "Individual",
    "PersonalAIEntity",
    "PersonalRobot",
    "SmartHome",
    "PersonalDevice",
    "DigitalAssistant",
    "KnowledgeRepository",
    "PersonalDigitalTwin",
    "LifeGoal",
    "AutomationWorkflow",
)
VALUE_OBJECTS = (
    "PersonalPreference",
    "ContextState",
    "TrustLevel",
    "PrivacySetting",
    "LearningProfile",
    "RoutinePattern",
    "HealthStatus",
    "InteractionHistory",
    "PersonalCapabilityScore",
)
BOUNDED_CONTEXTS = (
    {"id": "BC-01", "name": "Personal AI Assistant Context", "responsibilities": ("ai_companion_lifecycle", "personal_conversations", "intelligent_assistance")},
    {"id": "BC-02", "name": "Personal Robotics Context", "responsibilities": ("consumer_robots", "robot_management", "human_interaction")},
    {"id": "BC-03", "name": "Smart Home Intelligence Context", "responsibilities": ("home_automation", "ambient_intelligence", "device_coordination")},
    {"id": "BC-04", "name": "Personal Knowledge Context", "responsibilities": ("personal_memory", "knowledge_organisation", "information_intelligence")},
    {"id": "BC-05", "name": "Human Augmentation Context", "responsibilities": ("capability_enhancement", "cognitive_assistance", "productivity_improvement")},
    {"id": "BC-06", "name": "Personal Security Context", "responsibilities": ("privacy_protection", "identity_security", "trust_management")},
    {"id": "BC-07", "name": "Personal Digital Twin Context", "responsibilities": ("individual_modelling", "behaviour_intelligence", "personal_simulation")},
    {"id": "BC-08", "name": "Personal Governance Context", "responsibilities": ("consent_management", "ai_transparency", "personal_control")},
)
PERSONAL_ROBOTICS = {
    "present_required": True,
    "platform": "meos_personal_robotics_platform",
    "components": (
        "personal_robot_registry",
        "robot_interaction_engine",
        "personal_robot_controller",
        "home_assistance_engine",
        "companion_intelligence_layer",
        "robot_experience_dashboard",
    ),
    "supported_robotics": (
        "home_assistant_robots",
        "companion_robots",
        "accessibility_robots",
        "personal_service_robots",
        "learning_support_robots",
        "elder_assistance_robots",
    ),
    "capabilities": (
        "personal_assistance",
        "environmental_interaction",
        "routine_automation",
        "human_support",
        "context_awareness",
    ),
}
AI_COMPANION = {
    "present_required": True,
    "engine": "meos_personal_ai_companion_engine",
    "capabilities": (
        "conversation_intelligence",
        "personal_planning",
        "knowledge_assistance",
        "task_automation",
        "decision_support",
        "personal_learning",
        "context_awareness",
    ),
    "models": (
        "personal_foundation_models",
        "personal_memory_models",
        "preference_learning_models",
        "reasoning_models",
        "multimodal_interaction_models",
    ),
    "via_p214_z": True,
    "privacy_by_design": True,
    "human_control_by_design": True,
    "explainable_ai": True,
}
SMART_HOME = {
    "present_required": True,
    "platform": "meos_home_intelligence_platform",
    "capabilities": (
        "home_automation",
        "energy_optimisation",
        "security_intelligence",
        "device_coordination",
        "environmental_control",
        "lifestyle_optimisation",
    ),
    "integrations": (
        "iot_devices",
        "smart_appliances",
        "wearables",
        "home_robots",
        "personal_networks",
    ),
}
HUMAN_AUGMENTATION = {
    "present_required": True,
    "platform": "meos_human_capability_intelligence_platform",
    "capabilities": (
        "cognitive_assistance",
        "knowledge_augmentation",
        "productivity_enhancement",
        "personal_learning_acceleration",
        "accessibility_support",
        "human_machine_collaboration",
    ),
    "components": (
        "ai_cognitive_assistant",
        "personal_knowledge_engine",
        "augmented_interaction_layer",
        "capability_analytics_engine",
    ),
}
LIFE_AUTOMATION = {
    "present_required": True,
    "platform": "meos_life_automation_platform",
    "capabilities": (
        "routine_automation",
        "task_orchestration",
        "preference_driven_workflows",
        "consent_gated_execution",
    ),
}
PERSONAL_DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_personal_digital_twin_platform",
    "represents": (
        "individual_preferences", "knowledge", "goals", "habits",
        "devices", "activities", "skills", "personal_environment",
    ),
    "capabilities": (
        "personal_simulation",
        "decision_support",
        "routine_optimisation",
        "goal_planning",
        "lifestyle_improvement",
    ),
}
PERSONAL_KG = {
    "present_required": True,
    "graph": "meos_personal_knowledge_graph",
    "nodes": (
        "person", "memories", "documents", "skills", "goals",
        "relationships", "devices", "preferences", "experiences",
    ),
    "relationships": (
        "knows", "uses", "prefers", "learns",
        "achieves", "depends_on", "improves",
    ),
    "enables": (
        "personal_reasoning",
        "memory_intelligence",
        "context_awareness",
        "personalisation",
    ),
}
OBSERVABILITY = {
    "present_required": True,
    "platform": "meos_personal_observability_platform",
    "monitors": (
        "ai_assistant_quality",
        "robot_performance",
        "personalisation_accuracy",
        "privacy_events",
        "automation_success",
        "user_satisfaction",
        "digital_twin_accuracy",
        "capability_growth",
    ),
    "via_platform_observability": True,
}
SECURITY = {
    "present_required": True,
    "framework": "meos_personal_zero_trust_framework",
    "domains": (
        "personal_identity",
        "private_data",
        "personal_ai_memory",
        "robot_security",
        "device_security",
        "consent_management",
        "ai_transparency",
    ),
    "controls": (
        "data_sovereignty",
        "encryption",
        "privacy_policies",
        "permission_management",
        "audit_trails",
        "user_control_center",
    ),
    "zero_trust": True,
    "privacy_by_design": True,
    "personal_data_sovereignty": True,
    "human_control_by_design": True,
    "consent_management": True,
    "explainable_ai": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "via_integration_platform": True,
    "never_replace_identity_platform": True,
    "no_module_local_llm": True,
    "physical_ai_via_p214z_acl_only": True,
    "never_replace_p216_foundation": True,
    "never_replace_p216_v_science": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "ungated_physical_autonomy_strategy_forbidden": True,
    "opaque_safety_strategy_forbidden": True,
}
COMMANDS = (
    "CreatePersonalProfileCommand",
    "ActivatePersonalAssistantCommand",
    "ConnectRobotCommand",
    "CreateAutomationCommand",
    "UpdatePersonalTwinCommand",
    "LearnPreferenceCommand",
)
QUERIES = (
    "GetPersonalProfileQuery",
    "GetAssistantStateQuery",
    "GetRobotStatusQuery",
    "GetPersonalKnowledgeQuery",
    "GetTwinSimulationQuery",
)
CORE_EVENTS = (
    {"name": "PersonalCreatedEvent", "schema": "robotics.personal.profile.created.v1", "owner": "BC-01", "consumers": "security,twin,audit"},
    {"name": "AssistantActivatedEvent", "schema": "robotics.personal.assistant.activated.v1", "owner": "BC-01", "consumers": "robotics,governance,audit"},
    {"name": "InteractionCompletedEvent", "schema": "robotics.personal.interaction.completed.v1", "owner": "BC-01", "consumers": "knowledge,analytics,audit"},
    {"name": "PreferenceLearnedEvent", "schema": "robotics.personal.preference.learned.v1", "owner": "BC-04", "consumers": "twin,automation,audit"},
    {"name": "AutomationExecutedEvent", "schema": "robotics.personal.automation.executed.v1", "owner": "BC-03", "consumers": "home,governance,audit"},
    {"name": "RobotConnectedEvent", "schema": "robotics.personal.robot.connected.v1", "owner": "BC-02", "consumers": "runtime,home,audit"},
    {"name": "CapabilityImprovedEvent", "schema": "robotics.personal.capability.improved.v1", "owner": "BC-05", "consumers": "twin,analytics,audit"},
)
MICROSERVICES = (
    {"id": "personal_identity_service", "bc": "BC-06", "api": "/robotics/personal/identity", "db": "robotics_*", "events": ("PersonalCreatedEvent",), "security": ("robotics.write",), "scaling": "identity_workers", "responsibility": "Personal identity projections via Identity Platform ACL"},
    {"id": "ai_assistant_service", "bc": "BC-01", "api": "/robotics/personal/assistant", "db": "robotics_*", "events": ("AssistantActivatedEvent", "InteractionCompletedEvent"), "security": ("robotics.write",), "scaling": "assistant_workers", "responsibility": "Personal AI companion via P214-Z ACL"},
    {"id": "robotics_service", "bc": "BC-02", "api": "/robotics/personal/robots", "db": "robotics_*", "events": ("RobotConnectedEvent",), "security": ("robotics.write",), "scaling": "robot_workers", "responsibility": "Personal robot lifecycle orchestration"},
    {"id": "home_intelligence_service", "bc": "BC-03", "api": "/robotics/personal/home", "db": "robotics_*", "events": ("AutomationExecutedEvent",), "security": ("robotics.write",), "scaling": "home_workers", "responsibility": "Smart home intelligence projections"},
    {"id": "knowledge_graph_service", "bc": "BC-04", "api": "/robotics/personal/knowledge-graph", "db": "robotics_*", "events": ("PreferenceLearnedEvent", "InteractionCompletedEvent"), "security": ("robotics.read",), "scaling": "kg_workers", "responsibility": "Personal knowledge graph projections"},
    {"id": "digital_twin_service", "bc": "BC-07", "api": "/robotics/personal/digital-twin", "db": "robotics_*", "events": ("PreferenceLearnedEvent", "CapabilityImprovedEvent"), "security": ("robotics.read",), "scaling": "twin_workers", "responsibility": "Personal digital twin sync"},
    {"id": "automation_service", "bc": "BC-03", "api": "/robotics/personal/automation", "db": "robotics_*", "events": ("AutomationExecutedEvent",), "security": ("robotics.write",), "scaling": "automation_workers", "responsibility": "Life automation workflows"},
    {"id": "personal_analytics_service", "bc": "BC-05", "api": "/robotics/personal/analytics", "db": "robotics_*", "events": ("CapabilityImprovedEvent", "InteractionCompletedEvent"), "security": ("robotics.read",), "scaling": "analytics_workers", "responsibility": "Personal analytics and augmentation facets"},
    {"id": "security_service", "bc": "BC-06", "api": "/robotics/personal/security", "db": "robotics_*", "events": ("PersonalCreatedEvent",), "security": ("robotics.write",), "scaling": "security_workers", "responsibility": "Personal security and privacy facets"},
    {"id": "consent_management_service", "bc": "BC-08", "api": "/robotics/personal/consent", "db": "robotics_*", "events": ("AssistantActivatedEvent", "AutomationExecutedEvent"), "security": ("robotics.write",), "scaling": "consent_workers", "responsibility": "Consent and personal governance"},
)
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p216d_robotics_os",
        "p216e_physical_ai",
        "p216i_healthcare",
        "p216q_education",
        "p216r_finance",
        "p216t_government",
        "p214z_ai_master",
        "p215z_quantum_supreme",
        "identity_platform",
        "iot_ecosystems",
        "wearable_platforms",
        "smart_home_platforms",
        "personal_devices",
        "cloud_ai_platforms",
        "integration_platform",
    ),
    "mechanisms": (
        "personal_apis",
        "robot_mission_interfaces",
        "identity_via_identity_platform",
        "iot_via_integration_connectors",
        "personal_event_contracts",
    ),
    "via_p216_d": True,
    "via_p216_e": True,
    "via_p216_i": True,
    "via_p216_q": True,
    "via_p216_r": True,
    "via_p216_t": True,
    "via_p214_z": True,
    "via_p215_z": True,
    "via_p213": True,
    "via_identity": True,
    "via_integration_platform": True,
    "never_replace_identity_platform": True,
}
DEPLOYMENT = {
    "present_required": True,
    "model": "hybrid_personal_intelligence_infrastructure",
    "includes": (
        "personal_edge_ai_device",
        "home_intelligence_hub",
        "personal_cloud_platform",
        "ai_compute_layer",
        "robot_runtime_platform",
        "digital_twin_platform",
        "knowledge_graph_platform",
        "security_platform",
    ),
    "deployment_models": (
        "individual_user",
        "smart_home",
        "family_ecosystem",
        "consumer_network",
        "global_personal_intelligence_platform",
    ),
    "cloud_native": True,
    "edge_native": True,
}
TESTING = (
    "human_interaction_testing",
    "ai_assistant_validation",
    "robot_safety_testing",
    "privacy_testing",
    "security_testing",
    "personalisation_testing",
    "accessibility_testing",
    "reliability_testing",
    "human_oversight_testing",
)
API_SURFACES = (
    "/api/v1/robotics/personal",
    "/api/v1/robotics/personal/vision",
    "/api/v1/robotics/personal/domain",
    "/api/v1/robotics/personal/bounded-contexts",
    "/api/v1/robotics/personal/robotics",
    "/api/v1/robotics/personal/ai-companion",
    "/api/v1/robotics/personal/smart-home",
    "/api/v1/robotics/personal/human-augmentation",
    "/api/v1/robotics/personal/life-automation",
    "/api/v1/robotics/personal/digital-twin",
    "/api/v1/robotics/personal/knowledge-graph",
    "/api/v1/robotics/personal/observability",
    "/api/v1/robotics/personal/security",
    "/api/v1/robotics/personal/cqrs",
    "/api/v1/robotics/personal/events",
    "/api/v1/robotics/personal/microservices",
    "/api/v1/robotics/personal/integration",
    "/api/v1/robotics/personal/deployment",
    "/api/v1/robotics/personal/testing",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
QUALITY_GATES_REJECT_IF = (
    "personal_robotics_platform_is_missing",
    "ai_companion_platform_is_missing",
    "smart_home_intelligence_is_missing",
    "personal_digital_twin_is_missing",
    "human_augmentation_platform_is_missing",
    "personal_knowledge_graph_is_missing",
    "life_automation_platform_is_missing",
    "security_architecture_is_missing",
    "privacy_sovereignty_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "cloud_edge_deployment_is_missing",
    "enterprise_personal_integration_is_missing",
    "testing_architecture_is_missing",
    "sibling_robotics_bc",
    "replace_p216_v_science",
    "replace_identity_platform",
    "module_local_llm",
    "ungated_physical_autonomy",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Personal Intelligence Fabric",
        "personal_vision": PERSONAL_VISION,
        "mission": MISSION,
        "vision": VISION,
        "builds_on_p216": True,
        "builds_on_p216_v": True,
        "builds_on_p216_i": True,
        "builds_on_p216_q": True,
        "builds_on_p216_e": True,
        "builds_on_p216_d": True,
        "builds_on_p215_z": True,
        "builds_on_p214_z": True,
        "never_replace_p216_v_science": True,
        "foundation_gate": FOUNDATION_GATE,
        "science_gate": SCIENCE_GATE,
        "healthcare_gate": HEALTHCARE_GATE,
        "education_gate": EDUCATION_GATE,
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
    return dict(PERSONAL_ROBOTICS)

def ai_companion() -> dict[str, Any]:
    return dict(AI_COMPANION)

def smart_home() -> dict[str, Any]:
    return dict(SMART_HOME)

def human_augmentation() -> dict[str, Any]:
    return dict(HUMAN_AUGMENTATION)

def life_automation() -> dict[str, Any]:
    return dict(LIFE_AUTOMATION)

def digital_twin() -> dict[str, Any]:
    return dict(PERSONAL_DIGITAL_TWIN)

def knowledge_graph() -> dict[str, Any]:
    return dict(PERSONAL_KG)

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
        "science_gate_api": "/api/v1/robotics/science",
        "runtime_gate_api": "/api/v1/robotics/runtime",
    }

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p216_x": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "personal_vision": PERSONAL_VISION, "mission": MISSION, "vision": VISION, "principle": PERSONAL_VISION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE, "runtime_gate": RUNTIME_GATE,
        "physical_ai_gate": PHYSICAL_AI_GATE, "industrial_gate": INDUSTRIAL_GATE,
        "logistics_gate": LOGISTICS_GATE, "mobility_gate": MOBILITY_GATE,
        "healthcare_gate": HEALTHCARE_GATE, "construction_gate": CONSTRUCTION_GATE,
        "public_safety_gate": PUBLIC_SAFETY_GATE, "retail_gate": RETAIL_GATE,
        "hospitality_gate": HOSPITALITY_GATE, "education_gate": EDUCATION_GATE,
        "finance_gate": FINANCE_GATE, "government_gate": GOVERNMENT_GATE,
        "defense_gate": DEFENSE_GATE, "science_gate": SCIENCE_GATE,
        "supreme_gate": SUPREME_GATE, "ai_gate": AI_GATE,
        "builds_on": [
            "P216", "P216-A", "P216-B", "P216-C", "P216-D", "P216-E", "P216-F", "P216-G", "P216-H",
            "P216-I", "P216-K", "P216-L", "P216-O", "P216-P", "P216-Q", "P216-R", "P216-T", "P216-U",
            "P216-V", "P215-Z", "P214-Z", "P213",
            "ADR-472", "ADR-473", "ADR-474", "ADR-475", "ADR-476", "ADR-477", "ADR-478", "ADR-479",
            "ADR-480", "ADR-481", "ADR-483", "ADR-484", "ADR-487", "ADR-488", "ADR-489", "ADR-490",
            "ADR-492", "ADR-493", "ADR-494",
        ],
        "vision_pack": vision_pack(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "robotics_platform": robotics_platform(),
        "ai_companion": ai_companion(),
        "smart_home": smart_home(),
        "human_augmentation": human_augmentation(),
        "life_automation": life_automation(),
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
        "personal_robotics_platform_present_required": True,
        "ai_companion_platform_present_required": True,
        "smart_home_intelligence_present_required": True,
        "personal_digital_twin_present_required": True,
        "human_augmentation_platform_present_required": True,
        "personal_knowledge_graph_present_required": True,
        "life_automation_platform_present_required": True,
        "security_architecture_present_required": True,
        "privacy_sovereignty_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "cloud_edge_deployment_present_required": True,
        "enterprise_personal_integration_present_required": True,
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
        "never_replace_p216_l_public_safety": True,
        "never_replace_p216_o_retail": True,
        "never_replace_p216_p_hospitality": True,
        "never_replace_p216_q_education": True,
        "never_replace_p216_r_finance": True,
        "never_replace_p216_t_government": True,
        "never_replace_p216_u_defense": True,
        "never_replace_p216_v_science": True,
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_replace_identity_platform": True,
        "no_module_local_llm": True,
        "physical_ai_via_p214z_acl_only": True,
        "privacy_by_design_required": True,
        "personal_data_sovereignty_required": True,
        "human_control_by_design_required": True,
        "consent_management_required": True,
        "explainable_ai_required": True,
        "ungated_physical_autonomy_strategy_forbidden": True,
        "opaque_safety_strategy_forbidden": True,
        "builds_on_p216": True, "builds_on_p216_v": True, "builds_on_p216_i": True,
        "builds_on_p216_q": True, "builds_on_p216_e": True, "builds_on_p216_d": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p216_d": True, "via_p216_e": True, "via_p216_i": True, "via_p216_q": True,
        "via_p216_r": True, "via_p216_t": True,
        "via_p215_z": True, "via_p214_z": True, "via_p213": True,
        "via_identity": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "via_integration_platform": True,
        "api_prefix": f"{API_PREFIX}/personal",
        "forbidden_sibling_bc": [
            "personal_robotics_platform",
            "consumer_ai_robotics_platform",
            "home_intelligence_platform",
            "personal_ai_assistant_platform",
        ],
        "foundation_for_p216_x": True,
        "p216_j_agriculture_planned": True,
        "p216_m_space_planned": True,
        "p216_n_environmental_planned": True,
        "p216_s_legal_planned": True,
    }

def personal_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /robotics/personal",
        "GET /robotics/personal/vision",
        "GET /robotics/personal/domain",
        "GET /robotics/personal/bounded-contexts",
        "GET /robotics/personal/robotics",
        "GET /robotics/personal/ai-companion",
        "GET /robotics/personal/smart-home",
        "GET /robotics/personal/human-augmentation",
        "GET /robotics/personal/life-automation",
        "GET /robotics/personal/digital-twin",
        "GET /robotics/personal/knowledge-graph",
        "GET /robotics/personal/observability",
        "GET /robotics/personal/security",
        "GET /robotics/personal/cqrs",
        "GET /robotics/personal/events",
        "GET /robotics/personal/microservices",
        "GET /robotics/personal/integration",
        "GET /robotics/personal/deployment",
        "GET /robotics/personal/testing",
        "GET /robotics/personal/readiness",
    ], "science_gate_routes": ["GET /robotics/science", "GET /robotics/science/readiness"]}
