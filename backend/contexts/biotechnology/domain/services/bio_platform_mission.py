"""P217-A Enterprise Biotechnology Mission, Vision & Strategic Scope — immutable catalog."""
from __future__ import annotations
from typing import Any
PROMPT_ID = "P217-A"
ADR = 500
SOR = "biotechnology"
API_PREFIX = "/api/v1/biotechnology"
PRODUCT = "Enterprise Biotechnology Mission, Vision, Strategic Scope & Bio Intelligence Capability Framework"
CAPABILITY = "CAP-PLT-BIO-001"
MISSION = (
    "Build the world's most advanced enterprise biological intelligence ecosystem by combining "
    "Artificial Intelligence + Quantum Computing + Robotics Automation + Synthetic Biology + "
    "Digital Health Intelligence to transform biological research, healthcare, life science innovation "
    "and human wellbeing into an intelligent, connected and continuously evolving ecosystem."
)
VISION = (
    "Create a future where every biological system, health process, scientific discovery, "
    "therapeutic pathway and biological innovation can be understood, modelled, simulated "
    "and optimized through a unified intelligence ecosystem."
)
FABRIC = "meos_bio_intelligence_strategic_framework"
FOUNDATION_GATE = "P217"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"
CORE_DOMAIN = "enterprise_biotechnology_strategy_management"
SUPPORTING_DOMAINS = (
    {"id": "bio_vision", "purpose": "Long-term bio intelligence future 2040+."},
    {"id": "strategic_purposes", "purpose": "P01..P05 strategic purposes."},
    {"id": "strategic_objectives", "purpose": "OBJ-01..07 biotechnology objectives."},
    {"id": "bio_intelligence_domains", "purpose": "Six bio intelligence domains."},
    {"id": "capability_framework", "purpose": "Foundation through future capability levels."},
    {"id": "value_streams", "purpose": "Discovery, healthcare, synthetic, research acceleration."},
    {"id": "maturity_model", "purpose": "Five bio intelligence maturity levels."},
    {"id": "governance_strategy", "purpose": "Ethical, scientific, healthcare governance."},
    {"id": "evolution_roadmap", "purpose": "Five-phase biotechnology evolution."},
)
LOGICAL_BOUNDED_CONTEXTS = (
    {"id": "mission_vision", "bc": "BC-01", "name": "Bio Mission and Vision Context", "purpose": "Mission, vision, and strategic intent."},
    {"id": "strategic_scope", "bc": "BC-02", "name": "Strategic Scope and Purpose Context", "purpose": "Purposes and strategic objectives."},
    {"id": "capability_framework", "bc": "BC-03", "name": "Bio Capability Framework Context", "purpose": "Capability levels and domains."},
    {"id": "value_streams", "bc": "BC-04", "name": "Bio Value Streams Context", "purpose": "Enterprise biotechnology value streams."},
    {"id": "maturity_model", "bc": "BC-05", "name": "Bio Maturity Model Context", "purpose": "Maturity levels 01-05."},
    {"id": "governance_strategy", "bc": "BC-06", "name": "Bio Governance Strategy Context", "purpose": "Scientific and ethical governance."},
    {"id": "integration_evolution", "bc": "BC-07", "name": "Integration and Evolution Roadmap Context", "purpose": "MEOS peers and evolution phases."},
)
VISION_FUTURE_STATE = ("observable", "understandable", "predictable", "simulatable", "optimizable", "intelligent")
STRATEGIC_PURPOSES = (
    {"id": "P01", "name": "Transform traditional biology into digital intelligence"},
    {"id": "P02", "name": "Create AI-powered biological discovery systems"},
    {"id": "P03", "name": "Enable precision health intelligence"},
    {"id": "P04", "name": "Accelerate biotechnology innovation"},
    {"id": "P05", "name": "Connect biological intelligence with the complete MEOS ecosystem"},
)
STRATEGIC_OBJECTIVES = (
    {"id": "OBJ-01", "name": "Bio Intelligence Infrastructure", "capabilities": ("enterprise_bio_intelligence", "bio_data_infrastructure", "scientific_computing")},
    {"id": "OBJ-02", "name": "Synthetic Biology Acceleration", "capabilities": ("biological_design", "synthetic_engineering", "bio_manufacturing")},
    {"id": "OBJ-03", "name": "Digital Health Evolution", "capabilities": ("predictive_health", "clinical_analytics", "wellness_optimisation")},
    {"id": "OBJ-04", "name": "Scientific Discovery Acceleration", "capabilities": ("ai_research", "automated_workflows", "pattern_discovery")},
    {"id": "OBJ-05", "name": "Biological Digital Twin Development", "capabilities": ("biological_simulation", "health_forecasting", "intervention_optimisation")},
    {"id": "OBJ-06", "name": "Life Science Knowledge Intelligence", "capabilities": ("knowledge_graph", "global_bio_networks", "scientific_intelligence")},
    {"id": "OBJ-07", "name": "Responsible Biotechnology Governance", "capabilities": ("ethical_bioengineering", "safety_controls", "human_oversight")},
)
STRATEGIC_SCOPE = {
    "present_required": True,
    "bridge_statement": "Biological Intelligence is the bridge between MEOS multi-dimensional intelligence and living systems.",
    "in_scope": (
        "biotechnology_intelligence", "synthetic_biology", "bio_ai", "digital_health_intelligence",
        "precision_medicine_intelligence", "biological_digital_twins", "bioinformatics",
        "life_science_knowledge", "responsible_bio_governance", "scientific_workflows",
        "genomic_privacy", "sustainable_bioengineering",
    ),
    "out_of_scope_owned_elsewhere": (
        "hospital_emr", "laboratory_lims", "pharmacy_dispensing", "robotics_supreme_control",
        "quantum_supreme_core", "module_local_llm",
    ),
}
BIO_DOMAINS = (
    {"id": "DOMAIN-01", "name": "biotechnology_intelligence", "capabilities": ("bio_research_intelligence", "biological_modelling", "bio_innovation_management", "scientific_intelligence")},
    {"id": "DOMAIN-02", "name": "synthetic_biology_intelligence", "capabilities": ("biological_design", "synthetic_systems_engineering", "bio_manufacturing_intelligence", "biological_optimisation")},
    {"id": "DOMAIN-03", "name": "bio_ai_intelligence", "capabilities": ("biological_reasoning", "ai_biology_models", "pattern_discovery", "predictive_biology")},
    {"id": "DOMAIN-04", "name": "digital_health_intelligence", "capabilities": ("health_prediction", "personal_health_intelligence", "clinical_analytics", "wellness_optimisation")},
    {"id": "DOMAIN-05", "name": "precision_medicine_intelligence", "capabilities": ("personalised_treatment", "genetic_intelligence", "therapeutic_optimisation", "patient_modelling")},
    {"id": "DOMAIN-06", "name": "biological_digital_twin_intelligence", "capabilities": ("biological_simulation", "health_forecasting", "research_modelling", "intervention_optimisation")},
)
CAPABILITY_FRAMEWORK = {
    "present_required": True,
    "levels": (
        {"level": 1, "name": "foundation_capabilities", "capabilities": ("biological_data_management", "bioinformatics", "scientific_computing", "research_management", "biological_knowledge_management")},
        {"level": 2, "name": "advanced_capabilities", "capabilities": ("ai_biology_models", "synthetic_biology_engineering", "molecular_intelligence", "digital_health_analytics", "biological_simulation")},
        {"level": 3, "name": "strategic_capabilities", "capabilities": ("biological_digital_twins", "precision_medicine_intelligence", "autonomous_bio_research", "bio_innovation_networks", "life_intelligence_platforms")},
        {"level": 4, "name": "future_capabilities", "capabilities": ("advanced_human_health_intelligence", "bio_ai_symbiosis", "intelligent_life_systems", "next_generation_biotechnology_ecosystems")},
    ),
}
VALUE_STREAMS = {
    "present_required": True,
    "streams": (
        {"id": "VS-01", "name": "biological_discovery", "input": "scientific_data", "process": ("ai_analysis", "simulation", "validation"), "output": "scientific_discovery"},
        {"id": "VS-02", "name": "healthcare_intelligence", "input": "health_data", "process": ("prediction", "personalisation", "optimisation"), "output": "improved_health_outcomes"},
        {"id": "VS-03", "name": "synthetic_innovation", "input": "biological_knowledge", "process": ("design", "simulation", "engineering"), "output": "synthetic_biological_solutions"},
        {"id": "VS-04", "name": "research_acceleration", "input": "scientific_questions", "process": ("ai_reasoning", "automation", "discovery"), "output": "innovation_acceleration"},
    ),
}
MATURITY_MODEL = {
    "present_required": True,
    "levels": (
        {"level": 1, "name": "digital_biology_foundation", "characteristics": ("data_collection", "bioinformatics", "research_digitisation")},
        {"level": 2, "name": "intelligent_biology", "characteristics": ("ai_analysis", "predictive_models", "knowledge_intelligence")},
        {"level": 3, "name": "autonomous_biology", "characteristics": ("automated_research", "ai_experiments", "intelligent_laboratories")},
        {"level": 4, "name": "synthetic_intelligence_biology", "characteristics": ("synthetic_design", "biological_simulation", "advanced_engineering")},
        {"level": 5, "name": "meos_bio_intelligence_civilization_layer", "characteristics": ("global_biological_intelligence", "life_science_ecosystem", "advanced_human_wellbeing_intelligence")},
    ),
}
GOVERNANCE_STRATEGY = {
    "present_required": True,
    "model": "meos_biotechnology_governance_model",
    "domains": ("scientific_governance", "ethical_governance", "healthcare_governance", "data_governance", "research_governance", "ai_governance", "synthetic_biology_governance"),
    "controls": ("transparency", "safety", "compliance", "human_oversight", "auditability"),
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "opaque_bio_safety_strategy_forbidden": True,
    "genomic_privacy_strategy_required": True,
    "ethical_bioengineering_strategy_required": True,
    "scientific_integrity_strategy_required": True,
}
SECURITY_STRATEGY = {
    "present_required": True,
    "framework": "meos_bio_strategy_trust_framework",
    "includes": ("bio_privacy", "research_protection", "healthcare_security", "genomic_data_protection", "strategy_access_controls"),
    "via_identity": True,
    "zero_trust": True,
}
INTEGRATION_STRATEGY = {
    "present_required": True,
    "peers": ("P214-Z", "P215-Z", "P216-Z", "MEOS Data Intelligence", "MEOS Security Platform", "Policy Engine", "Workflow", "Audit", "Integration Platform"),
    "integrations": (
        {"peer": "P214-Z", "includes": ("ai_biology_models", "ai_agents", "reasoning_systems")},
        {"peer": "P215-Z", "includes": ("quantum_biology_simulation", "molecular_computing", "advanced_optimisation")},
        {"peer": "P216-Z", "includes": ("autonomous_laboratories", "bio_robotics", "scientific_automation")},
        {"peer": "data_intelligence", "includes": ("bio_data_lake", "knowledge_graph", "analytics")},
        {"peer": "security", "includes": ("bio_privacy", "research_protection", "healthcare_security")},
    ),
    "via_p214_z": True,
    "via_p215_z": True,
    "via_p216_z": True,
}
EVOLUTION_ROADMAP = {
    "present_required": True,
    "roadmap": "meos_biotechnology_evolution_roadmap",
    "phases": (
        {"phase": 1, "name": "digital_biology_era", "foundation": ("data", "ai", "analytics")},
        {"phase": 2, "name": "ai_biology_era", "foundation": ("biological_intelligence_models",)},
        {"phase": 3, "name": "synthetic_biology_era", "foundation": ("biological_engineering_intelligence",)},
        {"phase": 4, "name": "biological_digital_twin_era", "foundation": ("simulation_based_biology",)},
        {"phase": 5, "name": "meos_life_intelligence_era", "foundation": ("unified_ai_quantum_robotics_biology_ecosystem",)},
    ),
}
COMMANDS = (
    "CreateBioStrategyCommand", "DefineBioVisionCommand", "AssessBioReadinessCommand",
    "LaunchBioInitiativeCommand", "UpdateBioRoadmapCommand",
)
QUERIES = (
    "GetBioMissionQuery", "GetBioVisionQuery", "GetStrategicScopeQuery",
    "GetCapabilityFrameworkQuery", "GetMaturityStatusQuery",
)
CORE_EVENTS = (
    {"name": "BioStrategyCreatedEvent", "owner": "mission_vision", "consumers": "governance,analytics,audit"},
    {"name": "BioVisionDefinedEvent", "owner": "mission_vision", "consumers": "strategy,foundation"},
    {"name": "StrategicScopePublishedEvent", "owner": "strategic_scope", "consumers": "capability_framework,roadmap"},
    {"name": "BioRoadmapUpdatedEvent", "owner": "integration_evolution", "consumers": "analytics,twin"},
    {"name": "BioReadinessImprovedEvent", "owner": "maturity_model", "consumers": "strategy,notifications"},
)
MICROSERVICES = (
    {"id": "bio_strategy_service", "bc": "BC-01", "api": "/biotechnology/mission", "db": "biotechnology_*", "events": ("BioStrategyCreatedEvent",), "security": ("biotechnology.read",), "scaling": "strategy_replicas"},
    {"id": "bio_vision_service", "bc": "BC-01", "api": "/biotechnology/mission/vision", "db": "biotechnology_*", "events": ("BioVisionDefinedEvent",), "security": ("biotechnology.read",), "scaling": "vision_replicas"},
    {"id": "capability_framework_service", "bc": "BC-03", "api": "/biotechnology/mission/capabilities", "db": "biotechnology_*", "events": ("StrategicScopePublishedEvent",), "security": ("biotechnology.read",), "scaling": "capability_workers"},
    {"id": "value_streams_service", "bc": "BC-04", "api": "/biotechnology/mission/value-streams", "db": "biotechnology_*", "events": ("BioStrategyCreatedEvent",), "security": ("biotechnology.read",), "scaling": "value_replicas"},
    {"id": "maturity_model_service", "bc": "BC-05", "api": "/biotechnology/mission/maturity", "db": "biotechnology_*", "events": ("BioReadinessImprovedEvent",), "security": ("biotechnology.read",), "scaling": "maturity_replicas"},
    {"id": "evolution_roadmap_service", "bc": "BC-07", "api": "/biotechnology/mission/roadmap", "db": "biotechnology_*", "events": ("BioRoadmapUpdatedEvent",), "security": ("biotechnology.write",), "scaling": "roadmap_workers"},
    {"id": "governance_strategy_service", "bc": "BC-06", "api": "/biotechnology/mission/governance", "db": "biotechnology_*", "events": ("BioStrategyCreatedEvent",), "security": ("biotechnology.admin",), "scaling": "governance_replicas"},
    {"id": "integration_strategy_service", "bc": "BC-07", "api": "/biotechnology/mission/integration", "db": "biotechnology_*", "events": ("BioStrategyCreatedEvent",), "security": ("biotechnology.admin",), "scaling": "integration_replicas"},
)
API_SURFACES = (
    "/api/v1/biotechnology/mission",
    "/api/v1/biotechnology/mission/vision",
    "/api/v1/biotechnology/mission/objectives",
    "/api/v1/biotechnology/mission/scope",
    "/api/v1/biotechnology/mission/capabilities",
    "/api/v1/biotechnology/mission/value-streams",
    "/api/v1/biotechnology/mission/maturity",
    "/api/v1/biotechnology/mission/roadmap",
    "/api/v1/biotechnology/mission/governance",
    "/api/v1/biotechnology/mission/integration",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
SECURITY = {
    "present_required": True, "zero_trust": True, "via_identity": True, "via_policy_engine": True,
    "via_workflow": True, "via_audit": True,
    "never_replace_p217_foundation": True, "never_replace_core_platform": True,
    "never_replace_ai_platform": True, "never_replace_p215_z": True, "never_replace_p216_z": True,
    "never_replace_hospital_emr": True, "never_replace_laboratory_lims": True, "never_replace_pharmacy": True,
    "genomic_privacy_strategy_required": True, "ethical_bioengineering_strategy_required": True,
    "scientific_integrity_strategy_required": True, "opaque_bio_safety_strategy_forbidden": True,
    "controls": ("strategy_access_controls", "roadmap_change_controls", "bio_safety_strategy_gates", "mission_audit_controls"),
}
DEPLOYMENT = {
    "present_required": True, "cloud_native": True,
    "components": ("strategy_services_cluster", "capability_framework_service", "roadmap_engine", "strategic_observability"),
}
TESTING = (
    "mission_validation_testing", "vision_alignment_testing", "scope_boundary_testing",
    "capability_framework_testing", "value_stream_testing", "maturity_model_testing",
    "governance_strategy_testing", "integration_strategy_testing",
)
QUALITY_GATES_REJECT_IF = (
    "biotechnology_mission_framework_is_missing", "biotechnology_vision_framework_is_missing",
    "strategic_biotechnology_scope_is_missing", "bio_capability_framework_is_missing",
    "value_streams_framework_is_missing", "maturity_model_is_missing",
    "governance_framework_is_missing", "meos_integration_strategy_is_missing",
    "future_evolution_roadmap_is_missing", "cqrs_architecture_is_missing",
    "event_architecture_is_missing", "microservices_architecture_is_missing",
    "api_first_architecture_is_missing", "cloud_native_deployment_is_missing",
    "sibling_biotechnology_bc", "replace_p217_foundation",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Bio Intelligence Strategic Framework",
        "mission": MISSION, "vision": VISION,
        "future_state": list(VISION_FUTURE_STATE),
        "equation": "AI + Quantum + Robotics + Biological Intelligence = MEOS Multi-Dimensional Intelligence Ecosystem",
        "builds_on_p217": True, "builds_on_p216_z": True, "builds_on_p215_z": True, "builds_on_p214_z": True,
        "never_replace_p217_foundation": True,
        "foundation_gate": FOUNDATION_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
    }

def domain_model() -> dict[str, Any]:
    return {"core_domain": CORE_DOMAIN, "supporting_domains": [dict(d) for d in SUPPORTING_DOMAINS], "supporting_count": len(SUPPORTING_DOMAINS)}

def bounded_contexts() -> dict[str, Any]:
    return {"contexts": [dict(c) for c in LOGICAL_BOUNDED_CONTEXTS], "context_count": len(LOGICAL_BOUNDED_CONTEXTS)}

def mission() -> dict[str, Any]:
    return {"present_required": True, "statement": MISSION}

def bio_vision() -> dict[str, Any]:
    return {"present_required": True, "statement": VISION, "future_state": list(VISION_FUTURE_STATE)}

def purposes() -> dict[str, Any]:
    return {"present_required": True, "purposes": [dict(p) for p in STRATEGIC_PURPOSES], "purpose_count": len(STRATEGIC_PURPOSES)}

def objectives() -> dict[str, Any]:
    return {"present_required": True, "objectives": [dict(o) for o in STRATEGIC_OBJECTIVES], "objective_count": len(STRATEGIC_OBJECTIVES)}

def strategic_scope() -> dict[str, Any]:
    return dict(STRATEGIC_SCOPE)

def bio_domains() -> dict[str, Any]:
    return {"present_required": True, "domains": [dict(d) for d in BIO_DOMAINS], "domain_count": len(BIO_DOMAINS)}

def capability_framework() -> dict[str, Any]:
    return dict(CAPABILITY_FRAMEWORK)

def value_streams() -> dict[str, Any]:
    return dict(VALUE_STREAMS)

def maturity_model() -> dict[str, Any]:
    return dict(MATURITY_MODEL)

def evolution_roadmap() -> dict[str, Any]:
    return dict(EVOLUTION_ROADMAP)

def governance_strategy() -> dict[str, Any]:
    return dict(GOVERNANCE_STRATEGY)

def security_strategy() -> dict[str, Any]:
    return dict(SECURITY_STRATEGY)

def integration_strategy() -> dict[str, Any]:
    return dict(INTEGRATION_STRATEGY)

def cqrs() -> dict[str, Any]:
    return {"commands": list(COMMANDS), "command_count": len(COMMANDS), "queries": list(QUERIES), "query_count": len(QUERIES)}

def events() -> dict[str, Any]:
    return {"core_events": [dict(e) for e in CORE_EVENTS], "core_event_count": len(CORE_EVENTS)}

def microservices() -> dict[str, Any]:
    return {"services": [dict(s) for s in MICROSERVICES], "service_count": len(MICROSERVICES)}

def api() -> dict[str, Any]:
    return {"surfaces": list(API_SURFACES), "styles": list(API_STYLES), "api_first_present_required": True, "foundation_gate_api": "/api/v1/biotechnology/foundation"}

def security() -> dict[str, Any]:
    return dict(SECURITY)

def deployment() -> dict[str, Any]:
    return dict(DEPLOYMENT)

def testing() -> dict[str, Any]:
    return {"suites": list(TESTING), "suite_count": len(TESTING)}

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p217_b": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "mission_statement": MISSION, "vision_statement": VISION, "principle": MISSION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P217", "P216-Z", "P215-Z", "P214-Z", "ADR-499"],
        "vision": vision_pack(), "domain_model": domain_model(), "bounded_contexts": bounded_contexts(),
        "mission": mission(), "bio_vision": bio_vision(), "purposes": purposes(), "objectives": objectives(),
        "strategic_scope": strategic_scope(), "bio_domains": bio_domains(),
        "capability_framework": capability_framework(), "value_streams": value_streams(),
        "maturity_model": maturity_model(), "evolution_roadmap": evolution_roadmap(),
        "governance_strategy": governance_strategy(), "security_strategy": security_strategy(),
        "integration_strategy": integration_strategy(),
        "cqrs": cqrs(), "events": events(), "microservices": microservices(), "api": api(),
        "security": security(), "deployment": deployment(), "testing": testing(),
        "quality_gates": quality_gates(), "production_readiness": production_readiness(),
        "biotechnology_mission_framework_present_required": True,
        "biotechnology_vision_framework_present_required": True,
        "strategic_biotechnology_scope_present_required": True,
        "bio_capability_framework_present_required": True,
        "value_streams_framework_present_required": True,
        "maturity_model_present_required": True,
        "governance_framework_present_required": True,
        "meos_integration_strategy_present_required": True,
        "future_evolution_roadmap_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "cloud_native_deployment_present_required": True,
        "sibling_biotechnology_bc_forbidden": True,
        "never_replace_p217_foundation": True,
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
        "builds_on_p217": True, "builds_on_p216_z": True, "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p216_z": True, "via_p215_z": True, "via_p214_z": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "api_prefix": f"{API_PREFIX}/mission",
        "forbidden_sibling_bc": [
            "biotechnology_mission_platform",
            "bio_vision_platform",
            "bio_strategy_platform",
        ],
        "foundation_for_p217_b": True,
    }

def mission_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /biotechnology/mission",
        "GET /biotechnology/mission/vision",
        "GET /biotechnology/mission/objectives",
        "GET /biotechnology/mission/scope",
        "GET /biotechnology/mission/capabilities",
        "GET /biotechnology/mission/value-streams",
        "GET /biotechnology/mission/maturity",
        "GET /biotechnology/mission/roadmap",
        "GET /biotechnology/mission/governance",
        "GET /biotechnology/mission/integration",
        "GET /biotechnology/mission/readiness",
    ], "foundation_gate_routes": ["GET /biotechnology/foundation", "GET /biotechnology/foundation/readiness"]}
