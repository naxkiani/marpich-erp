"""P218-T Enterprise Space Intelligence Civilization Intelligence — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P218-T"
ADR = 546
SOR = "space"
API_PREFIX = "/api/v1/space"
PRODUCT = "Enterprise Space Intelligence Civilization Intelligence & MEOS Space Civilization Intelligence Platform"
CAPABILITY = "CAP-PLT-SP-001"
CIVILIZATION_MISSION = (
    "Create an intelligent civilization operating platform capable of modeling, governing and "
    "optimizing future human societies across Earth, orbital habitats, lunar settlements, Mars "
    "colonies and future interplanetary environments."
)
CIVILIZATION_VISION = (
    "Transform fragmented settlement and governance planning into an explainable, human-supervised "
    "civilization intelligence fabric spanning society modeling, interplanetary governance, ethical AI "
    "and long-horizon multi-planetary coordination."
)
FABRIC = "meos_space_civilization_intelligence_fabric"
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
SCIENTIFIC_GATE = "P218-K"
EXPLORATION_GATE = "P218-L"
MANUFACTURING_GATE = "P218-M"
RESOURCES_GATE = "P218-N"
LOGISTICS_GATE = "P218-O"
SECURITY_GATE = "P218-P"
SUSTAINABILITY_GATE = "P218-Q"
COMMERCE_GATE = "P218-R"
EDUCATION_GATE = "P218-S"
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

ARCHITECTURE_LAYERS = (
    {"id": "L01", "name": "Human Society Intelligence Layer", "components": ("population", "social_systems", "culture", "collective_intel")},
    {"id": "L02", "name": "Civilization Operations Layer", "components": ("settlements", "habitats", "public_services", "community_gov")},
    {"id": "L03", "name": "Governance Intelligence Layer", "components": ("policy_engine", "decision_intel", "diplomacy", "conflict_resolution")},
    {"id": "L04", "name": "Civilization Simulation Layer", "components": ("digital_twin", "scenario_modeling", "population_sim", "impact_analysis")},
    {"id": "L05", "name": "Future Civilization Intelligence Layer", "components": ("forecasting", "human_ai_collab", "long_term_planning", "evolution")},
)
LIFECYCLE_STAGES = (
    "civilization_registration", "settlement_planning", "community_formation", "society_modeling",
    "governance_design", "ethics_review", "policy_authorization", "scenario_simulation",
    "interplanetary_coordination", "civilization_forecasting",
)
SOCIETY = {
    "present_required": True,
    "platform": "meos_human_space_society_intelligence_platform",
    "domains": ("orbital_communities", "lunar_settlements", "mars_colonies", "space_habitats", "interplanetary_communities"),
    "capabilities": (
        "social_modeling", "community_formation", "settlement_planning",
        "human_wellbeing_intelligence", "cultural_preservation", "social_network_intelligence",
    ),
    "intelligence_functions": (
        "population_forecasting", "social_stability_analysis", "community_optimization", "human_experience_management",
    ),
}
GOVERNANCE_PLATFORM = {
    "present_required": True,
    "platform": "meos_interplanetary_governance_platform",
    "domains": (
        "planetary_governance", "orbital_governance", "lunar_governance",
        "mars_governance", "interplanetary_relations", "resource_governance",
    ),
    "capabilities": (
        "policy_creation", "regulation_management", "decision_support",
        "governance_simulation", "public_administration_intelligence", "conflict_prevention",
    ),
    "agents": (
        "policy_advisor", "governance_analyst", "diplomacy", "compliance", "social_impact",
    ),
}
FUTURE_ARCHITECTURE = {
    "present_required": True,
    "platform": "meos_future_space_civilization_architecture",
    "components": (
        "space_settlements", "orbital_cities", "planetary_colonies",
        "interplanetary_networks", "autonomous_infrastructure", "human_ai_systems",
    ),
    "architecture_domains": (
        "social", "economic", "political", "technological", "environmental", "cultural",
    ),
}
CIVILIZATION_AI = {
    "present_required": True,
    "platform": "meos_civilization_intelligence_ai_platform",
    "capabilities": (
        "civilization_modeling", "future_prediction", "policy_simulation",
        "social_optimization", "economic_forecasting", "risk_analysis", "collective_intelligence",
    ),
    "models": (
        {"id": "MODEL-01", "name": "Space Civilization Foundation Model"},
        {"id": "MODEL-02", "name": "Human Society Intelligence Model"},
        {"id": "MODEL-03", "name": "Governance Reasoning Model"},
        {"id": "MODEL-04", "name": "Future Scenario Model"},
        {"id": "MODEL-05", "name": "Social Dynamics Model"},
    ),
    "via_p214_z": True,
    "via_p218_e": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
}
DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_civilization_digital_twin",
    "represents": (
        "human_populations", "settlements", "habitats", "governance_systems",
        "economies", "cultural_networks", "infrastructure", "resources",
    ),
    "capabilities": (
        "civilization_simulation", "policy_testing", "future_scenario_analysis",
        "social_impact_prediction", "economic_modeling", "settlement_optimization",
    ),
}
CULTURE = {
    "present_required": True,
    "platform": "meos_space_knowledge_cultural_intelligence",
    "domains": (
        "human_history", "scientific_knowledge", "space_heritage",
        "cultural_systems", "civilization_values", "collective_memory",
    ),
    "capabilities": (
        "knowledge_preservation", "cultural_intelligence", "civilization_learning",
        "historical_simulation", "collective_knowledge_management",
    ),
}
KNOWLEDGE_GRAPH = {
    "present_required": True,
    "platform": "meos_space_civilization_knowledge_graph",
    "entities": (
        "human_community", "settlement", "governance_system", "policy", "culture",
        "resource", "institution", "organization", "civilization_model",
    ),
    "relationships": (
        "COMMUNITY_EXISTS_IN_SETTLEMENT", "POLICY_GOVERNS_SYSTEM", "RESOURCE_SUPPORTS_COMMUNITY",
        "CULTURE_INFLUENCES_SOCIETY", "INSTITUTION_SERVES_POPULATION",
    ),
    "capabilities": (
        "civilization_reasoning", "social_intelligence", "governance_analysis", "future_prediction",
    ),
}
ECONOMY = {
    "present_required": True,
    "domains": (
        "space_commerce", "resource_economy", "knowledge_economy",
        "manufacturing_economy", "interplanetary_trade",
    ),
    "capabilities": (
        "economic_planning", "resource_allocation", "market_intelligence",
        "social_prosperity_analysis", "long_term_economic_simulation",
    ),
    "via_p218_r": True, "via_p218_n": True, "via_p218_m": True, "via_p218_o": True,
}
ETHICS = {
    "present_required": True,
    "framework": "meos_space_civilization_ethics_framework",
    "domains": (
        "social_security", "governance_security", "ai_ethics",
        "human_rights_protection", "civilization_resilience",
    ),
    "controls": (
        "ethical_ai_governance", "transparent_decision_systems", "privacy_protection",
        "identity_sovereignty", "trust_framework",
    ),
    "never_ungated_governance_decision": True,
    "never_skip_ethical_ai_review": True,
    "never_skip_human_rights_protection": True,
}
GOVERNANCE = {
    "present_required": True,
    "domains": (
        "civilization_governance", "settlement_governance", "interplanetary_policy_governance",
        "ethics_governance", "cultural_governance", "social_rights_governance",
        "ai_civilization_governance", "future_planning_governance",
    ),
    "approval_gates": (
        "settlement_charter", "policy_approval", "governance_decision",
        "ethics_review", "interplanetary_agreement", "scenario_publication",
        "rights_impact_assessment",
    ),
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "never_ungated_governance_decision": True,
    "never_skip_ethical_ai_review": True,
    "never_skip_human_rights_protection": True,
    "never_opaque_unexplainable_civilization_decisions": True,
}
OBSERVABILITY = {
    "present_required": True,
    "dashboards": (
        "civilization_health", "settlement_status", "governance_pipeline",
        "social_stability", "ethics_compliance", "forecast_scenarios", "cultural_vitality",
    ),
    "kpis": (
        "settlement_readiness_index", "social_stability_score", "governance_transparency",
        "ethics_compliance_rate", "human_rights_protection_score", "scenario_fidelity",
        "interplanetary_coordination_index", "cultural_preservation_rate",
        "prosperity_index", "civilization_forecast_accuracy",
    ),
}
BOUNDED_CONTEXTS = (
    {"id": "BC-CIV-01", "name": "Civilization Management"},
    {"id": "BC-CIV-02", "name": "Human Society Management"},
    {"id": "BC-CIV-03", "name": "Settlement Governance"},
    {"id": "BC-CIV-04", "name": "Interplanetary Policy"},
    {"id": "BC-CIV-05", "name": "Social Intelligence"},
    {"id": "BC-CIV-06", "name": "Cultural Intelligence"},
    {"id": "BC-CIV-07", "name": "Future Planning"},
)
SECURITY = {
    "present_required": True,
    "controls": (
        "ethical_ai_governance", "transparent_decision_systems", "privacy_protection",
        "identity_sovereignty", "trust_framework", "human_rights_protection",
        "audit_trails", "human_override",
    ),
    "via_identity": True, "via_policy_engine": True, "via_workflow": True,
    "via_audit": True, "via_integration": True, "via_p218_s": True, "via_p218_p": True,
    "never_ungated_governance_decision": True,
    "never_skip_ethical_ai_review": True,
    "never_skip_human_rights_protection": True,
    "never_opaque_unexplainable_civilization_decisions": True,
    "never_replace_p218_s_education": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
}
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p218_foundation", "p218a_mission", "p218b_strategy", "p218c_domain",
        "p218d_infrastructure", "p218e_space_ai", "p218f_satellite", "p218g_orbital",
        "p218h_communications", "p218i_navigation", "p218j_mission_intel", "p218k_scientific",
        "p218l_exploration", "p218m_manufacturing", "p218n_resources", "p218o_logistics",
        "p218p_security", "p218q_sustainability", "p218r_commerce", "p218s_education",
        "p217z_bio_nexus", "p216z_robotics_supreme", "p215z_quantum_supreme", "p214z_ai_master",
        "policy_engine", "workflow", "audit", "identity", "integration_platform",
        "knowledge_graph", "digital_twin", "civilization_fabric",
    ),
    "mechanisms": ("api_gateway", "event_bus", "acl_peer_ids_only", "outbox", "versioned_contracts"),
}
DEPLOYMENT = {
    "present_required": True,
    "environments": ("civilization_ops", "governance_sim", "ethics_review", "civilization_archive"),
    "cloud_native": True,
    "safety_critical": True,
    "ethics_critical": True,
    "quantum_ready": True,
}
COMMANDS = (
    "CreateSettlementCommand", "EstablishCommunityCommand", "ApprovePolicyCommand",
    "MakeGovernanceDecisionCommand", "GenerateCivilizationScenarioCommand",
    "CreateInterplanetaryAgreementCommand", "PreserveCulturalAssetCommand",
    "CompleteEthicsReviewCommand",
)
QUERIES = (
    "GetCivilizationQuery", "GetSettlementQuery", "GetSocietyMetricsQuery",
    "GetGovernancePolicyQuery", "GetCivilizationForecastQuery", "GetSocialRiskQuery",
)
CORE_EVENTS = (
    {"name": "SettlementCreatedEvent", "schema": "space.civilization.settlement.created.v1", "owner": "BC-CIV-03"},
    {"name": "CommunityEstablishedEvent", "schema": "space.civilization.community.established.v1", "owner": "BC-CIV-02"},
    {"name": "PolicyApprovedEvent", "schema": "space.civilization.policy.approved.v1", "owner": "BC-CIV-04"},
    {"name": "GovernanceDecisionMadeEvent", "schema": "space.civilization.governance.decision.made.v1", "owner": "BC-CIV-04"},
    {"name": "SocialRiskDetectedEvent", "schema": "space.civilization.social.risk.detected.v1", "owner": "BC-CIV-05"},
    {"name": "CivilizationScenarioGeneratedEvent", "schema": "space.civilization.scenario.generated.v1", "owner": "BC-CIV-07"},
    {"name": "FutureModelUpdatedEvent", "schema": "space.civilization.future.model.updated.v1", "owner": "BC-CIV-07"},
    {"name": "InterplanetaryAgreementCreatedEvent", "schema": "space.civilization.agreement.created.v1", "owner": "BC-CIV-04"},
    {"name": "CulturalAssetPreservedEvent", "schema": "space.civilization.culture.preserved.v1", "owner": "BC-CIV-06"},
    {"name": "EthicsReviewCompletedEvent", "schema": "space.civilization.ethics.review.completed.v1", "owner": "BC-CIV-01"},
)
MICROSERVICES = (
    {"id": "civilization_intel_service", "api": "/space/civilization", "events": ("SettlementCreatedEvent",)},
    {"id": "society_service", "api": "/space/civilization/society", "events": ("CommunityEstablishedEvent",)},
    {"id": "governance_service", "api": "/space/civilization/governance", "events": ("GovernanceDecisionMadeEvent",)},
    {"id": "future_architecture_service", "api": "/space/civilization/future-architecture", "events": ("FutureModelUpdatedEvent",)},
    {"id": "civilization_ai_service", "api": "/space/civilization/civilization-ai", "events": ("CivilizationScenarioGeneratedEvent",)},
    {"id": "civilization_twin_service", "api": "/space/civilization/digital-twin", "events": ("SocialRiskDetectedEvent",)},
    {"id": "culture_service", "api": "/space/civilization/culture", "events": ("CulturalAssetPreservedEvent",)},
    {"id": "civilization_kg_service", "api": "/space/civilization/knowledge-graph", "events": ("InterplanetaryAgreementCreatedEvent",)},
    {"id": "civilization_economy_service", "api": "/space/civilization/economy", "events": ("PolicyApprovedEvent",)},
    {"id": "civilization_ethics_service", "api": "/space/civilization/ethics", "events": ("EthicsReviewCompletedEvent",)},
)
TESTING = (
    "civilization_lifecycle_testing", "society_modeling_testing", "governance_gate_testing",
    "ethics_review_testing", "civilization_ai_explainability_testing",
    "digital_twin_scenario_testing", "human_rights_protection_testing", "interplanetary_policy_testing",
)
ROADMAP_PHASES = (
    {"phase": 1, "name": "Civilization Intelligence Foundation"},
    {"phase": 2, "name": "Interplanetary Society Platform"},
    {"phase": 3, "name": "Future Civilization Modeling"},
    {"phase": 4, "name": "Multi-Planetary Civilization Operating System"},
)
QUALITY_GATES_REJECT_IF = (
    "space_civilization_platform_is_missing", "human_society_intelligence_is_missing",
    "interplanetary_governance_is_missing", "future_civilization_architecture_is_missing",
    "civilization_ai_is_missing", "digital_civilization_twin_is_missing",
    "knowledge_graph_is_missing", "ethics_framework_is_missing",
    "governance_is_missing", "civilization_architecture_is_missing",
    "ungated_governance_decision", "skip_ethical_ai_review",
    "skip_human_rights_protection", "opaque_unexplainable_civilization_decisions",
    "replace_p218_s_education", "module_local_llm", "sibling_space_bc",
)


def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Space Civilization Intelligence Fabric", "mission": CIVILIZATION_MISSION,
        "vision": CIVILIZATION_VISION, "builds_on_p218": True,
        **{f"builds_on_p218_{x.lower()}": True for x in "ABCDEFGHIJKLMNOPQRS"},
        "builds_on_p217_z": True, "builds_on_p216_z": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "never_replace_p218_s_education": True,
        "never_ungated_governance_decision": True,
        "never_skip_ethical_ai_review": True,
        "never_skip_human_rights_protection": True,
        "never_opaque_unexplainable_civilization_decisions": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
    }


def architecture() -> dict[str, Any]:
    return {"present_required": True, "layers": [dict(x) for x in ARCHITECTURE_LAYERS], "layer_count": len(ARCHITECTURE_LAYERS)}


def lifecycle() -> dict[str, Any]:
    return {
        "present_required": True, "stages": list(LIFECYCLE_STAGES), "stage_count": len(LIFECYCLE_STAGES),
        "governance_decision_gated": True, "ethical_ai_review_required": True,
        "human_rights_protection_required": True, "human_override_required": True,
    }


def society() -> dict[str, Any]:
    return dict(SOCIETY) | {
        "domain_count": len(SOCIETY["domains"]),
        "capability_count": len(SOCIETY["capabilities"]),
        "intelligence_function_count": len(SOCIETY["intelligence_functions"]),
    }


def governance_platform() -> dict[str, Any]:
    return dict(GOVERNANCE_PLATFORM) | {
        "domain_count": len(GOVERNANCE_PLATFORM["domains"]),
        "capability_count": len(GOVERNANCE_PLATFORM["capabilities"]),
        "agent_count": len(GOVERNANCE_PLATFORM["agents"]),
    }


def future_architecture() -> dict[str, Any]:
    return dict(FUTURE_ARCHITECTURE) | {
        "component_count": len(FUTURE_ARCHITECTURE["components"]),
        "architecture_domain_count": len(FUTURE_ARCHITECTURE["architecture_domains"]),
    }


def civilization_ai() -> dict[str, Any]:
    return dict(CIVILIZATION_AI) | {
        "capability_count": len(CIVILIZATION_AI["capabilities"]),
        "model_count": len(CIVILIZATION_AI["models"]),
    }


def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN) | {
        "representation_count": len(DIGITAL_TWIN["represents"]),
        "capability_count": len(DIGITAL_TWIN["capabilities"]),
    }


def culture() -> dict[str, Any]:
    return dict(CULTURE) | {
        "domain_count": len(CULTURE["domains"]),
        "capability_count": len(CULTURE["capabilities"]),
    }


def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH) | {
        "entity_count": len(KNOWLEDGE_GRAPH["entities"]),
        "relationship_count": len(KNOWLEDGE_GRAPH["relationships"]),
        "capability_count": len(KNOWLEDGE_GRAPH["capabilities"]),
    }


def economy() -> dict[str, Any]:
    return dict(ECONOMY) | {
        "domain_count": len(ECONOMY["domains"]),
        "capability_count": len(ECONOMY["capabilities"]),
    }


def ethics() -> dict[str, Any]:
    return dict(ETHICS) | {
        "domain_count": len(ETHICS["domains"]),
        "control_count": len(ETHICS["controls"]),
    }


def governance() -> dict[str, Any]:
    return dict(GOVERNANCE) | {
        "domain_count": len(GOVERNANCE["domains"]),
        "approval_gate_count": len(GOVERNANCE["approval_gates"]),
    }


def observability() -> dict[str, Any]:
    return dict(OBSERVABILITY) | {
        "dashboard_count": len(OBSERVABILITY["dashboards"]),
        "kpi_count": len(OBSERVABILITY["kpis"]),
    }


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
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p218_u": True}


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT,
        "capability": CAPABILITY, "civilization_mission": CIVILIZATION_MISSION,
        "civilization_vision": CIVILIZATION_VISION, "principle": CIVILIZATION_MISSION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "infrastructure_gate": INFRASTRUCTURE_GATE, "space_ai_gate": SPACE_AI_GATE,
        "satellite_gate": SATELLITE_GATE, "orbital_gate": ORBITAL_GATE,
        "communications_gate": COMMUNICATIONS_GATE, "navigation_gate": NAVIGATION_GATE,
        "mission_intel_gate": MISSION_INTEL_GATE, "scientific_gate": SCIENTIFIC_GATE,
        "exploration_gate": EXPLORATION_GATE, "manufacturing_gate": MANUFACTURING_GATE,
        "resources_gate": RESOURCES_GATE, "logistics_gate": LOGISTICS_GATE,
        "security_gate": SECURITY_GATE, "sustainability_gate": SUSTAINABILITY_GATE,
        "commerce_gate": COMMERCE_GATE, "education_gate": EDUCATION_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P218"] + [f"P218-{x}" for x in "ABCDEFGHIJKLMNOPQRS"] + ["P217-Z", "P216-Z", "P215-Z", "P214-Z"] + [f"ADR-{i}" for i in range(526, 546)],
        "vision": vision_pack(), "architecture": architecture(), "lifecycle": lifecycle(),
        "society": society(), "governance_platform": governance_platform(),
        "future_architecture": future_architecture(), "civilization_ai": civilization_ai(),
        "digital_twin": digital_twin(), "culture": culture(),
        "knowledge_graph": knowledge_graph(), "economy": economy(), "ethics": ethics(),
        "governance": governance(), "observability": observability(), "security": security(),
        "bounded_contexts": bounded_contexts(), "integration": integration(),
        "deployment": deployment(), "cqrs": cqrs(), "events": events(),
        "microservices": microservices(), "testing": testing(), "roadmap": roadmap(),
        "quality_gates": quality_gates(), "production_readiness": production_readiness(),
        "space_civilization_platform_present_required": True,
        "human_society_intelligence_present_required": True,
        "interplanetary_governance_present_required": True,
        "future_civilization_architecture_present_required": True,
        "civilization_ai_present_required": True,
        "digital_civilization_twin_present_required": True,
        "knowledge_graph_present_required": True,
        "ethics_framework_present_required": True,
        "ddd_model_present_required": True, "governance_present_required": True,
        "civilization_architecture_present_required": True, "observability_present_required": True,
        "deployment_architecture_present_required": True, "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True, "microservices_architecture_present_required": True,
        "sibling_space_bc_forbidden": True,
        "never_replace_p218_s_education": True,
        "never_ungated_governance_decision": True,
        "never_skip_ethical_ai_review": True,
        "never_skip_human_rights_protection": True,
        "never_opaque_unexplainable_civilization_decisions": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
        "api_prefix": f"{API_PREFIX}/civilization",
        "forbidden_sibling_bc": ["space_civilization_platform", "interplanetary_governance_bc", "human_space_society_bc"],
        "foundation_for_p218_u": True,
    }


def civilization_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /space/civilization", "GET /space/civilization/vision",
        "GET /space/civilization/architecture", "GET /space/civilization/lifecycle",
        "GET /space/civilization/society", "GET /space/civilization/governance",
        "GET /space/civilization/future-architecture", "GET /space/civilization/civilization-ai",
        "GET /space/civilization/digital-twin", "GET /space/civilization/culture",
        "GET /space/civilization/knowledge-graph", "GET /space/civilization/economy",
        "GET /space/civilization/observability", "GET /space/civilization/ethics",
        "GET /space/civilization/security", "GET /space/civilization/integration",
        "GET /space/civilization/deployment", "GET /space/civilization/testing",
        "GET /space/civilization/cqrs", "GET /space/civilization/events",
        "GET /space/civilization/readiness",
    ]}
