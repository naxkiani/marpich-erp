"""P215-Q Enterprise Quantum Research, Innovation Lab, Discovery & Future Evolution — immutable catalog."""
from __future__ import annotations
from typing import Any
PROMPT_ID = "P215-Q"
ADR = 462
SOR = "quantum"
API_PREFIX = "/api/v1/quantum"
PRODUCT = "Enterprise Quantum Research, Quantum Innovation Lab, Scientific Collaboration & Future Quantum Intelligence Evolution Platform"
CAPABILITY = "CAP-PLT-QC-001"
PRINCIPLE = "MEOS Quantum Research Platform SHALL provide the scientific intelligence foundation enabling discovery, experimentation, collaboration and evolution of future quantum capabilities."
FABRIC = "meos_quantum_discovery_intelligence_fabric"
CORE_DOMAIN = "enterprise_quantum_research_intelligence_management"
SUPPORTING_DOMAINS = (
    {"id": "quantum_research", "purpose": "Research lifecycle, projects and governance bindings."},
    {"id": "quantum_innovation_lab", "purpose": "Sandboxes, prototypes and innovation workflows."},
    {"id": "quantum_experiment", "purpose": "Experiment execution, hypotheses and reproducibility."},
    {"id": "scientific_collaboration", "purpose": "Partnerships, knowledge exchange and publications."},
    {"id": "discovery_intelligence", "purpose": "Pattern discovery and research recommendations."},
    {"id": "knowledge_evolution", "purpose": "Scientific knowledge graph evolution."},
    {"id": "research_asset", "purpose": "Datasets, publications and experiment artifacts refs."},
    {"id": "future_technology_intelligence", "purpose": "Technology radar and evolution modeling."},
    {"id": "innovation_governance", "purpose": "Dual-use and ethics via P215-K."},
)
GENERIC_DOMAINS = ("identity", "security", "observability", "documents", "search", "compliance")
LOGICAL_BOUNDED_CONTEXTS = (
    {"id": "quantum_research_management", "bc": "BC-01", "name": "Quantum Research Management Context", "owns": "QuantumResearchAggregate", "purpose": "Research lifecycle, projects, governance."},
    {"id": "quantum_innovation_lab", "bc": "BC-02", "name": "Quantum Innovation Lab Context", "owns": "QuantumInnovationLabAggregate", "purpose": "Experimental environments, innovation workflows, prototypes."},
    {"id": "quantum_experimentation", "bc": "BC-03", "name": "Quantum Experimentation Context", "owns": "QuantumExperimentAggregate", "purpose": "Experiment execution, hypothesis testing, scientific validation."},
    {"id": "scientific_collaboration", "bc": "BC-04", "name": "Scientific Collaboration Context", "owns": "ScientificCollaborationAggregate", "purpose": "Research partnerships, knowledge exchange, collaboration networks."},
    {"id": "quantum_discovery_intelligence", "bc": "BC-05", "name": "Quantum Discovery Intelligence Context", "owns": "QuantumDiscoveryAggregate", "purpose": "Discovery generation, pattern detection, research intelligence."},
    {"id": "future_intelligence_evolution", "bc": "BC-06", "name": "Future Intelligence Evolution Context", "owns": "FutureEvolutionAggregate", "purpose": "Technology forecasting, evolution modeling, future architecture analysis."},
)
AGGREGATES = (
    {"name": "EnterpriseQuantumResearchAggregate", "root": "QuantumResearchProject", "entities": ("QuantumResearchProject", "QuantumExperiment", "QuantumResearcher", "QuantumInnovationLab", "ScientificPublication", "ResearchDataset", "QuantumDiscovery", "InnovationHypothesis", "FutureTechnologyModel"), "value_objects": ("ResearchImpactScore", "InnovationMaturityScore", "DiscoveryConfidenceScore", "ScientificRelevanceScore", "ExperimentAccuracyScore", "TechnologyReadinessLevel"), "events": ("QuantumResearchStartedEvent", "ExperimentCreatedEvent", "DiscoveryGeneratedEvent", "ScientificKnowledgeAddedEvent", "InnovationValidatedEvent", "FutureTechnologyDetectedEvent")},
    {"name": "QuantumResearchAggregate", "root": "QuantumResearchProject", "entities": ("ResearchMilestone", "GovernanceGate"), "value_objects": ("ResearchImpactScore", "InnovationMaturityScore"), "events": ("ResearchStartedEvent", "QuantumResearchStartedEvent")},
    {"name": "QuantumInnovationLabAggregate", "root": "QuantumInnovationLab", "entities": ("Sandbox", "Prototype"), "value_objects": ("InnovationMaturityScore", "TechnologyReadinessLevel"), "events": ("InnovationValidatedEvent",)},
    {"name": "QuantumExperimentAggregate", "root": "QuantumExperiment", "entities": ("InnovationHypothesis", "ExperimentRun"), "value_objects": ("ExperimentAccuracyScore", "DiscoveryConfidenceScore"), "events": ("ExperimentCreatedEvent", "ExperimentExecutedEvent")},
    {"name": "ScientificCollaborationAggregate", "root": "ScientificPublication", "entities": ("Partnership", "CollaborationSpace"), "value_objects": ("ScientificRelevanceScore", "ResearchImpactScore"), "events": ("PublicationReleasedEvent", "ScientificKnowledgeAddedEvent")},
    {"name": "QuantumDiscoveryAggregate", "root": "QuantumDiscovery", "entities": ("PatternSignal", "Recommendation"), "value_objects": ("DiscoveryConfidenceScore", "ScientificRelevanceScore"), "events": ("DiscoveryCreatedEvent", "DiscoveryGeneratedEvent")},
    {"name": "FutureEvolutionAggregate", "root": "FutureTechnologyModel", "entities": ("RadarSignal", "ImpactAssessment"), "value_objects": ("TechnologyReadinessLevel", "InnovationMaturityScore"), "events": ("FutureTechnologyDetectedEvent",)},
)
DOMAIN_SERVICES = (
    {"id": "quantum_research_service", "responsibility": "manage research projects and lifecycle", "inputs": ("project_spec",), "outputs": ("project_ref",), "rules": ("via_p215_k",), "events": ("ResearchStartedEvent",)},
    {"id": "innovation_lab_service", "responsibility": "provision labs and sandboxes", "inputs": ("lab_spec",), "outputs": ("lab_ref",), "rules": ("via_p215_d",), "events": ("InnovationValidatedEvent",)},
    {"id": "experiment_management_service", "responsibility": "execute and track experiments", "inputs": ("experiment_spec",), "outputs": ("experiment_ref",), "rules": ("via_p215_g", "via_p215_o"), "events": ("ExperimentExecutedEvent",)},
    {"id": "scientific_collaboration_service", "responsibility": "manage collaborations and publications", "inputs": ("collab_spec",), "outputs": ("publication_ref",), "rules": ("via_document_exchange",), "events": ("PublicationReleasedEvent",)},
    {"id": "discovery_intelligence_service", "responsibility": "generate discoveries and recommendations", "inputs": ("discovery_request",), "outputs": ("discovery_ref",), "rules": ("via_p214_g", "via_p215_i"), "events": ("DiscoveryCreatedEvent",)},
    {"id": "ai_assisted_research_service", "responsibility": "research copilots and hypothesis assistance", "inputs": ("copilot_request",), "outputs": ("assistance_ref",), "rules": ("via_p215_f", "via_p214_z", "module_local_llm_forbidden"), "events": ("DiscoveryGeneratedEvent",)},
    {"id": "future_technology_radar_service", "responsibility": "monitor and score emerging technologies", "inputs": ("radar_query",), "outputs": ("radar_snapshot",), "rules": ("via_p213",), "events": ("FutureTechnologyDetectedEvent",)},
)
CORE_EVENTS = (
    {"name": "ResearchStartedEvent", "producer": "quantum_research_management", "consumers": "lab,kg,governance"},
    {"name": "ExperimentExecutedEvent", "producer": "quantum_experimentation", "consumers": "discovery,certification,twin"},
    {"name": "DiscoveryCreatedEvent", "producer": "quantum_discovery_intelligence", "consumers": "kg,marketplace,notifications"},
    {"name": "PublicationReleasedEvent", "producer": "scientific_collaboration", "consumers": "documents,search"},
    {"name": "InnovationValidatedEvent", "producer": "quantum_innovation_lab", "consumers": "certification,marketplace,governance"},
    {"name": "FutureTechnologyDetectedEvent", "producer": "future_intelligence_evolution", "consumers": "radar,decision,strategy"},
)
RESEARCH_PLATFORM = {"present_required": True, "capabilities": ("research_lifecycle", "project_governance", "reproducibility", "impact_scoring"), "equation": "Scientific Knowledge -> Research Intelligence -> Quantum Experiments -> AI Assisted Discovery -> Innovation Acceleration -> Future Quantum Evolution"}
INNOVATION_LAB = {"present_required": True, "capabilities": ("experiment_environments", "research_sandboxes", "prototype_development", "algorithm_exploration", "quantum_ai_experiments", "scientific_simulation"), "supports": ("researchers", "ai_agents", "quantum_engineers", "enterprise_innovation_teams"), "via_p215_d": True, "via_p215_g": True}
SCIENTIFIC_COLLABORATION = {"present_required": True, "connects": ("universities", "research_institutes", "enterprises", "quantum_providers", "ai_research_systems", "scientific_communities"), "capabilities": ("collaboration_spaces", "research_sharing", "joint_experiments", "knowledge_exchange", "publication_management"), "via_document_exchange": True, "module_local_publication_blob_forbidden": True}
DISCOVERY_INTELLIGENCE = {"present_required": True, "capabilities": ("scientific_pattern_discovery", "research_recommendation", "experiment_optimization", "knowledge_mining", "innovation_detection"), "via_p214_g": True, "via_p215_i": True}
AI_ASSISTED_RESEARCH = {"present_required": True, "capabilities": ("literature_analysis", "experiment_design_assistance", "hypothesis_generation", "simulation_assistance", "research_automation"), "via_p215_f": True, "via_p214_z": True, "module_local_llm_forbidden": True}
EXPERIMENT_MANAGEMENT = {"present_required": True, "manages": ("experiments", "hypotheses", "variables", "results", "reproducibility", "scientific_evidence"), "capabilities": ("experiment_tracking", "result_validation", "knowledge_capture", "experiment_evolution"), "via_p215_o": True}
FUTURE_TECHNOLOGY_RADAR = {"present_required": True, "monitors": ("quantum_hardware_progress", "quantum_algorithms", "quantum_ai_evolution", "quantum_networks", "quantum_security", "emerging_technologies"), "capabilities": ("trend_detection", "impact_analysis", "strategic_recommendations"), "via_p213": True}
CONTEXT_MAP = (
    {"from": "quantum_experimentation", "to": "quantum_scientific", "type": "anti_corruption_layer", "via": "P215-G"},
    {"from": "quantum_discovery_intelligence", "to": "ai_knowledge_rag", "type": "anti_corruption_layer", "via": "P214-G"},
    {"from": "quantum_discovery_intelligence", "to": "quantum_data", "type": "customer_supplier", "via": "P215-I"},
    {"from": "quantum_innovation_lab", "to": "quantum_infrastructure", "type": "customer_supplier", "via": "P215-D"},
    {"from": "scientific_collaboration", "to": "document_exchange", "type": "anti_corruption_layer", "via": "DocumentExchange"},
    {"from": "quantum_experimentation", "to": "quantum_quality", "type": "customer_supplier", "via": "P215-O"},
    {"from": "quantum_discovery_intelligence", "to": "quantum_marketplace", "type": "customer_supplier", "via": "P215-P"},
    {"from": "quantum_research_management", "to": "quantum_governance", "type": "conformist", "via": "P215-K"},
    {"from": "future_intelligence_evolution", "to": "decision_intelligence", "type": "anti_corruption_layer", "via": "P213"},
)
MICROSERVICES = (
    {"id": "quantum_research_service", "bc": "BC-01", "aggregate": "QuantumResearchAggregate", "api": "/quantum/research", "db": "quantum_*", "events": ("ResearchStartedEvent",), "security": ("quantum.read",), "scaling": "research_replicas"},
    {"id": "innovation_lab_service", "bc": "BC-02", "aggregate": "QuantumInnovationLabAggregate", "api": "/quantum/research/lab", "db": "quantum_*", "events": ("InnovationValidatedEvent",), "security": ("quantum.write",), "scaling": "lab_workers"},
    {"id": "experiment_management_service", "bc": "BC-03", "aggregate": "QuantumExperimentAggregate", "api": "/quantum/research/experiments", "db": "quantum_*", "events": ("ExperimentExecutedEvent",), "security": ("quantum.write",), "scaling": "experiment_workers"},
    {"id": "scientific_collaboration_service", "bc": "BC-04", "aggregate": "ScientificCollaborationAggregate", "api": "/quantum/research/collaboration", "db": "quantum_*", "events": ("PublicationReleasedEvent",), "security": ("quantum.write",), "scaling": "collab_workers"},
    {"id": "discovery_intelligence_service", "bc": "BC-05", "aggregate": "QuantumDiscoveryAggregate", "api": "/quantum/research/discovery", "db": "quantum_*", "events": ("DiscoveryCreatedEvent",), "security": ("quantum.write",), "scaling": "discovery_workers"},
    {"id": "research_knowledge_graph_service", "bc": "kg", "aggregate": "EnterpriseQuantumResearchAggregate", "api": "/quantum/research/knowledge-graph", "db": "quantum_*", "events": ("DiscoveryCreatedEvent",), "security": ("quantum.read",), "scaling": "kg_replicas"},
    {"id": "future_technology_radar_service", "bc": "BC-06", "aggregate": "FutureEvolutionAggregate", "api": "/quantum/research/radar", "db": "quantum_*", "events": ("FutureTechnologyDetectedEvent",), "security": ("quantum.read",), "scaling": "radar_replicas"},
    {"id": "research_digital_twin_service", "bc": "twin", "aggregate": "EnterpriseQuantumResearchAggregate", "api": "/quantum/research/digital-twin", "db": "quantum_*", "events": ("ExperimentExecutedEvent",), "security": ("quantum.read",), "scaling": "twin_replicas"},
    {"id": "scientific_analytics_service", "bc": "analytics", "aggregate": "EnterpriseQuantumResearchAggregate", "api": "/quantum/research/analytics", "db": "quantum_*", "events": ("FutureTechnologyDetectedEvent",), "security": ("quantum.read",), "scaling": "analytics_replicas"},
)
KNOWLEDGE_GRAPH = {"present_required": True, "nodes": ("researchers", "experiments", "algorithms", "publications", "discoveries", "datasets", "technologies", "hypotheses"), "relationships": ("created_by", "validated_by", "derived_from", "improves", "depends_on", "collaborates_with")}
DIGITAL_TWIN = {"present_required": True, "represents": ("research_ecosystem", "innovation_pipeline", "experiments", "scientific_assets", "technology_evolution"), "enables": ("innovation_simulation", "research_forecasting", "discovery_optimization"), "via_p215_l": True}
COMMANDS = ("CreateResearchProjectCommand", "StartExperimentCommand", "SubmitDiscoveryCommand", "CreateInnovationProposalCommand", "PublishResearchResultCommand", "UpdateTechnologyRadarCommand")
QUERIES = ("GetResearchProjectQuery", "GetExperimentResultQuery", "GetDiscoveryKnowledgeQuery", "GetInnovationPipelineQuery", "GetFutureTechnologyQuery")
API_SURFACES = ("/api/v1/quantum/research", "/api/v1/quantum/research/lab", "/api/v1/quantum/research/experiments", "/api/v1/quantum/research/collaboration", "/api/v1/quantum/research/discovery", "/api/v1/quantum/research/radar", "/api/v1/quantum/research/knowledge-graph", "/api/v1/quantum/research/digital-twin", "/api/v1/quantum/research/analytics")
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
SECURITY = {"present_required": True, "zero_trust_research": True, "via_p215_h": True, "via_p215_k": True, "via_workflow": True, "module_local_llm_forbidden": True, "module_local_publication_blob_forbidden": True, "ungated_dual_use_research_forbidden": True, "controls": ("research_authz", "dual_use_policy_gate", "document_id_refs_only", "tenant_isolation")}
DEPLOYMENT = {"present_required": True, "cloud_native": True, "components": ("kubernetes", "research_compute_cluster", "quantum_simulation_environment", "ai_research_infrastructure", "knowledge_graph_database", "experiment_storage", "collaboration_platform", "observability_platform")}
TESTING = ("experiment_reproducibility_testing", "research_workflow_testing", "scientific_validation_testing", "knowledge_graph_accuracy_testing", "ai_research_assistant_testing", "collaboration_platform_testing", "security_testing", "performance_testing")
CURSOR_OUTPUTS = ("enterprise_quantum_research_vision", "ddd_domain_model", "research_domain_architecture", "innovation_lab", "scientific_collaboration", "discovery_intelligence", "ai_assisted_research", "experiment_management", "knowledge_graph", "digital_twin", "future_technology_radar", "cqrs", "event_sourcing", "microservices", "integration", "deployment", "testing", "quality_gates_dod", "adr_462", "enterprise_quantum_research_law")
QUALITY_GATES_REJECT_IF = ("quantum_research_platform_is_missing", "quantum_innovation_lab_is_missing", "scientific_collaboration_platform_is_missing", "discovery_intelligence_is_missing", "ai_assisted_research_is_missing", "experiment_management_is_missing", "future_technology_radar_is_missing", "knowledge_graph_integration_is_missing", "digital_twin_integration_is_missing", "cqrs_architecture_is_missing", "event_architecture_is_missing", "microservices_architecture_is_missing", "api_first_architecture_is_missing", "cloud_native_deployment_is_missing", "sibling_quantum_bc")

def vision() -> dict[str, Any]:
    return {"role": "MEOS Quantum Discovery Intelligence Fabric", "principle": PRINCIPLE, "equation": RESEARCH_PLATFORM["equation"], "why": ("dedicated_research_ecosystems", "internal_quantum_laboratories", "ai_assisted_discovery", "collaboration_networks", "continuous_experimentation"), "builds_on_p215_a": True, "builds_on_p215_f": True, "builds_on_p215_g": True, "builds_on_p215_p": True, "via_p214_g": True, "governed_by_p215_k": True}

def domain_model() -> dict[str, Any]:
    return {"core_domain": CORE_DOMAIN, "supporting_domains": [dict(d) for d in SUPPORTING_DOMAINS], "supporting_count": len(SUPPORTING_DOMAINS), "generic_domains": list(GENERIC_DOMAINS)}

def bounded_contexts() -> dict[str, Any]:
    return {"contexts": [dict(c) for c in LOGICAL_BOUNDED_CONTEXTS], "context_count": len(LOGICAL_BOUNDED_CONTEXTS)}

def aggregates() -> dict[str, Any]:
    return {"aggregates": [dict(a) for a in AGGREGATES], "aggregate_count": len(AGGREGATES)}

def domain_services() -> dict[str, Any]:
    return {"services": [dict(s) for s in DOMAIN_SERVICES], "service_count": len(DOMAIN_SERVICES)}

def events() -> dict[str, Any]:
    return {"core_events": [dict(e) for e in CORE_EVENTS], "core_event_count": len(CORE_EVENTS), "version_strategy": "event_version_field", "retention_policy": "tenant_scoped_immutable_append"}

def research_platform() -> dict[str, Any]:
    return dict(RESEARCH_PLATFORM)

def innovation_lab() -> dict[str, Any]:
    return dict(INNOVATION_LAB)

def scientific_collaboration() -> dict[str, Any]:
    return dict(SCIENTIFIC_COLLABORATION)

def discovery_intelligence() -> dict[str, Any]:
    return dict(DISCOVERY_INTELLIGENCE)

def ai_assisted_research() -> dict[str, Any]:
    return dict(AI_ASSISTED_RESEARCH)

def experiment_management() -> dict[str, Any]:
    return dict(EXPERIMENT_MANAGEMENT)

def future_technology_radar() -> dict[str, Any]:
    return dict(FUTURE_TECHNOLOGY_RADAR)

def context_map() -> dict[str, Any]:
    return {"relationships": [dict(r) for r in CONTEXT_MAP], "relationship_count": len(CONTEXT_MAP)}

def microservices() -> dict[str, Any]:
    return {"services": [dict(s) for s in MICROSERVICES], "service_count": len(MICROSERVICES)}

def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH)

def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN)

def cqrs() -> dict[str, Any]:
    return {"commands": list(COMMANDS), "command_count": len(COMMANDS), "queries": list(QUERIES), "query_count": len(QUERIES)}

def api() -> dict[str, Any]:
    return {"surfaces": list(API_SURFACES), "styles": list(API_STYLES), "api_first_present_required": True}

def integrations() -> dict[str, Any]:
    return {"peers": ("P215-A", "P215-D", "P215-E", "P215-F", "P215-G", "P215-I", "P215-K", "P215-L", "P215-O", "P215-P", "P214-G", "P214-Z", "P213", "Document Exchange", "Workflow", "Enterprise Search"), "via_events_and_acl": True, "contracts": ("research_apis", "experiment_interfaces", "knowledge_contracts", "collaboration_protocols", "innovation_events")}

def security() -> dict[str, Any]:
    return dict(SECURITY)

def deployment() -> dict[str, Any]:
    return dict(DEPLOYMENT)

def testing() -> dict[str, Any]:
    return {"suites": list(TESTING), "suite_count": len(TESTING)}

def cursor_outputs() -> dict[str, Any]:
    return {"outputs": list(CURSOR_OUTPUTS), "count": len(CURSOR_OUTPUTS)}

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE"}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "principle": PRINCIPLE, "fabric": FABRIC,
        "builds_on": ["P215-A", "P215-B", "P215-C", "P215-D", "P215-E", "P215-F", "P215-G", "P215-H", "P215-I", "P215-J", "P215-K", "P215-L", "P215-M", "P215-N", "P215-O", "P215-P", "P214-G", "P214-Z", "P213", "ADR-447", "ADR-453", "ADR-403", "ADR-460", "ADR-461"],
        "vision": vision(), "domain_model": domain_model(), "bounded_contexts": bounded_contexts(),
        "aggregates": aggregates(), "domain_services": domain_services(), "events": events(),
        "research_platform": research_platform(), "innovation_lab": innovation_lab(),
        "scientific_collaboration": scientific_collaboration(), "discovery_intelligence": discovery_intelligence(),
        "ai_assisted_research": ai_assisted_research(), "experiment_management": experiment_management(),
        "future_technology_radar": future_technology_radar(), "context_map": context_map(),
        "microservices": microservices(), "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(), "cqrs": cqrs(), "api": api(), "integrations": integrations(),
        "security": security(), "deployment": deployment(), "testing": testing(),
        "cursor_outputs": cursor_outputs(), "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "quantum_research_platform_present_required": True,
        "quantum_innovation_lab_present_required": True,
        "scientific_collaboration_platform_present_required": True,
        "discovery_intelligence_present_required": True,
        "ai_assisted_research_present_required": True,
        "experiment_management_present_required": True,
        "future_technology_radar_present_required": True,
        "knowledge_graph_integration_present_required": True,
        "digital_twin_integration_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "cloud_native_deployment_present_required": True,
        "sibling_quantum_bc_forbidden": True,
        "builds_on_p215_a": True, "builds_on_p215_f": True, "builds_on_p215_g": True,
        "builds_on_p215_p": True, "via_p215_g": True, "via_p214_g": True,
        "via_p215_i": True, "via_p215_o": True, "via_p215_p": True,
        "via_document_exchange": True, "governed_by_p215_k": True,
        "api_prefix": f"{API_PREFIX}/research",
        "forbidden_sibling_bc": [
            "quantum_research_platform",
            "quantum_innovation_lab_platform",
            "quantum_discovery_platform",
            "quantum_experiment_platform",
            "quantum_future_radar_platform",
        ],
    }

def research_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /quantum/research",
        "GET /quantum/research/lab",
        "GET /quantum/research/experiments",
        "GET /quantum/research/collaboration",
        "GET /quantum/research/discovery",
        "GET /quantum/research/radar",
        "GET /quantum/research/knowledge-graph",
        "GET /quantum/research/digital-twin",
        "GET /quantum/research/analytics",
        "GET /quantum/research/readiness",
    ]}
