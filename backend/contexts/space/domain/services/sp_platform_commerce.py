"""P218-R Enterprise Space Intelligence Commerce Intelligence — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P218-R"
ADR = 544
SOR = "space"
API_PREFIX = "/api/v1/space"
PRODUCT = "Enterprise Space Intelligence Commerce Intelligence & MEOS Space Commerce Intelligence Platform"
CAPABILITY = "CAP-PLT-SP-001"
COMMERCE_MISSION = (
    "Create an intelligent commercial ecosystem enabling companies, governments, researchers and "
    "autonomous systems to exchange space-based products, services, resources and capabilities "
    "across Earth orbit and future interplanetary markets."
)
COMMERCE_VISION = (
    "Transform fragmented commercial space activity into an explainable, human-supervised commerce "
    "intelligence fabric spanning marketplaces, investment networks, contracts and civilization-scale "
    "economic modeling."
)
FABRIC = "meos_space_commerce_intelligence_fabric"
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
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

ARCHITECTURE_LAYERS = (
    {"id": "L01", "name": "Space Commerce Foundation Layer", "components": ("company_registry", "asset_registry", "provider_registry", "investor_registry")},
    {"id": "L02", "name": "Commercial Intelligence Layer", "components": ("market_analytics", "demand", "pricing", "investment_analysis")},
    {"id": "L03", "name": "Marketplace Layer", "components": ("service_market", "resource_market", "data_market", "tech_exchange")},
    {"id": "L04", "name": "Commercial Operations Layer", "components": ("contracts", "procurement", "billing", "service_mgmt")},
    {"id": "L05", "name": "Space Economy Intelligence Layer", "components": ("economic_twin", "market_ai", "investment_ai", "strategy_engine")},
)
LIFECYCLE_STAGES = (
    "company_registration", "identity_verification", "service_listing", "customer_matching",
    "contract_negotiation", "compliance_validation", "transaction_authorization", "settlement",
    "performance_monitoring", "market_analytics",
)
MARKETPLACE = {
    "present_required": True,
    "platform": "meos_space_marketplace_platform",
    "domains": (
        "space_transportation", "satellite_services", "space_data", "manufacturing_services",
        "resource", "research_services", "infrastructure",
    ),
    "capabilities": (
        "service_discovery", "provider_matching", "contract_management", "pricing_intelligence",
        "transaction_management", "reputation_system", "marketplace_analytics",
    ),
    "participants": (
        "space_companies", "government_agencies", "research_organizations", "investors",
        "manufacturers", "logistics_providers", "autonomous_systems",
    ),
}
COMMERCIAL_OPERATIONS = {
    "present_required": True,
    "platform": "meos_commercial_space_operations_platform",
    "domains": (
        "satellite_services", "space_manufacturing_services", "orbital_infrastructure_services",
        "launch_services", "transportation_services", "research_services", "resource_services",
    ),
    "capabilities": (
        "service_management", "customer_operations", "commercial_mission_planning",
        "revenue_optimization", "performance_analytics", "contract_lifecycle_management",
    ),
}
ECONOMY = {
    "present_required": True,
    "platform": "meos_space_economy_intelligence_engine",
    "ai_capabilities": (
        "market_forecasting", "economic_modeling", "investment_prediction", "demand_analysis",
        "price_optimization", "business_risk_assessment", "industry_trend_detection",
    ),
    "models": (
        {"id": "MODEL-01", "name": "Space Economy Foundation Model"},
        {"id": "MODEL-02", "name": "Market Intelligence Model"},
        {"id": "MODEL-03", "name": "Investment Prediction Model"},
        {"id": "MODEL-04", "name": "Commercial Strategy Model"},
        {"id": "MODEL-05", "name": "Industry Forecasting Model"},
    ),
    "via_p214_z": True,
    "via_p218_e": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
}
INVESTMENT = {
    "present_required": True,
    "platform": "meos_space_investment_intelligence_platform",
    "domains": (
        "space_startups", "orbital_infrastructure", "space_manufacturing",
        "space_resources", "satellite_networks", "exploration_ventures",
    ),
    "capabilities": (
        "investment_analysis", "technology_evaluation", "market_potential_assessment",
        "risk_modeling", "portfolio_intelligence", "opportunity_discovery",
    ),
    "agents": (
        "investor_advisor", "market_analyst", "risk_assessment", "opportunity_discovery",
    ),
}
CONTRACTS = {
    "present_required": True,
    "platform": "meos_space_contract_transaction_intelligence",
    "capabilities": (
        "smart_contracts", "commercial_agreements", "service_contracts",
        "resource_exchange_agreements", "manufacturing_contracts", "transportation_contracts",
    ),
    "intelligence_functions": (
        "contract_analysis", "risk_detection", "compliance_validation",
        "negotiation_support", "performance_monitoring",
    ),
    "never_skip_contract_compliance_validation": True,
    "never_ungated_commercial_transaction": True,
    "never_duplicate_financial_kernel": True,
}
COMMERCE_AI = {
    "present_required": True,
    "platform": "meos_space_commerce_ai_platform",
    "capabilities": (
        "market_forecasting", "economic_modeling", "investment_prediction",
        "demand_analysis", "price_optimization", "business_risk_assessment",
        "industry_trend_detection", "marketplace_matching",
    ),
    "models": (
        {"id": "MODEL-01", "name": "Space Economy Foundation Model"},
        {"id": "MODEL-02", "name": "Market Intelligence Model"},
        {"id": "MODEL-03", "name": "Investment Prediction Model"},
        {"id": "MODEL-04", "name": "Commercial Strategy Model"},
        {"id": "MODEL-05", "name": "Industry Forecasting Model"},
    ),
    "via_p214_z": True,
    "via_p218_e": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
}
DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_space_commerce_digital_twin",
    "represents": (
        "space_economy", "companies", "markets", "services", "resources",
        "infrastructure", "investments", "supply_chains", "commercial_missions",
    ),
    "capabilities": (
        "economic_simulation", "market_forecasting", "scenario_analysis",
        "business_optimization", "investment_simulation", "industry_planning",
    ),
}
KNOWLEDGE_GRAPH = {
    "present_required": True,
    "platform": "meos_space_commerce_knowledge_graph",
    "entities": (
        "company", "space_asset", "service", "product", "market",
        "contract", "investment", "customer", "supplier", "technology",
    ),
    "relationships": (
        "COMPANY_PROVIDES_SERVICE", "CUSTOMER_PURCHASES_SERVICE", "INVESTMENT_SUPPORTS_COMPANY",
        "ASSET_ENABLES_SERVICE", "CONTRACT_CONNECTS_PARTIES", "TECHNOLOGY_ENABLES_MARKET",
    ),
    "capabilities": (
        "commercial_reasoning", "market_discovery", "business_intelligence",
        "investment_analysis", "economic_optimization",
    ),
}
GOVERNANCE = {
    "present_required": True,
    "domains": (
        "commercial_governance", "economic_governance", "marketplace_governance",
        "investment_governance", "contract_governance", "financial_governance",
        "identity_governance", "sustainable_commerce_governance",
    ),
    "approval_gates": (
        "company_onboarding", "service_listing_approval", "contract_activation",
        "transaction_authorization", "investment_disclosure", "settlement_posting",
        "marketplace_suspension",
    ),
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "via_financial_kernel": True,
    "never_ungated_commercial_transaction": True,
    "never_skip_marketplace_identity_verification": True,
    "never_skip_contract_compliance_validation": True,
    "never_opaque_unexplainable_commerce_decisions": True,
    "never_duplicate_financial_kernel": True,
}
OBSERVABILITY = {
    "present_required": True,
    "dashboards": (
        "marketplace_health", "commercial_pipeline", "investment_landscape",
        "contract_lifecycle", "settlement_status", "market_trends", "risk_posture",
    ),
    "kpis": (
        "marketplace_gmv", "active_listings", "contract_cycle_time", "settlement_success_rate",
        "investment_pipeline_value", "customer_match_rate", "pricing_accuracy",
        "commerce_compliance_score", "market_forecast_accuracy", "economic_index",
    ),
}
BOUNDED_CONTEXTS = (
    {"id": "BC-COM-01", "name": "Space Commerce Management"},
    {"id": "BC-COM-02", "name": "Marketplace Management"},
    {"id": "BC-COM-03", "name": "Commercial Operations"},
    {"id": "BC-COM-04", "name": "Investment Intelligence"},
    {"id": "BC-COM-05", "name": "Contract Management"},
    {"id": "BC-COM-06", "name": "Economic Analytics"},
    {"id": "BC-COM-07", "name": "Business Governance"},
)
SECURITY = {
    "present_required": True,
    "controls": (
        "zero_trust_commerce", "identity_verification", "transaction_security",
        "data_protection", "audit_logging", "policy_enforcement",
        "financial_kernel_settlement", "human_override",
    ),
    "via_identity": True, "via_policy_engine": True, "via_workflow": True,
    "via_audit": True, "via_integration": True, "via_financial_kernel": True,
    "via_p218_p": True, "via_p218_q": True,
    "never_ungated_commercial_transaction": True,
    "never_skip_marketplace_identity_verification": True,
    "never_skip_contract_compliance_validation": True,
    "never_opaque_unexplainable_commerce_decisions": True,
    "never_duplicate_financial_kernel": True,
    "never_replace_p218_q_sustainability": True,
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
        "p218p_security", "p218q_sustainability", "p217z_bio_nexus", "p216z_robotics_supreme",
        "p215z_quantum_supreme", "p214z_ai_master", "policy_engine", "workflow", "audit",
        "identity", "integration_platform", "financial_kernel", "knowledge_graph",
        "digital_twin", "commerce_fabric",
    ),
    "mechanisms": ("api_gateway", "event_bus", "acl_peer_ids_only", "outbox", "versioned_contracts"),
}
DEPLOYMENT = {
    "present_required": True,
    "environments": ("commerce_ops", "marketplace_sandbox", "settlement", "commerce_archive"),
    "cloud_native": True,
    "safety_critical": False,
    "financial_critical": True,
    "quantum_ready": True,
}
COMMANDS = (
    "RegisterSpaceCompanyCommand", "ListCommercialServiceCommand", "MatchCustomerCommand",
    "CreateContractCommand", "AuthorizeTransactionCommand", "IdentifyInvestmentCommand",
    "PostSettlementCommand", "SuspendMarketplaceListingCommand",
)
QUERIES = (
    "GetSpaceCompanyQuery", "GetMarketplaceListingQuery", "GetContractQuery",
    "GetInvestmentOpportunityQuery", "GetMarketForecastQuery", "GetEconomicIndicatorQuery",
)
CORE_EVENTS = (
    {"name": "CompanyRegisteredEvent", "schema": "space.commerce.company.registered.v1", "owner": "BC-COM-01"},
    {"name": "ServiceListedEvent", "schema": "space.commerce.service.listed.v1", "owner": "BC-COM-02"},
    {"name": "CustomerMatchedEvent", "schema": "space.commerce.customer.matched.v1", "owner": "BC-COM-02"},
    {"name": "ContractCreatedEvent", "schema": "space.commerce.contract.created.v1", "owner": "BC-COM-05"},
    {"name": "InvestmentIdentifiedEvent", "schema": "space.commerce.investment.identified.v1", "owner": "BC-COM-04"},
    {"name": "TransactionCompletedEvent", "schema": "space.commerce.transaction.completed.v1", "owner": "BC-COM-03"},
    {"name": "MarketTrendDetectedEvent", "schema": "space.commerce.market.trend.detected.v1", "owner": "BC-COM-06"},
    {"name": "BusinessRiskDetectedEvent", "schema": "space.commerce.business.risk.detected.v1", "owner": "BC-COM-06"},
    {"name": "CommercialMissionCreatedEvent", "schema": "space.commerce.mission.created.v1", "owner": "BC-COM-03"},
    {"name": "SettlementPostedEvent", "schema": "space.commerce.settlement.posted.v1", "owner": "BC-COM-05"},
)
MICROSERVICES = (
    {"id": "commerce_intel_service", "api": "/space/commerce", "events": ("CompanyRegisteredEvent",)},
    {"id": "marketplace_service", "api": "/space/commerce/marketplace", "events": ("ServiceListedEvent",)},
    {"id": "operations_service", "api": "/space/commerce/operations", "events": ("CommercialMissionCreatedEvent",)},
    {"id": "economy_service", "api": "/space/commerce/economy", "events": ("MarketTrendDetectedEvent",)},
    {"id": "investment_service", "api": "/space/commerce/investment", "events": ("InvestmentIdentifiedEvent",)},
    {"id": "contracts_service", "api": "/space/commerce/contracts", "events": ("ContractCreatedEvent",)},
    {"id": "commerce_ai_service", "api": "/space/commerce/commerce-ai", "events": ("BusinessRiskDetectedEvent",)},
    {"id": "commerce_twin_service", "api": "/space/commerce/digital-twin", "events": ("CustomerMatchedEvent",)},
    {"id": "commerce_observability_service", "api": "/space/commerce/observability", "events": ("TransactionCompletedEvent",)},
    {"id": "commerce_security_service", "api": "/space/commerce/security", "events": ("SettlementPostedEvent",)},
)
TESTING = (
    "commerce_lifecycle_testing", "marketplace_matching_testing", "contract_compliance_testing",
    "investment_intelligence_testing", "commerce_ai_explainability_testing",
    "economic_twin_sim_testing", "transaction_gate_testing", "financial_kernel_settlement_testing",
)
ROADMAP_PHASES = (
    {"phase": 1, "name": "Space Commerce Foundation"},
    {"phase": 2, "name": "Commercial Space Operations"},
    {"phase": 3, "name": "Space Economy Intelligence"},
    {"phase": 4, "name": "Interplanetary Space Economy"},
)
QUALITY_GATES_REJECT_IF = (
    "space_commerce_platform_is_missing", "space_economy_intelligence_is_missing",
    "commercial_operations_is_missing", "space_marketplace_is_missing",
    "investment_intelligence_is_missing", "contract_intelligence_is_missing",
    "commerce_ai_is_missing", "economic_digital_twin_is_missing",
    "governance_is_missing", "commerce_architecture_is_missing",
    "ungated_commercial_transaction", "skip_marketplace_identity_verification",
    "skip_contract_compliance_validation", "opaque_unexplainable_commerce_decisions",
    "duplicate_financial_kernel", "replace_p218_q_sustainability",
    "module_local_llm", "sibling_space_bc",
)


def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Space Commerce Intelligence Fabric", "mission": COMMERCE_MISSION,
        "vision": COMMERCE_VISION, "builds_on_p218": True,
        **{f"builds_on_p218_{x.lower()}": True for x in "ABCDEFGHIJKLMNOPQ"},
        "builds_on_p217_z": True, "builds_on_p216_z": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "never_replace_p218_q_sustainability": True,
        "never_ungated_commercial_transaction": True,
        "never_skip_marketplace_identity_verification": True,
        "never_skip_contract_compliance_validation": True,
        "never_opaque_unexplainable_commerce_decisions": True,
        "never_duplicate_financial_kernel": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
    }


def architecture() -> dict[str, Any]:
    return {"present_required": True, "layers": [dict(x) for x in ARCHITECTURE_LAYERS], "layer_count": len(ARCHITECTURE_LAYERS)}


def lifecycle() -> dict[str, Any]:
    return {
        "present_required": True, "stages": list(LIFECYCLE_STAGES), "stage_count": len(LIFECYCLE_STAGES),
        "commercial_transaction_gated": True, "marketplace_identity_required": True,
        "contract_compliance_required": True, "financial_kernel_settlement_required": True,
        "human_override_required": True,
    }


def marketplace() -> dict[str, Any]:
    return dict(MARKETPLACE) | {
        "domain_count": len(MARKETPLACE["domains"]),
        "capability_count": len(MARKETPLACE["capabilities"]),
        "participant_count": len(MARKETPLACE["participants"]),
    }


def operations() -> dict[str, Any]:
    return dict(COMMERCIAL_OPERATIONS) | {
        "domain_count": len(COMMERCIAL_OPERATIONS["domains"]),
        "capability_count": len(COMMERCIAL_OPERATIONS["capabilities"]),
    }


def economy() -> dict[str, Any]:
    return dict(ECONOMY) | {
        "ai_capability_count": len(ECONOMY["ai_capabilities"]),
        "model_count": len(ECONOMY["models"]),
    }


def investment() -> dict[str, Any]:
    return dict(INVESTMENT) | {
        "domain_count": len(INVESTMENT["domains"]),
        "capability_count": len(INVESTMENT["capabilities"]),
        "agent_count": len(INVESTMENT["agents"]),
    }


def contracts() -> dict[str, Any]:
    return dict(CONTRACTS) | {
        "capability_count": len(CONTRACTS["capabilities"]),
        "intelligence_function_count": len(CONTRACTS["intelligence_functions"]),
    }


def commerce_ai() -> dict[str, Any]:
    return dict(COMMERCE_AI) | {
        "capability_count": len(COMMERCE_AI["capabilities"]),
        "model_count": len(COMMERCE_AI["models"]),
    }


def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN) | {
        "representation_count": len(DIGITAL_TWIN["represents"]),
        "capability_count": len(DIGITAL_TWIN["capabilities"]),
    }


def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH) | {
        "entity_count": len(KNOWLEDGE_GRAPH["entities"]),
        "relationship_count": len(KNOWLEDGE_GRAPH["relationships"]),
        "capability_count": len(KNOWLEDGE_GRAPH["capabilities"]),
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
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p218_s": True}


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT,
        "capability": CAPABILITY, "commerce_mission": COMMERCE_MISSION,
        "commerce_vision": COMMERCE_VISION, "principle": COMMERCE_MISSION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "infrastructure_gate": INFRASTRUCTURE_GATE, "space_ai_gate": SPACE_AI_GATE,
        "satellite_gate": SATELLITE_GATE, "orbital_gate": ORBITAL_GATE,
        "communications_gate": COMMUNICATIONS_GATE, "navigation_gate": NAVIGATION_GATE,
        "mission_intel_gate": MISSION_INTEL_GATE, "scientific_gate": SCIENTIFIC_GATE,
        "exploration_gate": EXPLORATION_GATE, "manufacturing_gate": MANUFACTURING_GATE,
        "resources_gate": RESOURCES_GATE, "logistics_gate": LOGISTICS_GATE,
        "security_gate": SECURITY_GATE, "sustainability_gate": SUSTAINABILITY_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P218"] + [f"P218-{x}" for x in "ABCDEFGHIJKLMNOPQ"] + ["P217-Z", "P216-Z", "P215-Z", "P214-Z"] + [f"ADR-{i}" for i in range(526, 544)],
        "vision": vision_pack(), "architecture": architecture(), "lifecycle": lifecycle(),
        "marketplace": marketplace(), "operations": operations(), "economy": economy(),
        "investment": investment(), "contracts": contracts(), "commerce_ai": commerce_ai(),
        "digital_twin": digital_twin(), "knowledge_graph": knowledge_graph(),
        "governance": governance(), "observability": observability(), "security": security(),
        "bounded_contexts": bounded_contexts(), "integration": integration(),
        "deployment": deployment(), "cqrs": cqrs(), "events": events(),
        "microservices": microservices(), "testing": testing(), "roadmap": roadmap(),
        "quality_gates": quality_gates(), "production_readiness": production_readiness(),
        "space_commerce_platform_present_required": True,
        "space_economy_intelligence_present_required": True,
        "commercial_operations_present_required": True,
        "space_marketplace_present_required": True,
        "investment_intelligence_present_required": True,
        "contract_intelligence_present_required": True,
        "commerce_ai_present_required": True,
        "economic_digital_twin_present_required": True,
        "knowledge_graph_present_required": True,
        "ddd_model_present_required": True, "governance_present_required": True,
        "commerce_architecture_present_required": True, "observability_present_required": True,
        "deployment_architecture_present_required": True, "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True, "microservices_architecture_present_required": True,
        "sibling_space_bc_forbidden": True,
        "never_replace_p218_q_sustainability": True,
        "never_ungated_commercial_transaction": True,
        "never_skip_marketplace_identity_verification": True,
        "never_skip_contract_compliance_validation": True,
        "never_opaque_unexplainable_commerce_decisions": True,
        "never_duplicate_financial_kernel": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
        "api_prefix": f"{API_PREFIX}/commerce",
        "forbidden_sibling_bc": ["space_commerce_platform", "space_marketplace_bc", "space_economy_bc"],
        "foundation_for_p218_s": True,
    }


def commerce_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /space/commerce", "GET /space/commerce/vision",
        "GET /space/commerce/architecture", "GET /space/commerce/lifecycle",
        "GET /space/commerce/marketplace", "GET /space/commerce/operations",
        "GET /space/commerce/economy", "GET /space/commerce/investment",
        "GET /space/commerce/contracts", "GET /space/commerce/commerce-ai",
        "GET /space/commerce/digital-twin", "GET /space/commerce/knowledge-graph",
        "GET /space/commerce/observability", "GET /space/commerce/governance",
        "GET /space/commerce/security", "GET /space/commerce/integration",
        "GET /space/commerce/deployment", "GET /space/commerce/testing",
        "GET /space/commerce/cqrs", "GET /space/commerce/events",
        "GET /space/commerce/readiness",
    ]}
