"""P216-V Enterprise Scientific Intelligence — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P216-V"
ADR = 494
SOR = "robotics"
API_PREFIX = "/api/v1/robotics"
PRODUCT = (
    "Enterprise Robotics Science Robotics, Research Automation, "
    "Autonomous Laboratories, Scientific AI Intelligence & Discovery Acceleration Platform"
)
CAPABILITY = "CAP-PLT-RB-001"
SCIENCE_VISION = (
    "MEOS Scientific Intelligence Platform SHALL unify science robotics, "
    "autonomous laboratories, AI scientist systems and scientific digital twins as "
    "intelligent participants within the MEOS Scientific Intelligence Ecosystem."
)
MISSION = (
    "Create an AI-native, robotics-enabled scientific ecosystem "
    "that accelerates discovery, automates experiments, "
    "improves research productivity and enables collaborative intelligence "
    "between humans and machines."
)
VISION = (
    "Every researcher, experiment, laboratory, scientific dataset, hypothesis, "
    "simulation, robotic instrument and discovery process shall become an intelligent participant "
    "inside the MEOS Scientific Intelligence Ecosystem."
)
FABRIC = "meos_scientific_intelligence_fabric"
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
SUPREME_GATE = "P215-Z"
AI_GATE = "P214-Z"
CORE_DOMAIN = "enterprise_scientific_intelligence"
AGGREGATE = "ScientificIntelligenceAggregate"

SUPPORTING_DOMAINS = (
    "research_intelligence",
    "laboratory_automation",
    "scientific_robotics",
    "experiment_management",
    "scientific_simulation",
    "discovery_intelligence",
    "knowledge_management",
    "scientific_data_intelligence",
    "publication_intelligence",
    "innovation_management",
    "scientific_digital_twin",
    "research_governance",
)
ENTITIES = (
    "ResearchInstitution",
    "Laboratory",
    "Researcher",
    "ScientificProject",
    "Experiment",
    "Hypothesis",
    "ScientificRobot",
    "ResearchInstrument",
    "Dataset",
    "ScientificModel",
    "Discovery",
    "ScientificDigitalTwin",
)
VALUE_OBJECTS = (
    "ResearchObjective",
    "ExperimentStatus",
    "ConfidenceScore",
    "ScientificEvidence",
    "ReproducibilityScore",
    "DiscoveryImpactScore",
    "ModelAccuracy",
    "ResearchPriority",
    "ValidationStatus",
)
BOUNDED_CONTEXTS = (
    {"id": "BC-01", "name": "Scientific Research Context", "responsibilities": ("research_lifecycle", "scientific_projects", "research_collaboration")},
    {"id": "BC-02", "name": "Science Robotics Context", "responsibilities": ("laboratory_robots", "scientific_automation", "robot_lifecycle")},
    {"id": "BC-03", "name": "Autonomous Laboratory Context", "responsibilities": ("experiment_execution", "lab_workflow_automation", "instrument_coordination")},
    {"id": "BC-04", "name": "AI Scientist Context", "responsibilities": ("hypothesis_generation", "scientific_reasoning", "discovery_assistance")},
    {"id": "BC-05", "name": "Scientific Data Intelligence Context", "responsibilities": ("scientific_datasets", "data_analysis", "research_intelligence")},
    {"id": "BC-06", "name": "Simulation & Modelling Context", "responsibilities": ("scientific_simulation", "predictive_modelling", "experiment_optimisation")},
    {"id": "BC-07", "name": "Scientific Digital Twin Context", "responsibilities": ("laboratory_simulation", "research_environment_modelling", "discovery_forecasting")},
    {"id": "BC-08", "name": "Research Governance Context", "responsibilities": ("ethics", "reproducibility", "scientific_compliance", "human_oversight")},
)
SCIENCE_ROBOTICS = {
    "present_required": True,
    "platform": "meos_science_robotics_platform",
    "components": (
        "scientific_robot_registry",
        "laboratory_robot_controller",
        "experiment_automation_engine",
        "research_instrument_manager",
        "scientific_mission_planner",
        "robotic_laboratory_dashboard",
    ),
    "supported_robotics": (
        "laboratory_manipulation_robots",
        "microscopy_robots",
        "chemical_experiment_robots",
        "biological_research_robots",
        "material_science_robots",
        "scientific_inspection_robots",
    ),
    "capabilities": (
        "experiment_automation",
        "sample_handling",
        "instrument_operation",
        "research_workflow_execution",
        "laboratory_optimisation",
    ),
}
AUTONOMOUS_LABORATORY = {
    "present_required": True,
    "platform": "meos_autonomous_laboratory_intelligence_platform",
    "capabilities": (
        "automated_experiments",
        "robot_human_collaboration",
        "laboratory_scheduling",
        "instrument_optimisation",
        "experiment_monitoring",
        "research_workflow_automation",
    ),
    "laboratory_intelligence": (
        "smart_laboratory_operations",
        "self_optimising_experiments",
        "automated_data_collection",
        "experiment_reproducibility",
    ),
}
AI_SCIENTIST = {
    "present_required": True,
    "engine": "meos_ai_scientist_engine",
    "capabilities": (
        "hypothesis_generation",
        "scientific_reasoning",
        "literature_intelligence",
        "experiment_planning",
        "research_recommendation",
        "discovery_prediction",
    ),
    "models": (
        "scientific_foundation_models",
        "research_language_models",
        "simulation_models",
        "discovery_prediction_models",
        "knowledge_reasoning_models",
    ),
    "via_p214_z": True,
    "explainable_ai": True,
    "human_scientific_oversight": True,
    "responsible_ai": True,
}
DISCOVERY_ACCELERATION = {
    "present_required": True,
    "engine": "meos_scientific_discovery_engine",
    "capabilities": (
        "discovery_identification",
        "pattern_discovery",
        "research_acceleration",
        "cross_domain_knowledge_discovery",
        "innovation_recommendation",
        "scientific_breakthrough_prediction",
    ),
}
RESEARCH_AUTOMATION = {
    "present_required": True,
    "platform": "meos_research_automation_platform",
    "capabilities": (
        "experiment_design",
        "workflow_orchestration",
        "instrument_scheduling",
        "result_validation",
    ),
}
SCIENTIFIC_DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_scientific_digital_twin_platform",
    "represents": (
        "laboratories", "experiments", "scientific_instruments", "research_projects",
        "scientific_models", "datasets", "research_networks", "discovery_processes",
    ),
    "capabilities": (
        "experiment_simulation",
        "research_scenario_modelling",
        "laboratory_optimisation",
        "discovery_forecasting",
        "scientific_planning",
    ),
}
SCIENTIFIC_KG = {
    "present_required": True,
    "graph": "meos_scientific_knowledge_graph",
    "nodes": (
        "research_papers", "experiments", "researchers", "datasets", "models",
        "hypotheses", "discoveries", "laboratories", "scientific_concepts",
    ),
    "relationships": (
        "studies", "proves", "uses", "depends_on",
        "supports", "contradicts", "validates", "discovers",
    ),
    "enables": (
        "scientific_reasoning",
        "research_intelligence",
        "knowledge_discovery",
        "innovation_acceleration",
    ),
}
OBSERVABILITY = {
    "present_required": True,
    "platform": "meos_science_observability_platform",
    "monitors": (
        "experiment_performance",
        "robot_operations",
        "ai_scientist_accuracy",
        "research_productivity",
        "discovery_quality",
        "data_integrity",
        "digital_twin_accuracy",
        "scientific_kpis",
    ),
    "via_platform_observability": True,
}
SECURITY = {
    "present_required": True,
    "framework": "meos_scientific_zero_trust_framework",
    "domains": (
        "research_identity",
        "laboratory_security",
        "scientific_data_protection",
        "ai_model_protection",
        "intellectual_property_protection",
        "research_ethics",
        "audit_governance",
    ),
    "controls": (
        "encryption",
        "access_governance",
        "data_integrity",
        "experiment_traceability",
        "ai_explainability",
        "research_compliance",
    ),
    "zero_trust": True,
    "human_scientific_oversight": True,
    "reproducibility_by_design": True,
    "research_ethics_governance": True,
    "explainable_ai": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "via_integration_platform": True,
    "no_module_local_llm": True,
    "physical_ai_via_p214z_acl_only": True,
    "never_replace_p216_foundation": True,
    "never_replace_p216_u_defense": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "ungated_physical_autonomy_strategy_forbidden": True,
    "opaque_safety_strategy_forbidden": True,
}
COMMANDS = (
    "CreateResearchProjectCommand",
    "GenerateHypothesisCommand",
    "DesignExperimentCommand",
    "ExecuteRobotExperimentCommand",
    "ValidateDiscoveryCommand",
    "UpdateScientificTwinCommand",
)
QUERIES = (
    "GetResearchStatusQuery",
    "GetExperimentResultQuery",
    "GetScientificModelQuery",
    "GetDiscoveryAnalysisQuery",
    "GetLaboratoryTwinQuery",
)
CORE_EVENTS = (
    {"name": "ResearchCreatedEvent", "schema": "robotics.science.research.created.v1", "owner": "BC-01", "consumers": "lab,ai,audit"},
    {"name": "HypothesisGeneratedEvent", "schema": "robotics.science.hypothesis.generated.v1", "owner": "BC-04", "consumers": "lab,governance,audit"},
    {"name": "ExperimentCompletedEvent", "schema": "robotics.science.experiment.completed.v1", "owner": "BC-03", "consumers": "discovery,twin,audit"},
    {"name": "ScientificDiscoveryEvent", "schema": "robotics.science.discovery.detected.v1", "owner": "BC-04", "consumers": "kg,governance,audit"},
    {"name": "ModelUpdatedEvent", "schema": "robotics.science.model.updated.v1", "owner": "BC-06", "consumers": "twin,ai,audit"},
    {"name": "ValidationCompletedEvent", "schema": "robotics.science.validation.completed.v1", "owner": "BC-08", "consumers": "discovery,analytics,audit"},
    {"name": "KnowledgeExpandedEvent", "schema": "robotics.science.knowledge.expanded.v1", "owner": "BC-05", "consumers": "kg,analytics,audit"},
)
MICROSERVICES = (
    {"id": "scientific_research_service", "bc": "BC-01", "api": "/robotics/science/research", "db": "robotics_*", "events": ("ResearchCreatedEvent",), "security": ("robotics.write",), "scaling": "research_workers", "responsibility": "Scientific research project projections"},
    {"id": "science_robotics_service", "bc": "BC-02", "api": "/robotics/science/robots", "db": "robotics_*", "events": ("ExperimentCompletedEvent",), "security": ("robotics.write",), "scaling": "robot_workers", "responsibility": "Science robot mission orchestration"},
    {"id": "laboratory_automation_service", "bc": "BC-03", "api": "/robotics/science/laboratory", "db": "robotics_*", "events": ("ExperimentCompletedEvent",), "security": ("robotics.write",), "scaling": "lab_workers", "responsibility": "Autonomous laboratory workflows"},
    {"id": "ai_scientist_service", "bc": "BC-04", "api": "/robotics/science/ai-scientist", "db": "robotics_*", "events": ("HypothesisGeneratedEvent", "ScientificDiscoveryEvent"), "security": ("robotics.write",), "scaling": "ai_workers", "responsibility": "AI Scientist via P214-Z ACL"},
    {"id": "scientific_data_service", "bc": "BC-05", "api": "/robotics/science/data", "db": "robotics_*", "events": ("KnowledgeExpandedEvent",), "security": ("robotics.read",), "scaling": "data_workers", "responsibility": "Scientific data intelligence"},
    {"id": "simulation_service", "bc": "BC-06", "api": "/robotics/science/simulation", "db": "robotics_*", "events": ("ModelUpdatedEvent",), "security": ("robotics.write",), "scaling": "sim_workers", "responsibility": "Scientific simulation and modelling"},
    {"id": "discovery_intelligence_service", "bc": "BC-04", "api": "/robotics/science/discovery", "db": "robotics_*", "events": ("ScientificDiscoveryEvent", "ValidationCompletedEvent"), "security": ("robotics.write",), "scaling": "discovery_workers", "responsibility": "Discovery acceleration facets"},
    {"id": "digital_twin_service", "bc": "BC-07", "api": "/robotics/science/digital-twin", "db": "robotics_*", "events": ("ExperimentCompletedEvent", "ModelUpdatedEvent"), "security": ("robotics.read",), "scaling": "twin_workers", "responsibility": "Scientific digital twin sync"},
    {"id": "knowledge_graph_service", "bc": "BC-07", "api": "/robotics/science/knowledge-graph", "db": "robotics_*", "events": ("KnowledgeExpandedEvent", "ScientificDiscoveryEvent"), "security": ("robotics.read",), "scaling": "kg_workers", "responsibility": "Scientific knowledge graph projections"},
    {"id": "research_analytics_service", "bc": "BC-08", "api": "/robotics/science/analytics", "db": "robotics_*", "events": ("ValidationCompletedEvent", "KnowledgeExpandedEvent"), "security": ("robotics.read",), "scaling": "analytics_workers", "responsibility": "Research analytics and governance facets"},
)
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p216d_robotics_os",
        "p216e_physical_ai",
        "p216i_healthcare",
        "p216j_agriculture_planned",
        "p216m_space_planned",
        "p216n_environmental_planned",
        "p214z_ai_master",
        "p215z_quantum_supreme",
        "research_institutions",
        "scientific_databases",
        "simulation_platforms",
        "supercomputing_platforms",
        "laboratory_information_systems",
        "integration_platform",
    ),
    "mechanisms": (
        "science_apis",
        "robot_mission_interfaces",
        "lims_via_peer_api",
        "scientific_db_via_integration_connectors",
        "science_event_contracts",
    ),
    "via_p216_d": True,
    "via_p216_e": True,
    "via_p216_i": True,
    "via_p214_z": True,
    "via_p215_z": True,
    "via_p213": True,
    "via_integration_platform": True,
    "p216_j_agriculture_planned": True,
    "p216_m_space_planned": True,
    "p216_n_environmental_planned": True,
}
DEPLOYMENT = {
    "present_required": True,
    "model": "hybrid_scientific_intelligence_infrastructure",
    "includes": (
        "laboratory_edge_platform",
        "scientific_cloud_platform",
        "ai_research_compute_cluster",
        "robot_runtime_platform",
        "simulation_cluster",
        "digital_twin_platform",
        "knowledge_graph_platform",
        "analytics_platform",
        "security_operations_platform",
    ),
    "deployment_models": (
        "university_research_lab",
        "corporate_research_center",
        "national_science_platform",
        "global_discovery_network",
    ),
    "cloud_native": True,
    "edge_native": True,
}
TESTING = (
    "scientific_ai_validation",
    "experiment_reproducibility_testing",
    "robot_laboratory_testing",
    "simulation_validation",
    "data_quality_testing",
    "security_testing",
    "performance_testing",
    "research_ethics_testing",
    "human_oversight_testing",
)
API_SURFACES = (
    "/api/v1/robotics/science",
    "/api/v1/robotics/science/vision",
    "/api/v1/robotics/science/domain",
    "/api/v1/robotics/science/bounded-contexts",
    "/api/v1/robotics/science/robotics",
    "/api/v1/robotics/science/autonomous-laboratory",
    "/api/v1/robotics/science/ai-scientist",
    "/api/v1/robotics/science/discovery",
    "/api/v1/robotics/science/research-automation",
    "/api/v1/robotics/science/digital-twin",
    "/api/v1/robotics/science/knowledge-graph",
    "/api/v1/robotics/science/observability",
    "/api/v1/robotics/science/security",
    "/api/v1/robotics/science/cqrs",
    "/api/v1/robotics/science/events",
    "/api/v1/robotics/science/microservices",
    "/api/v1/robotics/science/integration",
    "/api/v1/robotics/science/deployment",
    "/api/v1/robotics/science/testing",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
QUALITY_GATES_REJECT_IF = (
    "science_robotics_platform_is_missing",
    "autonomous_laboratory_platform_is_missing",
    "ai_scientist_platform_is_missing",
    "scientific_discovery_engine_is_missing",
    "research_automation_platform_is_missing",
    "scientific_digital_twin_is_missing",
    "scientific_knowledge_graph_is_missing",
    "security_architecture_is_missing",
    "human_scientific_oversight_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "cloud_edge_deployment_is_missing",
    "enterprise_science_integration_is_missing",
    "testing_architecture_is_missing",
    "sibling_robotics_bc",
    "replace_p216_u_defense",
    "module_local_llm",
    "ungated_physical_autonomy",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Scientific Intelligence Fabric",
        "science_vision": SCIENCE_VISION,
        "mission": MISSION,
        "vision": VISION,
        "builds_on_p216": True,
        "builds_on_p216_u": True,
        "builds_on_p216_i": True,
        "builds_on_p216_e": True,
        "builds_on_p216_d": True,
        "builds_on_p215_z": True,
        "builds_on_p214_z": True,
        "never_replace_p216_u_defense": True,
        "foundation_gate": FOUNDATION_GATE,
        "defense_gate": DEFENSE_GATE,
        "healthcare_gate": HEALTHCARE_GATE,
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
    return dict(SCIENCE_ROBOTICS)

def autonomous_laboratory() -> dict[str, Any]:
    return dict(AUTONOMOUS_LABORATORY)

def ai_scientist() -> dict[str, Any]:
    return dict(AI_SCIENTIST)

def discovery() -> dict[str, Any]:
    return dict(DISCOVERY_ACCELERATION)

def research_automation() -> dict[str, Any]:
    return dict(RESEARCH_AUTOMATION)

def digital_twin() -> dict[str, Any]:
    return dict(SCIENTIFIC_DIGITAL_TWIN)

def knowledge_graph() -> dict[str, Any]:
    return dict(SCIENTIFIC_KG)

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
        "defense_gate_api": "/api/v1/robotics/defense",
        "runtime_gate_api": "/api/v1/robotics/runtime",
    }

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p216_w": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "science_vision": SCIENCE_VISION, "mission": MISSION, "vision": VISION, "principle": SCIENCE_VISION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE, "runtime_gate": RUNTIME_GATE,
        "physical_ai_gate": PHYSICAL_AI_GATE, "industrial_gate": INDUSTRIAL_GATE,
        "logistics_gate": LOGISTICS_GATE, "mobility_gate": MOBILITY_GATE,
        "healthcare_gate": HEALTHCARE_GATE, "construction_gate": CONSTRUCTION_GATE,
        "public_safety_gate": PUBLIC_SAFETY_GATE, "retail_gate": RETAIL_GATE,
        "hospitality_gate": HOSPITALITY_GATE, "education_gate": EDUCATION_GATE,
        "finance_gate": FINANCE_GATE, "government_gate": GOVERNMENT_GATE,
        "defense_gate": DEFENSE_GATE,
        "supreme_gate": SUPREME_GATE, "ai_gate": AI_GATE,
        "builds_on": [
            "P216", "P216-A", "P216-B", "P216-C", "P216-D", "P216-E", "P216-F", "P216-G", "P216-H",
            "P216-I", "P216-K", "P216-L", "P216-O", "P216-P", "P216-Q", "P216-R", "P216-T", "P216-U",
            "P215-Z", "P214-Z", "P213",
            "ADR-472", "ADR-473", "ADR-474", "ADR-475", "ADR-476", "ADR-477", "ADR-478", "ADR-479",
            "ADR-480", "ADR-481", "ADR-483", "ADR-484", "ADR-487", "ADR-488", "ADR-489", "ADR-490",
            "ADR-492", "ADR-493",
        ],
        "vision_pack": vision_pack(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "robotics_platform": robotics_platform(),
        "autonomous_laboratory": autonomous_laboratory(),
        "ai_scientist": ai_scientist(),
        "discovery": discovery(),
        "research_automation": research_automation(),
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
        "science_robotics_platform_present_required": True,
        "autonomous_laboratory_platform_present_required": True,
        "ai_scientist_platform_present_required": True,
        "scientific_discovery_engine_present_required": True,
        "research_automation_platform_present_required": True,
        "scientific_digital_twin_present_required": True,
        "scientific_knowledge_graph_present_required": True,
        "security_architecture_present_required": True,
        "human_scientific_oversight_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "cloud_edge_deployment_present_required": True,
        "enterprise_science_integration_present_required": True,
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
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "no_module_local_llm": True,
        "physical_ai_via_p214z_acl_only": True,
        "human_scientific_oversight_required": True,
        "reproducibility_by_design_required": True,
        "research_ethics_governance_required": True,
        "explainable_ai_required": True,
        "ungated_physical_autonomy_strategy_forbidden": True,
        "opaque_safety_strategy_forbidden": True,
        "builds_on_p216": True, "builds_on_p216_u": True, "builds_on_p216_i": True,
        "builds_on_p216_e": True, "builds_on_p216_d": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p216_d": True, "via_p216_e": True, "via_p216_i": True,
        "via_p215_z": True, "via_p214_z": True, "via_p213": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "via_integration_platform": True,
        "api_prefix": f"{API_PREFIX}/science",
        "forbidden_sibling_bc": [
            "science_robotics_platform",
            "autonomous_laboratory_platform",
            "scientific_ai_intelligence_platform",
            "ai_scientist_platform",
        ],
        "foundation_for_p216_w": True,
        "p216_j_agriculture_planned": True,
        "p216_m_space_planned": True,
        "p216_n_environmental_planned": True,
        "p216_s_legal_planned": True,
    }

def science_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /robotics/science",
        "GET /robotics/science/vision",
        "GET /robotics/science/domain",
        "GET /robotics/science/bounded-contexts",
        "GET /robotics/science/robotics",
        "GET /robotics/science/autonomous-laboratory",
        "GET /robotics/science/ai-scientist",
        "GET /robotics/science/discovery",
        "GET /robotics/science/research-automation",
        "GET /robotics/science/digital-twin",
        "GET /robotics/science/knowledge-graph",
        "GET /robotics/science/observability",
        "GET /robotics/science/security",
        "GET /robotics/science/cqrs",
        "GET /robotics/science/events",
        "GET /robotics/science/microservices",
        "GET /robotics/science/integration",
        "GET /robotics/science/deployment",
        "GET /robotics/science/testing",
        "GET /robotics/science/readiness",
    ], "defense_gate_routes": ["GET /robotics/defense", "GET /robotics/defense/readiness"]}
