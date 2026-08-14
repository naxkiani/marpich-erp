"""P218-K Enterprise Space Intelligence Scientific Intelligence — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P218-K"
ADR = 537
SOR = "space"
API_PREFIX = "/api/v1/space"
PRODUCT = "Enterprise Space Intelligence Scientific Intelligence & MEOS Scientific Intelligence Platform"
CAPABILITY = "CAP-PLT-SP-001"
SCIENTIFIC_MISSION = (
    "Create an enterprise scientific platform capable of autonomously generating hypotheses, "
    "conducting experiments, analysing results and accelerating scientific discovery throughout "
    "the Solar System and beyond."
)
SCIENTIFIC_VISION = (
    "Transform fragmented space research into an explainable, FAIR-compliant, human-supervised "
    "scientific intelligence fabric spanning observation through publication and long-term knowledge preservation."
)
FABRIC = "meos_scientific_intelligence_fabric"
FOUNDATION_GATE = "P218"
MISSION_GATE = "P218-A"
STRATEGY_GATE = "P218-B"
DOMAIN_GATE = "P218-C"
INFRASTRUCTURE_GATE = "P218-D"
SPACE_AI_GATE = "P218-E"
SATELLITE_GATE = "P218-F"
ORBITAL_GATE = "P218-G"
COMMUNICATIONS_GATE = "P218-H"
NAVIGATION_GATE = "P218-I"
MISSION_INTEL_GATE = "P218-J"
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

ARCHITECTURE_LAYERS = (
    {"id": "L01", "name": "Scientific Data Layer", "components": ("mission_data", "scientific_data_lake", "samples", "experiment_archive")},
    {"id": "L02", "name": "Research Platform Layer", "components": ("experiment_manager", "hypothesis_manager", "simulation", "scientific_notebook")},
    {"id": "L03", "name": "Scientific Intelligence Layer", "components": ("scientific_ai", "discovery_engine", "pattern_recognition", "knowledge_extraction")},
    {"id": "L04", "name": "Laboratory Intelligence Layer", "components": ("autonomous_lab", "instrument_orchestration", "calibration", "safety")},
    {"id": "L05", "name": "Knowledge & Collaboration Layer", "components": ("knowledge_graph", "peer_review", "publication", "innovation_marketplace")},
)
LIFECYCLE_STAGES = (
    "proposal", "approval", "planning", "preparation", "execution",
    "monitoring", "analysis", "validation", "publication", "archival",
)
RESEARCH = {
    "present_required": True,
    "platform": "meos_space_research_platform",
    "domains": (
        "planetary_science", "astrobiology", "heliophysics", "space_physics", "astronomy",
        "geology", "materials_science", "life_sciences", "microgravity", "space_medicine",
    ),
    "services": (
        "research_portfolio", "research_lifecycle", "research_funding", "research_scheduling",
        "research_governance", "research_metrics", "research_knowledge_management", "collaboration",
    ),
}
DISCOVERY = {
    "present_required": True,
    "platform": "meos_autonomous_scientific_discovery_platform",
    "workflow": (
        "observation", "hypothesis_generation", "experiment_design", "simulation", "execution",
        "validation", "analysis", "knowledge_creation", "publication", "continuous_learning",
    ),
    "ai_capabilities": (
        "hypothesis_generation", "pattern_discovery", "novelty_detection", "knowledge_synthesis",
        "scientific_recommendations", "research_prioritisation", "literature_analysis", "discovery_confidence_scoring",
    ),
}
LABORATORY = {
    "present_required": True,
    "platform": "meos_space_laboratory_intelligence_platform",
    "types": (
        "orbital", "lunar", "planetary", "deep_space", "mobile", "robotic", "virtual", "hybrid",
    ),
    "capabilities": (
        "experiment_automation", "instrument_scheduling", "sample_management", "environmental_control",
        "laboratory_robotics", "remote_operation", "safety_monitoring", "scientific_validation",
    ),
    "via_p216_z": True,
    "never_ungated_autonomous_experiment_execution": True,
}
SCIENTIFIC_AI = {
    "present_required": True,
    "platform": "meos_scientific_ai_platform",
    "capabilities": (
        "scientific_copilot", "research_assistant", "experiment_advisor", "discovery_assistant",
        "literature_intelligence", "research_translator", "scientific_validator", "scientific_reviewer",
        "hypothesis_generation", "knowledge_synthesis",
    ),
    "models": (
        {"id": "MODEL-01", "name": "Scientific Foundation Model"},
        {"id": "MODEL-02", "name": "Research Language Model"},
        {"id": "MODEL-03", "name": "Experiment Planning Model"},
        {"id": "MODEL-04", "name": "Scientific Reasoning Model"},
        {"id": "MODEL-05", "name": "Discovery Prediction Model"},
        {"id": "MODEL-06", "name": "Laboratory Control Model"},
        {"id": "MODEL-07", "name": "Publication Intelligence Model"},
        {"id": "MODEL-08", "name": "Knowledge Synthesis Model"},
    ),
    "via_p214_z": True,
    "via_p218_e": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
}
EXPERIMENT = {
    "present_required": True,
    "platform": "meos_experiment_management_platform",
    "categories": (
        "physical", "chemical", "biological", "materials",
        "astronomical", "planetary", "environmental", "computational",
    ),
    "services": (
        "experiment_proposal", "experiment_approval", "experiment_planning", "experiment_execution",
        "experiment_monitoring", "experiment_analysis", "experiment_validation", "experiment_archival",
    ),
}
DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_scientific_digital_twin",
    "represents": ("laboratories", "experiments", "instruments", "samples", "mission_environment", "planetary_environment", "researchers", "research_assets"),
    "capabilities": ("experiment_simulation", "instrument_simulation", "failure_simulation", "scientific_forecasting", "parameter_optimisation", "virtual_experimentation", "scientific_validation", "mission_replay"),
}
GOVERNANCE = {
    "present_required": True,
    "domains": (
        "research_governance", "experiment_governance", "scientific_ethics", "data_governance",
        "publication_governance", "knowledge_governance", "laboratory_governance", "ai_governance",
    ),
    "approval_gates": (
        "concept_approval", "ethics_review", "experiment_approval", "peer_review",
        "reproducibility_validation", "publication_approval", "knowledge_preservation",
    ),
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "never_skip_scientific_ethics_review": True,
    "never_skip_peer_review_gate": True,
    "never_skip_reproducibility_validation": True,
    "never_ungated_autonomous_experiment_execution": True,
    "never_violate_fair_data_principles": True,
}
OBSERVABILITY = {
    "present_required": True,
    "dashboards": (
        "research_portfolio", "active_experiments", "laboratory_status", "scientific_discoveries",
        "knowledge_growth", "publication_pipeline", "ai_recommendations", "research_collaboration",
    ),
    "kpis": (
        "experiment_success_rate", "scientific_discovery_rate", "research_throughput",
        "publication_velocity", "knowledge_reuse", "laboratory_utilisation",
        "ai_recommendation_accuracy", "scientific_impact_index",
        "research_collaboration_score", "innovation_velocity",
    ),
}
BOUNDED_CONTEXTS = (
    {"id": "BC-SCI-01", "name": "Scientific Intelligence Platform"},
    {"id": "BC-SCI-02", "name": "Space Research"},
    {"id": "BC-SCI-03", "name": "Autonomous Discovery"},
    {"id": "BC-SCI-04", "name": "Laboratory Operations"},
    {"id": "BC-SCI-05", "name": "Scientific AI"},
    {"id": "BC-SCI-06", "name": "Experiment Management"},
    {"id": "BC-SCI-07", "name": "Scientific Digital Twin"},
    {"id": "BC-SCI-08", "name": "Scientific Governance"},
)
SECURITY = {
    "present_required": True,
    "controls": (
        "zero_trust", "scientific_authentication", "scientific_authorization", "data_provenance",
        "sample_chain_of_custody", "human_override", "ethics_evidence", "peer_review",
    ),
    "via_identity": True, "via_policy_engine": True, "via_workflow": True,
    "via_audit": True, "via_integration": True,
    "never_ungated_autonomous_experiment_execution": True,
    "never_skip_scientific_ethics_review": True,
    "never_skip_peer_review_gate": True,
    "never_skip_reproducibility_validation": True,
    "never_violate_fair_data_principles": True,
    "never_replace_p218_j_mission_intel": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
}
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p218_foundation", "p218a_mission", "p218b_strategy", "p218c_domain",
        "p218d_infrastructure", "p218e_space_ai", "p218f_satellite", "p218g_orbital",
        "p218h_communications", "p218i_navigation", "p218j_mission_intel",
        "p217z_bio_nexus", "p216z_robotics_supreme", "p215z_quantum_supreme", "p214z_ai_master",
        "policy_engine", "workflow", "audit", "identity", "integration_platform",
        "knowledge_graph", "digital_twin",
    ),
    "mechanisms": ("api_gateway", "event_bus", "acl_peer_ids_only", "outbox", "versioned_contracts"),
}
DEPLOYMENT = {
    "present_required": True,
    "environments": ("research_planning", "laboratory_simulation", "laboratory_operations", "scientific_archive"),
    "cloud_native": True,
    "fair_data_principles": True,
}
COMMANDS = (
    "CreateResearchProjectCommand", "GenerateHypothesisCommand", "ApproveExperimentCommand",
    "StartExperimentCommand", "ValidateReproducibilityCommand", "SubmitPublicationCommand",
    "UpdateKnowledgeGraphCommand", "ArchiveExperimentCommand",
)
QUERIES = (
    "GetResearchProjectQuery", "GetExperimentQuery", "GetDiscoveryQuery",
    "GetLaboratoryStatusQuery", "GetPublicationQuery", "GetKnowledgeLineageQuery",
)
CORE_EVENTS = (
    {"name": "ResearchCreatedEvent", "schema": "space.scientific.research.created.v1", "owner": "BC-SCI-02"},
    {"name": "HypothesisGeneratedEvent", "schema": "space.scientific.hypothesis.generated.v1", "owner": "BC-SCI-03"},
    {"name": "ExperimentApprovedEvent", "schema": "space.scientific.experiment.approved.v1", "owner": "BC-SCI-06"},
    {"name": "ExperimentStartedEvent", "schema": "space.scientific.experiment.started.v1", "owner": "BC-SCI-06"},
    {"name": "ExperimentCompletedEvent", "schema": "space.scientific.experiment.completed.v1", "owner": "BC-SCI-06"},
    {"name": "DiscoveryDetectedEvent", "schema": "space.scientific.discovery.detected.v1", "owner": "BC-SCI-03"},
    {"name": "PublicationSubmittedEvent", "schema": "space.scientific.publication.submitted.v1", "owner": "BC-SCI-08"},
    {"name": "PublicationPublishedEvent", "schema": "space.scientific.publication.published.v1", "owner": "BC-SCI-08"},
    {"name": "KnowledgeGraphUpdatedEvent", "schema": "space.scientific.knowledge.updated.v1", "owner": "BC-SCI-01"},
    {"name": "ScientificBreakthroughIdentifiedEvent", "schema": "space.scientific.breakthrough.identified.v1", "owner": "BC-SCI-03"},
)
MICROSERVICES = (
    {"id": "scientific_intel_service", "api": "/space/scientific", "events": ("ResearchCreatedEvent",)},
    {"id": "research_service", "api": "/space/scientific/research", "events": ("ResearchCreatedEvent",)},
    {"id": "discovery_service", "api": "/space/scientific/discovery", "events": ("DiscoveryDetectedEvent",)},
    {"id": "laboratory_service", "api": "/space/scientific/laboratory", "events": ("ExperimentStartedEvent",)},
    {"id": "scientific_ai_service", "api": "/space/scientific/scientific-ai", "events": ("HypothesisGeneratedEvent",)},
    {"id": "experiment_service", "api": "/space/scientific/experiment", "events": ("ExperimentCompletedEvent",)},
    {"id": "scientific_twin_service", "api": "/space/scientific/digital-twin", "events": ("ExperimentApprovedEvent",)},
    {"id": "scientific_observability_service", "api": "/space/scientific/observability", "events": ("ScientificBreakthroughIdentifiedEvent",)},
    {"id": "scientific_governance_service", "api": "/space/scientific/governance", "events": ("PublicationPublishedEvent",)},
    {"id": "scientific_security_service", "api": "/space/scientific/security", "events": ("PublicationSubmittedEvent",)},
)
TESTING = (
    "research_lifecycle_testing", "discovery_workflow_testing", "laboratory_automation_testing",
    "scientific_ai_explainability_testing", "experiment_orchestration_testing", "digital_twin_testing",
    "ethics_review_gate_testing", "reproducibility_validation_testing",
)
ROADMAP_PHASES = (
    {"phase": 1, "name": "Scientific Foundation"},
    {"phase": 2, "name": "Laboratory Intelligence"},
    {"phase": 3, "name": "Autonomous Discovery"},
    {"phase": 4, "name": "Enterprise Scientific Intelligence"},
)
QUALITY_GATES_REJECT_IF = (
    "scientific_intelligence_platform_is_missing", "space_research_platform_is_missing",
    "autonomous_scientific_discovery_is_missing", "space_laboratory_intelligence_is_missing",
    "scientific_ai_is_missing", "experiment_management_is_missing",
    "scientific_digital_twin_is_missing", "scientific_governance_is_missing",
    "security_architecture_is_missing", "observability_is_missing",
    "ungated_autonomous_experiment_execution", "skip_scientific_ethics_review",
    "skip_peer_review_gate", "skip_reproducibility_validation", "violate_fair_data_principles",
    "replace_p218_j_mission_intel", "module_local_llm", "sibling_space_bc",
)


def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Scientific Intelligence Fabric", "mission": SCIENTIFIC_MISSION,
        "vision": SCIENTIFIC_VISION, "builds_on_p218": True,
        **{f"builds_on_p218_{x.lower()}": True for x in "ABCDEFGHIJ"},
        "builds_on_p217_z": True, "builds_on_p216_z": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "never_replace_p218_j_mission_intel": True,
        "never_ungated_autonomous_experiment_execution": True,
        "never_skip_scientific_ethics_review": True,
        "never_skip_peer_review_gate": True,
        "never_skip_reproducibility_validation": True,
        "never_violate_fair_data_principles": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
    }


def architecture() -> dict[str, Any]:
    return {"present_required": True, "layers": [dict(x) for x in ARCHITECTURE_LAYERS], "layer_count": len(ARCHITECTURE_LAYERS)}


def lifecycle() -> dict[str, Any]:
    return {
        "present_required": True, "stages": list(LIFECYCLE_STAGES), "stage_count": len(LIFECYCLE_STAGES),
        "ethics_review_required": True, "peer_review_gated": True,
        "reproducibility_validation_required": True, "fair_data_principles": True,
    }


def research() -> dict[str, Any]:
    return dict(RESEARCH) | {"domain_count": len(RESEARCH["domains"]), "service_count": len(RESEARCH["services"])}


def discovery() -> dict[str, Any]:
    return dict(DISCOVERY) | {"workflow_step_count": len(DISCOVERY["workflow"]), "ai_capability_count": len(DISCOVERY["ai_capabilities"])}


def laboratory() -> dict[str, Any]:
    return dict(LABORATORY) | {"type_count": len(LABORATORY["types"]), "capability_count": len(LABORATORY["capabilities"])}


def scientific_ai() -> dict[str, Any]:
    return dict(SCIENTIFIC_AI) | {"capability_count": len(SCIENTIFIC_AI["capabilities"]), "model_count": len(SCIENTIFIC_AI["models"])}


def experiment() -> dict[str, Any]:
    return dict(EXPERIMENT) | {"category_count": len(EXPERIMENT["categories"]), "service_count": len(EXPERIMENT["services"])}


def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN) | {"representation_count": len(DIGITAL_TWIN["represents"]), "capability_count": len(DIGITAL_TWIN["capabilities"])}


def governance() -> dict[str, Any]:
    return dict(GOVERNANCE) | {"domain_count": len(GOVERNANCE["domains"]), "approval_gate_count": len(GOVERNANCE["approval_gates"])}


def observability() -> dict[str, Any]:
    return dict(OBSERVABILITY) | {"dashboard_count": len(OBSERVABILITY["dashboards"]), "kpi_count": len(OBSERVABILITY["kpis"])}


def security() -> dict[str, Any]:
    return dict(SECURITY)


def bounded_contexts() -> dict[str, Any]:
    return {"present_required": True, "contexts": [dict(x) for x in BOUNDED_CONTEXTS], "context_count": len(BOUNDED_CONTEXTS)}


def integration() -> dict[str, Any]:
    return dict(INTEGRATION)


def deployment() -> dict[str, Any]:
    return dict(DEPLOYMENT)


def cqrs() -> dict[str, Any]:
    return {"present_required": True, "commands": list(COMMANDS), "queries": list(QUERIES)}


def events() -> dict[str, Any]:
    return {"present_required": True, "core_events": [dict(x) for x in CORE_EVENTS], "core_event_count": len(CORE_EVENTS)}


def microservices() -> dict[str, Any]:
    return {"present_required": True, "services": [dict(x) for x in MICROSERVICES], "service_count": len(MICROSERVICES)}


def testing() -> dict[str, Any]:
    return {"present_required": True, "suites": list(TESTING)}


def roadmap() -> dict[str, Any]:
    return {"present_required": True, "phases": [dict(x) for x in ROADMAP_PHASES], "phase_count": len(ROADMAP_PHASES)}


def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF)}


def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p218_l": True}


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT,
        "capability": CAPABILITY, "scientific_mission": SCIENTIFIC_MISSION,
        "scientific_vision": SCIENTIFIC_VISION, "principle": SCIENTIFIC_MISSION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "infrastructure_gate": INFRASTRUCTURE_GATE, "space_ai_gate": SPACE_AI_GATE,
        "satellite_gate": SATELLITE_GATE, "orbital_gate": ORBITAL_GATE,
        "communications_gate": COMMUNICATIONS_GATE, "navigation_gate": NAVIGATION_GATE,
        "mission_intel_gate": MISSION_INTEL_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P218"] + [f"P218-{x}" for x in "ABCDEFGHIJ"] + ["P217-Z", "P216-Z", "P215-Z", "P214-Z"] + [f"ADR-{i}" for i in range(526, 537)],
        "vision": vision_pack(), "architecture": architecture(), "lifecycle": lifecycle(),
        "research": research(), "discovery": discovery(), "laboratory": laboratory(),
        "scientific_ai": scientific_ai(), "experiment": experiment(),
        "digital_twin": digital_twin(),
        "governance": governance(), "observability": observability(), "security": security(),
        "bounded_contexts": bounded_contexts(), "integration": integration(),
        "deployment": deployment(), "cqrs": cqrs(), "events": events(),
        "microservices": microservices(), "testing": testing(), "roadmap": roadmap(),
        "quality_gates": quality_gates(), "production_readiness": production_readiness(),
        "scientific_intelligence_platform_present_required": True,
        "space_research_platform_present_required": True,
        "autonomous_scientific_discovery_present_required": True,
        "space_laboratory_intelligence_present_required": True,
        "scientific_ai_present_required": True,
        "experiment_management_present_required": True,
        "scientific_digital_twin_present_required": True,
        "ddd_model_present_required": True, "scientific_governance_present_required": True,
        "security_architecture_present_required": True, "observability_present_required": True,
        "deployment_architecture_present_required": True, "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True, "microservices_architecture_present_required": True,
        "sibling_space_bc_forbidden": True,
        "never_replace_p218_j_mission_intel": True,
        "never_ungated_autonomous_experiment_execution": True,
        "never_skip_scientific_ethics_review": True,
        "never_skip_peer_review_gate": True,
        "never_skip_reproducibility_validation": True,
        "never_violate_fair_data_principles": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
        "api_prefix": f"{API_PREFIX}/scientific",
        "forbidden_sibling_bc": ["scientific_intelligence_platform", "space_research_bc", "laboratory_intelligence_bc"],
        "foundation_for_p218_l": True,
    }


def scientific_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /space/scientific", "GET /space/scientific/vision",
        "GET /space/scientific/architecture", "GET /space/scientific/lifecycle",
        "GET /space/scientific/research", "GET /space/scientific/discovery",
        "GET /space/scientific/laboratory", "GET /space/scientific/scientific-ai",
        "GET /space/scientific/experiment", "GET /space/scientific/digital-twin",
        "GET /space/scientific/observability", "GET /space/scientific/governance",
        "GET /space/scientific/security", "GET /space/scientific/integration",
        "GET /space/scientific/deployment", "GET /space/scientific/testing",
        "GET /space/scientific/cqrs", "GET /space/scientific/events",
        "GET /space/scientific/readiness",
    ]}
