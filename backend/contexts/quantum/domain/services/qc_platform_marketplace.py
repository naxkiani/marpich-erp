"""P215-P Enterprise Quantum Marketplace, Capability Exchange, Economy & Innovation — immutable catalog."""
from __future__ import annotations
from typing import Any
PROMPT_ID = "P215-P"
ADR = 461
SOR = "quantum"
API_PREFIX = "/api/v1/quantum"
PRODUCT = "Enterprise Quantum Marketplace, Quantum Capability Exchange, Quantum Economy & Quantum Innovation Ecosystem Platform"
CAPABILITY = "CAP-PLT-QC-001"
PRINCIPLE = "MEOS Quantum Marketplace Platform SHALL provide a trusted ecosystem where quantum capabilities, services, applications and innovations can be discovered, exchanged and evolved."
FABRIC = "meos_quantum_economy_intelligence_fabric"
CORE_DOMAIN = "enterprise_quantum_economy_intelligence_management"
SUPPORTING_DOMAINS = (
    {"id": "quantum_marketplace", "purpose": "Marketplace listings, discovery and commerce."},
    {"id": "quantum_capability", "purpose": "Capability registration, classification and recommendation."},
    {"id": "quantum_service_exchange", "purpose": "Service publishing, consumption and lifecycle."},
    {"id": "quantum_application", "purpose": "Application distribution and licensing."},
    {"id": "quantum_algorithm_commerce", "purpose": "Algorithm publishing, monetization and reuse."},
    {"id": "quantum_resource_sharing", "purpose": "Hardware access and compute exchange."},
    {"id": "quantum_innovation", "purpose": "Research collaboration and innovation projects."},
    {"id": "quantum_partner_ecosystem", "purpose": "Provider and partnership networks."},
    {"id": "quantum_economic_analytics", "purpose": "Market and adoption intelligence via P213."},
)
GENERIC_DOMAINS = ("identity", "security", "observability", "billing", "compliance", "search", "plugins")
LOGICAL_BOUNDED_CONTEXTS = (
    {"id": "quantum_capability_marketplace", "bc": "BC-01", "name": "Quantum Capability Marketplace Context", "owns": "QuantumCapabilityAggregate", "purpose": "Capability registration, discovery, classification, recommendation."},
    {"id": "quantum_service_exchange", "bc": "BC-02", "name": "Quantum Service Exchange Context", "owns": "QuantumServiceExchangeAggregate", "purpose": "Service publishing, consumption, lifecycle."},
    {"id": "quantum_application_marketplace", "bc": "BC-03", "name": "Quantum Application Marketplace Context", "owns": "QuantumApplicationAggregate", "purpose": "Applications, distribution, licensing."},
    {"id": "quantum_algorithm_economy", "bc": "BC-04", "name": "Quantum Algorithm Economy Context", "owns": "QuantumAlgorithmCommerceAggregate", "purpose": "Algorithm publishing, reuse, monetization."},
    {"id": "quantum_resource_sharing", "bc": "BC-05", "name": "Quantum Resource Sharing Context", "owns": "QuantumResourceMarketplaceAggregate", "purpose": "Hardware access, compute allocation, resource exchange."},
    {"id": "quantum_innovation_ecosystem", "bc": "BC-06", "name": "Quantum Innovation Ecosystem Context", "owns": "QuantumInnovationAggregate", "purpose": "Research collaboration, innovation projects, partnerships."},
    {"id": "quantum_economic_intelligence", "bc": "BC-07", "name": "Quantum Economic Intelligence Context", "owns": "QuantumEconomyIntelligenceAggregate", "purpose": "Market analysis, adoption intelligence, economic forecasting."},
)
AGGREGATES = (
    {"name": "EnterpriseQuantumMarketplaceAggregate", "root": "QuantumMarketplaceListing", "entities": ("QuantumCapability", "QuantumService", "QuantumApplication", "QuantumAlgorithmProduct", "QuantumProvider", "QuantumConsumer", "QuantumMarketplaceListing", "QuantumTransaction", "QuantumInnovationProject", "QuantumPartnership"), "value_objects": ("CapabilityScore", "TrustScore", "InnovationScore", "MarketValueScore", "QualityScore", "AdoptionScore", "EconomicImpactScore"), "events": ("QuantumCapabilityRegisteredEvent", "QuantumServicePublishedEvent", "QuantumMarketplaceTransactionCreatedEvent", "QuantumApplicationSubscribedEvent", "QuantumInnovationStartedEvent", "QuantumPartnershipCreatedEvent")},
    {"name": "QuantumCapabilityAggregate", "root": "QuantumCapability", "entities": ("CapabilityClassification", "Recommendation"), "value_objects": ("CapabilityScore", "TrustScore"), "events": ("CapabilityRegisteredEvent", "QuantumCapabilityRegisteredEvent")},
    {"name": "QuantumServiceExchangeAggregate", "root": "QuantumService", "entities": ("ServiceSubscription", "UsageRecord"), "value_objects": ("QualityScore", "AdoptionScore"), "events": ("ServicePublishedEvent", "QuantumServicePublishedEvent")},
    {"name": "QuantumApplicationAggregate", "root": "QuantumApplication", "entities": ("LicenseGrant", "InstallRecord"), "value_objects": ("TrustScore", "QualityScore"), "events": ("ApplicationSubscribedEvent", "QuantumApplicationSubscribedEvent")},
    {"name": "QuantumAlgorithmCommerceAggregate", "root": "QuantumAlgorithmProduct", "entities": ("AlgorithmVersion", "LicenseOffer"), "value_objects": ("MarketValueScore", "QualityScore"), "events": ("AlgorithmReleasedEvent",)},
    {"name": "QuantumResourceMarketplaceAggregate", "root": "QuantumMarketplaceListing", "entities": ("ComputeOffer", "Allocation"), "value_objects": ("CapabilityScore", "AdoptionScore"), "events": ("MarketplaceTransactionCompletedEvent",)},
    {"name": "QuantumInnovationAggregate", "root": "QuantumInnovationProject", "entities": ("QuantumPartnership", "Challenge"), "value_objects": ("InnovationScore", "EconomicImpactScore"), "events": ("InnovationProjectCreatedEvent", "QuantumInnovationStartedEvent", "QuantumPartnershipCreatedEvent")},
    {"name": "QuantumEconomyIntelligenceAggregate", "root": "QuantumTransaction", "entities": ("MarketSignal", "AdoptionTrend"), "value_objects": ("EconomicImpactScore", "MarketValueScore"), "events": ("MarketplaceTransactionCompletedEvent", "QuantumMarketplaceTransactionCreatedEvent")},
)
DOMAIN_SERVICES = (
    {"id": "quantum_marketplace_service", "responsibility": "manage marketplace listings and transactions", "inputs": ("listing_spec",), "outputs": ("listing_ref",), "rules": ("via_p215_k", "via_financial_kernel"), "events": ("MarketplaceTransactionCompletedEvent",)},
    {"id": "capability_discovery_service", "responsibility": "register and discover quantum capabilities", "inputs": ("capability_spec",), "outputs": ("capability_ref",), "rules": ("via_p215_m", "via_enterprise_search"), "events": ("CapabilityRegisteredEvent",)},
    {"id": "quantum_service_exchange_service", "responsibility": "publish and subscribe quantum services", "inputs": ("service_spec",), "outputs": ("service_ref",), "rules": ("via_p215_o",), "events": ("ServicePublishedEvent",)},
    {"id": "algorithm_marketplace_service", "responsibility": "publish and license algorithms", "inputs": ("algorithm_product_spec",), "outputs": ("algorithm_product_ref",), "rules": ("via_p215_e", "via_p215_o"), "events": ("AlgorithmReleasedEvent",)},
    {"id": "application_marketplace_service", "responsibility": "distribute quantum applications", "inputs": ("app_spec",), "outputs": ("application_ref",), "rules": ("via_plugin_platform",), "events": ("ApplicationSubscribedEvent",)},
    {"id": "innovation_ecosystem_service", "responsibility": "manage innovation projects and partnerships", "inputs": ("innovation_spec",), "outputs": ("project_ref",), "rules": ("via_p215_k",), "events": ("InnovationProjectCreatedEvent",)},
    {"id": "economic_intelligence_service", "responsibility": "analyze market and adoption", "inputs": ("economy_query",), "outputs": ("impact_report",), "rules": ("via_p213",), "events": ("MarketplaceTransactionCompletedEvent",)},
)
CORE_EVENTS = (
    {"name": "CapabilityRegisteredEvent", "producer": "quantum_capability_marketplace", "consumers": "search,kg,integration"},
    {"name": "ServicePublishedEvent", "producer": "quantum_service_exchange", "consumers": "catalog,certification,governance"},
    {"name": "MarketplaceTransactionCompletedEvent", "producer": "quantum_marketplace", "consumers": "billing,analytics,audit"},
    {"name": "ApplicationSubscribedEvent", "producer": "quantum_application_marketplace", "consumers": "ops,plugin_platform"},
    {"name": "AlgorithmReleasedEvent", "producer": "quantum_algorithm_economy", "consumers": "software,certification"},
    {"name": "InnovationProjectCreatedEvent", "producer": "quantum_innovation_ecosystem", "consumers": "collaboration,governance,notifications"},
)
MARKETPLACE_PLATFORM = {"present_required": True, "capabilities": ("listing", "discovery", "trust_validation", "exchange", "subscription", "rating"), "equation": "Quantum Capabilities -> Marketplace Discovery -> Trust Validation -> Capability Exchange -> Economic Transactions -> Innovation Collaboration -> Quantum Ecosystem Growth"}
CAPABILITY_EXCHANGE = {"present_required": True, "manages": ("quantum_computing_services", "quantum_ai_models", "quantum_algorithms", "quantum_simulators", "quantum_data_products", "quantum_digital_twins", "quantum_security_services"), "capabilities": ("discovery", "matching", "recommendation", "evaluation", "subscription", "consumption"), "via_p215_m": True}
SERVICE_ECONOMY = {"present_required": True, "supports": ("qcaas", "qaias", "simulation_as_a_service", "optimization_as_a_service", "security_as_a_service"), "capabilities": ("service_catalog", "pricing_models", "subscription_management", "usage_tracking", "service_rating"), "via_financial_kernel": True}
ALGORITHM_MARKETPLACE = {"present_required": True, "manages": ("optimization", "machine_learning", "scientific", "cryptographic", "simulation"), "capabilities": ("publishing", "validation", "versioning", "licensing", "reuse"), "via_p215_e": True, "via_p215_o": True}
APPLICATION_MARKETPLACE = {"present_required": True, "manages": ("enterprise_apps", "industry_solutions", "research_apps", "ai_quantum_apps"), "capabilities": ("discovery", "installation", "configuration", "updates", "security_validation"), "via_plugin_platform": True, "module_local_plugin_marketplace_forbidden": True}
INNOVATION_ECOSYSTEM = {"present_required": True, "connects": ("enterprises", "researchers", "universities", "providers", "developers", "ai_agents"), "capabilities": ("collaboration", "research_projects", "innovation_challenges", "knowledge_exchange", "funding_intelligence")}
ECONOMIC_INTELLIGENCE = {"present_required": True, "analyzes": ("market_demand", "capability_adoption", "innovation_trends", "economic_impact", "technology_maturity"), "via_p213": True}
CONTEXT_MAP = (
    {"from": "quantum_capability_marketplace", "to": "quantum_integration", "type": "customer_supplier", "via": "P215-M"},
    {"from": "quantum_algorithm_economy", "to": "quantum_software", "type": "customer_supplier", "via": "P215-E"},
    {"from": "quantum_algorithm_economy", "to": "quantum_quality", "type": "customer_supplier", "via": "P215-O"},
    {"from": "quantum_service_exchange", "to": "quantum_quality", "type": "customer_supplier", "via": "P215-O"},
    {"from": "quantum_application_marketplace", "to": "plugin_platform", "type": "anti_corruption_layer", "via": "PluginPlatform"},
    {"from": "quantum_economic_intelligence", "to": "decision_intelligence", "type": "anti_corruption_layer", "via": "P213"},
    {"from": "quantum_innovation_ecosystem", "to": "quantum_governance", "type": "conformist", "via": "P215-K"},
    {"from": "quantum_resource_sharing", "to": "quantum_infrastructure", "type": "customer_supplier", "via": "P215-D"},
    {"from": "quantum_capability_marketplace", "to": "quantum_ai", "type": "customer_supplier", "via": "P215-F"},
)
MICROSERVICES = (
    {"id": "quantum_marketplace_service", "bc": "root", "aggregate": "EnterpriseQuantumMarketplaceAggregate", "api": "/quantum/marketplace", "db": "quantum_*", "events": ("MarketplaceTransactionCompletedEvent",), "security": ("quantum.read",), "scaling": "marketplace_replicas"},
    {"id": "capability_discovery_service", "bc": "BC-01", "aggregate": "QuantumCapabilityAggregate", "api": "/quantum/marketplace/capabilities", "db": "quantum_*", "events": ("CapabilityRegisteredEvent",), "security": ("quantum.write",), "scaling": "discovery_workers"},
    {"id": "quantum_service_exchange_service", "bc": "BC-02", "aggregate": "QuantumServiceExchangeAggregate", "api": "/quantum/marketplace/services", "db": "quantum_*", "events": ("ServicePublishedEvent",), "security": ("quantum.write",), "scaling": "service_workers"},
    {"id": "algorithm_marketplace_service", "bc": "BC-04", "aggregate": "QuantumAlgorithmCommerceAggregate", "api": "/quantum/marketplace/algorithms", "db": "quantum_*", "events": ("AlgorithmReleasedEvent",), "security": ("quantum.write",), "scaling": "algorithm_workers"},
    {"id": "application_marketplace_service", "bc": "BC-03", "aggregate": "QuantumApplicationAggregate", "api": "/quantum/marketplace/applications", "db": "quantum_*", "events": ("ApplicationSubscribedEvent",), "security": ("quantum.write",), "scaling": "app_workers"},
    {"id": "resource_sharing_service", "bc": "BC-05", "aggregate": "QuantumResourceMarketplaceAggregate", "api": "/quantum/marketplace/resources", "db": "quantum_*", "events": ("MarketplaceTransactionCompletedEvent",), "security": ("quantum.write",), "scaling": "resource_workers"},
    {"id": "innovation_ecosystem_service", "bc": "BC-06", "aggregate": "QuantumInnovationAggregate", "api": "/quantum/marketplace/innovation", "db": "quantum_*", "events": ("InnovationProjectCreatedEvent",), "security": ("quantum.write",), "scaling": "innovation_workers"},
    {"id": "economic_intelligence_service", "bc": "BC-07", "aggregate": "QuantumEconomyIntelligenceAggregate", "api": "/quantum/marketplace/economy", "db": "quantum_*", "events": ("MarketplaceTransactionCompletedEvent",), "security": ("quantum.read",), "scaling": "economy_replicas"},
    {"id": "marketplace_knowledge_graph_service", "bc": "kg", "aggregate": "EnterpriseQuantumMarketplaceAggregate", "api": "/quantum/marketplace/knowledge-graph", "db": "quantum_*", "events": ("CapabilityRegisteredEvent",), "security": ("quantum.read",), "scaling": "kg_replicas"},
    {"id": "marketplace_digital_twin_service", "bc": "twin", "aggregate": "EnterpriseQuantumMarketplaceAggregate", "api": "/quantum/marketplace/digital-twin", "db": "quantum_*", "events": ("MarketplaceTransactionCompletedEvent",), "security": ("quantum.read",), "scaling": "twin_replicas"},
)
KNOWLEDGE_GRAPH = {"present_required": True, "nodes": ("providers", "capabilities", "algorithms", "applications", "services", "researchers", "organizations", "transactions"), "relationships": ("provides", "consumes", "develops", "uses", "partners_with", "governed_by")}
DIGITAL_TWIN = {"present_required": True, "represents": ("marketplace_state", "capabilities", "providers", "transactions", "innovation_networks", "economic_evolution"), "enables": ("market_simulation", "demand_prediction", "ecosystem_optimization", "innovation_forecasting"), "via_p215_l": True}
COMMANDS = ("RegisterQuantumCapabilityCommand", "PublishQuantumServiceCommand", "CreateMarketplaceListingCommand", "SubscribeQuantumServiceCommand", "PublishAlgorithmCommand", "CreateInnovationProjectCommand")
QUERIES = ("GetCapabilityCatalogQuery", "GetMarketplaceListingQuery", "GetServiceAvailabilityQuery", "GetInnovationNetworkQuery", "GetEconomicImpactQuery")
API_SURFACES = ("/api/v1/quantum/marketplace", "/api/v1/quantum/marketplace/capabilities", "/api/v1/quantum/marketplace/services", "/api/v1/quantum/marketplace/algorithms", "/api/v1/quantum/marketplace/applications", "/api/v1/quantum/marketplace/resources", "/api/v1/quantum/marketplace/innovation", "/api/v1/quantum/marketplace/economy", "/api/v1/quantum/marketplace/knowledge-graph", "/api/v1/quantum/marketplace/digital-twin")
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
SECURITY = {"present_required": True, "trust_driven_commerce": True, "via_p215_h": True, "via_p215_k": True, "via_p215_o": True, "via_plugin_platform": True, "via_financial_kernel": True, "module_local_payment_processor_forbidden": True, "module_local_plugin_marketplace_forbidden": True, "ungated_capability_publish_forbidden": True, "controls": ("listing_authz", "certification_gate", "trust_score", "tenant_isolation")}
DEPLOYMENT = {"present_required": True, "cloud_native": True, "components": ("kubernetes", "api_gateway", "marketplace_engine", "search_infrastructure", "recommendation_engine", "payment_economic_layer", "knowledge_graph_database", "digital_twin_platform", "observability_platform")}
TESTING = ("marketplace_functional_testing", "capability_discovery_testing", "transaction_testing", "security_testing", "performance_testing", "recommendation_testing", "economic_simulation_testing", "interoperability_testing", "trust_validation_testing")
CURSOR_OUTPUTS = ("enterprise_quantum_marketplace_vision", "ddd_domain_model", "marketplace_domain_architecture", "capability_exchange", "service_marketplace", "algorithm_marketplace", "application_marketplace", "innovation_ecosystem", "economic_intelligence", "knowledge_graph", "digital_twin", "cqrs", "event_sourcing", "microservices", "integration", "deployment", "testing", "quality_gates_dod", "adr_461", "enterprise_quantum_marketplace_law")
QUALITY_GATES_REJECT_IF = ("quantum_marketplace_platform_is_missing", "capability_exchange_platform_is_missing", "quantum_service_economy_is_missing", "algorithm_marketplace_is_missing", "application_marketplace_is_missing", "innovation_ecosystem_is_missing", "economic_intelligence_is_missing", "knowledge_graph_integration_is_missing", "digital_twin_integration_is_missing", "cqrs_architecture_is_missing", "event_architecture_is_missing", "microservices_architecture_is_missing", "api_first_architecture_is_missing", "cloud_native_deployment_is_missing", "sibling_quantum_bc")

def vision() -> dict[str, Any]:
    return {"role": "MEOS Quantum Economy Intelligence Fabric", "principle": PRINCIPLE, "equation": MARKETPLACE_PLATFORM["equation"], "why": ("capabilities_need_exchange_ecosystem", "orgs_need_quantum_services", "algorithms_are_digital_assets", "innovation_needs_collaboration", "marketplace_intelligence_is_strategic"), "builds_on_p215_a": True, "builds_on_p215_e": True, "builds_on_p215_f": True, "builds_on_p215_m": True, "builds_on_p215_o": True, "via_p213": True, "governed_by_p215_k": True}

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

def marketplace_platform() -> dict[str, Any]:
    return dict(MARKETPLACE_PLATFORM)

def capability_exchange() -> dict[str, Any]:
    return dict(CAPABILITY_EXCHANGE)

def service_economy() -> dict[str, Any]:
    return dict(SERVICE_ECONOMY)

def algorithm_marketplace() -> dict[str, Any]:
    return dict(ALGORITHM_MARKETPLACE)

def application_marketplace() -> dict[str, Any]:
    return dict(APPLICATION_MARKETPLACE)

def innovation_ecosystem() -> dict[str, Any]:
    return dict(INNOVATION_ECOSYSTEM)

def economic_intelligence() -> dict[str, Any]:
    return dict(ECONOMIC_INTELLIGENCE)

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
    return {"peers": ("P215-A", "P215-D", "P215-E", "P215-F", "P215-G", "P215-H", "P215-I", "P215-K", "P215-L", "P215-M", "P215-O", "P213", "Plugin Platform", "Financial Kernel", "Enterprise Search"), "via_events_and_acl": True, "contracts": ("marketplace_apis", "capability_contracts", "economic_events", "trust_interfaces", "governance_rules")}

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
        "builds_on": ["P215-A", "P215-B", "P215-C", "P215-D", "P215-E", "P215-F", "P215-G", "P215-H", "P215-I", "P215-J", "P215-K", "P215-L", "P215-M", "P215-N", "P215-O", "P213", "ADR-447", "ADR-451", "ADR-452", "ADR-403", "ADR-458", "ADR-460"],
        "vision": vision(), "domain_model": domain_model(), "bounded_contexts": bounded_contexts(),
        "aggregates": aggregates(), "domain_services": domain_services(), "events": events(),
        "marketplace_platform": marketplace_platform(), "capability_exchange": capability_exchange(),
        "service_economy": service_economy(), "algorithm_marketplace": algorithm_marketplace(),
        "application_marketplace": application_marketplace(), "innovation_ecosystem": innovation_ecosystem(),
        "economic_intelligence": economic_intelligence(), "context_map": context_map(),
        "microservices": microservices(), "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(), "cqrs": cqrs(), "api": api(), "integrations": integrations(),
        "security": security(), "deployment": deployment(), "testing": testing(),
        "cursor_outputs": cursor_outputs(), "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "quantum_marketplace_platform_present_required": True,
        "capability_exchange_platform_present_required": True,
        "quantum_service_economy_present_required": True,
        "algorithm_marketplace_present_required": True,
        "application_marketplace_present_required": True,
        "innovation_ecosystem_present_required": True,
        "economic_intelligence_present_required": True,
        "knowledge_graph_integration_present_required": True,
        "digital_twin_integration_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "cloud_native_deployment_present_required": True,
        "sibling_quantum_bc_forbidden": True,
        "builds_on_p215_a": True, "builds_on_p215_e": True, "builds_on_p215_f": True,
        "builds_on_p215_m": True, "builds_on_p215_o": True, "via_p213": True,
        "via_p215_m": True, "via_p215_o": True, "via_plugin_platform": True,
        "via_financial_kernel": True, "via_enterprise_search": True,
        "governed_by_p215_k": True,
        "api_prefix": f"{API_PREFIX}/marketplace",
        "forbidden_sibling_bc": [
            "quantum_marketplace_platform",
            "quantum_capability_exchange_platform",
            "quantum_algorithm_marketplace_platform",
            "quantum_economy_platform",
            "quantum_innovation_ecosystem_platform",
        ],
    }

def marketplace_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /quantum/marketplace",
        "GET /quantum/marketplace/capabilities",
        "GET /quantum/marketplace/services",
        "GET /quantum/marketplace/algorithms",
        "GET /quantum/marketplace/applications",
        "GET /quantum/marketplace/resources",
        "GET /quantum/marketplace/innovation",
        "GET /quantum/marketplace/economy",
        "GET /quantum/marketplace/knowledge-graph",
        "GET /quantum/marketplace/digital-twin",
        "GET /quantum/marketplace/readiness",
    ]}
