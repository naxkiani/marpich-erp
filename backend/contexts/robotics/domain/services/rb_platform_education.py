"""P216-Q Enterprise Education Intelligence — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P216-Q"
ADR = 489
SOR = "robotics"
API_PREFIX = "/api/v1/robotics"
PRODUCT = (
    "Enterprise Robotics Education Robotics, Intelligent Learning Systems, "
    "Autonomous Campus Operations & AI Education Intelligence Platform"
)
CAPABILITY = "CAP-PLT-RB-001"
EDUCATION_VISION = (
    "MEOS Education Intelligence Platform SHALL unify education robotics, "
    "AI learning systems, autonomous campus operations and education digital twins as "
    "intelligent participants within the MEOS Education Intelligence Ecosystem."
)
MISSION = (
    "Create an AI-native, robotics-enabled, personalised education ecosystem "
    "that improves learning outcomes, automates academic operations "
    "and creates intelligent educational institutions."
)
VISION = (
    "Every student, teacher, course, classroom, robot, campus asset "
    "and academic process shall become an intelligent participant "
    "inside the MEOS Education Intelligence Ecosystem."
)
FABRIC = "meos_education_intelligence_fabric"
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
SUPREME_GATE = "P215-Z"
AI_GATE = "P214-Z"
CORE_DOMAIN = "enterprise_education_intelligence"
AGGREGATE = "EducationIntelligenceAggregate"

SUPPORTING_DOMAINS = (
    "student_intelligence",
    "learning_management",
    "academic_operations",
    "education_robotics",
    "smart_classroom",
    "campus_automation",
    "assessment_intelligence",
    "research_intelligence",
    "knowledge_management",
    "education_analytics",
    "digital_education_twin",
    "learning_personalisation",
)
ENTITIES = (
    "EducationInstitution",
    "Campus",
    "Building",
    "Classroom",
    "Student",
    "Teacher",
    "Course",
    "LearningPath",
    "Assessment",
    "EducationRobot",
    "LearningAssistantRobot",
    "ResearchProject",
    "DigitalClassroom",
    "EducationDigitalTwin",
)
VALUE_OBJECTS = (
    "StudentProfile",
    "LearningPreference",
    "SkillLevel",
    "CourseProgress",
    "AssessmentScore",
    "AcademicPerformance",
    "LearningObjective",
    "CampusStatus",
    "ClassroomState",
    "EngagementScore",
)
BOUNDED_CONTEXTS = (
    {"id": "BC-01", "name": "Student Intelligence Context", "responsibilities": ("student_lifecycle", "learning_profile", "personalisation")},
    {"id": "BC-02", "name": "AI Learning Context", "responsibilities": ("adaptive_learning", "ai_tutoring", "learning_optimisation")},
    {"id": "BC-03", "name": "Education Robotics Context", "responsibilities": ("educational_robots", "learning_assistants", "robot_lifecycle")},
    {"id": "BC-04", "name": "Smart Classroom Context", "responsibilities": ("classroom_automation", "learning_environment_optimisation")},
    {"id": "BC-05", "name": "Campus Operations Context", "responsibilities": ("campus_automation", "facility_intelligence", "resource_management")},
    {"id": "BC-06", "name": "Academic Intelligence Context", "responsibilities": ("analytics", "performance_intelligence", "institutional_insights")},
    {"id": "BC-07", "name": "Education Digital Twin Context", "responsibilities": ("institution_simulation", "campus_modelling", "learning_optimisation")},
    {"id": "BC-08", "name": "Education Governance Context", "responsibilities": ("privacy", "compliance", "ai_governance", "academic_policy")},
)
EDUCATION_ROBOTICS = {
    "present_required": True,
    "platform": "meos_education_robotics_platform",
    "components": (
        "education_robot_registry",
        "teaching_assistant_robot_manager",
        "classroom_robot_controller",
        "learning_interaction_engine",
        "robot_knowledge_assistant",
        "campus_robot_operations_console",
    ),
    "supported_robotics": (
        "teaching_assistant_robots",
        "laboratory_robots",
        "library_assistance_robots",
        "campus_service_robots",
        "accessibility_support_robots",
        "research_robots",
    ),
    "capabilities": (
        "learning_support",
        "interactive_teaching",
        "demonstration_assistance",
        "laboratory_support",
        "student_guidance",
        "campus_services",
    ),
}
AI_LEARNING = {
    "present_required": True,
    "engine": "meos_learning_intelligence_engine",
    "capabilities": (
        "adaptive_learning",
        "personalised_curriculum",
        "ai_tutoring",
        "learning_recommendation",
        "skill_gap_analysis",
        "learning_prediction",
        "knowledge_assessment",
    ),
    "models": (
        "education_foundation_models",
        "tutor_models",
        "assessment_models",
        "knowledge_retrieval_models",
        "learning_behaviour_models",
    ),
    "via_p214_z": True,
    "privacy_by_design": True,
    "accessibility_by_design": True,
    "human_centered_learning": True,
    "responsible_ai": True,
}
SMART_CAMPUS = {
    "present_required": True,
    "platform": "meos_autonomous_campus_intelligence_platform",
    "capabilities": (
        "campus_automation",
        "smart_classrooms",
        "energy_optimisation",
        "facility_management",
        "security_coordination",
        "resource_allocation",
        "campus_experience_management",
    ),
}
AUTONOMOUS_OPERATIONS = {
    "present_required": True,
    "platform": "meos_academic_automation_platform",
    "capabilities": (
        "automated_scheduling",
        "classroom_allocation",
        "resource_optimisation",
        "student_service_automation",
        "administrative_workflow_automation",
        "academic_reporting",
    ),
}
ACADEMIC_INTELLIGENCE = {
    "present_required": True,
    "platform": "meos_academic_intelligence_platform",
    "capabilities": (
        "analytics",
        "performance_intelligence",
        "institutional_insights",
        "learning_outcome_tracking",
    ),
}
EDUCATION_DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_education_digital_twin_platform",
    "represents": (
        "universities", "schools", "campuses", "classrooms", "students",
        "teachers", "courses", "research_facilities", "learning_networks",
    ),
    "capabilities": (
        "campus_simulation",
        "learning_scenario_modelling",
        "student_journey_analysis",
        "resource_optimisation",
        "institution_planning",
        "operational_replay",
    ),
}
LEARNING_KG = {
    "present_required": True,
    "graph": "meos_learning_knowledge_graph",
    "nodes": (
        "students", "teachers", "courses", "skills", "research",
        "learning_materials", "robots", "classrooms", "institutions", "projects",
    ),
    "relationships": (
        "learns", "teaches", "requires", "supports",
        "collaborates", "researches", "uses", "improves",
    ),
    "enables": (
        "learning_reasoning",
        "academic_intelligence",
        "skill_discovery",
        "research_collaboration",
    ),
}
OBSERVABILITY = {
    "present_required": True,
    "platform": "meos_education_observability_platform",
    "monitors": (
        "learning_outcomes",
        "student_engagement",
        "robot_performance",
        "campus_operations",
        "ai_model_performance",
        "academic_kpis",
        "digital_twin_accuracy",
        "institution_efficiency",
    ),
    "via_platform_observability": True,
}
SECURITY = {
    "present_required": True,
    "framework": "meos_education_zero_trust_framework",
    "domains": (
        "student_identity",
        "teacher_identity",
        "robot_identity",
        "institution_identity",
        "research_data_protection",
        "academic_privacy",
        "ai_governance",
        "audit_management",
    ),
    "controls": (
        "identity_governance",
        "encryption",
        "access_control",
        "privacy_protection",
        "ai_transparency",
        "compliance_monitoring",
    ),
    "zero_trust": True,
    "privacy_by_design": True,
    "accessibility_by_design": True,
    "human_centered_learning": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "via_integration_platform": True,
    "never_duplicate_sis_lms_core_logic": True,
    "no_module_local_llm": True,
    "physical_ai_via_p214z_acl_only": True,
    "never_replace_p216_foundation": True,
    "never_replace_p216_p_hospitality": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "ungated_physical_autonomy_strategy_forbidden": True,
    "opaque_safety_strategy_forbidden": True,
}
COMMANDS = (
    "RegisterStudentCommand",
    "CreateLearningPathCommand",
    "AssignEducationRobotCommand",
    "GenerateAssessmentCommand",
    "OptimiseCampusOperationCommand",
    "UpdateEducationTwinCommand",
)
QUERIES = (
    "GetStudentProfileQuery",
    "GetLearningProgressQuery",
    "GetCourseStatusQuery",
    "GetCampusStatusQuery",
    "GetEducationTwinQuery",
)
CORE_EVENTS = (
    {"name": "StudentRegisteredEvent", "schema": "robotics.education.student.registered.v1", "owner": "BC-01", "consumers": "learning,campus,audit"},
    {"name": "LearningStartedEvent", "schema": "robotics.education.learning.started.v1", "owner": "BC-02", "consumers": "robotics,twin,audit"},
    {"name": "AssessmentCompletedEvent", "schema": "robotics.education.assessment.completed.v1", "owner": "BC-02", "consumers": "student,analytics,audit"},
    {"name": "RobotTeachingSessionCompletedEvent", "schema": "robotics.education.robot.session.completed.v1", "owner": "BC-03", "consumers": "runtime,learning,audit"},
    {"name": "CampusOptimisedEvent", "schema": "robotics.education.campus.optimised.v1", "owner": "BC-05", "consumers": "twin,analytics,audit"},
    {"name": "ResearchUpdatedEvent", "schema": "robotics.education.research.updated.v1", "owner": "BC-06", "consumers": "kg,governance,audit"},
    {"name": "LearningOutcomeChangedEvent", "schema": "robotics.education.learning.outcome.changed.v1", "owner": "BC-01", "consumers": "ai,governance,audit"},
)
MICROSERVICES = (
    {"id": "student_intelligence_service", "bc": "BC-01", "api": "/robotics/education/students", "db": "robotics_*", "events": ("StudentRegisteredEvent", "LearningOutcomeChangedEvent"), "security": ("robotics.write",), "scaling": "student_replicas", "responsibility": "Student lifecycle and personalisation projections"},
    {"id": "learning_management_service", "bc": "BC-02", "api": "/robotics/education/learning", "db": "robotics_*", "events": ("LearningStartedEvent", "AssessmentCompletedEvent"), "security": ("robotics.write",), "scaling": "learning_workers", "responsibility": "Adaptive learning via P214-Z ACL"},
    {"id": "education_robotics_service", "bc": "BC-03", "api": "/robotics/education/robots", "db": "robotics_*", "events": ("RobotTeachingSessionCompletedEvent",), "security": ("robotics.write",), "scaling": "robot_workers", "responsibility": "Education robot mission orchestration"},
    {"id": "smart_classroom_service", "bc": "BC-04", "api": "/robotics/education/classrooms", "db": "robotics_*", "events": ("LearningStartedEvent",), "security": ("robotics.write",), "scaling": "classroom_workers", "responsibility": "Smart classroom automation"},
    {"id": "campus_operations_service", "bc": "BC-05", "api": "/robotics/education/campus", "db": "robotics_*", "events": ("CampusOptimisedEvent",), "security": ("robotics.write",), "scaling": "campus_workers", "responsibility": "Autonomous campus operations"},
    {"id": "assessment_intelligence_service", "bc": "BC-02", "api": "/robotics/education/assessments", "db": "robotics_*", "events": ("AssessmentCompletedEvent",), "security": ("robotics.write",), "scaling": "assessment_workers", "responsibility": "Assessment intelligence projections"},
    {"id": "research_intelligence_service", "bc": "BC-06", "api": "/robotics/education/research", "db": "robotics_*", "events": ("ResearchUpdatedEvent",), "security": ("robotics.read",), "scaling": "research_workers", "responsibility": "Research intelligence facets"},
    {"id": "digital_twin_service", "bc": "BC-07", "api": "/robotics/education/digital-twin", "db": "robotics_*", "events": ("CampusOptimisedEvent", "LearningStartedEvent"), "security": ("robotics.read",), "scaling": "twin_workers", "responsibility": "Education digital twin sync"},
    {"id": "knowledge_graph_service", "bc": "BC-07", "api": "/robotics/education/knowledge-graph", "db": "robotics_*", "events": ("StudentRegisteredEvent", "ResearchUpdatedEvent"), "security": ("robotics.read",), "scaling": "kg_workers", "responsibility": "Learning knowledge graph projections"},
    {"id": "education_analytics_service", "bc": "BC-08", "api": "/robotics/education/analytics", "db": "robotics_*", "events": ("LearningOutcomeChangedEvent", "CampusOptimisedEvent"), "security": ("robotics.read",), "scaling": "analytics_workers", "responsibility": "Education analytics and governance facets"},
)
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p216d_robotics_os",
        "p216e_physical_ai",
        "p216p_hospitality",
        "p214z_ai_master",
        "p215z_quantum_supreme",
        "erp",
        "student_information_systems",
        "learning_management_systems",
        "research_platforms",
        "library_systems",
        "iot_platforms",
        "smart_building_platforms",
        "integration_platform",
    ),
    "mechanisms": (
        "education_apis",
        "robot_mission_interfaces",
        "sis_via_peer_api",
        "lms_via_peer_api",
        "library_via_integration_connectors",
        "education_event_contracts",
    ),
    "via_p216_d": True,
    "via_p216_e": True,
    "via_p216_p": True,
    "via_p214_z": True,
    "via_p215_z": True,
    "via_p213": True,
    "via_integration_platform": True,
    "never_duplicate_sis_lms_core_logic": True,
}
DEPLOYMENT = {
    "present_required": True,
    "model": "hybrid_education_intelligence_infrastructure",
    "includes": (
        "campus_edge_platform",
        "smart_classroom_runtime",
        "education_cloud_platform",
        "ai_compute_cluster",
        "robot_control_platform",
        "digital_twin_cluster",
        "knowledge_graph_cluster",
        "analytics_platform",
        "security_operations_platform",
    ),
    "deployment_models": (
        "school",
        "university",
        "research_institute",
        "education_network",
        "global_learning_ecosystem",
    ),
    "cloud_native": True,
    "edge_native": True,
}
TESTING = (
    "learning_system_testing",
    "robot_interaction_testing",
    "ai_tutor_validation",
    "assessment_testing",
    "digital_twin_validation",
    "security_testing",
    "performance_testing",
    "accessibility_testing",
    "scalability_testing",
    "resilience_testing",
)
API_SURFACES = (
    "/api/v1/robotics/education",
    "/api/v1/robotics/education/vision",
    "/api/v1/robotics/education/domain",
    "/api/v1/robotics/education/bounded-contexts",
    "/api/v1/robotics/education/robotics",
    "/api/v1/robotics/education/ai-learning",
    "/api/v1/robotics/education/smart-campus",
    "/api/v1/robotics/education/autonomous-operations",
    "/api/v1/robotics/education/academic-intelligence",
    "/api/v1/robotics/education/digital-twin",
    "/api/v1/robotics/education/knowledge-graph",
    "/api/v1/robotics/education/observability",
    "/api/v1/robotics/education/security",
    "/api/v1/robotics/education/cqrs",
    "/api/v1/robotics/education/events",
    "/api/v1/robotics/education/microservices",
    "/api/v1/robotics/education/integration",
    "/api/v1/robotics/education/deployment",
    "/api/v1/robotics/education/testing",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
QUALITY_GATES_REJECT_IF = (
    "education_robotics_platform_is_missing",
    "ai_learning_platform_is_missing",
    "smart_campus_platform_is_missing",
    "autonomous_education_operations_is_missing",
    "academic_intelligence_platform_is_missing",
    "education_digital_twin_is_missing",
    "learning_knowledge_graph_is_missing",
    "security_architecture_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "cloud_edge_deployment_is_missing",
    "enterprise_education_integration_is_missing",
    "testing_architecture_is_missing",
    "sibling_robotics_bc",
    "replace_p216_p_hospitality",
    "duplicate_sis_lms_core_logic",
    "module_local_llm",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Education Intelligence Fabric",
        "education_vision": EDUCATION_VISION,
        "mission": MISSION,
        "vision": VISION,
        "builds_on_p216": True,
        "builds_on_p216_p": True,
        "builds_on_p216_e": True,
        "builds_on_p216_d": True,
        "builds_on_p215_z": True,
        "builds_on_p214_z": True,
        "never_replace_p216_p_hospitality": True,
        "foundation_gate": FOUNDATION_GATE,
        "hospitality_gate": HOSPITALITY_GATE,
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
    return dict(EDUCATION_ROBOTICS)

def ai_learning() -> dict[str, Any]:
    return dict(AI_LEARNING)

def smart_campus() -> dict[str, Any]:
    return dict(SMART_CAMPUS)

def autonomous_operations() -> dict[str, Any]:
    return dict(AUTONOMOUS_OPERATIONS)

def academic_intelligence() -> dict[str, Any]:
    return dict(ACADEMIC_INTELLIGENCE)

def digital_twin() -> dict[str, Any]:
    return dict(EDUCATION_DIGITAL_TWIN)

def knowledge_graph() -> dict[str, Any]:
    return dict(LEARNING_KG)

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
        "hospitality_gate_api": "/api/v1/robotics/hospitality",
        "runtime_gate_api": "/api/v1/robotics/runtime",
    }

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p216_r": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "education_vision": EDUCATION_VISION, "mission": MISSION, "vision": VISION, "principle": EDUCATION_VISION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE, "runtime_gate": RUNTIME_GATE,
        "physical_ai_gate": PHYSICAL_AI_GATE, "industrial_gate": INDUSTRIAL_GATE,
        "logistics_gate": LOGISTICS_GATE, "mobility_gate": MOBILITY_GATE,
        "healthcare_gate": HEALTHCARE_GATE, "construction_gate": CONSTRUCTION_GATE,
        "public_safety_gate": PUBLIC_SAFETY_GATE, "retail_gate": RETAIL_GATE,
        "hospitality_gate": HOSPITALITY_GATE,
        "supreme_gate": SUPREME_GATE, "ai_gate": AI_GATE,
        "builds_on": [
            "P216", "P216-A", "P216-B", "P216-C", "P216-D", "P216-E", "P216-F", "P216-G", "P216-H",
            "P216-I", "P216-K", "P216-L", "P216-O", "P216-P", "P215-Z", "P214-Z", "P213",
            "ADR-472", "ADR-473", "ADR-474", "ADR-475", "ADR-476", "ADR-477", "ADR-478", "ADR-479",
            "ADR-480", "ADR-481", "ADR-483", "ADR-484", "ADR-487", "ADR-488",
        ],
        "vision_pack": vision_pack(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "robotics_platform": robotics_platform(),
        "ai_learning": ai_learning(),
        "smart_campus": smart_campus(),
        "autonomous_operations": autonomous_operations(),
        "academic_intelligence": academic_intelligence(),
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
        "education_robotics_platform_present_required": True,
        "ai_learning_platform_present_required": True,
        "smart_campus_platform_present_required": True,
        "autonomous_education_operations_present_required": True,
        "academic_intelligence_platform_present_required": True,
        "education_digital_twin_present_required": True,
        "learning_knowledge_graph_present_required": True,
        "security_architecture_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "cloud_edge_deployment_present_required": True,
        "enterprise_education_integration_present_required": True,
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
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_duplicate_sis_lms_core_logic": True,
        "no_module_local_llm": True,
        "physical_ai_via_p214z_acl_only": True,
        "privacy_by_design_required": True,
        "accessibility_by_design_required": True,
        "human_centered_learning_required": True,
        "ungated_physical_autonomy_strategy_forbidden": True,
        "opaque_safety_strategy_forbidden": True,
        "builds_on_p216": True, "builds_on_p216_p": True,
        "builds_on_p216_e": True, "builds_on_p216_d": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p216_d": True, "via_p216_e": True, "via_p216_p": True,
        "via_p215_z": True, "via_p214_z": True, "via_p213": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "via_integration_platform": True,
        "api_prefix": f"{API_PREFIX}/education",
        "forbidden_sibling_bc": [
            "education_robotics_platform",
            "ai_learning_intelligence_platform",
            "autonomous_campus_operations_platform",
            "smart_university_platform",
        ],
        "foundation_for_p216_r": True,
        "p216_j_agriculture_planned": True,
        "p216_m_space_planned": True,
        "p216_n_environmental_planned": True,
    }

def education_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /robotics/education",
        "GET /robotics/education/vision",
        "GET /robotics/education/domain",
        "GET /robotics/education/bounded-contexts",
        "GET /robotics/education/robotics",
        "GET /robotics/education/ai-learning",
        "GET /robotics/education/smart-campus",
        "GET /robotics/education/autonomous-operations",
        "GET /robotics/education/academic-intelligence",
        "GET /robotics/education/digital-twin",
        "GET /robotics/education/knowledge-graph",
        "GET /robotics/education/observability",
        "GET /robotics/education/security",
        "GET /robotics/education/cqrs",
        "GET /robotics/education/events",
        "GET /robotics/education/microservices",
        "GET /robotics/education/integration",
        "GET /robotics/education/deployment",
        "GET /robotics/education/testing",
        "GET /robotics/education/readiness",
    ], "hospitality_gate_routes": ["GET /robotics/hospitality", "GET /robotics/hospitality/readiness"]}
