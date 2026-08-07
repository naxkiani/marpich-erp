"""P218-N Enterprise Space Intelligence Resource Intelligence — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P218-N"
ADR = 540
SOR = "space"
API_PREFIX = "/api/v1/space"
PRODUCT = "Enterprise Space Intelligence Resource Intelligence & MEOS Space Resource Intelligence Platform"
CAPABILITY = "CAP-PLT-SP-001"
RESOURCES_MISSION = (
    "Create an intelligent planetary-scale resource platform capable of discovering, evaluating "
    "and managing extraterrestrial resources required for exploration, manufacturing and future space civilization."
)
RESOURCES_VISION = (
    "Transform Earth-dependent supply into an explainable, human-supervised, planetary-protection-compliant "
    "resource intelligence fabric spanning ISRU, asteroid mining and circular space resource economies."
)
FABRIC = "meos_space_resource_intelligence_fabric"
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
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

ARCHITECTURE_LAYERS = (
    {"id": "L01", "name": "Resource Discovery Layer", "components": ("orbital_surveys", "spectral_analysis", "remote_sensing", "detection_ai")},
    {"id": "L02", "name": "Resource Intelligence Layer", "components": ("classification", "value_assessment", "feasibility", "forecasting")},
    {"id": "L03", "name": "Extraction Intelligence Layer", "components": ("mining_ai", "robotic_extraction", "processing", "safety")},
    {"id": "L04", "name": "Resource Economy Layer", "components": ("marketplace", "trading", "pricing", "supply_management")},
    {"id": "L05", "name": "Resource Governance & Knowledge Layer", "components": ("planetary_protection", "resource_rights", "sustainability", "knowledge_graph")},
)
LIFECYCLE_STAGES = (
    "resource_detection", "resource_validation", "site_selection", "extraction_planning",
    "extraction_authorization", "extraction", "processing", "storage", "distribution", "utilization",
)
ISRU = {
    "present_required": True,
    "platform": "meos_isru_intelligence_platform",
    "capabilities": (
        "water_extraction", "oxygen_production", "fuel_production", "regolith_processing",
        "construction_materials", "chemical_processing", "energy_resource_utilization",
    ),
    "operations": (
        "resource_detection", "site_selection", "extraction_planning", "processing",
        "storage", "distribution", "utilization",
    ),
}
ASTEROID = {
    "present_required": True,
    "platform": "meos_asteroid_mining_intelligence_platform",
    "targets": ("near_earth_objects", "metallic_asteroids", "carbonaceous_asteroids", "water_rich_asteroids"),
    "capabilities": (
        "asteroid_identification", "composition_analysis", "mining_feasibility", "mission_planning",
        "extraction_optimization", "return_strategy", "resource_valuation",
    ),
}
PLANETARY = {
    "present_required": True,
    "platform": "meos_planetary_resource_management_platform",
    "domains": (
        "lunar", "mars", "asteroid", "planetary_atmosphere", "subsurface", "ice_deposits", "mineral_deposits",
    ),
    "capabilities": (
        "resource_mapping", "resource_inventory", "extraction_planning", "consumption_forecasting",
        "reserve_management", "sustainability_analysis",
    ),
}
AUTONOMY = {
    "present_required": True,
    "platform": "meos_autonomous_resource_extraction_platform",
    "agents": (
        "mining", "exploration", "resource_assessment", "extraction_planning",
        "processing", "logistics", "safety",
    ),
    "functions": (
        "autonomous_survey", "site_selection", "extraction_execution",
        "equipment_management", "resource_processing", "failure_recovery",
    ),
    "via_p216_z": True,
    "never_ungated_resource_extraction_authorization": True,
    "never_disable_human_override": True,
}
RESOURCE_AI = {
    "present_required": True,
    "platform": "meos_space_resource_ai_platform",
    "capabilities": (
        "resource_discovery", "composition_prediction", "extraction_optimization", "mining_simulation",
        "demand_forecasting", "economic_modeling", "risk_prediction",
    ),
    "models": (
        {"id": "MODEL-01", "name": "Space Resource Foundation Model"},
        {"id": "MODEL-02", "name": "Planetary Geology Model"},
        {"id": "MODEL-03", "name": "Mining Optimization Model"},
        {"id": "MODEL-04", "name": "Resource Economics Model"},
        {"id": "MODEL-05", "name": "ISRU Planning Model"},
    ),
    "via_p214_z": True,
    "via_p218_e": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
}
DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_space_resource_digital_twin",
    "represents": ("resource_deposits", "mining_sites", "extraction_systems", "robots", "processing_facilities", "transport_systems", "resource_markets"),
    "capabilities": ("resource_simulation", "extraction_forecasting", "mining_optimization", "environmental_impact_analysis", "economic_simulation", "operational_planning"),
}
ECONOMY = {
    "present_required": True,
    "platform": "meos_space_resource_marketplace",
    "capabilities": ("resource_trading", "demand_forecasting", "pricing_intelligence", "supply_management", "contract_management"),
}
GOVERNANCE = {
    "present_required": True,
    "domains": (
        "planetary_protection", "resource_rights", "environmental_management",
        "extraction_ethics", "resource_sustainability", "economic_governance",
        "operational_safety", "traceability",
    ),
    "approval_gates": (
        "resource_validation", "environmental_assessment", "planetary_protection_for_extraction",
        "extraction_authorization", "processing_authorization", "transfer_authorization", "depletion_closure",
    ),
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "never_ungated_resource_extraction_authorization": True,
    "never_skip_resource_environmental_assessment": True,
    "never_skip_planetary_protection_for_extraction": True,
    "never_violate_circular_resource_economy_principles": True,
}
OBSERVABILITY = {
    "present_required": True,
    "dashboards": (
        "resource_portfolio", "isru_operations", "asteroid_targets", "extraction_status",
        "reserves", "marketplace", "environmental_impact", "resource_ai",
    ),
    "kpis": (
        "discovery_rate", "validated_reserve_volume", "extraction_efficiency", "isru_yield",
        "autonomous_extraction_rate", "environmental_compliance_score", "circular_reuse_rate",
        "marketplace_liquidity", "earth_dependency_reduction", "sustainability_index",
    ),
}
BOUNDED_CONTEXTS = (
    {"id": "BC-RES-01", "name": "Resource Discovery"},
    {"id": "BC-RES-02", "name": "Resource Assessment"},
    {"id": "BC-RES-03", "name": "ISRU Operations"},
    {"id": "BC-RES-04", "name": "Mining Operations"},
    {"id": "BC-RES-05", "name": "Resource Processing"},
    {"id": "BC-RES-06", "name": "Resource Marketplace"},
    {"id": "BC-RES-07", "name": "Resource Digital Twin"},
    {"id": "BC-RES-08", "name": "Resource Governance"},
)
SECURITY = {
    "present_required": True,
    "controls": (
        "zero_trust", "resource_authentication", "extraction_authorization", "planetary_protection",
        "environmental_controls", "human_override", "audit_trail", "marketplace_integrity",
    ),
    "via_identity": True, "via_policy_engine": True, "via_workflow": True,
    "via_audit": True, "via_integration": True,
    "never_ungated_resource_extraction_authorization": True,
    "never_skip_resource_environmental_assessment": True,
    "never_skip_planetary_protection_for_extraction": True,
    "never_violate_circular_resource_economy_principles": True,
    "never_replace_p218_m_manufacturing": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
}
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p218_foundation", "p218a_mission", "p218b_strategy", "p218c_domain",
        "p218d_infrastructure", "p218e_space_ai", "p218f_satellite", "p218g_orbital",
        "p218h_communications", "p218i_navigation", "p218j_mission_intel", "p218k_scientific",
        "p218l_exploration", "p218m_manufacturing",
        "p217z_bio_nexus", "p216z_robotics_supreme", "p215z_quantum_supreme", "p214z_ai_master",
        "policy_engine", "workflow", "audit", "identity", "integration_platform",
        "knowledge_graph", "digital_twin",
    ),
    "mechanisms": ("api_gateway", "event_bus", "acl_peer_ids_only", "outbox", "versioned_contracts"),
}
DEPLOYMENT = {
    "present_required": True,
    "environments": ("resource_survey", "extraction_simulation", "isru_operations", "resource_archive"),
    "cloud_native": True,
    "safety_critical": True,
    "circular_resource_economy": True,
}
COMMANDS = (
    "DetectResourceCommand", "ValidateResourceCommand", "AuthorizeExtractionCommand",
    "StartExtractionCommand", "CompleteProcessingCommand", "TransferResourceCommand",
    "UpdateReserveCommand", "CloseDepletedResourceCommand",
)
QUERIES = (
    "GetResourceDepositQuery", "GetMiningSiteQuery", "GetISRUFacilityQuery",
    "GetResourceInventoryQuery", "GetExtractionMissionQuery", "GetResourceValueQuery",
)
CORE_EVENTS = (
    {"name": "ResourceDetectedEvent", "schema": "space.resources.resource.detected.v1", "owner": "BC-RES-01"},
    {"name": "ResourceValidatedEvent", "schema": "space.resources.resource.validated.v1", "owner": "BC-RES-02"},
    {"name": "MiningMissionCreatedEvent", "schema": "space.resources.mining.created.v1", "owner": "BC-RES-04"},
    {"name": "ExtractionStartedEvent", "schema": "space.resources.extraction.started.v1", "owner": "BC-RES-04"},
    {"name": "ProcessingCompletedEvent", "schema": "space.resources.processing.completed.v1", "owner": "BC-RES-05"},
    {"name": "ResourceTransferredEvent", "schema": "space.resources.resource.transferred.v1", "owner": "BC-RES-06"},
    {"name": "ReserveUpdatedEvent", "schema": "space.resources.reserve.updated.v1", "owner": "BC-RES-02"},
    {"name": "ResourceDepletedEvent", "schema": "space.resources.resource.depleted.v1", "owner": "BC-RES-08"},
    {"name": "ISRUFacilityActivatedEvent", "schema": "space.resources.isru.activated.v1", "owner": "BC-RES-03"},
    {"name": "ExtractionAuthorizedEvent", "schema": "space.resources.extraction.authorized.v1", "owner": "BC-RES-08"},
)
MICROSERVICES = (
    {"id": "resources_intel_service", "api": "/space/resources", "events": ("ResourceDetectedEvent",)},
    {"id": "isru_service", "api": "/space/resources/isru", "events": ("ISRUFacilityActivatedEvent",)},
    {"id": "asteroid_service", "api": "/space/resources/asteroid", "events": ("MiningMissionCreatedEvent",)},
    {"id": "planetary_service", "api": "/space/resources/planetary", "events": ("ReserveUpdatedEvent",)},
    {"id": "autonomy_service", "api": "/space/resources/autonomy", "events": ("ExtractionStartedEvent",)},
    {"id": "resource_ai_service", "api": "/space/resources/resource-ai", "events": ("ResourceValidatedEvent",)},
    {"id": "resources_twin_service", "api": "/space/resources/digital-twin", "events": ("ProcessingCompletedEvent",)},
    {"id": "resources_observability_service", "api": "/space/resources/observability", "events": ("ResourceTransferredEvent",)},
    {"id": "resources_governance_service", "api": "/space/resources/governance", "events": ("ExtractionAuthorizedEvent",)},
    {"id": "resources_security_service", "api": "/space/resources/security", "events": ("ResourceDepletedEvent",)},
)
TESTING = (
    "resource_lifecycle_testing", "isru_operations_testing", "asteroid_mining_testing",
    "planetary_inventory_testing", "autonomy_override_testing", "resource_ai_explainability_testing",
    "extraction_authorization_gate_testing", "planetary_protection_extraction_gate_testing",
)
ROADMAP_PHASES = (
    {"phase": 1, "name": "Resource Intelligence Foundation"},
    {"phase": 2, "name": "ISRU Operations"},
    {"phase": 3, "name": "Space Resource Economy"},
    {"phase": 4, "name": "Planetary Resource Civilization"},
)
QUALITY_GATES_REJECT_IF = (
    "resource_intelligence_is_missing", "isru_platform_is_missing",
    "asteroid_mining_intelligence_is_missing", "planetary_resource_management_is_missing",
    "autonomous_extraction_is_missing", "resource_ai_is_missing",
    "digital_twin_is_missing", "governance_is_missing",
    "security_architecture_is_missing", "observability_is_missing",
    "ungated_resource_extraction_authorization", "skip_resource_environmental_assessment",
    "skip_planetary_protection_for_extraction", "violate_circular_resource_economy_principles",
    "replace_p218_m_manufacturing", "module_local_llm", "sibling_space_bc",
)


def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Space Resource Intelligence Fabric", "mission": RESOURCES_MISSION,
        "vision": RESOURCES_VISION, "builds_on_p218": True,
        **{f"builds_on_p218_{x.lower()}": True for x in "ABCDEFGHIJKLM"},
        "builds_on_p217_z": True, "builds_on_p216_z": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "never_replace_p218_m_manufacturing": True,
        "never_ungated_resource_extraction_authorization": True,
        "never_skip_resource_environmental_assessment": True,
        "never_skip_planetary_protection_for_extraction": True,
        "never_violate_circular_resource_economy_principles": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
    }


def architecture() -> dict[str, Any]:
    return {"present_required": True, "layers": [dict(x) for x in ARCHITECTURE_LAYERS], "layer_count": len(ARCHITECTURE_LAYERS)}


def lifecycle() -> dict[str, Any]:
    return {
        "present_required": True, "stages": list(LIFECYCLE_STAGES), "stage_count": len(LIFECYCLE_STAGES),
        "extraction_authorization_gated": True, "environmental_assessment_required": True,
        "planetary_protection_for_extraction_required": True, "circular_resource_economy": True,
    }


def isru() -> dict[str, Any]:
    return dict(ISRU) | {"capability_count": len(ISRU["capabilities"]), "operation_count": len(ISRU["operations"])}


def asteroid() -> dict[str, Any]:
    return dict(ASTEROID) | {"target_count": len(ASTEROID["targets"]), "capability_count": len(ASTEROID["capabilities"])}


def planetary() -> dict[str, Any]:
    return dict(PLANETARY) | {"domain_count": len(PLANETARY["domains"]), "capability_count": len(PLANETARY["capabilities"])}


def autonomy() -> dict[str, Any]:
    return dict(AUTONOMY) | {"agent_count": len(AUTONOMY["agents"]), "function_count": len(AUTONOMY["functions"])}


def resource_ai() -> dict[str, Any]:
    return dict(RESOURCE_AI) | {"capability_count": len(RESOURCE_AI["capabilities"]), "model_count": len(RESOURCE_AI["models"])}


def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN) | {"representation_count": len(DIGITAL_TWIN["represents"]), "capability_count": len(DIGITAL_TWIN["capabilities"])}


def economy() -> dict[str, Any]:
    return dict(ECONOMY) | {"capability_count": len(ECONOMY["capabilities"])}


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
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p218_o": True}


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT,
        "capability": CAPABILITY, "resources_mission": RESOURCES_MISSION,
        "resources_vision": RESOURCES_VISION, "principle": RESOURCES_MISSION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "infrastructure_gate": INFRASTRUCTURE_GATE, "space_ai_gate": SPACE_AI_GATE,
        "satellite_gate": SATELLITE_GATE, "orbital_gate": ORBITAL_GATE,
        "communications_gate": COMMUNICATIONS_GATE, "navigation_gate": NAVIGATION_GATE,
        "mission_intel_gate": MISSION_INTEL_GATE, "scientific_gate": SCIENTIFIC_GATE,
        "exploration_gate": EXPLORATION_GATE, "manufacturing_gate": MANUFACTURING_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P218"] + [f"P218-{x}" for x in "ABCDEFGHIJKLM"] + ["P217-Z", "P216-Z", "P215-Z", "P214-Z"] + [f"ADR-{i}" for i in range(526, 540)],
        "vision": vision_pack(), "architecture": architecture(), "lifecycle": lifecycle(),
        "isru": isru(), "asteroid": asteroid(), "planetary": planetary(),
        "autonomy": autonomy(), "resource_ai": resource_ai(),
        "digital_twin": digital_twin(), "economy": economy(),
        "governance": governance(), "observability": observability(), "security": security(),
        "bounded_contexts": bounded_contexts(), "integration": integration(),
        "deployment": deployment(), "cqrs": cqrs(), "events": events(),
        "microservices": microservices(), "testing": testing(), "roadmap": roadmap(),
        "quality_gates": quality_gates(), "production_readiness": production_readiness(),
        "resource_intelligence_present_required": True,
        "isru_platform_present_required": True,
        "asteroid_mining_intelligence_present_required": True,
        "planetary_resource_management_present_required": True,
        "autonomous_extraction_present_required": True,
        "resource_ai_present_required": True,
        "digital_twin_present_required": True,
        "ddd_model_present_required": True, "governance_present_required": True,
        "security_architecture_present_required": True, "observability_present_required": True,
        "deployment_architecture_present_required": True, "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True, "microservices_architecture_present_required": True,
        "sibling_space_bc_forbidden": True,
        "never_replace_p218_m_manufacturing": True,
        "never_ungated_resource_extraction_authorization": True,
        "never_skip_resource_environmental_assessment": True,
        "never_skip_planetary_protection_for_extraction": True,
        "never_violate_circular_resource_economy_principles": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
        "api_prefix": f"{API_PREFIX}/resources",
        "forbidden_sibling_bc": ["space_resource_platform", "isru_platform_bc", "asteroid_mining_bc"],
        "foundation_for_p218_o": True,
    }


def resources_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /space/resources", "GET /space/resources/vision",
        "GET /space/resources/architecture", "GET /space/resources/lifecycle",
        "GET /space/resources/isru", "GET /space/resources/asteroid",
        "GET /space/resources/planetary", "GET /space/resources/autonomy",
        "GET /space/resources/resource-ai", "GET /space/resources/digital-twin",
        "GET /space/resources/economy", "GET /space/resources/observability",
        "GET /space/resources/governance", "GET /space/resources/security",
        "GET /space/resources/integration", "GET /space/resources/deployment",
        "GET /space/resources/testing", "GET /space/resources/cqrs",
        "GET /space/resources/events", "GET /space/resources/readiness",
    ]}
