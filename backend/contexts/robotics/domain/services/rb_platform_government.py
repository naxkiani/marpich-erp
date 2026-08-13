"""P216-T Enterprise Government Intelligence — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P216-T"
ADR = 492
SOR = "robotics"
API_PREFIX = "/api/v1/robotics"
PRODUCT = (
    "Enterprise Robotics Government Robotics, Autonomous Public Services, "
    "Digital Government Intelligence & Smart Governance Automation Platform"
)
CAPABILITY = "CAP-PLT-RB-001"
GOVERNMENT_VISION = (
    "MEOS Government Intelligence Platform SHALL unify government robotics, "
    "autonomous public services, digital government intelligence and government digital twins as "
    "intelligent participants within the MEOS Government Intelligence Ecosystem."
)
MISSION = (
    "Create an AI-native, secure, transparent and citizen-centric government ecosystem "
    "that automates public services, improves governance decisions "
    "and increases administrative efficiency."
)
VISION = (
    "Every citizen, government institution, public service, policy, regulation, "
    "asset and administrative process shall become an intelligent participant "
    "inside the MEOS Government Intelligence Ecosystem."
)
FABRIC = "meos_government_intelligence_fabric"
FOUNDATION_GATE = "P216"
MISSION_GATE = "P216-A"
STRATEGY_GATE = "P216-B"
DOMAIN_GATE = "P216-C"
RUNTIME_GATE = "P216-D"
PHYSICAL_AI_GATE = "P216-E"
INDUSTRIAL_GATE = "P216-F"
LOGISTICS_GATE = "P216-G"
MOBILITY_GATE = "P216-H"
HEALTHCARE_GATE = "P216-I"
CONSTRUCTION_GATE = "P216-K"
PUBLIC_SAFETY_GATE = "P216-L"
RETAIL_GATE = "P216-O"
HOSPITALITY_GATE = "P216-P"
EDUCATION_GATE = "P216-Q"
FINANCE_GATE = "P216-R"
SUPREME_GATE = "P215-Z"
AI_GATE = "P214-Z"
CORE_DOMAIN = "enterprise_government_intelligence"
AGGREGATE = "GovernmentIntelligenceAggregate"

SUPPORTING_DOMAINS = (
    "citizen_services",
    "government_operations",
    "digital_identity",
    "public_administration",
    "policy_intelligence",
    "regulatory_intelligence",
    "government_robotics",
    "smart_infrastructure",
    "public_finance_intelligence",
    "national_data_intelligence",
    "government_analytics",
    "government_digital_twin",
)
ENTITIES = (
    "GovernmentOrganization",
    "PublicAgency",
    "Citizen",
    "DigitalIdentity",
    "PublicService",
    "GovernmentProcess",
    "Policy",
    "Regulation",
    "GovernmentRobot",
    "PublicAsset",
    "GovernmentDigitalTwin",
    "NationalProgram",
)
VALUE_OBJECTS = (
    "CitizenProfile",
    "ServiceRequest",
    "PolicyImpactScore",
    "GovernanceScore",
    "ComplianceStatus",
    "PublicServicePriority",
    "RiskLevel",
    "IdentityTrustScore",
    "OperationalStatus",
)
BOUNDED_CONTEXTS = (
    {"id": "BC-01", "name": "Citizen Experience Context", "responsibilities": ("citizen_lifecycle", "digital_services", "citizen_interaction")},
    {"id": "BC-02", "name": "Government Robotics Context", "responsibilities": ("government_ai_agents", "service_automation", "robot_lifecycle")},
    {"id": "BC-03", "name": "Public Service Automation Context", "responsibilities": ("service_workflows", "administrative_automation", "case_management")},
    {"id": "BC-04", "name": "Digital Identity Context", "responsibilities": ("citizen_identity", "authentication", "trust_management")},
    {"id": "BC-05", "name": "Policy Intelligence Context", "responsibilities": ("policy_analysis", "impact_prediction", "decision_support")},
    {"id": "BC-06", "name": "Government Data Intelligence Context", "responsibilities": ("public_data_analytics", "knowledge_management", "information_governance")},
    {"id": "BC-07", "name": "Government Digital Twin Context", "responsibilities": ("national_simulation", "public_infrastructure_modelling", "policy_scenario_analysis")},
    {"id": "BC-08", "name": "Governance & Compliance Context", "responsibilities": ("transparency", "audit", "ethics", "regulatory_compliance")},
)
GOVERNMENT_ROBOTICS = {
    "present_required": True,
    "platform": "meos_government_robotics_platform",
    "components": (
        "government_robot_registry",
        "public_service_agent_manager",
        "administrative_automation_engine",
        "citizen_assistance_agent",
        "government_workflow_controller",
        "governance_operations_dashboard",
    ),
    "supported_ai_agents": (
        "citizen_service_agent",
        "policy_analysis_agent",
        "administrative_agent",
        "regulatory_monitoring_agent",
        "public_information_agent",
        "government_document_agent",
    ),
    "capabilities": (
        "public_service_automation",
        "citizen_assistance",
        "administrative_processing",
        "information_delivery",
        "government_workflow_optimisation",
    ),
}
AUTONOMOUS_PUBLIC_SERVICES = {
    "present_required": True,
    "engine": "meos_public_service_intelligence_engine",
    "capabilities": (
        "digital_service_delivery",
        "automated_applications",
        "citizen_support",
        "document_processing",
        "government_workflow_automation",
        "service_recommendation",
    ),
    "services": (
        "licensing",
        "registration",
        "permits",
        "public_information",
        "administrative_requests",
        "citizen_communication",
    ),
}
DIGITAL_GOVERNMENT = {
    "present_required": True,
    "engine": "meos_government_ai_intelligence_engine",
    "capabilities": (
        "policy_intelligence",
        "public_sector_analytics",
        "decision_support",
        "government_forecasting",
        "resource_optimisation",
        "administrative_intelligence",
    ),
    "models": (
        "government_foundation_models",
        "policy_intelligence_models",
        "public_service_models",
        "citizen_behaviour_models",
        "administrative_reasoning_models",
    ),
    "via_p214_z": True,
    "explainable_ai": True,
    "human_governance_oversight": True,
    "responsible_ai": True,
}
SMART_GOVERNANCE = {
    "present_required": True,
    "platform": "meos_governance_automation_platform",
    "capabilities": (
        "automated_compliance",
        "policy_monitoring",
        "workflow_optimisation",
        "institution_performance_analysis",
        "public_value_measurement",
        "governance_transparency",
    ),
}
CITIZEN_INTELLIGENCE = {
    "present_required": True,
    "platform": "meos_citizen_intelligence_platform",
    "capabilities": (
        "citizen_lifecycle",
        "personalisation",
        "experience_management",
        "service_recommendation",
    ),
    "privacy_by_design": True,
    "citizen_centric": True,
}
POLICY_INTELLIGENCE = {
    "present_required": True,
    "platform": "meos_policy_intelligence_platform",
    "capabilities": (
        "policy_analysis",
        "impact_prediction",
        "decision_support",
        "scenario_modelling",
    ),
    "via_policy_engine": True,
    "via_p214_z": True,
}
GOVERNMENT_DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_national_government_digital_twin_platform",
    "represents": (
        "government_institutions", "citizens", "public_services", "infrastructure",
        "policies", "regulations", "budgets", "national_programs", "administrative_processes",
    ),
    "capabilities": (
        "policy_simulation",
        "public_service_optimisation",
        "resource_planning",
        "crisis_scenario_modelling",
        "governance_forecasting",
    ),
}
PUBLIC_KG = {
    "present_required": True,
    "graph": "meos_government_knowledge_graph",
    "nodes": (
        "citizens", "institutions", "policies", "regulations", "services",
        "assets", "programs", "government_agents", "public_data",
    ),
    "relationships": (
        "uses", "provides", "regulates", "impacts",
        "depends_on", "governed_by", "serves", "optimises",
    ),
    "enables": (
        "policy_reasoning",
        "citizen_intelligence",
        "governance_analysis",
        "public_decision_support",
    ),
}
OBSERVABILITY = {
    "present_required": True,
    "platform": "meos_government_observability_platform",
    "monitors": (
        "citizen_experience",
        "public_service_performance",
        "government_agent_activity",
        "policy_intelligence",
        "institution_performance",
        "ai_accuracy",
        "digital_twin_accuracy",
        "governance_kpis",
    ),
    "via_platform_observability": True,
}
SECURITY = {
    "present_required": True,
    "framework": "meos_government_zero_trust_framework",
    "domains": (
        "citizen_identity",
        "government_identity",
        "public_data_protection",
        "ai_governance",
        "national_security",
        "administrative_integrity",
        "audit_protection",
    ),
    "controls": (
        "identity_governance",
        "encryption",
        "data_sovereignty",
        "access_control",
        "ai_explainability",
        "continuous_monitoring",
        "transparency_management",
    ),
    "zero_trust": True,
    "privacy_by_design": True,
    "human_governance_oversight": True,
    "explainable_ai": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "via_integration_platform": True,
    "never_duplicate_government_core_logic": True,
    "never_duplicate_municipality_core_logic": True,
    "never_replace_identity_platform": True,
    "no_module_local_llm": True,
    "physical_ai_via_p214z_acl_only": True,
    "never_replace_p216_foundation": True,
    "never_replace_p216_r_finance": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "ungated_physical_autonomy_strategy_forbidden": True,
    "opaque_safety_strategy_forbidden": True,
}
COMMANDS = (
    "RegisterCitizenCommand",
    "RequestPublicServiceCommand",
    "ActivateGovernmentAgentCommand",
    "AnalysePolicyCommand",
    "OptimiseGovernmentWorkflowCommand",
    "UpdateGovernmentTwinCommand",
)
QUERIES = (
    "GetCitizenProfileQuery",
    "GetServiceStatusQuery",
    "GetPolicyImpactQuery",
    "GetGovernmentStatusQuery",
    "GetNationalTwinQuery",
)
CORE_EVENTS = (
    {"name": "CitizenInteractionEvent", "schema": "robotics.government.citizen.interaction.v1", "owner": "BC-01", "consumers": "services,twin,audit"},
    {"name": "ServiceRequestCreatedEvent", "schema": "robotics.government.service.request.created.v1", "owner": "BC-03", "consumers": "robotics,workflow,audit"},
    {"name": "GovernmentAgentCompletedEvent", "schema": "robotics.government.agent.completed.v1", "owner": "BC-02", "consumers": "runtime,services,audit"},
    {"name": "PolicyImpactCalculatedEvent", "schema": "robotics.government.policy.impact.calculated.v1", "owner": "BC-05", "consumers": "twin,governance,audit"},
    {"name": "RegulationChangedEvent", "schema": "robotics.government.regulation.changed.v1", "owner": "BC-05", "consumers": "compliance,kg,audit"},
    {"name": "PublicServiceCompletedEvent", "schema": "robotics.government.service.completed.v1", "owner": "BC-03", "consumers": "citizen,analytics,audit"},
    {"name": "GovernanceRiskDetectedEvent", "schema": "robotics.government.governance.risk.detected.v1", "owner": "BC-08", "consumers": "workflow,governance,audit"},
)
MICROSERVICES = (
    {"id": "citizen_intelligence_service", "bc": "BC-01", "api": "/robotics/government/citizens", "db": "robotics_*", "events": ("CitizenInteractionEvent", "PublicServiceCompletedEvent"), "security": ("robotics.write",), "scaling": "citizen_replicas", "responsibility": "Citizen experience projections"},
    {"id": "government_robotics_service", "bc": "BC-02", "api": "/robotics/government/robots", "db": "robotics_*", "events": ("GovernmentAgentCompletedEvent",), "security": ("robotics.write",), "scaling": "agent_workers", "responsibility": "Government agent mission orchestration"},
    {"id": "public_service_service", "bc": "BC-03", "api": "/robotics/government/services", "db": "robotics_*", "events": ("ServiceRequestCreatedEvent", "PublicServiceCompletedEvent"), "security": ("robotics.write",), "scaling": "service_workers", "responsibility": "Public service automation"},
    {"id": "digital_identity_service", "bc": "BC-04", "api": "/robotics/government/identity", "db": "robotics_*", "events": ("CitizenInteractionEvent",), "security": ("robotics.write",), "scaling": "identity_workers", "responsibility": "Digital identity projections via Identity Platform ACL"},
    {"id": "policy_intelligence_service", "bc": "BC-05", "api": "/robotics/government/policy", "db": "robotics_*", "events": ("PolicyImpactCalculatedEvent", "RegulationChangedEvent"), "security": ("robotics.write",), "scaling": "policy_workers", "responsibility": "Policy intelligence via P214-Z ACL"},
    {"id": "regulatory_intelligence_service", "bc": "BC-05", "api": "/robotics/government/regulatory", "db": "robotics_*", "events": ("RegulationChangedEvent",), "security": ("robotics.read",), "scaling": "regulatory_workers", "responsibility": "Regulatory intelligence facets"},
    {"id": "government_data_service", "bc": "BC-06", "api": "/robotics/government/data", "db": "robotics_*", "events": ("CitizenInteractionEvent", "PolicyImpactCalculatedEvent"), "security": ("robotics.read",), "scaling": "data_workers", "responsibility": "Government data intelligence"},
    {"id": "digital_twin_service", "bc": "BC-07", "api": "/robotics/government/digital-twin", "db": "robotics_*", "events": ("PolicyImpactCalculatedEvent", "PublicServiceCompletedEvent"), "security": ("robotics.read",), "scaling": "twin_workers", "responsibility": "Government digital twin sync"},
    {"id": "knowledge_graph_service", "bc": "BC-07", "api": "/robotics/government/knowledge-graph", "db": "robotics_*", "events": ("RegulationChangedEvent", "ServiceRequestCreatedEvent"), "security": ("robotics.read",), "scaling": "kg_workers", "responsibility": "Public knowledge graph projections"},
    {"id": "governance_analytics_service", "bc": "BC-08", "api": "/robotics/government/analytics", "db": "robotics_*", "events": ("GovernanceRiskDetectedEvent", "PublicServiceCompletedEvent"), "security": ("robotics.read",), "scaling": "analytics_workers", "responsibility": "Governance analytics and compliance facets"},
)
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p216d_robotics_os",
        "p216e_physical_ai",
        "p216l_public_safety",
        "p216r_finance",
        "p216s_legal_planned",
        "p214z_ai_master",
        "p215z_quantum_supreme",
        "identity_platform",
        "national_identity_systems",
        "government_erp",
        "public_data_platforms",
        "smart_city_platforms",
        "healthcare_systems",
        "education_systems",
        "integration_platform",
    ),
    "mechanisms": (
        "government_apis",
        "agent_mission_interfaces",
        "identity_via_identity_platform",
        "national_id_via_integration_connectors",
        "government_erp_via_peer_api",
        "government_event_contracts",
    ),
    "via_p216_d": True,
    "via_p216_e": True,
    "via_p216_l": True,
    "via_p216_r": True,
    "via_p214_z": True,
    "via_p215_z": True,
    "via_p213": True,
    "via_identity": True,
    "via_integration_platform": True,
    "never_duplicate_government_core_logic": True,
    "never_duplicate_municipality_core_logic": True,
    "never_replace_identity_platform": True,
    "p216_s_legal_planned": True,
}
DEPLOYMENT = {
    "present_required": True,
    "model": "hybrid_government_intelligence_infrastructure",
    "includes": (
        "government_edge_platform",
        "public_service_runtime",
        "government_cloud_platform",
        "ai_compute_cluster",
        "agent_runtime_platform",
        "digital_twin_cluster",
        "knowledge_graph_cluster",
        "analytics_platform",
        "security_operations_platform",
    ),
    "deployment_models": (
        "municipal_government",
        "national_government",
        "government_federation",
        "smart_nation_ecosystem",
    ),
    "cloud_native": True,
    "edge_native": True,
}
TESTING = (
    "citizen_service_testing",
    "government_workflow_testing",
    "ai_decision_validation",
    "policy_simulation_testing",
    "agent_behaviour_testing",
    "security_testing",
    "privacy_testing",
    "performance_testing",
    "resilience_testing",
    "transparency_testing",
)
API_SURFACES = (
    "/api/v1/robotics/government",
    "/api/v1/robotics/government/vision",
    "/api/v1/robotics/government/domain",
    "/api/v1/robotics/government/bounded-contexts",
    "/api/v1/robotics/government/robotics",
    "/api/v1/robotics/government/public-services",
    "/api/v1/robotics/government/digital-government",
    "/api/v1/robotics/government/smart-governance",
    "/api/v1/robotics/government/citizen-intelligence",
    "/api/v1/robotics/government/policy-intelligence",
    "/api/v1/robotics/government/digital-twin",
    "/api/v1/robotics/government/knowledge-graph",
    "/api/v1/robotics/government/observability",
    "/api/v1/robotics/government/security",
    "/api/v1/robotics/government/cqrs",
    "/api/v1/robotics/government/events",
    "/api/v1/robotics/government/microservices",
    "/api/v1/robotics/government/integration",
    "/api/v1/robotics/government/deployment",
    "/api/v1/robotics/government/testing",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
QUALITY_GATES_REJECT_IF = (
    "government_robotics_platform_is_missing",
    "autonomous_public_services_is_missing",
    "digital_government_intelligence_is_missing",
    "smart_governance_automation_is_missing",
    "citizen_intelligence_platform_is_missing",
    "policy_intelligence_platform_is_missing",
    "government_digital_twin_is_missing",
    "public_knowledge_graph_is_missing",
    "security_architecture_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "cloud_edge_deployment_is_missing",
    "enterprise_government_integration_is_missing",
    "testing_architecture_is_missing",
    "sibling_robotics_bc",
    "replace_p216_r_finance",
    "duplicate_government_core_logic",
    "duplicate_municipality_core_logic",
    "replace_identity_platform",
    "module_local_llm",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Government Intelligence Fabric",
        "government_vision": GOVERNMENT_VISION,
        "mission": MISSION,
        "vision": VISION,
        "builds_on_p216": True,
        "builds_on_p216_r": True,
        "builds_on_p216_l": True,
        "builds_on_p216_e": True,
        "builds_on_p216_d": True,
        "builds_on_p215_z": True,
        "builds_on_p214_z": True,
        "never_replace_p216_r_finance": True,
        "foundation_gate": FOUNDATION_GATE,
        "finance_gate": FINANCE_GATE,
        "public_safety_gate": PUBLIC_SAFETY_GATE,
        "physical_ai_gate": PHYSICAL_AI_GATE,
        "runtime_gate": RUNTIME_GATE,
        "supreme_gate": SUPREME_GATE,
        "ai_gate": AI_GATE,
        "p216_s_legal_planned": True,
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

def robotics_platform() -> dict[str, Any]:
    return dict(GOVERNMENT_ROBOTICS)

def public_services() -> dict[str, Any]:
    return dict(AUTONOMOUS_PUBLIC_SERVICES)

def digital_government() -> dict[str, Any]:
    return dict(DIGITAL_GOVERNMENT)

def smart_governance() -> dict[str, Any]:
    return dict(SMART_GOVERNANCE)

def citizen_intelligence() -> dict[str, Any]:
    return dict(CITIZEN_INTELLIGENCE)

def policy_intelligence() -> dict[str, Any]:
    return dict(POLICY_INTELLIGENCE)

def digital_twin() -> dict[str, Any]:
    return dict(GOVERNMENT_DIGITAL_TWIN)

def knowledge_graph() -> dict[str, Any]:
    return dict(PUBLIC_KG)

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
        "finance_gate_api": "/api/v1/robotics/finance",
        "runtime_gate_api": "/api/v1/robotics/runtime",
    }

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p216_u": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "government_vision": GOVERNMENT_VISION, "mission": MISSION, "vision": VISION, "principle": GOVERNMENT_VISION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE, "runtime_gate": RUNTIME_GATE,
        "physical_ai_gate": PHYSICAL_AI_GATE, "industrial_gate": INDUSTRIAL_GATE,
        "logistics_gate": LOGISTICS_GATE, "mobility_gate": MOBILITY_GATE,
        "healthcare_gate": HEALTHCARE_GATE, "construction_gate": CONSTRUCTION_GATE,
        "public_safety_gate": PUBLIC_SAFETY_GATE, "retail_gate": RETAIL_GATE,
        "hospitality_gate": HOSPITALITY_GATE, "education_gate": EDUCATION_GATE,
        "finance_gate": FINANCE_GATE,
        "supreme_gate": SUPREME_GATE, "ai_gate": AI_GATE,
        "builds_on": [
            "P216", "P216-A", "P216-B", "P216-C", "P216-D", "P216-E", "P216-F", "P216-G", "P216-H",
            "P216-I", "P216-K", "P216-L", "P216-O", "P216-P", "P216-Q", "P216-R", "P215-Z", "P214-Z", "P213",
            "ADR-472", "ADR-473", "ADR-474", "ADR-475", "ADR-476", "ADR-477", "ADR-478", "ADR-479",
            "ADR-480", "ADR-481", "ADR-483", "ADR-484", "ADR-487", "ADR-488", "ADR-489", "ADR-490",
        ],
        "vision_pack": vision_pack(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "robotics_platform": robotics_platform(),
        "public_services": public_services(),
        "digital_government": digital_government(),
        "smart_governance": smart_governance(),
        "citizen_intelligence": citizen_intelligence(),
        "policy_intelligence": policy_intelligence(),
        "digital_twin": digital_twin(),
        "knowledge_graph": knowledge_graph(),
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
        "government_robotics_platform_present_required": True,
        "autonomous_public_services_present_required": True,
        "digital_government_intelligence_present_required": True,
        "smart_governance_automation_present_required": True,
        "citizen_intelligence_platform_present_required": True,
        "policy_intelligence_platform_present_required": True,
        "government_digital_twin_present_required": True,
        "public_knowledge_graph_present_required": True,
        "security_architecture_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "cloud_edge_deployment_present_required": True,
        "enterprise_government_integration_present_required": True,
        "testing_architecture_present_required": True,
        "sibling_robotics_bc_forbidden": True,
        "never_replace_p216_foundation": True,
        "never_replace_p216_a_mission": True,
        "never_replace_p216_b_strategy": True,
        "never_replace_p216_c_domain": True,
        "never_replace_p216_d_runtime": True,
        "never_replace_p216_e_physical_ai": True,
        "never_replace_p216_f_industrial": True,
        "never_replace_p216_g_logistics": True,
        "never_replace_p216_h_mobility": True,
        "never_replace_p216_i_healthcare": True,
        "never_replace_p216_k_construction": True,
        "never_replace_p216_l_public_safety": True,
        "never_replace_p216_o_retail": True,
        "never_replace_p216_p_hospitality": True,
        "never_replace_p216_q_education": True,
        "never_replace_p216_r_finance": True,
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_replace_identity_platform": True,
        "never_duplicate_government_core_logic": True,
        "never_duplicate_municipality_core_logic": True,
        "no_module_local_llm": True,
        "physical_ai_via_p214z_acl_only": True,
        "privacy_by_design_required": True,
        "human_governance_oversight_required": True,
        "explainable_ai_required": True,
        "ungated_physical_autonomy_strategy_forbidden": True,
        "opaque_safety_strategy_forbidden": True,
        "builds_on_p216": True, "builds_on_p216_r": True, "builds_on_p216_l": True,
        "builds_on_p216_e": True, "builds_on_p216_d": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p216_d": True, "via_p216_e": True, "via_p216_l": True, "via_p216_r": True,
        "via_p215_z": True, "via_p214_z": True, "via_p213": True,
        "via_identity": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "via_integration_platform": True,
        "api_prefix": f"{API_PREFIX}/government",
        "forbidden_sibling_bc": [
            "government_robotics_platform",
            "autonomous_public_service_platform",
            "digital_government_intelligence_platform",
            "smart_governance_automation_platform",
        ],
        "foundation_for_p216_u": True,
        "p216_s_legal_planned": True,
        "p216_j_agriculture_planned": True,
        "p216_m_space_planned": True,
        "p216_n_environmental_planned": True,
    }

def government_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /robotics/government",
        "GET /robotics/government/vision",
        "GET /robotics/government/domain",
        "GET /robotics/government/bounded-contexts",
        "GET /robotics/government/robotics",
        "GET /robotics/government/public-services",
        "GET /robotics/government/digital-government",
        "GET /robotics/government/smart-governance",
        "GET /robotics/government/citizen-intelligence",
        "GET /robotics/government/policy-intelligence",
        "GET /robotics/government/digital-twin",
        "GET /robotics/government/knowledge-graph",
        "GET /robotics/government/observability",
        "GET /robotics/government/security",
        "GET /robotics/government/cqrs",
        "GET /robotics/government/events",
        "GET /robotics/government/microservices",
        "GET /robotics/government/integration",
        "GET /robotics/government/deployment",
        "GET /robotics/government/testing",
        "GET /robotics/government/readiness",
    ], "finance_gate_routes": ["GET /robotics/finance", "GET /robotics/finance/readiness"]}
