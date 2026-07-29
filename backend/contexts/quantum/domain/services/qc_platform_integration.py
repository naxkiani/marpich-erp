"""P215-M Enterprise Quantum Integration, API Gateway, Service Mesh & Hybrid Interoperability — immutable catalog."""
from __future__ import annotations
from typing import Any
PROMPT_ID = "P215-M"
ADR = 458
SOR = "quantum"
API_PREFIX = "/api/v1/quantum"
PRODUCT = "Enterprise Quantum Integration, Quantum API Gateway, Quantum Service Mesh & Hybrid Intelligence Interoperability Platform"
CAPABILITY = "CAP-PLT-QC-001"
PRINCIPLE = "MEOS Quantum Integration Platform SHALL provide the intelligent interoperability layer connecting quantum, classical and autonomous enterprise capabilities."
FABRIC = "meos_quantum_integration_intelligence_fabric"
CORE_DOMAIN = "enterprise_quantum_integration_intelligence_management"
SUPPORTING_DOMAINS = (
    {"id": "quantum_api", "purpose": "API lifecycle, exposure, security and governance bindings."},
    {"id": "quantum_service_mesh", "purpose": "Service communication, traffic, discovery and reliability."},
    {"id": "integration_workflow", "purpose": "Hybrid quantum-classical workflow orchestration."},
    {"id": "event_integration", "purpose": "Event routing, transformation and backbone bindings."},
    {"id": "application_federation", "purpose": "Application and capability federation."},
    {"id": "hybrid_computing", "purpose": "Quantum-classical execution coordination."},
    {"id": "integration_governance", "purpose": "Policy-driven integration via P215-K / Policy Engine."},
    {"id": "capability_discovery", "purpose": "Capability catalog and marketplace federation."},
    {"id": "service_intelligence", "purpose": "Service health, dependency and impact intelligence."},
)
GENERIC_DOMAINS = ("identity", "security", "observability", "billing", "compliance", "api_gateway", "event_bus")
LOGICAL_BOUNDED_CONTEXTS = (
    {"id": "quantum_api_management", "bc": "BC-01", "name": "Quantum API Management Context", "owns": "QuantumAPIAggregate", "purpose": "API lifecycle, exposure, security, governance."},
    {"id": "quantum_service_mesh", "bc": "BC-02", "name": "Quantum Service Mesh Context", "owns": "QuantumServiceMeshAggregate", "purpose": "Service communication, traffic, discovery, reliability."},
    {"id": "hybrid_intelligence_integration", "bc": "BC-03", "name": "Hybrid Intelligence Integration Context", "owns": "HybridIntegrationAggregate", "purpose": "Quantum-classical workflows, hybrid execution, intelligence exchange."},
    {"id": "quantum_connector", "bc": "BC-04", "name": "Quantum Connector Context", "owns": "QuantumConnectorAggregate", "purpose": "External connections, platform adapters, enterprise integrations."},
    {"id": "event_integration", "bc": "BC-05", "name": "Event Integration Context", "owns": "QuantumEventIntegrationAggregate", "purpose": "Event streaming, routing, orchestration."},
    {"id": "capability_federation", "bc": "BC-06", "name": "Capability Federation Context", "owns": "QuantumCapabilityAggregate", "purpose": "Capability discovery, service catalog, resource federation."},
)
AGGREGATES = (
    {"name": "EnterpriseQuantumIntegrationAggregate", "root": "QuantumIntegrationFlow", "entities": ("QuantumAPI", "QuantumService", "QuantumIntegrationFlow", "QuantumConnector", "QuantumEventChannel", "QuantumServiceMeshNode", "QuantumCapability", "QuantumApplication", "QuantumIntegrationPolicy"), "value_objects": ("APITrustScore", "IntegrationHealthScore", "ServiceReliabilityScore", "LatencyScore", "CompatibilityScore", "QuantumCapabilityScore"), "events": ("QuantumAPIRegisteredEvent", "QuantumServiceConnectedEvent", "IntegrationWorkflowStartedEvent", "QuantumEventPublishedEvent", "ServiceMeshNodeUpdatedEvent", "CapabilityDiscoveredEvent")},
    {"name": "QuantumAPIAggregate", "root": "QuantumAPI", "entities": ("APIVersion", "APIContract"), "value_objects": ("APITrustScore", "LatencyScore"), "events": ("QuantumAPIRegisteredEvent",)},
    {"name": "QuantumServiceMeshAggregate", "root": "QuantumServiceMeshNode", "entities": ("SidecarBinding", "TrafficPolicy"), "value_objects": ("ServiceReliabilityScore", "LatencyScore"), "events": ("ServiceMeshNodeUpdatedEvent", "ServiceConnectedEvent", "ServiceFailureDetectedEvent")},
    {"name": "HybridIntegrationAggregate", "root": "QuantumIntegrationFlow", "entities": ("HybridTask", "ResultExchange"), "value_objects": ("CompatibilityScore", "IntegrationHealthScore"), "events": ("IntegrationWorkflowStartedEvent", "IntegrationExecutedEvent")},
    {"name": "QuantumConnectorAggregate", "root": "QuantumConnector", "entities": ("PlatformAdapter", "EnterpriseBinding"), "value_objects": ("CompatibilityScore", "APITrustScore"), "events": ("ServiceConnectedEvent",)},
    {"name": "QuantumEventIntegrationAggregate", "root": "QuantumEventChannel", "entities": ("EventRoute", "EventTransform"), "value_objects": ("LatencyScore", "IntegrationHealthScore"), "events": ("QuantumEventPublishedEvent",)},
    {"name": "QuantumCapabilityAggregate", "root": "QuantumCapability", "entities": ("CapabilitySubscription", "CatalogEntry"), "value_objects": ("QuantumCapabilityScore", "CompatibilityScore"), "events": ("CapabilityDiscoveredEvent", "CapabilityRegisteredEvent")},
)
DOMAIN_SERVICES = (
    {"id": "quantum_api_gateway_service", "responsibility": "register and govern quantum API surfaces via platform gateway", "inputs": ("api_spec",), "outputs": ("api_ref",), "rules": ("via_platform_api_gateway", "via_p215_e", "via_p215_f"), "events": ("QuantumAPIRegisteredEvent",)},
    {"id": "quantum_service_mesh_service", "responsibility": "manage mesh topology and traffic policies", "inputs": ("mesh_policy",), "outputs": ("mesh_ref",), "rules": ("via_p215_h", "zero_trust"), "events": ("ServiceMeshNodeUpdatedEvent",)},
    {"id": "integration_workflow_service", "responsibility": "orchestrate hybrid quantum-classical workflows", "inputs": ("flow_spec",), "outputs": ("flow_ref",), "rules": ("via_workflow", "via_p215_d"), "events": ("IntegrationWorkflowStartedEvent",)},
    {"id": "quantum_connector_service", "responsibility": "bind connectors through Integration Platform", "inputs": ("connector_spec",), "outputs": ("connector_ref",), "rules": ("via_integration_platform",), "events": ("ServiceConnectedEvent",)},
    {"id": "event_integration_service", "responsibility": "route quantum events on Event Fabric", "inputs": ("event_channel_spec",), "outputs": ("channel_ref",), "rules": ("via_event_fabric", "outbox_required"), "events": ("QuantumEventPublishedEvent",)},
    {"id": "capability_federation_service", "responsibility": "discover and federate quantum capabilities", "inputs": ("capability_spec",), "outputs": ("capability_ref",), "rules": ("via_p215_k",), "events": ("CapabilityRegisteredEvent",)},
    {"id": "integration_governance_service", "responsibility": "enforce integration policies and trust", "inputs": ("policy_query",), "outputs": ("governance_decision",), "rules": ("via_p215_k", "via_policy_engine"), "events": ("IntegrationExecutedEvent",)},
)
CORE_EVENTS = (
    {"name": "QuantumAPIRegisteredEvent", "producer": "quantum_api_management", "consumers": "gateway,mesh,kg"},
    {"name": "ServiceConnectedEvent", "producer": "quantum_connector", "consumers": "mesh,governance,twin"},
    {"name": "IntegrationExecutedEvent", "producer": "hybrid_intelligence_integration", "consumers": "audit,observability"},
    {"name": "QuantumEventPublishedEvent", "producer": "event_integration", "consumers": "event_fabric,ai,data"},
    {"name": "CapabilityRegisteredEvent", "producer": "capability_federation", "consumers": "marketplace,kg"},
    {"name": "ServiceFailureDetectedEvent", "producer": "quantum_service_mesh", "consumers": "aiops,security,twin"},
)
INTEGRATION_PLATFORM = {"present_required": True, "capabilities": ("quantum_service_federation", "enterprise_application_bridge", "ai_agent_interoperability", "data_platform_exchange", "api_event_network_twin_unify"), "equation": "Quantum Capabilities -> API Gateway -> Service Mesh -> Integration Events -> Enterprise Applications -> AI Intelligence Systems -> Autonomous Agents"}
API_GATEWAY = {"present_required": True, "capabilities": ("quantum_api_discovery", "api_registration", "api_security", "api_versioning", "api_transformation", "api_monitoring", "api_analytics"), "supports": ("REST", "GraphQL", "gRPC", "Quantum Runtime APIs", "AI Service APIs"), "via_platform_api_gateway": True, "integrates_with": ("P215-E", "P215-F"), "module_local_gateway_forbidden": True}
SERVICE_MESH = {"present_required": True, "capabilities": ("service_discovery", "traffic_management", "load_balancing", "fault_tolerance", "security_enforcement", "observability"), "includes": ("quantum_sidecar_architecture", "service_identity", "policy_enforcement", "communication_encryption"), "integrates_with": "P215-H"}
HYBRID_BRIDGE = {"present_required": True, "manages": ("classical_applications", "quantum_applications", "ai_systems", "data_platforms", "simulation_systems"), "capabilities": ("workflow_orchestration", "task_distribution", "execution_coordination", "result_exchange")}
EVENT_BACKBONE = {"present_required": True, "manages": ("quantum_events", "ai_events", "data_events", "security_events", "governance_events", "digital_twin_events"), "capabilities": ("event_routing", "event_transformation", "event_replay", "event_analytics"), "via_event_fabric": True, "module_local_broker_forbidden": True}
CAPABILITY_FEDERATION = {"present_required": True, "discovers": ("quantum_algorithms", "quantum_services", "ai_models", "quantum_applications", "data_products", "simulation_models"), "capabilities": ("registration", "discovery", "subscription", "consumption", "governance")}
INTEGRATION_GOVERNANCE = {"present_required": True, "manages": ("api_governance", "mesh_policies", "connector_grants", "capability_trust", "hybrid_workflow_approvals"), "integrates_with": "P215-K"}
CONTEXT_MAP = (
    {"from": "quantum_api_management", "to": "quantum_software", "type": "customer_supplier", "via": "P215-E"},
    {"from": "quantum_api_management", "to": "quantum_ai", "type": "customer_supplier", "via": "P215-F"},
    {"from": "quantum_service_mesh", "to": "quantum_security", "type": "conformist", "via": "P215-H"},
    {"from": "quantum_connector", "to": "integration_platform", "type": "anti_corruption_layer", "via": "integration"},
    {"from": "event_integration", "to": "event_fabric", "type": "conformist", "via": "event_bus"},
    {"from": "hybrid_intelligence_integration", "to": "quantum_infrastructure", "type": "customer_supplier", "via": "P215-D"},
    {"from": "hybrid_intelligence_integration", "to": "quantum_scientific", "type": "customer_supplier", "via": "P215-G"},
    {"from": "capability_federation", "to": "quantum_data", "type": "customer_supplier", "via": "P215-I"},
    {"from": "quantum_service_mesh", "to": "quantum_network", "type": "customer_supplier", "via": "P215-J"},
    {"from": "integration_governance", "to": "quantum_governance", "type": "conformist", "via": "P215-K"},
    {"from": "hybrid_intelligence_integration", "to": "quantum_twin", "type": "customer_supplier", "via": "P215-L"},
    {"from": "capability_federation", "to": "ai_master_intelligence", "type": "anti_corruption_layer", "via": "P214-Z"},
)
MICROSERVICES = (
    {"id": "quantum_api_gateway_service", "bc": "BC-01", "aggregate": "QuantumAPIAggregate", "api": "/quantum/integration/api-gateway", "db": "quantum_*", "events": ("QuantumAPIRegisteredEvent",), "security": ("quantum.read",), "scaling": "gateway_replicas"},
    {"id": "quantum_service_mesh_service", "bc": "BC-02", "aggregate": "QuantumServiceMeshAggregate", "api": "/quantum/integration/service-mesh", "db": "quantum_*", "events": ("ServiceMeshNodeUpdatedEvent",), "security": ("quantum.write",), "scaling": "mesh_control_plane"},
    {"id": "integration_workflow_service", "bc": "BC-03", "aggregate": "HybridIntegrationAggregate", "api": "/quantum/integration/hybrid", "db": "quantum_*", "events": ("IntegrationExecutedEvent",), "security": ("quantum.write",), "scaling": "workflow_workers"},
    {"id": "quantum_connector_service", "bc": "BC-04", "aggregate": "QuantumConnectorAggregate", "api": "/quantum/integration/connectors", "db": "quantum_*", "events": ("ServiceConnectedEvent",), "security": ("quantum.write",), "scaling": "connector_workers"},
    {"id": "event_integration_service", "bc": "BC-05", "aggregate": "QuantumEventIntegrationAggregate", "api": "/quantum/integration/events", "db": "quantum_*", "events": ("QuantumEventPublishedEvent",), "security": ("quantum.write",), "scaling": "event_workers"},
    {"id": "capability_federation_service", "bc": "BC-06", "aggregate": "QuantumCapabilityAggregate", "api": "/quantum/integration/capabilities", "db": "quantum_*", "events": ("CapabilityRegisteredEvent",), "security": ("quantum.read",), "scaling": "federation_replicas"},
    {"id": "integration_governance_service", "bc": "gov", "aggregate": "EnterpriseQuantumIntegrationAggregate", "api": "/quantum/integration/governance", "db": "quantum_*", "events": ("IntegrationExecutedEvent",), "security": ("quantum.read",), "scaling": "gov_replicas"},
    {"id": "service_intelligence_service", "bc": "intel", "aggregate": "EnterpriseQuantumIntegrationAggregate", "api": "/quantum/integration/intelligence", "db": "quantum_*", "events": ("ServiceFailureDetectedEvent",), "security": ("quantum.read",), "scaling": "intel_replicas"},
    {"id": "integration_knowledge_graph_service", "bc": "kg", "aggregate": "EnterpriseQuantumIntegrationAggregate", "api": "/quantum/integration/knowledge-graph", "db": "quantum_*", "events": ("QuantumAPIRegisteredEvent",), "security": ("quantum.read",), "scaling": "kg_replicas"},
    {"id": "integration_digital_twin_service", "bc": "twin", "aggregate": "EnterpriseQuantumIntegrationAggregate", "api": "/quantum/integration/digital-twin", "db": "quantum_*", "events": ("ServiceFailureDetectedEvent",), "security": ("quantum.read",), "scaling": "twin_replicas"},
)
KNOWLEDGE_GRAPH = {"present_required": True, "nodes": ("apis", "services", "applications", "quantum_resources", "ai_agents", "events", "policies"), "relationships": ("consumes", "provides", "connected_to", "depends_on", "secured_by", "governed_by")}
DIGITAL_TWIN = {"present_required": True, "represents": ("api_landscape", "service_mesh", "integration_flows", "dependencies", "performance", "failures"), "enables": ("simulation", "optimization", "failure_prediction", "architecture_evolution"), "via_p215_l": True}
COMMANDS = ("RegisterQuantumAPICommand", "CreateServiceConnectionCommand", "DeployIntegrationFlowCommand", "PublishQuantumEventCommand", "RegisterCapabilityCommand", "OptimizeServiceMeshCommand")
QUERIES = ("GetAPIStatusQuery", "GetIntegrationHealthQuery", "GetServiceMeshTopologyQuery", "GetCapabilityCatalogQuery", "GetDependencyGraphQuery")
API_SURFACES = ("/api/v1/quantum/integration", "/api/v1/quantum/integration/api-gateway", "/api/v1/quantum/integration/service-mesh", "/api/v1/quantum/integration/hybrid", "/api/v1/quantum/integration/connectors", "/api/v1/quantum/integration/events", "/api/v1/quantum/integration/capabilities", "/api/v1/quantum/integration/governance", "/api/v1/quantum/integration/intelligence", "/api/v1/quantum/integration/knowledge-graph", "/api/v1/quantum/integration/digital-twin")
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
SECURITY = {"present_required": True, "zero_trust": True, "via_p215_h": True, "via_p215_k": True, "via_platform_api_gateway": True, "controls": ("api_authz", "mesh_mtls", "connector_grants", "tenant_isolation")}
DEPLOYMENT = {"present_required": True, "cloud_native": True, "components": ("kubernetes", "api_gateway_cluster", "service_mesh_control_plane", "event_streaming_infrastructure", "integration_runtime", "observability_platform", "security_enforcement_layer")}
TESTING = ("api_testing", "integration_testing", "service_mesh_testing", "event_flow_testing", "interoperability_testing", "performance_testing", "security_testing", "failure_recovery_testing", "quantum_classical_workflow_testing")
CURSOR_OUTPUTS = ("enterprise_quantum_integration_vision", "ddd_domain_model", "quantum_integration_domain_architecture", "api_gateway", "service_mesh", "hybrid_bridge", "event_backbone", "capability_federation", "knowledge_graph", "digital_twin", "cqrs", "event_sourcing", "microservices", "integration", "deployment", "testing", "quality_gates_dod", "adr_458", "enterprise_quantum_integration_law")
QUALITY_GATES_REJECT_IF = ("quantum_integration_platform_is_missing", "quantum_api_gateway_is_missing", "quantum_service_mesh_is_missing", "hybrid_intelligence_bridge_is_missing", "event_integration_backbone_is_missing", "capability_federation_is_missing", "knowledge_graph_integration_is_missing", "digital_twin_integration_is_missing", "cqrs_architecture_is_missing", "event_architecture_is_missing", "microservices_architecture_is_missing", "api_first_architecture_is_missing", "cloud_native_deployment_is_missing", "sibling_quantum_bc")

def vision() -> dict[str, Any]:
    return {"role": "MEOS Quantum Integration Intelligence Fabric", "principle": PRINCIPLE, "equation": INTEGRATION_PLATFORM["equation"], "why": ("quantum_requires_enterprise_integration", "hybrid_needs_orchestration", "apis_bridge_quantum_and_business", "service_mesh_required_at_scale", "autonomous_intelligence_needs_interoperability"), "builds_on_p215_a": True, "builds_on_p215_d": True, "builds_on_p215_e": True, "builds_on_p215_f": True, "builds_on_p215_l": True, "governed_by_p215_k": True}

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

def integration_platform() -> dict[str, Any]:
    return dict(INTEGRATION_PLATFORM)

def api_gateway() -> dict[str, Any]:
    return dict(API_GATEWAY)

def service_mesh() -> dict[str, Any]:
    return dict(SERVICE_MESH)

def hybrid_bridge() -> dict[str, Any]:
    return dict(HYBRID_BRIDGE)

def event_backbone() -> dict[str, Any]:
    return dict(EVENT_BACKBONE)

def capability_federation() -> dict[str, Any]:
    return dict(CAPABILITY_FEDERATION)

def integration_governance() -> dict[str, Any]:
    return dict(INTEGRATION_GOVERNANCE)

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
    return {"peers": ("P215-A", "P215-D", "P215-E", "P215-F", "P215-G", "P215-H", "P215-I", "P215-J", "P215-K", "P215-L", "P214-Z", "api_gateway", "integration", "event_bus"), "via_events_and_acl": True, "contracts": ("api_contracts", "event_contracts", "service_interfaces", "security_boundaries", "governance_rules")}

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
        "builds_on": ["P215-A", "P215-B", "P215-C", "P215-D", "P215-E", "P215-F", "P215-G", "P215-H", "P215-I", "P215-J", "P215-K", "P215-L", "P214-Z", "ADR-447", "ADR-450", "ADR-451", "ADR-452", "ADR-453", "ADR-454", "ADR-455", "ADR-456", "ADR-403", "ADR-457"],
        "vision": vision(), "domain_model": domain_model(), "bounded_contexts": bounded_contexts(),
        "aggregates": aggregates(), "domain_services": domain_services(), "events": events(),
        "integration_platform": integration_platform(), "api_gateway": api_gateway(),
        "service_mesh": service_mesh(), "hybrid_bridge": hybrid_bridge(),
        "event_backbone": event_backbone(), "capability_federation": capability_federation(),
        "integration_governance": integration_governance(), "context_map": context_map(),
        "microservices": microservices(), "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(), "cqrs": cqrs(), "api": api(), "integrations": integrations(),
        "security": security(), "deployment": deployment(), "testing": testing(),
        "cursor_outputs": cursor_outputs(), "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "quantum_integration_platform_present_required": True,
        "quantum_api_gateway_present_required": True,
        "quantum_service_mesh_present_required": True,
        "hybrid_intelligence_bridge_present_required": True,
        "event_integration_backbone_present_required": True,
        "capability_federation_present_required": True,
        "knowledge_graph_integration_present_required": True,
        "digital_twin_integration_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "cloud_native_deployment_present_required": True,
        "security_architecture_present_required": True,
        "governance_architecture_present_required": True,
        "sibling_quantum_bc_forbidden": True,
        "builds_on_p215_a": True, "builds_on_p215_d": True, "builds_on_p215_e": True,
        "builds_on_p215_f": True, "builds_on_p215_h": True, "builds_on_p215_l": True,
        "governed_by_p215_k": True,
        "api_prefix": f"{API_PREFIX}/integration",
        "forbidden_sibling_bc": [
            "quantum_api_gateway_platform",
            "quantum_service_mesh_platform",
            "quantum_hybrid_integration_platform",
            "quantum_capability_federation_platform",
        ],
    }

def integration_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /quantum/integration",
        "GET /quantum/integration/api-gateway",
        "GET /quantum/integration/service-mesh",
        "GET /quantum/integration/hybrid",
        "GET /quantum/integration/connectors",
        "GET /quantum/integration/events",
        "GET /quantum/integration/capabilities",
        "GET /quantum/integration/governance",
        "GET /quantum/integration/intelligence",
        "GET /quantum/integration/knowledge-graph",
        "GET /quantum/integration/digital-twin",
        "GET /quantum/integration/readiness",
    ]}
