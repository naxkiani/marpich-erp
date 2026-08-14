"""P219-I Knowledge Civilization Core — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P219-I"
ADR = 562
SOR = "civilization"
API_PREFIX = "/api/v1/civilization"
PRODUCT = (
    "Enterprise Civilization Operating System Global Knowledge Civilization Platform, "
    "Universal Knowledge Graph, Scientific Intelligence Network, Collective Intelligence "
    "Architecture & MEOS Knowledge Civilization Core"
)
CAPABILITY = "CAP-PLT-CIV-001"
PRIMARY_CAPABILITY = (
    "Create a civilization-scale knowledge intelligence platform capable of "
    "preserving, connecting, understanding and expanding humanity's collective "
    "knowledge while accelerating scientific discovery, innovation and intelligent "
    "decision-making."
)
FABRIC = "meos_civilization_os_knowledge_civilization_framework"
FOUNDATION_GATE = "P219"
MISSION_GATE = "P219-A"
STRATEGY_GATE = "P219-B"
DOMAIN_GATE = "P219-C"
PLANETARY_GATE = "P219-D"
AI_OS_GATE = "P219-E"
SIMULATION_GATE = "P219-F"
RESOURCES_GATE = "P219-G"
ECONOMY_GATE = "P219-H"
INTELLIGENCE_NEXUS_GATE = "P218-Z"
SPACE_GATE = "P218"
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

EVOLUTION = (
    "Information Civilization", "Connected Knowledge Civilization",
    "Intelligent Knowledge Civilization", "Collective Intelligence Civilization",
    "Universal Knowledge Civilization", "MEOS Knowledge Civilization",
)
KNOWLEDGE_DOMAINS = (
    "scientific", "technical", "cultural", "historical", "educational",
    "industrial", "medical", "environmental", "space", "economic",
)
UKG_LAYERS = (
    {"id": "L01", "name": "Knowledge Entity Layer"},
    {"id": "L02", "name": "Semantic Relationship Layer"},
    {"id": "L03", "name": "Reasoning Layer"},
    {"id": "L04", "name": "Knowledge Evolution Layer"},
)
ENTITY_TYPES = (
    "Human", "Organization", "Scientific Discovery", "Technology", "Theory",
    "Concept", "Document", "Resource", "Event", "Location", "Institution",
)
RELATIONSHIPS = (
    "DISCOVERED_BY", "CREATED_BY", "DEPENDS_ON", "PROVES", "IMPACTS",
    "EVOLVES", "RELATED_TO", "DERIVED_FROM", "CONTRIBUTES_TO",
)
SCIENTIFIC_DOMAINS = (
    "physics", "biology", "medicine", "engineering",
    "ai_research", "quantum_science", "space_science", "environmental_science",
)
SCIENTIFIC_AGENTS = (
    "Scientific Discovery Agent", "Literature Intelligence Agent",
    "Experiment Intelligence Agent", "Innovation Intelligence Agent",
)
LEARNING_AGENTS = (
    "Education Agent", "Skill Intelligence Agent",
    "Knowledge Tutor Agent", "Career Evolution Agent",
)
PLATFORM_CAPABILITIES = (
    "knowledge_acquisition", "knowledge_integration", "knowledge_representation",
    "knowledge_reasoning", "knowledge_discovery", "knowledge_distribution", "knowledge_evolution",
)
REASONING_PIPELINE = (
    "Knowledge Input", "Semantic Processing", "Reasoning Engine",
    "Insight Generation", "Knowledge Evolution",
)
BOUNDED_CONTEXTS = (
    {
        "id": "BC-KNW-01", "name": "Universal Knowledge Core Context", "type": "CORE",
        "aggregate": "KnowledgeUniverseAggregate",
        "entities": ("KnowledgeNode", "KnowledgeDomain", "KnowledgeRelationship", "KnowledgeAsset"),
        "value_objects": ("KnowledgeId", "ConfidenceScore", "KnowledgeMaturity"),
        "services": ("KnowledgeManagementService", "KnowledgeReasoningService"),
        "events": ("KnowledgeCreatedEvent", "KnowledgeConnectedEvent", "KnowledgeValidatedEvent"),
    },
    {
        "id": "BC-KNW-02", "name": "Scientific Intelligence Context", "type": "CORE",
        "aggregate": "ScientificDiscoveryAggregate",
        "entities": ("ResearchProject", "ScientificDiscovery", "ExperimentModel", "ResearcherProfile"),
        "value_objects": ("DiscoveryScore", "ScientificConfidence", "ResearchImpact"),
        "services": ("DiscoveryAccelerationService", "ScientificAnalysisService"),
        "events": ("DiscoveryCreatedEvent", "ResearchCompletedEvent", "ScientificBreakthroughDetectedEvent"),
    },
    {
        "id": "BC-KNW-03", "name": "Collective Intelligence Context", "type": "CORE",
        "aggregate": "CollectiveIntelligenceAggregate",
        "entities": ("IntelligenceNetwork", "ExpertCommunity", "CollaborationNetwork"),
        "value_objects": ("IntelligenceScore", "CollaborationLevel"),
        "services": ("CollectiveReasoningService",),
        "events": ("NetworkCreatedEvent", "CollectiveInsightGeneratedEvent", "CollaborationEstablishedEvent"),
    },
    {
        "id": "BC-KNW-04", "name": "Learning Civilization Context", "type": "SUPPORTING",
        "aggregate": "LearningEcosystemAggregate",
        "entities": ("LearningPath", "EducationSystem", "SkillModel"),
        "value_objects": ("LearningLevel", "CapabilityScore"),
        "services": ("LearningOptimizationService",),
        "events": ("LearningPathCreatedEvent", "CapabilityImprovedEvent"),
    },
)
PRIMARY_AGGREGATES = (
    "KnowledgeUniverseAggregate", "KnowledgeGraphAggregate",
    "ScientificDiscoveryAggregate", "CollectiveIntelligenceAggregate", "LearningEcosystemAggregate",
)
COMMANDS = (
    "CreateKnowledgeNodeCommand", "ConnectKnowledgeEntityCommand", "ValidateKnowledgeCommand",
    "GenerateScientificInsightCommand", "CreateResearchNetworkCommand", "OptimizeLearningPathCommand",
)
QUERIES = (
    "GetKnowledgeGraphQuery", "GetScientificDiscoveryQuery", "GetResearchNetworkQuery",
    "GetKnowledgeEvolutionQuery", "GetLearningIntelligenceQuery",
)
CORE_EVENTS = (
    {"name": "KnowledgeCreatedEvent", "owner": "BC-KNW-01"},
    {"name": "KnowledgeUpdatedEvent", "owner": "BC-KNW-01"},
    {"name": "KnowledgeConnectedEvent", "owner": "BC-KNW-01"},
    {"name": "KnowledgeValidatedEvent", "owner": "BC-KNW-01"},
    {"name": "KnowledgeDiscoveredEvent", "owner": "BC-KNW-01"},
    {"name": "KnowledgeExpandedEvent", "owner": "BC-KNW-01"},
    {"name": "ResearchStartedEvent", "owner": "BC-KNW-02"},
    {"name": "ExperimentCompletedEvent", "owner": "BC-KNW-02"},
    {"name": "DiscoveryGeneratedEvent", "owner": "BC-KNW-02"},
    {"name": "BreakthroughDetectedEvent", "owner": "BC-KNW-02"},
    {"name": "CollaborationCreatedEvent", "owner": "BC-KNW-03"},
    {"name": "CollectiveInsightGeneratedEvent", "owner": "BC-KNW-03"},
    {"name": "IntelligenceNetworkExpandedEvent", "owner": "BC-KNW-03"},
)
KNOWLEDGE_GRAPH = {
    "present_required": True,
    "entity_types": ENTITY_TYPES,
    "relationships": RELATIONSHIPS,
    "layers": UKG_LAYERS,
    "capabilities": ("inference", "pattern_discovery", "causal_reasoning", "knowledge_validation", "hypothesis_generation"),
}
DIGITAL_TWIN = {
    "present_required": True,
    "represents": ("scientific_knowledge", "technology_evolution", "human_expertise", "research_networks", "educational_systems"),
    "capabilities": ("knowledge_simulation", "discovery_prediction", "knowledge_gap_analysis", "innovation_forecasting"),
}
INTEGRATION = {
    "present_required": True,
    "peers": (
        "P214-Z", "P215-Z", "P216-Z", "P217-Z", "P218", "P218-Z",
        "P219", "P219-A", "P219-B", "P219-C", "P219-D", "P219-E", "P219-F", "P219-G", "P219-H",
        "Enterprise Search", "Document Exchange", "MEOS Core",
    ),
    "integrations": (
        {"peer": "P214-Z", "provides": ("knowledge_intelligence_models",)},
        {"peer": "P215-Z", "provides": ("advanced_knowledge_computation",)},
        {"peer": "P216-Z", "provides": ("embodied_knowledge_systems",)},
        {"peer": "P217-Z", "provides": ("biological_knowledge_systems",)},
        {"peer": "P218", "provides": ("space_science_knowledge",)},
        {"peer": "P218-Z", "provides": ("civilization_intelligence_coordination",)},
        {"peer": "P219-E", "provides": ("knowledge_reasoning_engine",)},
        {"peer": "P219-F", "provides": ("scientific_simulation_knowledge",)},
        {"peer": "P219-H", "provides": ("economic_knowledge_intelligence",)},
        {"peer": "Enterprise Search", "provides": ("index_and_query",)},
        {"peer": "Document Exchange", "provides": ("document_id_refs",)},
    ),
}
ROADMAP = {
    "phases": (
        {"id": "P01", "name": "Knowledge Foundation"},
        {"id": "P02", "name": "Scientific Intelligence Activation"},
        {"id": "P03", "name": "Collective Intelligence Network"},
        {"id": "P04", "name": "Universal Knowledge Civilization"},
    ),
}
MICROSERVICES = (
    {"id": "knowledge_core_service", "api": "/civilization/knowledge", "bc": "BC-KNW-01"},
    {"id": "ukg_service", "api": "/civilization/knowledge/graph", "bc": "BC-KNW-01"},
    {"id": "scientific_intelligence_service", "api": "/civilization/knowledge/scientific", "bc": "BC-KNW-02"},
    {"id": "collective_intelligence_service", "api": "/civilization/knowledge/collective", "bc": "BC-KNW-03"},
    {"id": "learning_civilization_service", "api": "/civilization/knowledge/learning", "bc": "BC-KNW-04"},
    {"id": "knowledge_reasoning_service", "api": "/civilization/knowledge/reasoning", "bc": "BC-KNW-01"},
    {"id": "knowledge_twin_service", "api": "/civilization/knowledge/digital-twin", "bc": "BC-KNW-01"},
    {"id": "knowledge_agents_service", "api": "/civilization/knowledge/agents", "bc": "BC-KNW-02"},
    {"id": "knowledge_events_service", "api": "/civilization/knowledge/events", "bc": "BC-KNW-01"},
    {"id": "knowledge_integration_service", "api": "/civilization/knowledge/integration", "bc": "BC-KNW-01"},
)


def vision_pack() -> dict[str, Any]:
    return {
        "primary_capability": PRIMARY_CAPABILITY,
        "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "planetary_gate": PLANETARY_GATE, "ai_os_gate": AI_OS_GATE,
        "simulation_gate": SIMULATION_GATE, "resources_gate": RESOURCES_GATE,
        "economy_gate": ECONOMY_GATE,
        "intelligence_nexus_gate": INTELLIGENCE_NEXUS_GATE, "space_gate": SPACE_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "never_replace_p219_h_economy": True,
        "never_replace_enterprise_search": True,
        "never_replace_document_exchange": True,
        "foundation_for_p219_j": True,
    }


def architecture() -> dict[str, Any]:
    return {
        "present_required": True,
        "evolution": list(EVOLUTION),
        "evolution_stage_count": len(EVOLUTION),
        "knowledge_domains": list(KNOWLEDGE_DOMAINS),
        "knowledge_domain_count": len(KNOWLEDGE_DOMAINS),
        "ukg_layers": [dict(l) for l in UKG_LAYERS],
        "ukg_layer_count": len(UKG_LAYERS),
        "entity_types": list(ENTITY_TYPES),
        "entity_type_count": len(ENTITY_TYPES),
        "relationships": list(RELATIONSHIPS),
        "relationship_count": len(RELATIONSHIPS),
        "platform_capabilities": list(PLATFORM_CAPABILITIES),
        "platform_capability_count": len(PLATFORM_CAPABILITIES),
        "reasoning_pipeline": list(REASONING_PIPELINE),
        "reasoning_pipeline_step_count": len(REASONING_PIPELINE),
    }


def scientific() -> dict[str, Any]:
    return {
        "present_required": True,
        "domains": list(SCIENTIFIC_DOMAINS),
        "domain_count": len(SCIENTIFIC_DOMAINS),
        "agents": list(SCIENTIFIC_AGENTS),
        "agent_count": len(SCIENTIFIC_AGENTS),
    }


def collective() -> dict[str, Any]:
    return {
        "present_required": True,
        "model": (
            "Human Intelligence", "Artificial Intelligence", "Scientific Intelligence",
            "Institutional Intelligence", "Historical Intelligence",
        ),
        "components": (
            "Human Knowledge Network", "AI Reasoning Network", "Expert Intelligence Network",
            "Research Collaboration Network", "Learning Network",
        ),
        "component_count": 5,
    }


def learning() -> dict[str, Any]:
    return {
        "present_required": True,
        "agents": list(LEARNING_AGENTS),
        "agent_count": len(LEARNING_AGENTS),
        "capabilities": (
            "personalized_learning_intelligence", "global_education_intelligence",
            "skill_evolution_modeling", "knowledge_accessibility", "learning_path_optimization",
        ),
    }


def agents() -> dict[str, Any]:
    all_agents = list(SCIENTIFIC_AGENTS) + list(LEARNING_AGENTS)
    return {
        "present_required": True,
        "agents": all_agents,
        "agent_count": len(all_agents),
        "scientific_agent_count": len(SCIENTIFIC_AGENTS),
        "learning_agent_count": len(LEARNING_AGENTS),
    }


def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN) | {
        "represent_count": len(DIGITAL_TWIN["represents"]),
        "capability_count": len(DIGITAL_TWIN["capabilities"]),
    }


def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH) | {
        "entity_type_count": len(ENTITY_TYPES),
        "relationship_count": len(RELATIONSHIPS),
        "layer_count": len(UKG_LAYERS),
    }


def bounded_contexts() -> dict[str, Any]:
    return {
        "present_required": True,
        "contexts": [dict(c) for c in BOUNDED_CONTEXTS],
        "context_count": len(BOUNDED_CONTEXTS),
    }


def aggregates() -> dict[str, Any]:
    return {
        "present_required": True,
        "primary_aggregates": list(PRIMARY_AGGREGATES),
        "aggregate_count": len(PRIMARY_AGGREGATES),
    }


def entities() -> dict[str, Any]:
    ents: list[str] = []
    for bc in BOUNDED_CONTEXTS:
        ents.extend(bc["entities"])
    return {"present_required": True, "entities": ents, "entity_count": len(ents)}


def value_objects() -> dict[str, Any]:
    vos: list[str] = []
    for bc in BOUNDED_CONTEXTS:
        vos.extend(bc["value_objects"])
    return {"present_required": True, "value_objects": vos, "value_object_count": len(vos)}


def domain_services() -> dict[str, Any]:
    svcs: list[str] = []
    for bc in BOUNDED_CONTEXTS:
        svcs.extend(bc["services"])
    return {"present_required": True, "services": svcs, "service_count": len(svcs)}


def events() -> dict[str, Any]:
    return {
        "present_required": True,
        "core_events": [dict(e) for e in CORE_EVENTS],
        "core_event_count": len(CORE_EVENTS),
    }


def cqrs() -> dict[str, Any]:
    return {
        "present_required": True,
        "commands": list(COMMANDS), "command_count": len(COMMANDS),
        "queries": list(QUERIES), "query_count": len(QUERIES),
    }


def relationships() -> dict[str, Any]:
    return {
        "present_required": True,
        "edges": list(RELATIONSHIPS),
        "edge_count": len(RELATIONSHIPS),
        "never_cross_context_aggregate_imports": True,
    }


def integration() -> dict[str, Any]:
    return dict(INTEGRATION)


def microservices() -> dict[str, Any]:
    return {
        "present_required": True,
        "services": [dict(s) for s in MICROSERVICES],
        "service_count": len(MICROSERVICES),
    }


def roadmap() -> dict[str, Any]:
    return dict(ROADMAP) | {"phase_count": len(ROADMAP["phases"])}


def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p219_j": True}


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "primary_capability": PRIMARY_CAPABILITY, "principle": PRIMARY_CAPABILITY, "fabric": FABRIC,
        "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "planetary_gate": PLANETARY_GATE, "ai_os_gate": AI_OS_GATE,
        "simulation_gate": SIMULATION_GATE, "resources_gate": RESOURCES_GATE,
        "economy_gate": ECONOMY_GATE,
        "intelligence_nexus_gate": INTELLIGENCE_NEXUS_GATE, "space_gate": SPACE_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": [
            "P219-H", "P219-G", "P219-F", "P219-E", "P219-D", "P219-C", "P219-B", "P219-A", "P219",
            "P218-Z", "P218", "P217-Z", "P216-Z", "P215-Z", "P214-Z", "ADR-561",
        ],
        "vision": vision_pack(),
        "architecture": architecture(),
        "scientific": scientific(),
        "collective": collective(),
        "learning": learning(),
        "agents": agents(),
        "digital_twin": digital_twin(),
        "knowledge_graph": knowledge_graph(),
        "bounded_contexts": bounded_contexts(),
        "aggregates": aggregates(),
        "entities": entities(),
        "value_objects": value_objects(),
        "domain_services": domain_services(),
        "events": events(),
        "cqrs": cqrs(),
        "relationships": relationships(),
        "integration": integration(),
        "microservices": microservices(),
        "roadmap": roadmap(),
        "production_readiness": production_readiness(),
        "meos_knowledge_civilization_platform_present_required": True,
        "universal_knowledge_graph_present_required": True,
        "scientific_intelligence_network_present_required": True,
        "collective_intelligence_architecture_present_required": True,
        "knowledge_reasoning_engine_present_required": True,
        "civilization_learning_foundation_present_required": True,
        "meos_knowledge_civilization_core_present_required": True,
        "knowledge_digital_twin_present_required": True,
        "knowledge_event_architecture_present_required": True,
        "knowledge_cqrs_model_present_required": True,
        "meos_knowledge_integration_map_present_required": True,
        "never_replace_p219_foundation": True,
        "never_replace_p219_a_mission": True,
        "never_replace_p219_b_strategy": True,
        "never_replace_p219_c_domain": True,
        "never_replace_p219_d_planetary": True,
        "never_replace_p219_e_ai_os": True,
        "never_replace_p219_f_simulation": True,
        "never_replace_p219_g_resources": True,
        "never_replace_p219_h_economy": True,
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_enterprise_search": True,
        "never_replace_document_exchange": True,
        "never_replace_p215_z": True,
        "never_replace_p216_z": True,
        "never_replace_biotechnology": True,
        "never_replace_space": True,
        "never_replace_p218_z_intelligence_nexus": True,
        "never_merge_p218_t_space_civilization": True,
        "never_cross_context_aggregate_imports": True,
        "never_opaque_unexplainable_knowledge_decisions": True,
        "never_ungated_knowledge_publication": True,
        "never_skip_human_authority_knowledge": True,
        "never_skip_ethical_knowledge_governance": True,
        "never_violate_human_sovereignty_knowledge": True,
        "never_bypass_trusted_knowledge_validation": True,
        "no_module_local_llm": True,
        "sibling_knowledge_civilization_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/knowledge",
        "forbidden_sibling_bc": [
            "knowledge_civilization_platform",
            "universal_knowledge_graph_bc",
            "scientific_intelligence_network_bc",
        ],
        "foundation_for_p219_j": True,
    }


def knowledge_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /civilization/knowledge",
        "GET /civilization/knowledge/architecture",
        "GET /civilization/knowledge/graph",
        "GET /civilization/knowledge/scientific",
        "GET /civilization/knowledge/collective",
        "GET /civilization/knowledge/learning",
        "GET /civilization/knowledge/reasoning",
        "GET /civilization/knowledge/digital-twin",
        "GET /civilization/knowledge/agents",
        "GET /civilization/knowledge/bounded-contexts",
        "GET /civilization/knowledge/aggregates",
        "GET /civilization/knowledge/events",
        "GET /civilization/knowledge/cqrs",
        "GET /civilization/knowledge/integration",
        "GET /civilization/knowledge/readiness",
    ]}
