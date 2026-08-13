"""P217 Enterprise Biotechnology / Bio Intelligence Foundation — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P217"
ADR = 499
SOR = "biotechnology"
API_PREFIX = "/api/v1/biotechnology"
PRODUCT = (
    "Enterprise Biotechnology, Synthetic Biology, Bio-AI Intelligence, "
    "Digital Health Evolution & MEOS Bio Intelligence Platform"
)
CAPABILITY = "CAP-PLT-BIO-001"
BIO_VISION = (
    "MEOS Bio Intelligence Platform SHALL unify biotechnology, synthetic biology, "
    "bio-AI, digital health and precision medicine as intelligent participants "
    "within the MEOS Bio Intelligence Ecosystem."
)
MISSION = (
    "Create an AI-native biological intelligence ecosystem "
    "that connects biotechnology, synthetic biology, health intelligence, "
    "biological research and human wellness systems "
    "into a unified enterprise intelligence platform."
)
VISION = (
    "Every biological system, health condition, genetic profile, "
    "biological process, scientific discovery and medical innovation "
    "shall become an intelligent participant inside "
    "MEOS BIO INTELLIGENCE ECOSYSTEM."
)
FABRIC = "meos_bio_intelligence_fabric"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"
CORE_DOMAIN = "enterprise_biological_intelligence_management"
AGGREGATE = "BioIntelligenceAggregate"

SUPPORTING_DOMAINS = (
    "biotechnology_research",
    "synthetic_biology_engineering",
    "bioinformatics",
    "computational_biology",
    "digital_health_intelligence",
    "precision_medicine",
    "biological_simulation",
    "bio_manufacturing",
    "healthcare_intelligence",
    "bio_knowledge_management",
    "bio_governance",
)
ENTITIES = (
    "BiologicalEntity",
    "ResearchProject",
    "SyntheticOrganism",
    "GenomeProfile",
    "HealthProfile",
    "BioModel",
    "ClinicalDataset",
    "BiologicalDigitalTwin",
    "TherapeuticSolution",
    "ScientificDiscovery",
)
VALUE_OBJECTS = (
    "GeneticProfile",
    "BiologicalState",
    "HealthRiskScore",
    "ResearchConfidence",
    "TreatmentResponse",
    "BiologicalSimilarity",
    "SafetyScore",
    "ComplianceStatus",
)
BOUNDED_CONTEXTS = (
    {"id": "BC-01", "name": "Biotechnology Research Context", "responsibilities": ("biotechnology_lifecycle", "research_management", "scientific_discovery")},
    {"id": "BC-02", "name": "Synthetic Biology Context", "responsibilities": ("biological_engineering", "synthetic_systems", "bio_design")},
    {"id": "BC-03", "name": "Bioinformatics Intelligence Context", "responsibilities": ("biological_data_analysis", "genome_intelligence", "molecular_insights")},
    {"id": "BC-04", "name": "Bio-AI Intelligence Context", "responsibilities": ("ai_biology_models", "biological_reasoning", "prediction_intelligence")},
    {"id": "BC-05", "name": "Digital Health Intelligence Context", "responsibilities": ("health_intelligence", "personal_health_analytics", "digital_medicine")},
    {"id": "BC-06", "name": "Precision Medicine Context", "responsibilities": ("personalised_treatment", "health_optimisation", "clinical_intelligence")},
    {"id": "BC-07", "name": "Biological Digital Twin Context", "responsibilities": ("human_biological_modelling", "simulation", "prediction")},
    {"id": "BC-08", "name": "Bio Governance Context", "responsibilities": ("ethics", "regulation", "safety", "compliance")},
)
SYNTHETIC_BIOLOGY = {
    "present_required": True,
    "platform": "meos_synthetic_biology_intelligence_platform",
    "capabilities": (
        "biological_design_automation",
        "synthetic_pathway_engineering",
        "bio_simulation",
        "genetic_optimisation",
        "biological_system_modelling",
        "bio_manufacturing_intelligence",
    ),
    "components": (
        "bio_design_engine",
        "synthetic_model_generator",
        "biological_simulation_engine",
        "bio_validation_framework",
        "synthetic_workflow_manager",
    ),
}
BIO_AI = {
    "present_required": True,
    "engine": "meos_bio_ai_intelligence_core",
    "capabilities": (
        "biological_reasoning",
        "disease_prediction",
        "molecular_intelligence",
        "research_acceleration",
        "scientific_discovery",
        "health_optimisation",
    ),
    "models": (
        "biology_foundation_models",
        "protein_intelligence_models",
        "genome_intelligence_models",
        "molecular_prediction_models",
        "clinical_reasoning_models",
    ),
    "via_p214_z": True,
    "module_local_llm_forbidden": True,
    "explainable_bio_ai": True,
    "scientific_reproducibility": True,
}
DIGITAL_HEALTH = {
    "present_required": True,
    "platform": "meos_digital_health_intelligence_platform",
    "capabilities": (
        "health_monitoring",
        "predictive_healthcare",
        "personal_wellness_intelligence",
        "clinical_decision_support",
        "healthcare_automation",
    ),
    "integrations": (
        "medical_devices",
        "wearables",
        "healthcare_systems",
        "patient_data_platforms",
        "healthcare_robotics",
    ),
    "never_replace_hospital_emr": True,
    "privacy_first_healthcare": True,
}
PRECISION_MEDICINE = {
    "present_required": True,
    "platform": "meos_precision_intelligence_platform",
    "capabilities": (
        "personalised_treatment",
        "genomic_analysis",
        "drug_response_prediction",
        "disease_prevention",
        "health_optimisation",
    ),
    "components": (
        "genomic_intelligence_engine",
        "clinical_ai_engine",
        "treatment_simulation_engine",
        "patient_intelligence_model",
    ),
}
BIOLOGICAL_DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_biological_digital_twin_universe",
    "represents": (
        "human_biology", "cells", "organs", "genomes",
        "diseases", "therapeutic_responses", "biological_processes",
    ),
    "capabilities": (
        "simulation",
        "prediction",
        "health_forecasting",
        "treatment_optimisation",
        "research_acceleration",
    ),
}
LIFE_SCIENCE_KG = {
    "present_required": True,
    "graph": "meos_life_science_knowledge_graph",
    "nodes": (
        "genes", "proteins", "cells", "organisms", "diseases",
        "treatments", "research_papers", "clinical_data", "scientists",
    ),
    "relationships": (
        "causes", "influences", "treats", "depends_on",
        "expresses", "validates", "discovers",
    ),
    "enables": (
        "biological_reasoning",
        "scientific_discovery",
        "health_intelligence",
        "research_acceleration",
    ),
}
BIO_ETHICS_GOVERNANCE = {
    "present_required": True,
    "framework": "meos_bio_trust_framework",
    "responsibilities": ("ethics", "regulation", "safety", "compliance"),
    "ethical_bioengineering": True,
    "scientific_reproducibility": True,
    "opaque_bio_safety_decisions_forbidden": True,
}
OBSERVABILITY = {
    "present_required": True,
    "platform": "meos_bio_observability_platform",
    "monitors": (
        "research_performance",
        "ai_model_accuracy",
        "biological_simulation_quality",
        "health_intelligence_accuracy",
        "clinical_outcomes",
        "data_integrity",
        "safety_metrics",
        "innovation_progress",
    ),
    "via_platform_observability": True,
}
SECURITY = {
    "present_required": True,
    "framework": "meos_bio_trust_framework",
    "domains": (
        "biological_data",
        "genomic_privacy",
        "research_assets",
        "synthetic_designs",
        "clinical_intelligence",
        "bio_ai_models",
    ),
    "controls": (
        "encryption",
        "access_governance",
        "audit_intelligence",
        "ethical_review",
        "compliance_management",
        "data_sovereignty",
    ),
    "zero_trust": True,
    "genomic_privacy": True,
    "ethical_bioengineering": True,
    "scientific_reproducibility": True,
    "human_centered_health_intelligence": True,
    "privacy_first_healthcare": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "via_integration_platform": True,
    "never_replace_identity_platform": True,
    "never_replace_hospital_emr": True,
    "never_replace_laboratory_lims": True,
    "never_replace_pharmacy": True,
    "never_replace_robotics_supreme": True,
    "no_module_local_llm": True,
    "physical_ai_via_p214z_acl_only": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "opaque_bio_safety_decisions_forbidden": True,
}
COMMANDS = (
    "CreateBioResearchProjectCommand",
    "AnalyzeGenomeCommand",
    "DesignSyntheticSystemCommand",
    "GenerateHealthInsightCommand",
    "UpdateBioDigitalTwinCommand",
    "ValidateTherapeuticSolutionCommand",
)
QUERIES = (
    "GetBiologicalProfileQuery",
    "GetGenomeAnalysisQuery",
    "GetHealthPredictionQuery",
    "GetDigitalTwinStateQuery",
    "GetResearchDiscoveryQuery",
)
CORE_EVENTS = (
    {"name": "BioProjectCreatedEvent", "schema": "biotechnology.foundation.project.created.v1", "owner": "BC-01", "consumers": "governance,kg,audit"},
    {"name": "GenomeProcessedEvent", "schema": "biotechnology.foundation.genome.processed.v1", "owner": "BC-03", "consumers": "precision,twin,audit"},
    {"name": "SyntheticDesignCompletedEvent", "schema": "biotechnology.foundation.synthetic.completed.v1", "owner": "BC-02", "consumers": "governance,bio_ai,audit"},
    {"name": "HealthInsightCreatedEvent", "schema": "biotechnology.foundation.health.insight.created.v1", "owner": "BC-05", "consumers": "precision,analytics,audit"},
    {"name": "TreatmentValidatedEvent", "schema": "biotechnology.foundation.treatment.validated.v1", "owner": "BC-06", "consumers": "governance,twin,audit"},
    {"name": "DiscoveryGeneratedEvent", "schema": "biotechnology.foundation.discovery.generated.v1", "owner": "BC-04", "consumers": "research,kg,audit"},
    {"name": "BiologicalTwinUpdatedEvent", "schema": "biotechnology.foundation.twin.updated.v1", "owner": "BC-07", "consumers": "precision,analytics,audit"},
)
MICROSERVICES = (
    {"id": "biotechnology_service", "bc": "BC-01", "api": "/biotechnology/foundation/research", "db": "biotechnology_*", "events": ("BioProjectCreatedEvent",), "security": ("biotechnology.write",), "scaling": "research_workers", "responsibility": "Biotechnology research project projections"},
    {"id": "synthetic_biology_service", "bc": "BC-02", "api": "/biotechnology/foundation/synthetic", "db": "biotechnology_*", "events": ("SyntheticDesignCompletedEvent",), "security": ("biotechnology.write",), "scaling": "synthetic_workers", "responsibility": "Synthetic biology design workflows"},
    {"id": "bioinformatics_service", "bc": "BC-03", "api": "/biotechnology/foundation/bioinformatics", "db": "biotechnology_*", "events": ("GenomeProcessedEvent",), "security": ("biotechnology.read",), "scaling": "bioinfo_workers", "responsibility": "Bioinformatics and genome intelligence"},
    {"id": "bio_ai_service", "bc": "BC-04", "api": "/biotechnology/foundation/bio-ai", "db": "biotechnology_*", "events": ("DiscoveryGeneratedEvent",), "security": ("biotechnology.ai.infer",), "scaling": "bio_ai_workers", "responsibility": "Bio-AI via P214-Z ACL"},
    {"id": "digital_health_service", "bc": "BC-05", "api": "/biotechnology/foundation/digital-health", "db": "biotechnology_*", "events": ("HealthInsightCreatedEvent",), "security": ("biotechnology.write",), "scaling": "health_workers", "responsibility": "Digital health intelligence projections"},
    {"id": "precision_medicine_service", "bc": "BC-06", "api": "/biotechnology/foundation/precision", "db": "biotechnology_*", "events": ("TreatmentValidatedEvent", "GenomeProcessedEvent"), "security": ("biotechnology.write",), "scaling": "precision_workers", "responsibility": "Precision medicine facets"},
    {"id": "biological_twin_service", "bc": "BC-07", "api": "/biotechnology/foundation/digital-twin", "db": "biotechnology_*", "events": ("BiologicalTwinUpdatedEvent",), "security": ("biotechnology.read",), "scaling": "twin_workers", "responsibility": "Biological digital twin sync"},
    {"id": "knowledge_graph_service", "bc": "BC-01", "api": "/biotechnology/foundation/knowledge-graph", "db": "biotechnology_*", "events": ("DiscoveryGeneratedEvent", "BioProjectCreatedEvent"), "security": ("biotechnology.read",), "scaling": "kg_workers", "responsibility": "Life science knowledge graph"},
    {"id": "research_intelligence_service", "bc": "BC-04", "api": "/biotechnology/foundation/research-intelligence", "db": "biotechnology_*", "events": ("DiscoveryGeneratedEvent",), "security": ("biotechnology.read",), "scaling": "research_intel_workers", "responsibility": "Research intelligence analytics"},
    {"id": "governance_service", "bc": "BC-08", "api": "/biotechnology/foundation/governance", "db": "biotechnology_*", "events": ("TreatmentValidatedEvent", "SyntheticDesignCompletedEvent"), "security": ("biotechnology.admin",), "scaling": "governance_workers", "responsibility": "Bio ethics and governance"},
)
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p214z_ai_master",
        "p215z_quantum_supreme",
        "p216z_robotics_supreme",
        "meos_data_intelligence",
        "meos_security_platform",
        "meos_knowledge_graph_platform",
        "healthcare_ecosystems",
        "research_institutions",
        "scientific_computing_platforms",
        "laboratory_robotics",
        "integration_platform",
    ),
    "mechanisms": (
        "biotechnology_apis",
        "peer_fabric_acl",
        "healthcare_via_peer_api",
        "bio_event_contracts",
    ),
    "via_p214_z": True,
    "via_p215_z": True,
    "via_p216_z": True,
    "via_p213": True,
    "via_identity": True,
    "via_integration_platform": True,
    "never_replace_identity_platform": True,
    "never_replace_hospital_emr": True,
    "never_replace_laboratory_lims": True,
    "never_replace_pharmacy": True,
}
DEPLOYMENT = {
    "present_required": True,
    "model": "hybrid_bio_intelligence_infrastructure",
    "includes": (
        "bio_edge_intelligence",
        "scientific_cloud_platform",
        "ai_biology_compute_cluster",
        "biological_digital_twin_platform",
        "knowledge_graph_platform",
        "healthcare_intelligence_platform",
        "security_operations_platform",
    ),
    "deployment_models": (
        "research_laboratory",
        "healthcare_enterprise",
        "biotechnology_company",
        "national_health_platform",
        "global_bio_intelligence_ecosystem",
    ),
    "cloud_native": True,
    "edge_native": True,
}
TESTING = (
    "scientific_validation_testing",
    "biological_model_testing",
    "ai_accuracy_testing",
    "clinical_validation",
    "privacy_testing",
    "security_testing",
    "simulation_validation",
    "ethical_compliance_testing",
    "reproducibility_testing",
)
API_SURFACES = (
    "/api/v1/biotechnology/foundation",
    "/api/v1/biotechnology/foundation/vision",
    "/api/v1/biotechnology/foundation/domain",
    "/api/v1/biotechnology/foundation/bounded-contexts",
    "/api/v1/biotechnology/foundation/synthetic-biology",
    "/api/v1/biotechnology/foundation/bio-ai",
    "/api/v1/biotechnology/foundation/digital-health",
    "/api/v1/biotechnology/foundation/precision-medicine",
    "/api/v1/biotechnology/foundation/digital-twin",
    "/api/v1/biotechnology/foundation/knowledge-graph",
    "/api/v1/biotechnology/foundation/governance",
    "/api/v1/biotechnology/foundation/observability",
    "/api/v1/biotechnology/foundation/security",
    "/api/v1/biotechnology/foundation/cqrs",
    "/api/v1/biotechnology/foundation/events",
    "/api/v1/biotechnology/foundation/microservices",
    "/api/v1/biotechnology/foundation/integration",
    "/api/v1/biotechnology/foundation/deployment",
    "/api/v1/biotechnology/foundation/testing",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
QUALITY_GATES_REJECT_IF = (
    "biotechnology_platform_is_missing",
    "synthetic_biology_platform_is_missing",
    "bio_ai_intelligence_engine_is_missing",
    "digital_health_platform_is_missing",
    "precision_medicine_platform_is_missing",
    "biological_digital_twin_is_missing",
    "life_science_knowledge_graph_is_missing",
    "bio_ethics_governance_is_missing",
    "security_architecture_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "cloud_edge_deployment_is_missing",
    "enterprise_bio_integration_is_missing",
    "testing_architecture_is_missing",
    "sibling_biotechnology_bc",
    "replace_hospital_emr",
    "replace_laboratory_lims",
    "replace_pharmacy",
    "module_local_llm",
    "opaque_bio_safety_decisions",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Bio Intelligence Fabric",
        "bio_vision": BIO_VISION,
        "mission": MISSION,
        "vision": VISION,
        "builds_on_p216_z": True,
        "builds_on_p215_z": True,
        "builds_on_p214_z": True,
        "never_replace_robotics_supreme": True,
        "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE,
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

def synthetic_biology() -> dict[str, Any]:
    return dict(SYNTHETIC_BIOLOGY)

def bio_ai() -> dict[str, Any]:
    return dict(BIO_AI)

def digital_health() -> dict[str, Any]:
    return dict(DIGITAL_HEALTH)

def precision_medicine() -> dict[str, Any]:
    return dict(PRECISION_MEDICINE)

def digital_twin() -> dict[str, Any]:
    return dict(BIOLOGICAL_DIGITAL_TWIN)

def knowledge_graph() -> dict[str, Any]:
    return dict(LIFE_SCIENCE_KG)

def governance() -> dict[str, Any]:
    return dict(BIO_ETHICS_GOVERNANCE)

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
        "robotics_gate_api": "/api/v1/robotics/supreme",
    }

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p217_a": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "bio_vision": BIO_VISION, "mission": MISSION, "vision": VISION, "principle": BIO_VISION,
        "fabric": FABRIC, "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P214-Z", "P215-Z", "P216-Z", "P213", "ADR-498", "ADR-471"],
        "vision_pack": vision_pack(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "synthetic_biology": synthetic_biology(),
        "bio_ai": bio_ai(),
        "digital_health": digital_health(),
        "precision_medicine": precision_medicine(),
        "digital_twin": digital_twin(),
        "knowledge_graph": knowledge_graph(),
        "governance": governance(),
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
        "biotechnology_platform_present_required": True,
        "synthetic_biology_platform_present_required": True,
        "bio_ai_intelligence_engine_present_required": True,
        "digital_health_platform_present_required": True,
        "precision_medicine_platform_present_required": True,
        "biological_digital_twin_present_required": True,
        "life_science_knowledge_graph_present_required": True,
        "bio_ethics_governance_present_required": True,
        "security_architecture_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "cloud_edge_deployment_present_required": True,
        "enterprise_bio_integration_present_required": True,
        "testing_architecture_present_required": True,
        "sibling_biotechnology_bc_forbidden": True,
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_replace_robotics_supreme": True,
        "never_replace_hospital_emr": True,
        "never_replace_laboratory_lims": True,
        "never_replace_pharmacy": True,
        "never_replace_identity_platform": True,
        "no_module_local_llm": True,
        "physical_ai_via_p214z_acl_only": True,
        "genomic_privacy_required": True,
        "ethical_bioengineering_required": True,
        "scientific_reproducibility_required": True,
        "human_centered_health_intelligence_required": True,
        "privacy_first_healthcare_required": True,
        "opaque_bio_safety_decisions_forbidden": True,
        "builds_on_p216_z": True, "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p216_z": True, "via_p215_z": True, "via_p214_z": True, "via_p213": True,
        "via_identity": True, "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "via_integration_platform": True,
        "api_prefix": f"{API_PREFIX}/foundation",
        "forbidden_sibling_bc": [
            "biotechnology_platform",
            "bio_ai_platform",
            "synthetic_biology_platform",
            "digital_health_platform",
        ],
        "foundation_for_p217_a": True,
    }

def foundation_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /biotechnology/foundation",
        "GET /biotechnology/foundation/vision",
        "GET /biotechnology/foundation/domain",
        "GET /biotechnology/foundation/bounded-contexts",
        "GET /biotechnology/foundation/synthetic-biology",
        "GET /biotechnology/foundation/bio-ai",
        "GET /biotechnology/foundation/digital-health",
        "GET /biotechnology/foundation/precision-medicine",
        "GET /biotechnology/foundation/digital-twin",
        "GET /biotechnology/foundation/knowledge-graph",
        "GET /biotechnology/foundation/governance",
        "GET /biotechnology/foundation/observability",
        "GET /biotechnology/foundation/security",
        "GET /biotechnology/foundation/cqrs",
        "GET /biotechnology/foundation/events",
        "GET /biotechnology/foundation/microservices",
        "GET /biotechnology/foundation/integration",
        "GET /biotechnology/foundation/deployment",
        "GET /biotechnology/foundation/testing",
        "GET /biotechnology/foundation/readiness",
    ]}
