"""P217-F Enterprise Biotechnology Synthetic Biology Intelligence Platform — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P217-F"
ADR = 505
SOR = "biotechnology"
API_PREFIX = "/api/v1/biotechnology"
PRODUCT = (
    "Enterprise Biotechnology Synthetic Biology Intelligence Platform, "
    "Biological Engineering Automation, Bio Design Intelligence & Synthetic Life Systems Architecture"
)
CAPABILITY = "CAP-PLT-BIO-001"
SYNTHETIC_MISSION = (
    "Create an intelligent biological engineering ecosystem capable of designing, modelling, "
    "optimizing and managing synthetic biological systems through AI, automation and computational intelligence."
)
SYNTHETIC_VISION = (
    "Enable a future where biological systems can be digitally designed, simulated, validated "
    "and responsibly engineered through MEOS intelligence."
)
FABRIC = "meos_synthetic_biology_intelligence_fabric"
FOUNDATION_GATE = "P217"
MISSION_GATE = "P217-A"
STRATEGY_GATE = "P217-B"
DOMAIN_GATE = "P217-C"
INFRASTRUCTURE_GATE = "P217-D"
BIO_AI_GATE = "P217-E"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

FUTURE_EVOLUTION = (
    "biological_observation", "biological_understanding", "biological_design",
    "biological_simulation", "biological_engineering", "synthetic_biological_intelligence",
)
ARCHITECTURE_LAYERS = (
    {"id": "L01", "name": "Biological Knowledge Layer", "responsibilities": ("biological_knowledge_management", "genetic_information", "biological_components", "scientific_intelligence"), "components": ("bio_knowledge_graph", "genetic_library", "biological_component_registry", "scientific_knowledge_base")},
    {"id": "L02", "name": "Bio Design Intelligence Layer", "responsibilities": ("biological_system_design", "synthetic_planning", "optimization"), "components": ("bio_design_engine", "synthetic_design_assistant", "design_recommendation_engine", "ai_engineering_agent")},
    {"id": "L03", "name": "Synthetic Engineering Layer", "responsibilities": ("biological_construction", "engineering_workflows", "system_assembly"), "components": ("engineering_workflow_engine", "bio_assembly_platform", "validation_platform", "experiment_management")},
    {"id": "L04", "name": "Synthetic System Intelligence Layer", "responsibilities": ("synthetic_organism_management", "system_monitoring", "optimization"), "components": ("synthetic_system_twin", "synthetic_lifecycle_manager", "performance_intelligence_engine")},
    {"id": "L05", "name": "Governance & Safety Layer", "responsibilities": ("bio_safety", "regulatory_control", "ethical_governance"), "components": ("bio_safety_engine", "compliance_intelligence", "risk_assessment_platform")},
)
DESIGN_CAPABILITIES = (
    {"id": "CAP-01", "name": "Biological Design Generation", "functions": ("design_recommendations", "component_selection", "architecture_generation", "engineering_planning")},
    {"id": "CAP-02", "name": "Genetic Design Intelligence", "functions": ("sequence_analysis", "genetic_optimization", "design_evaluation", "variant_intelligence")},
    {"id": "CAP-03", "name": "Synthetic System Optimization", "functions": ("performance_prediction", "stability_analysis", "resource_optimization", "improvement_recommendations")},
    {"id": "CAP-04", "name": "AI Engineering Assistant", "functions": ("research_assistance", "design_automation", "experiment_planning", "knowledge_retrieval")},
)
AUTOMATION_DOMAINS = (
    {"id": "DOM-01", "name": "Design Automation", "capabilities": ("automated_biological_design", "ai_generated_engineering_plans", "design_validation")},
    {"id": "DOM-02", "name": "Research Automation", "capabilities": ("experiment_workflows", "automated_analysis", "result_interpretation")},
    {"id": "DOM-03", "name": "Laboratory Automation Integration", "capabilities": ("robotic_laboratory_connection", "instrument_orchestration", "workflow_execution"), "via_p216_z": True},
    {"id": "DOM-04", "name": "Optimization Automation", "capabilities": ("continuous_improvement", "performance_optimization", "adaptive_engineering")},
)
LIFECYCLE_PHASES = (
    {"id": "PHASE-01", "name": "Concept Definition", "activities": ("objective_definition", "biological_requirements", "design_specification")},
    {"id": "PHASE-02", "name": "Digital Design", "activities": ("computational_modelling", "ai_design_generation", "simulation")},
    {"id": "PHASE-03", "name": "Engineering", "activities": ("biological_construction", "system_implementation", "validation")},
    {"id": "PHASE-04", "name": "Monitoring", "activities": ("performance_tracking", "intelligence_analysis", "optimization")},
    {"id": "PHASE-05", "name": "Evolution", "activities": ("adaptive_improvement", "system_enhancement", "lifecycle_management")},
)
DOMAIN_MODELS = (
    {"id": "DOMAIN-01", "name": "Synthetic Design Intelligence Domain", "aggregate": "SyntheticDesignAggregate", "entities": ("DesignSpecification", "BiologicalBlueprint", "DesignVersion", "ComponentSelection"), "events": ("SyntheticDesignCreatedEvent", "DesignOptimizedEvent")},
    {"id": "DOMAIN-02", "name": "Biological Component Intelligence Domain", "aggregate": "BioComponentAggregate", "entities": ("GeneComponent", "ProteinComponent", "BiologicalModule", "GeneticSequence"), "events": ("ComponentRegisteredEvent", "ComponentValidatedEvent")},
    {"id": "DOMAIN-03", "name": "Synthetic Engineering Domain", "aggregate": "EngineeringProjectAggregate", "entities": ("EngineeringProject", "AssemblyWorkflow", "ValidationProcess", "ExperimentPlan"), "events": ("EngineeringStartedEvent", "ValidationCompletedEvent")},
    {"id": "DOMAIN-04", "name": "Synthetic System Intelligence Domain", "aggregate": "SyntheticSystemAggregate", "entities": ("SyntheticSystem", "SystemModel", "PerformanceProfile", "LifecycleState"), "events": ("SyntheticSystemCreatedEvent", "SystemImprovedEvent")},
)
BOUNDED_CONTEXTS = (
    {"id": "BC-01", "name": "Synthetic Biology Platform Context", "responsibilities": ("platform_orchestration", "layer_coordination", "synthetic_lifecycle")},
    {"id": "BC-02", "name": "Synthetic Design Intelligence Context", "responsibilities": ("design_generation", "genetic_optimization", "design_versioning")},
    {"id": "BC-03", "name": "Biological Component Intelligence Context", "responsibilities": ("component_registry", "compatibility", "sequence_identity")},
    {"id": "BC-04", "name": "Synthetic Engineering Context", "responsibilities": ("engineering_projects", "assembly", "validation")},
    {"id": "BC-05", "name": "Synthetic System Intelligence Context", "responsibilities": ("system_twins", "performance", "evolution")},
    {"id": "BC-06", "name": "Bio Manufacturing Intelligence Context", "responsibilities": ("production_optimization", "quality_prediction", "process_intelligence")},
    {"id": "BC-07", "name": "Responsible Synthetic Biology Governance Context", "responsibilities": ("bio_safety", "ethical_review", "release_approval", "human_oversight")},
)
BIO_MANUFACTURING = {
    "present_required": True,
    "platform": "meos_intelligent_bio_manufacturing_platform",
    "capabilities": ("biological_production_optimization", "process_intelligence", "quality_prediction", "manufacturing_automation"),
    "components": ("bio_manufacturing_digital_twin", "process_intelligence_engine", "quality_intelligence_system", "production_optimization_engine"),
    "via_p216_z": True,
}
DIGITAL_TWIN = {
    "present_required": True,
    "platform": "synthetic_biology_digital_twin",
    "functions": ("virtual_biological_modelling", "performance_prediction", "scenario_simulation", "risk_analysis"),
    "before_engineering": ("simulation", "prediction", "optimization"),
}
SYNTHETIC_AGENTS = (
    {"id": "bio_design_agent", "responsibilities": ("generate_biological_designs",)},
    {"id": "engineering_agent", "responsibilities": ("optimize_engineering_workflows",)},
    {"id": "simulation_agent", "responsibilities": ("analyze_synthetic_systems",)},
    {"id": "safety_agent", "responsibilities": ("evaluate_biological_risks",)},
    {"id": "innovation_agent", "responsibilities": ("discover_new_biological_opportunities",)},
)
GOVERNANCE = {
    "present_required": True,
    "framework": "meos_responsible_synthetic_biology_framework",
    "areas": ("biological_safety", "ethical_engineering", "regulatory_compliance", "research_approval", "risk_management"),
    "controls": ("design_review", "safety_validation", "access_control", "audit_trail", "human_approval"),
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "never_opaque_unexplainable_decisions": True,
    "never_unsupervised_synthetic_release": True,
}
SECURITY = {
    "present_required": True,
    "domains": ("design_ip_protection", "sequence_data_protection", "engineering_asset_protection", "bio_safety_controls", "clinical_data_security"),
    "controls": ("encryption", "identity_management", "access_policies", "threat_detection", "secure_design_deployment"),
    "zero_trust": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "bio_ai_via_p214z_acl_only": True,
    "lab_robotics_via_p216z_acl_only": True,
    "no_module_local_llm": True,
    "never_opaque_unexplainable_decisions": True,
    "never_unsupervised_synthetic_release": True,
    "never_replace_p217_foundation": True,
    "never_replace_p217_a_mission": True,
    "never_replace_p217_b_strategy": True,
    "never_replace_p217_c_domain": True,
    "never_replace_p217_d_infrastructure": True,
    "never_replace_p217_e_bio_ai": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "never_replace_p216_z": True,
    "never_replace_hospital_emr": True,
    "never_replace_laboratory_lims": True,
    "never_replace_pharmacy": True,
    "genomic_privacy_strategy_required": True,
    "ethical_bioengineering_strategy_required": True,
    "scientific_integrity_strategy_required": True,
    "opaque_bio_safety_strategy_forbidden": True,
}
INTEGRATION = {
    "present_required": True,
    "targets": ("p214z_ai_master", "p215z_quantum_supreme", "p216z_robotics_supreme", "p217d_bio_infrastructure", "p217e_bio_ai", "meos_knowledge_graph"),
    "mechanisms": ("api_gateway", "event_bus", "acl_peer_ids_only", "inference_intents_not_models", "robotics_orchestration_intents"),
    "via_p214_z": True, "via_p215_z": True, "via_p216_z": True, "via_p217_d": True, "via_p217_e": True,
}
ROADMAP = {
    "present_required": True,
    "phases": (
        {"phase": 1, "name": "AI Assisted Synthetic Biology", "focus": ("ai_design_support", "computational_modelling")},
        {"phase": 2, "name": "Automated Bio Engineering", "focus": ("laboratory_automation", "workflow_intelligence")},
        {"phase": 3, "name": "Synthetic System Intelligence", "focus": ("digital_twins", "adaptive_optimization")},
        {"phase": 4, "name": "MEOS Synthetic Life Intelligence", "focus": ("advanced_biological_intelligence_ecosystem",)},
    ),
}
COMMANDS = (
    "CreateSyntheticDesignCommand", "OptimizeDesignCommand", "StartEngineeringProjectCommand",
    "ValidateAssemblyCommand", "ApproveSyntheticReleaseCommand",
)
QUERIES = (
    "GetSyntheticPlatformQuery", "GetDesignQuery", "GetEngineeringProjectQuery",
    "GetSyntheticSystemQuery", "GetSafetyGovernanceQuery",
)
CORE_EVENTS = (
    {"name": "SyntheticBiologyPlatformActivatedEvent", "schema": "biotechnology.synthetic.platform.activated.v1", "owner": "BC-01", "consumers": "audit,observability,analytics"},
    {"name": "SyntheticDesignCreatedEvent", "schema": "biotechnology.synthetic.design.created.v1", "owner": "BC-02", "consumers": "audit,search,ai"},
    {"name": "DesignOptimizedEvent", "schema": "biotechnology.synthetic.design.optimized.v1", "owner": "BC-02", "consumers": "audit,analytics"},
    {"name": "EngineeringStartedEvent", "schema": "biotechnology.synthetic.engineering.started.v1", "owner": "BC-04", "consumers": "audit,workflow,robotics"},
    {"name": "ValidationCompletedEvent", "schema": "biotechnology.synthetic.validation.completed.v1", "owner": "BC-04", "consumers": "audit,governance"},
    {"name": "SyntheticSystemCreatedEvent", "schema": "biotechnology.synthetic.system.created.v1", "owner": "BC-05", "consumers": "audit,twin,analytics"},
    {"name": "SystemImprovedEvent", "schema": "biotechnology.synthetic.system.improved.v1", "owner": "BC-05", "consumers": "audit,analytics"},
    {"name": "SyntheticSafetyViolationEvent", "schema": "biotechnology.synthetic.safety.violation.v1", "owner": "BC-07", "consumers": "audit,compliance,notifications"},
)
MICROSERVICES = (
    {"id": "synthetic_platform_service", "api": "/biotechnology/synthetic", "db": "biotechnology_*", "events": ("SyntheticBiologyPlatformActivatedEvent",), "security": ("biotechnology.read",), "scaling": "synthetic_replicas"},
    {"id": "bio_design_service", "api": "/biotechnology/synthetic/design", "db": "biotechnology_*", "events": ("SyntheticDesignCreatedEvent", "DesignOptimizedEvent"), "security": ("biotechnology.write",), "scaling": "design_workers"},
    {"id": "engineering_automation_service", "api": "/biotechnology/synthetic/automation", "db": "biotechnology_*", "events": ("EngineeringStartedEvent", "ValidationCompletedEvent"), "security": ("biotechnology.write",), "scaling": "engineering_workers"},
    {"id": "synthetic_lifecycle_service", "api": "/biotechnology/synthetic/lifecycle", "db": "biotechnology_*", "events": ("SyntheticSystemCreatedEvent", "SystemImprovedEvent"), "security": ("biotechnology.read",), "scaling": "lifecycle_workers"},
    {"id": "component_intelligence_service", "api": "/biotechnology/synthetic/domains", "db": "biotechnology_*", "events": ("SyntheticDesignCreatedEvent",), "security": ("biotechnology.read",), "scaling": "component_workers"},
    {"id": "bio_manufacturing_service", "api": "/biotechnology/synthetic/manufacturing", "db": "biotechnology_*", "events": ("SystemImprovedEvent",), "security": ("biotechnology.write",), "scaling": "manufacturing_workers"},
    {"id": "digital_twin_service", "api": "/biotechnology/synthetic/digital-twin", "db": "biotechnology_*", "events": ("SyntheticSystemCreatedEvent",), "security": ("biotechnology.read",), "scaling": "twin_workers"},
    {"id": "synthetic_agent_service", "api": "/biotechnology/synthetic/agents", "db": "biotechnology_*", "events": ("DesignOptimizedEvent",), "security": ("biotechnology.ai.infer",), "scaling": "agent_workers"},
    {"id": "synthetic_governance_service", "api": "/biotechnology/synthetic/governance", "db": "biotechnology_*", "events": ("SyntheticSafetyViolationEvent",), "security": ("biotechnology.admin",), "scaling": "governance_replicas"},
    {"id": "synthetic_integration_service", "api": "/biotechnology/synthetic/integration", "db": "biotechnology_*", "events": ("SyntheticBiologyPlatformActivatedEvent",), "security": ("biotechnology.admin",), "scaling": "integration_workers"},
)
API_SURFACES = (
    "/api/v1/biotechnology/synthetic",
    "/api/v1/biotechnology/synthetic/vision",
    "/api/v1/biotechnology/synthetic/architecture",
    "/api/v1/biotechnology/synthetic/design",
    "/api/v1/biotechnology/synthetic/automation",
    "/api/v1/biotechnology/synthetic/lifecycle",
    "/api/v1/biotechnology/synthetic/domains",
    "/api/v1/biotechnology/synthetic/manufacturing",
    "/api/v1/biotechnology/synthetic/digital-twin",
    "/api/v1/biotechnology/synthetic/agents",
    "/api/v1/biotechnology/synthetic/governance",
    "/api/v1/biotechnology/synthetic/security",
    "/api/v1/biotechnology/synthetic/integration",
    "/api/v1/biotechnology/synthetic/roadmap",
    "/api/v1/biotechnology/synthetic/cqrs",
    "/api/v1/biotechnology/synthetic/events",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
TESTING = (
    "design_validation_testing", "engineering_workflow_testing", "safety_validation_testing",
    "reproducibility_testing", "digital_twin_accuracy_testing", "security_testing", "bias_testing",
)
QUALITY_GATES_REJECT_IF = (
    "synthetic_biology_platform_is_missing", "bio_design_intelligence_is_missing",
    "engineering_automation_is_missing", "synthetic_life_architecture_is_missing",
    "domain_model_is_missing", "ai_agent_ecosystem_is_missing", "safety_governance_is_missing",
    "digital_twin_integration_is_missing", "bio_manufacturing_intelligence_is_missing",
    "security_architecture_is_missing", "cqrs_architecture_is_missing",
    "event_architecture_is_missing", "microservices_architecture_is_missing",
    "sibling_biotechnology_bc", "replace_p217_foundation", "replace_p217_e_bio_ai",
    "module_local_llm", "opaque_unexplainable_decisions", "unsupervised_synthetic_release",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Synthetic Biology Intelligence Fabric",
        "mission": SYNTHETIC_MISSION, "vision": SYNTHETIC_VISION,
        "future_evolution": list(FUTURE_EVOLUTION),
        "builds_on_p217": True, "builds_on_p217_a": True, "builds_on_p217_b": True,
        "builds_on_p217_c": True, "builds_on_p217_d": True, "builds_on_p217_e": True,
        "builds_on_p216_z": True, "builds_on_p215_z": True, "builds_on_p214_z": True,
        "never_replace_p217_e_bio_ai": True,
        "bio_ai_via_p214z_acl_only": True, "lab_robotics_via_p216z_acl_only": True,
        "no_module_local_llm": True, "never_unsupervised_synthetic_release": True,
        "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "infrastructure_gate": INFRASTRUCTURE_GATE, "bio_ai_gate": BIO_AI_GATE,
        "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
    }

def architecture() -> dict[str, Any]:
    return {"present_required": True, "layers": [dict(x) for x in ARCHITECTURE_LAYERS], "layer_count": len(ARCHITECTURE_LAYERS)}

def design_intelligence() -> dict[str, Any]:
    return {"present_required": True, "capabilities": [dict(c) for c in DESIGN_CAPABILITIES], "capability_count": len(DESIGN_CAPABILITIES)}

def engineering_automation() -> dict[str, Any]:
    return {"present_required": True, "domains": [dict(d) for d in AUTOMATION_DOMAINS], "domain_count": len(AUTOMATION_DOMAINS)}

def synthetic_lifecycle() -> dict[str, Any]:
    return {"present_required": True, "phases": [dict(p) for p in LIFECYCLE_PHASES], "phase_count": len(LIFECYCLE_PHASES)}

def domain_models() -> dict[str, Any]:
    return {"present_required": True, "domains": [dict(d) for d in DOMAIN_MODELS], "domain_count": len(DOMAIN_MODELS)}

def bounded_contexts() -> dict[str, Any]:
    return {"present_required": True, "contexts": [dict(c) for c in BOUNDED_CONTEXTS], "context_count": len(BOUNDED_CONTEXTS)}

def bio_manufacturing() -> dict[str, Any]:
    return dict(BIO_MANUFACTURING)

def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN)

def synthetic_agents() -> dict[str, Any]:
    return {"present_required": True, "agents": [dict(a) for a in SYNTHETIC_AGENTS], "agent_count": len(SYNTHETIC_AGENTS)}

def governance() -> dict[str, Any]:
    return dict(GOVERNANCE)

def security() -> dict[str, Any]:
    return dict(SECURITY)

def integration() -> dict[str, Any]:
    return dict(INTEGRATION)

def roadmap() -> dict[str, Any]:
    return dict(ROADMAP) | {"phase_count": len(ROADMAP["phases"])}

def cqrs() -> dict[str, Any]:
    return {"commands": list(COMMANDS), "command_count": len(COMMANDS), "queries": list(QUERIES), "query_count": len(QUERIES)}

def events() -> dict[str, Any]:
    return {"core_events": [dict(e) for e in CORE_EVENTS], "core_event_count": len(CORE_EVENTS)}

def microservices() -> dict[str, Any]:
    return {"services": [dict(s) for s in MICROSERVICES], "service_count": len(MICROSERVICES)}

def testing() -> dict[str, Any]:
    return {"present_required": True, "suites": list(TESTING), "suite_count": len(TESTING)}

def api() -> dict[str, Any]:
    return {
        "surfaces": list(API_SURFACES), "styles": list(API_STYLES), "api_first_present_required": True,
        "foundation_gate_api": "/api/v1/biotechnology/foundation",
        "mission_gate_api": "/api/v1/biotechnology/mission",
        "strategy_gate_api": "/api/v1/biotechnology/strategy",
        "domain_gate_api": "/api/v1/biotechnology/domain",
        "infrastructure_gate_api": "/api/v1/biotechnology/infrastructure",
        "bio_ai_gate_api": "/api/v1/biotechnology/bio-ai",
    }

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p217_g": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "synthetic_mission": SYNTHETIC_MISSION, "synthetic_vision": SYNTHETIC_VISION, "principle": SYNTHETIC_MISSION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "infrastructure_gate": INFRASTRUCTURE_GATE, "bio_ai_gate": BIO_AI_GATE,
        "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P217", "P217-A", "P217-B", "P217-C", "P217-D", "P217-E", "P216-Z", "P215-Z", "P214-Z", "ADR-499", "ADR-500", "ADR-501", "ADR-502", "ADR-503", "ADR-504"],
        "vision": vision_pack(),
        "architecture": architecture(),
        "design_intelligence": design_intelligence(),
        "engineering_automation": engineering_automation(),
        "synthetic_lifecycle": synthetic_lifecycle(),
        "domain_models": domain_models(),
        "bounded_contexts": bounded_contexts(),
        "bio_manufacturing": bio_manufacturing(),
        "digital_twin": digital_twin(),
        "synthetic_agents": synthetic_agents(),
        "governance": governance(),
        "security": security(),
        "integration": integration(),
        "roadmap": roadmap(),
        "cqrs": cqrs(), "events": events(), "microservices": microservices(),
        "api": api(), "testing": testing(), "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "synthetic_biology_platform_present_required": True,
        "bio_design_intelligence_present_required": True,
        "engineering_automation_present_required": True,
        "synthetic_life_architecture_present_required": True,
        "domain_model_present_required": True,
        "ai_agent_ecosystem_present_required": True,
        "safety_governance_present_required": True,
        "digital_twin_integration_present_required": True,
        "bio_manufacturing_intelligence_present_required": True,
        "security_architecture_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "sibling_biotechnology_bc_forbidden": True,
        "never_replace_p217_foundation": True,
        "never_replace_p217_a_mission": True,
        "never_replace_p217_b_strategy": True,
        "never_replace_p217_c_domain": True,
        "never_replace_p217_d_infrastructure": True,
        "never_replace_p217_e_bio_ai": True,
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_replace_p216_z": True,
        "never_replace_hospital_emr": True,
        "never_replace_laboratory_lims": True,
        "never_replace_pharmacy": True,
        "bio_ai_via_p214z_acl_only": True,
        "lab_robotics_via_p216z_acl_only": True,
        "no_module_local_llm": True,
        "never_opaque_unexplainable_decisions": True,
        "never_unsupervised_synthetic_release": True,
        "genomic_privacy_strategy_required": True,
        "ethical_bioengineering_strategy_required": True,
        "scientific_integrity_strategy_required": True,
        "opaque_bio_safety_strategy_forbidden": True,
        "builds_on_p217": True, "builds_on_p217_a": True, "builds_on_p217_b": True,
        "builds_on_p217_c": True, "builds_on_p217_d": True, "builds_on_p217_e": True,
        "builds_on_p216_z": True, "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p216_z": True, "via_p215_z": True, "via_p214_z": True, "via_p217_d": True, "via_p217_e": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "api_prefix": f"{API_PREFIX}/synthetic",
        "forbidden_sibling_bc": [
            "synthetic_biology_platform",
            "bio_design_intelligence_platform",
            "synthetic_life_systems_platform",
        ],
        "foundation_for_p217_g": True,
    }

def synthetic_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /biotechnology/synthetic",
        "GET /biotechnology/synthetic/vision",
        "GET /biotechnology/synthetic/architecture",
        "GET /biotechnology/synthetic/design",
        "GET /biotechnology/synthetic/automation",
        "GET /biotechnology/synthetic/lifecycle",
        "GET /biotechnology/synthetic/domains",
        "GET /biotechnology/synthetic/manufacturing",
        "GET /biotechnology/synthetic/digital-twin",
        "GET /biotechnology/synthetic/agents",
        "GET /biotechnology/synthetic/governance",
        "GET /biotechnology/synthetic/security",
        "GET /biotechnology/synthetic/integration",
        "GET /biotechnology/synthetic/roadmap",
        "GET /biotechnology/synthetic/cqrs",
        "GET /biotechnology/synthetic/events",
        "GET /biotechnology/synthetic/readiness",
    ], "bio_ai_gate_routes": ["GET /biotechnology/bio-ai"],
       "infrastructure_gate_routes": ["GET /biotechnology/infrastructure"]}
