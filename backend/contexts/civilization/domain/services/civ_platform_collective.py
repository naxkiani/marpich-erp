"""P219-W Collective Intelligence & Global Coordination Core — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P219-W"
ADR = 576
SOR = "civilization"
API_PREFIX = "/api/v1/civilization"
PRODUCT = (
    "Enterprise Civilization Operating System Collective Intelligence, Global Coordination, "
    "Distributed Knowledge Collaboration, Collective Decision Support, Enterprise Coordination Intelligence "
    "& MEOS Collective Intelligence & Global Coordination Core"
)
CAPABILITY = "CAP-PLT-CIV-001"
PRIMARY_CAPABILITY = (
    "Create a civilization-scale collaboration platform capable of "
    "integrating distributed expertise, institutional knowledge and AI-assisted analysis "
    "into coordinated strategic execution."
)
FABRIC = "meos_civilization_os_collective_intelligence_global_coordination_framework"
FOUNDATION_GATE = "P219"
MISSION_GATE = "P219-A"
STRATEGY_GATE = "P219-B"
DOMAIN_GATE = "P219-C"
PLANETARY_GATE = "P219-D"
AI_OS_GATE = "P219-E"
SIMULATION_GATE = "P219-F"
RESOURCES_GATE = "P219-G"
ECONOMY_GATE = "P219-H"
KNOWLEDGE_GATE = "P219-I"
HUMAN_GATE = "P219-J"
GOVERNANCE_GATE = "P219-K"
INNOVATION_GATE = "P219-L"
SECURITY_GATE = "P219-M"
SUSTAINABILITY_GATE = "P219-N"
PROSPERITY_GATE = "P219-O"
COLLABORATION_GATE = "P219-P"
CONSCIOUSNESS_GATE = "P219-Q"
EVOLUTION_GATE = "P219-R"
FUTURES_GATE = "P219-S"
INTEL_GOV_GATE = "P219-T"
AUTO_OPS_GATE = "P219-U"
GEN_INTEL_GATE = "P219-V"
INTELLIGENCE_NEXUS_GATE = "P218-Z"
SPACE_GATE = "P218"
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

MATURITY = (
    "Individual Knowledge", "Shared Information", "Collaborative Knowledge",
    "Coordinated Intelligence", "Collective Intelligence", "Civilization Coordination Intelligence",
)
LAYERS = (
    {"id": "L01", "name": "Knowledge Communities"},
    {"id": "L02", "name": "Collaboration Layer"},
    {"id": "L03", "name": "Collective Intelligence Layer"},
    {"id": "L04", "name": "Coordination Digital Twin"},
    {"id": "L05", "name": "Decision Support Layer"},
    {"id": "L06", "name": "Adaptive Coordination Layer"},
)
COMMUNITY_DOMAINS = (
    "government", "industry", "research", "healthcare", "education",
    "infrastructure", "environment", "economy", "security", "space",
)
KNOWLEDGE_SOURCES = (
    "enterprise_systems", "knowledge_graphs", "research", "operational_metrics",
    "policies", "simulation_outputs", "expert_contributions", "historical_archives",
)
CONSENSUS_LIFECYCLE = (
    "Problem Definition", "Evidence Collection", "Alternative Analysis",
    "Impact Assessment", "Recommendation", "Human Decision", "Review",
)
COLLECTIVE_AGENTS = (
    "Knowledge Coordination Agent", "Collaboration Agent", "Evidence Intelligence Agent",
    "Recommendation Agent", "Learning Agent",
)
KG_ENTITIES = (
    "Community", "Expert", "Organization", "Mission", "Knowledge",
    "Evidence", "Capability", "Recommendation", "Decision", "Relationship",
)
KG_RELATIONSHIPS = (
    "CONTRIBUTES_TO", "SUPPORTS", "VALIDATES", "COLLABORATES_WITH",
    "DEPENDS_ON", "COORDINATES", "SHARES", "ENABLES",
)
DIGITAL_TWINS = (
    "Organization Twin", "Collaboration Twin", "Knowledge Twin", "Mission Twin", "Coordination Twin",
)
BOUNDED_CONTEXTS = (
    {
        "id": "BC-COLL-01", "name": "Collective Coordination Core", "type": "CORE",
        "aggregate": "CoordinationAggregate",
        "entities": ("Community", "CoordinationSession", "MissionWorkspace"),
        "value_objects": ("CoordinationPriority", "ParticipationLevel", "CoordinationStatus"),
        "services": ("CoordinationService", "CommunityManagementService"),
        "events": ("CommunityCreatedEvent", "CoordinationStartedEvent", "CoordinationCompletedEvent"),
    },
    {
        "id": "BC-COLL-02", "name": "Knowledge Collaboration Context", "type": "CORE",
        "aggregate": "KnowledgeAggregate",
        "entities": ("KnowledgeAsset", "Evidence", "KnowledgeContribution"),
        "value_objects": ("EvidenceStrength", "KnowledgeQuality", "ContributionScore"),
        "services": ("KnowledgeCollaborationService", "EvidenceManagementService"),
        "events": ("KnowledgeSharedEvent", "EvidenceValidatedEvent", "KnowledgeUpdatedEvent"),
    },
    {
        "id": "BC-COLL-03", "name": "Decision Support Context", "type": "CORE",
        "aggregate": "DecisionSupportAggregate",
        "entities": ("Recommendation", "DecisionContext", "Alternative"),
        "value_objects": ("RecommendationScore", "ConfidenceLevel", "StrategicImpact"),
        "services": ("RecommendationService", "DecisionSupportService"),
        "events": ("RecommendationPublishedEvent", "AlternativeEvaluatedEvent", "DecisionSupportedEvent"),
    },
    {
        "id": "BC-COLL-04", "name": "Learning Context", "type": "SUPPORTING",
        "aggregate": "LearningAggregate",
        "entities": ("LearningCycle", "Insight", "ImprovementAction"),
        "value_objects": ("LearningScore", "InsightQuality", "ImprovementPriority"),
        "services": ("LearningService", "ContinuousImprovementService"),
        "events": ("InsightCapturedEvent", "LearningCompletedEvent", "ImprovementInitiatedEvent"),
    },
)
PRIMARY_AGGREGATES = (
    "CoordinationAggregate", "CommunityAggregate", "KnowledgeAggregate",
    "DecisionSupportAggregate", "LearningAggregate",
)
COMMANDS = (
    "CreateCommunityCommand", "ShareKnowledgeCommand", "ValidateEvidenceCommand",
    "GenerateRecommendationCommand", "CoordinateMissionCommand", "CaptureInsightCommand",
)
QUERIES = (
    "GetCoordinationDashboardQuery", "GetCommunityInsightsQuery", "GetKnowledgeRepositoryQuery",
    "GetRecommendationCatalogQuery", "GetParticipationMetricsQuery", "GetLearningReportQuery",
)
CORE_EVENTS = (
    {"name": "CommunityCreatedEvent", "owner": "BC-COLL-01"},
    {"name": "KnowledgeSharedEvent", "owner": "BC-COLL-02"},
    {"name": "EvidenceValidatedEvent", "owner": "BC-COLL-02"},
    {"name": "RecommendationGeneratedEvent", "owner": "BC-COLL-03"},
    {"name": "CoordinationStartedEvent", "owner": "BC-COLL-01"},
    {"name": "CoordinationCompletedEvent", "owner": "BC-COLL-01"},
    {"name": "DecisionSupportedEvent", "owner": "BC-COLL-03"},
    {"name": "InsightCapturedEvent", "owner": "BC-COLL-04"},
    {"name": "KnowledgeGraphUpdatedEvent", "owner": "BC-COLL-02"},
    {"name": "LearningCompletedEvent", "owner": "BC-COLL-04"},
    {"name": "AlternativeEvaluatedEvent", "owner": "BC-COLL-03"},
    {"name": "ImprovementInitiatedEvent", "owner": "BC-COLL-04"},
)
KNOWLEDGE_GRAPH = {
    "present_required": True,
    "entities": KG_ENTITIES,
    "relationships": KG_RELATIONSHIPS,
    "capabilities": (
        "knowledge_navigation", "expert_discovery",
        "dependency_analysis", "contextual_reasoning",
    ),
}
DIGITAL_TWIN = {
    "present_required": True,
    "twins": DIGITAL_TWINS,
    "capabilities": (
        "coordination_simulation", "dependency_analysis",
        "collaboration_optimization", "operational_forecasting",
    ),
}
INTEGRATION = {
    "present_required": True,
    "peers": (
        "P214-Z", "P215-Z", "P216-Z", "P217-Z", "P218", "P218-Z",
        "P219", "P219-A", "P219-B", "P219-C", "P219-D", "P219-E", "P219-F",
        "P219-G", "P219-H", "P219-I", "P219-J", "P219-K", "P219-L", "P219-M",
        "P219-N", "P219-O", "P219-P", "P219-Q", "P219-R", "P219-S", "P219-T",
        "P219-U", "P219-V",
        "Policy Engine", "Workflow", "Audit", "MEOS Core",
    ),
    "integrations": (
        {"peer": "P214-Z", "provides": ("analytical_models",)},
        {"peer": "P215-Z", "provides": ("optimization_services",)},
        {"peer": "P216-Z", "provides": ("operational_coordination",)},
        {"peer": "P217-Z", "provides": ("scientific_collaboration",)},
        {"peer": "P218", "provides": ("mission_collaboration",)},
        {"peer": "P219-I", "provides": ("knowledge_federation",)},
        {"peer": "P219-K", "provides": ("policy_coordination",)},
        {"peer": "P219-P", "provides": ("enterprise_collaboration",)},
        {"peer": "P219-Q", "provides": ("shared_situational_awareness",)},
        {"peer": "P219-R", "provides": ("evolution_insights",)},
        {"peer": "P219-S", "provides": ("scenario_collaboration",)},
        {"peer": "P219-T", "provides": ("governance_coordination",)},
        {"peer": "P219-U", "provides": ("operational_coordination",)},
        {"peer": "P219-V", "provides": ("cross_domain_reasoning_coordination",)},
    ),
}
ROADMAP = {
    "phases": (
        {"id": "P01", "name": "Knowledge Foundation"},
        {"id": "P02", "name": "Collaboration Intelligence"},
        {"id": "P03", "name": "Adaptive Coordination"},
        {"id": "P04", "name": "Collective Intelligence"},
    ),
}
MICROSERVICES = (
    {"id": "collective_service", "api": "/civilization/collective-intelligence", "bc": "BC-COLL-01"},
    {"id": "global_coordination_service", "api": "/civilization/collective-intelligence/coordination", "bc": "BC-COLL-01"},
    {"id": "knowledge_collaboration_service", "api": "/civilization/collective-intelligence/knowledge", "bc": "BC-COLL-02"},
    {"id": "consensus_service", "api": "/civilization/collective-intelligence/consensus", "bc": "BC-COLL-03"},
    {"id": "learning_service", "api": "/civilization/collective-intelligence/learning", "bc": "BC-COLL-04"},
    {"id": "collective_twin_service", "api": "/civilization/collective-intelligence/digital-twin", "bc": "BC-COLL-01"},
    {"id": "collective_kg_service", "api": "/civilization/collective-intelligence/knowledge-graph", "bc": "BC-COLL-02"},
    {"id": "collective_agents_service", "api": "/civilization/collective-intelligence/agents", "bc": "BC-COLL-01"},
    {"id": "collective_events_service", "api": "/civilization/collective-intelligence/events", "bc": "BC-COLL-01"},
    {"id": "collective_integration_service", "api": "/civilization/collective-intelligence/integration", "bc": "BC-COLL-01"},
)


def vision_pack() -> dict[str, Any]:
    return {
        "primary_capability": PRIMARY_CAPABILITY,
        "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "planetary_gate": PLANETARY_GATE, "ai_os_gate": AI_OS_GATE,
        "simulation_gate": SIMULATION_GATE, "resources_gate": RESOURCES_GATE,
        "economy_gate": ECONOMY_GATE, "knowledge_gate": KNOWLEDGE_GATE,
        "human_gate": HUMAN_GATE, "governance_gate": GOVERNANCE_GATE,
        "innovation_gate": INNOVATION_GATE, "security_gate": SECURITY_GATE,
        "sustainability_gate": SUSTAINABILITY_GATE, "prosperity_gate": PROSPERITY_GATE,
        "collaboration_gate": COLLABORATION_GATE, "consciousness_gate": CONSCIOUSNESS_GATE,
        "evolution_gate": EVOLUTION_GATE, "futures_gate": FUTURES_GATE,
        "intel_gov_gate": INTEL_GOV_GATE, "auto_ops_gate": AUTO_OPS_GATE,
        "gen_intel_gate": GEN_INTEL_GATE,
        "intelligence_nexus_gate": INTELLIGENCE_NEXUS_GATE, "space_gate": SPACE_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "never_replace_p219_p_collaboration": True,
        "never_replace_p219_v_general_intelligence": True,
        "never_replace_p219_i_knowledge": True,
        "never_replace_institutional_governance": True,
        "never_centralized_autonomous_control_of_collective_intelligence": True,
        "never_ungated_collective_decision_execution": True,
        "never_opaque_unexplainable_collective_recommendations": True,
        "never_bypass_human_accountability_collective_intelligence": True,
        "foundation_for_p219_x": True,
    }


def architecture() -> dict[str, Any]:
    return {
        "present_required": True,
        "maturity": list(MATURITY),
        "maturity_stage_count": len(MATURITY),
        "layers": [dict(l) for l in LAYERS],
        "layer_count": len(LAYERS),
        "community_domains": list(COMMUNITY_DOMAINS),
        "community_domain_count": len(COMMUNITY_DOMAINS),
        "knowledge_sources": list(KNOWLEDGE_SOURCES),
        "knowledge_source_count": len(KNOWLEDGE_SOURCES),
        "consensus_lifecycle": list(CONSENSUS_LIFECYCLE),
        "consensus_lifecycle_step_count": len(CONSENSUS_LIFECYCLE),
    }


def global_coordination() -> dict[str, Any]:
    return {
        "present_required": True,
        "capabilities": (
            "mission_coordination", "cross_organization_planning",
            "shared_objectives", "dependency_management", "execution_synchronization",
        ),
        "never_replace_p219_p_collaboration": True,
    }


def knowledge_collaboration() -> dict[str, Any]:
    return {
        "present_required": True,
        "sources": list(KNOWLEDGE_SOURCES),
        "source_count": len(KNOWLEDGE_SOURCES),
        "capabilities": (
            "knowledge_federation", "semantic_search",
            "knowledge_validation", "knowledge_lineage", "context_assembly",
        ),
        "never_replace_p219_i_knowledge": True,
    }


def consensus() -> dict[str, Any]:
    return {
        "present_required": True,
        "lifecycle": list(CONSENSUS_LIFECYCLE),
        "lifecycle_step_count": len(CONSENSUS_LIFECYCLE),
        "capabilities": (
            "evidence_comparison", "alternative_ranking",
            "trade_off_analysis", "decision_documentation",
        ),
        "never_ungated_collective_decision_execution": True,
        "never_bypass_human_accountability_collective_intelligence": True,
    }


def learning() -> dict[str, Any]:
    return {
        "present_required": True,
        "capabilities": (
            "knowledge_evolution", "collaboration_analytics", "continuous_improvement",
        ),
        "entities": ("LearningCycle", "Insight", "ImprovementAction"),
        "events": ("InsightCaptured", "LearningCompleted", "ImprovementInitiated"),
    }


def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN) | {
        "twin_count": len(DIGITAL_TWINS),
        "capability_count": len(DIGITAL_TWIN["capabilities"]),
    }


def agents() -> dict[str, Any]:
    return {"present_required": True, "agents": list(COLLECTIVE_AGENTS), "agent_count": len(COLLECTIVE_AGENTS)}


def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH) | {
        "entity_count": len(KG_ENTITIES),
        "relationship_count": len(KG_RELATIONSHIPS),
        "capability_count": len(KNOWLEDGE_GRAPH["capabilities"]),
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
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p219_x": True}


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "primary_capability": PRIMARY_CAPABILITY, "principle": PRIMARY_CAPABILITY, "fabric": FABRIC,
        "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "planetary_gate": PLANETARY_GATE, "ai_os_gate": AI_OS_GATE,
        "simulation_gate": SIMULATION_GATE, "resources_gate": RESOURCES_GATE,
        "economy_gate": ECONOMY_GATE, "knowledge_gate": KNOWLEDGE_GATE,
        "human_gate": HUMAN_GATE, "governance_gate": GOVERNANCE_GATE,
        "innovation_gate": INNOVATION_GATE, "security_gate": SECURITY_GATE,
        "sustainability_gate": SUSTAINABILITY_GATE, "prosperity_gate": PROSPERITY_GATE,
        "collaboration_gate": COLLABORATION_GATE, "consciousness_gate": CONSCIOUSNESS_GATE,
        "evolution_gate": EVOLUTION_GATE, "futures_gate": FUTURES_GATE,
        "intel_gov_gate": INTEL_GOV_GATE, "auto_ops_gate": AUTO_OPS_GATE,
        "gen_intel_gate": GEN_INTEL_GATE,
        "intelligence_nexus_gate": INTELLIGENCE_NEXUS_GATE, "space_gate": SPACE_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": [
            "P219-V", "P219-U", "P219-T", "P219-S", "P219-R", "P219-Q", "P219-P", "P219-O", "P219-N", "P219-M",
            "P219-L", "P219-K", "P219-J", "P219-I", "P219-H", "P219-G", "P219-F", "P219-E", "P219-D", "P219-C",
            "P219-B", "P219-A", "P219", "P218-Z", "P218", "P217-Z", "P216-Z", "P215-Z", "P214-Z", "ADR-575",
        ],
        "vision": vision_pack(),
        "architecture": architecture(),
        "global_coordination": global_coordination(),
        "knowledge_collaboration": knowledge_collaboration(),
        "consensus": consensus(),
        "digital_twin": digital_twin(),
        "agents": agents(),
        "knowledge_graph": knowledge_graph(),
        "bounded_contexts": bounded_contexts(),
        "aggregates": aggregates(),
        "events": events(),
        "cqrs": cqrs(),
        "integration": integration(),
        "microservices": microservices(),
        "roadmap": roadmap(),
        "production_readiness": production_readiness(),
        "collective_intelligence_platform_present_required": True,
        "global_coordination_platform_present_required": True,
        "knowledge_collaboration_platform_present_required": True,
        "consensus_decision_support_platform_present_required": True,
        "coordination_digital_twin_present_required": True,
        "meos_collective_intelligence_global_coordination_core_present_required": True,
        "collective_intelligence_knowledge_graph_present_required": True,
        "collective_intelligence_event_architecture_present_required": True,
        "collective_intelligence_cqrs_model_present_required": True,
        "meos_collective_intelligence_integration_map_present_required": True,
        "never_replace_p219_foundation": True,
        "never_replace_p219_a_mission": True,
        "never_replace_p219_b_strategy": True,
        "never_replace_p219_c_domain": True,
        "never_replace_p219_d_planetary": True,
        "never_replace_p219_e_ai_os": True,
        "never_replace_p219_f_simulation": True,
        "never_replace_p219_g_resources": True,
        "never_replace_p219_h_economy": True,
        "never_replace_p219_i_knowledge": True,
        "never_replace_p219_j_human": True,
        "never_replace_p219_k_governance": True,
        "never_replace_p219_l_innovation": True,
        "never_replace_p219_m_security": True,
        "never_replace_p219_n_sustainability": True,
        "never_replace_p219_o_prosperity": True,
        "never_replace_p219_p_collaboration": True,
        "never_replace_p219_q_consciousness": True,
        "never_replace_p219_r_evolution": True,
        "never_replace_p219_s_futures": True,
        "never_replace_p219_t_intelligence_governance": True,
        "never_replace_p219_u_autonomous_operations": True,
        "never_replace_p219_v_general_intelligence": True,
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_policy_engine": True,
        "never_replace_workflow": True,
        "never_replace_audit": True,
        "never_replace_p215_z": True,
        "never_replace_p216_z": True,
        "never_replace_biotechnology": True,
        "never_replace_space": True,
        "never_replace_p218_z_intelligence_nexus": True,
        "never_merge_p218_t_space_civilization": True,
        "never_cross_context_aggregate_imports": True,
        "never_replace_institutional_governance": True,
        "never_centralized_autonomous_control_of_collective_intelligence": True,
        "never_opaque_unexplainable_collective_recommendations": True,
        "never_ungated_collective_decision_execution": True,
        "never_skip_ethical_collective_collaboration": True,
        "never_skip_human_authority_collective_decisions": True,
        "never_violate_human_sovereignty_collective_intelligence": True,
        "never_bypass_trusted_collective_validation": True,
        "never_bypass_human_supervision_collective_intelligence": True,
        "never_bypass_human_accountability_collective_intelligence": True,
        "no_module_local_llm": True,
        "sibling_collective_intelligence_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/collective-intelligence",
        "forbidden_sibling_bc": [
            "collective_intelligence_platform",
            "global_coordination_platform_bc",
            "distributed_knowledge_collaboration_bc",
        ],
        "foundation_for_p219_x": True,
    }


def collective_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /civilization/collective-intelligence",
        "GET /civilization/collective-intelligence/architecture",
        "GET /civilization/collective-intelligence/coordination",
        "GET /civilization/collective-intelligence/knowledge",
        "GET /civilization/collective-intelligence/consensus",
        "GET /civilization/collective-intelligence/learning",
        "GET /civilization/collective-intelligence/digital-twin",
        "GET /civilization/collective-intelligence/knowledge-graph",
        "GET /civilization/collective-intelligence/agents",
        "GET /civilization/collective-intelligence/bounded-contexts",
        "GET /civilization/collective-intelligence/aggregates",
        "GET /civilization/collective-intelligence/events",
        "GET /civilization/collective-intelligence/cqrs",
        "GET /civilization/collective-intelligence/integration",
        "GET /civilization/collective-intelligence/readiness",
    ]}
