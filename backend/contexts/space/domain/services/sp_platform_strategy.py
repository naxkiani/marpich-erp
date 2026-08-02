"""P218-B Enterprise Space Intelligence Strategic Architecture — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P218-B"
ADR = 528
SOR = "space"
API_PREFIX = "/api/v1/space"
PRODUCT = "Enterprise Space Intelligence Strategic Architecture, Enterprise Capability Model, Operating Model & Space Operating Framework"
CAPABILITY = "CAP-PLT-SP-001"
ARCHITECTURE_VISION = (
    "MEOS Space Intelligence Architecture SHALL provide a unified enterprise framework where "
    "mission intelligence, orbital operations, satellite fleets, space AI, autonomous systems and "
    "future planetary ecosystems operate as an integrated intelligent space operating system."
)
FABRIC = "meos_space_intelligence_strategic_architecture_framework"
FOUNDATION_GATE = "P218"
MISSION_GATE = "P218-A"
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"
CORE_DOMAIN = "enterprise_space_strategic_architecture"
SUPPORTING_DOMAINS = (
    {"id": "architecture_layers", "purpose": "Five-layer space enterprise architecture model."},
    {"id": "capability_model", "purpose": "Six capability groups covering twenty L1 capabilities."},
    {"id": "operating_framework", "purpose": "Ten operating dimensions and space operating framework."},
    {"id": "platform_model", "purpose": "Five space platform teams."},
    {"id": "service_model", "purpose": "Space enterprise service catalog."},
    {"id": "organizational_governance", "purpose": "Governance bodies and CoE."},
    {"id": "data_architecture", "purpose": "Space data platforms and sources."},
    {"id": "integration_architecture", "purpose": "MEOS peer integration patterns."},
    {"id": "security_architecture", "purpose": "Space strategy security framework."},
    {"id": "scalability_maturity", "purpose": "Scale dimensions and six maturity levels."},
    {"id": "transformation_roadmap", "purpose": "Four-phase strategic transformation."},
)
LOGICAL_BOUNDED_CONTEXTS = (
    {"id": "strategy_architecture", "bc": "BC-01", "name": "Space Strategic Architecture Context", "purpose": "Five architecture layers and vision."},
    {"id": "capability_model", "bc": "BC-02", "name": "Space Capability Model Context", "purpose": "Six capability groups and twenty L1 capabilities."},
    {"id": "operating_framework", "bc": "BC-03", "name": "Space Operating Framework Context", "purpose": "Operating dimensions and space operating framework."},
    {"id": "service_platform_model", "bc": "BC-04", "name": "Space Service and Platform Model Context", "purpose": "Service catalog and platform teams."},
    {"id": "organization_governance", "bc": "BC-05", "name": "Space Org and Governance Context", "purpose": "Governance bodies and CoE."},
    {"id": "data_integration", "bc": "BC-06", "name": "Space Data and Integration Context", "purpose": "Data platforms and peer integration."},
    {"id": "security_scale_maturity", "bc": "BC-07", "name": "Space Security Scale Maturity Context", "purpose": "Security, scale, maturity, transformation, CQRS, events."},
)
ARCHITECTURE_GOALS = (
    "standardized_space_capabilities",
    "enterprise_scalability",
    "mission_critical_reliability",
    "autonomous_operations_with_oversight",
    "cross_domain_meos_integration",
    "continuous_space_intelligence_improvement",
)
ARCHITECTURE_LAYERS = (
    {"id": "L01", "name": "Business Strategy Layer", "responsibilities": ("enterprise_strategy", "space_portfolio_management", "investment_governance", "space_ecosystem_planning", "capability_planning", "innovation_governance"), "outputs": ("space_strategy", "business_goals", "strategic_kpis", "enterprise_roadmap")},
    {"id": "L02", "name": "Business Capability Layer", "responsibilities": ("capability_architecture", "value_stream_architecture", "business_service_portfolio", "enterprise_ownership", "capability_lifecycle"), "outputs": ("capability_map", "capability_dependencies", "business_services", "service_catalogue")},
    {"id": "L03", "name": "Business Process Layer", "responsibilities": ("mission_lifecycle", "satellite_lifecycle", "research_lifecycle", "asset_lifecycle", "incident_lifecycle", "commercial_lifecycle"), "outputs": ("enterprise_process_catalogue", "business_workflows", "process_kpis")},
    {"id": "L04", "name": "Application Architecture Layer", "responsibilities": ("space_platforms", "mission_systems", "ai_services", "analytics_platforms", "integration_services"), "outputs": ("application_portfolio", "service_architecture", "integration_architecture")},
    {"id": "L05", "name": "Technology Layer", "responsibilities": ("cloud", "edge", "space_communications", "ground_infrastructure", "ai_infrastructure", "security_infrastructure"), "outputs": ("technology_reference_model", "infrastructure_blueprint")},
)
REFERENCE_DOMAINS = (
    {"id": "RD01", "name": "mission_intelligence_architecture", "capabilities": ("mission_planning", "mission_execution", "mission_monitoring", "mission_recovery")},
    {"id": "RD02", "name": "orbital_satellite_architecture", "capabilities": ("satellite_operations", "orbital_operations", "traffic_management", "debris_management")},
    {"id": "RD03", "name": "space_ai_autonomy_architecture", "capabilities": ("space_ai", "autonomous_operations", "decision_intelligence", "digital_twin")},
    {"id": "RD04", "name": "scientific_commercial_architecture", "capabilities": ("scientific_intelligence", "space_economy", "space_communications", "navigation_intelligence")},
    {"id": "RD05", "name": "space_governance_architecture", "capabilities": ("space_security", "space_governance", "space_sustainability", "enterprise_administration")},
)
L1_CAPABILITIES = (
    {"id": "CAP-L1-01", "name": "Mission Intelligence"},
    {"id": "CAP-L1-02", "name": "Space AI"},
    {"id": "CAP-L1-03", "name": "Satellite Operations"},
    {"id": "CAP-L1-04", "name": "Orbital Operations"},
    {"id": "CAP-L1-05", "name": "Space Robotics"},
    {"id": "CAP-L1-06", "name": "Navigation Intelligence"},
    {"id": "CAP-L1-07", "name": "Ground Segment Operations"},
    {"id": "CAP-L1-08", "name": "Space Communications"},
    {"id": "CAP-L1-09", "name": "Scientific Intelligence"},
    {"id": "CAP-L1-10", "name": "Space Economy"},
    {"id": "CAP-L1-11", "name": "Space Security"},
    {"id": "CAP-L1-12", "name": "Space Governance"},
    {"id": "CAP-L1-13", "name": "Space Sustainability"},
    {"id": "CAP-L1-14", "name": "Digital Twin Platform"},
    {"id": "CAP-L1-15", "name": "Knowledge Graph Platform"},
    {"id": "CAP-L1-16", "name": "Enterprise Analytics"},
    {"id": "CAP-L1-17", "name": "Decision Intelligence"},
    {"id": "CAP-L1-18", "name": "Autonomous Operations"},
    {"id": "CAP-L1-19", "name": "Integration Platform"},
    {"id": "CAP-L1-20", "name": "Enterprise Administration"},
)
CAPABILITY_GROUPS = (
    {"id": "CG01", "name": "Mission and Orbital Operations", "capabilities": ("mission_intelligence", "satellite_operations", "orbital_operations", "ground_segment_operations")},
    {"id": "CG02", "name": "Space AI and Autonomy", "capabilities": ("space_ai", "autonomous_operations", "decision_intelligence", "space_robotics")},
    {"id": "CG03", "name": "Scientific Navigation and Communications", "capabilities": ("scientific_intelligence", "navigation_intelligence", "space_communications")},
    {"id": "CG04", "name": "Space Economy and Commercial", "capabilities": ("space_economy",)},
    {"id": "CG05", "name": "Security Governance and Sustainability", "capabilities": ("space_security", "space_governance", "space_sustainability")},
    {"id": "CG06", "name": "Platform Services and Administration", "capabilities": ("digital_twin_platform", "knowledge_graph_platform", "enterprise_analytics", "integration_platform", "enterprise_administration")},
)
OPERATING_COMPONENTS = (
    {"id": "OM01", "name": "Mission Operations", "purpose": "Plan execute monitor recover missions", "automation_level": "ai_assisted_with_human_oversight"},
    {"id": "OM02", "name": "Scientific Operations", "purpose": "Scientific planning discovery publication", "automation_level": "ai_assisted"},
    {"id": "OM03", "name": "Satellite Operations", "purpose": "Fleet deployment configuration maintenance", "automation_level": "ai_assisted_with_human_oversight"},
    {"id": "OM04", "name": "Orbital Operations", "purpose": "Tracking traffic collision debris", "automation_level": "high_automation_gated"},
    {"id": "OM05", "name": "Commercial Operations", "purpose": "Service delivery marketplace contracts", "automation_level": "digitised_integrated"},
    {"id": "OM06", "name": "Engineering Operations", "purpose": "Asset lifecycle engineering change", "automation_level": "digitised"},
    {"id": "OM07", "name": "Security Operations", "purpose": "Cyber physical space security", "automation_level": "continuous_monitoring"},
    {"id": "OM08", "name": "Compliance Operations", "purpose": "Regulatory sustainability compliance", "automation_level": "policy_driven"},
    {"id": "OM09", "name": "Platform Operations", "purpose": "MEOS space platform SRE", "automation_level": "cloud_native"},
    {"id": "OM10", "name": "Enterprise Governance", "purpose": "Strategic operational governance", "automation_level": "committee_gated"},
)
SPACE_OPERATING_FRAMEWORK = (
    {"id": "SOF01", "name": "Mission Framework", "stages": ("mission_planning", "mission_approval", "mission_execution", "mission_monitoring", "mission_recovery")},
    {"id": "SOF02", "name": "Satellite Framework", "stages": ("deployment", "configuration", "operations", "maintenance", "retirement")},
    {"id": "SOF03", "name": "Orbital Framework", "stages": ("tracking", "collision_prevention", "traffic_management", "orbit_optimisation", "debris_management")},
    {"id": "SOF04", "name": "Research Framework", "stages": ("scientific_planning", "experiment_lifecycle", "data_collection", "discovery", "publication")},
    {"id": "SOF05", "name": "Commercial Framework", "stages": ("service_delivery", "billing", "marketplace", "contracts", "partner_management")},
    {"id": "SOF06", "name": "Governance Framework", "stages": ("risk", "compliance", "audit", "security", "performance", "continuous_improvement")},
)
PLATFORM_TEAMS = (
    {"id": "PT01", "name": "Space Intelligence Platform Team", "responsibilities": ("space_ai", "mission_intelligence", "decision_intelligence")},
    {"id": "PT02", "name": "Orbital Operations Platform Team", "responsibilities": ("satellite_ops", "orbital_traffic", "ground_segment")},
    {"id": "PT03", "name": "Space Digital Twin Team", "responsibilities": ("twins", "simulation", "knowledge_graph")},
    {"id": "PT04", "name": "Autonomous Mission Team", "responsibilities": ("autonomy", "robotics_acl", "recovery")},
    {"id": "PT05", "name": "Space Governance Team", "responsibilities": ("security", "compliance", "sustainability", "oversight")},
)
CORE_SERVICES = (
    {"id": "mission_planning", "category": "mission_intelligence", "purpose": "Mission planning and approval intents", "ownership": "space", "apis": ("/api/v1/space/missions/plan",), "events": ("space.mission.planned.v1",)},
    {"id": "mission_monitoring", "category": "mission_intelligence", "purpose": "Mission health and anomaly surfaces", "ownership": "space", "apis": ("/api/v1/space/missions/monitor",), "events": ("space.mission.anomaly.detected.v1",)},
    {"id": "satellite_fleet", "category": "satellite_operations", "purpose": "Satellite fleet lifecycle", "ownership": "space", "apis": ("/api/v1/space/satellites",), "events": ("space.satellite.state.changed.v1",)},
    {"id": "orbital_traffic", "category": "orbital_operations", "purpose": "Orbital traffic and collision risk", "ownership": "space", "apis": ("/api/v1/space/orbital/traffic",), "events": ("space.orbital.collision_risk.raised.v1",)},
    {"id": "space_ai_surfaces", "category": "space_ai", "purpose": "Space AI via P214-Z ACL only", "ownership": "space_acl_to_ai", "apis": ("/api/v1/ai",), "events": ("ai.insight.generated.v1",)},
    {"id": "prediction_services", "category": "space_ai", "purpose": "Orbital prediction via AI Platform", "ownership": "space_acl_to_ai", "apis": ("/api/v1/ai",), "events": ("ai.prediction.completed.v1",)},
    {"id": "autonomy_orchestration", "category": "autonomous_operations", "purpose": "Gated autonomous mission orchestration", "ownership": "space", "apis": ("/api/v1/space/autonomy",), "events": ("space.autonomy.decision.proposed.v1",)},
    {"id": "robotics_acl", "category": "space_robotics", "purpose": "Physical autonomy via P216-Z", "ownership": "space_acl_to_robotics", "apis": ("/api/v1/robotics",), "events": ("robotics.task.completed.v1",)},
    {"id": "quantum_optimisation", "category": "navigation_intelligence", "purpose": "Trajectory optimisation via P215-Z", "ownership": "space_acl_to_quantum", "apis": ("/api/v1/quantum",), "events": ("quantum.optimisation.completed.v1",)},
    {"id": "bio_life_support", "category": "scientific_intelligence", "purpose": "Life support via P217-Z", "ownership": "space_acl_to_bio", "apis": ("/api/v1/biotechnology",), "events": ("biotechnology.life_support.updated.v1",)},
    {"id": "digital_twin", "category": "platform", "purpose": "Space digital twin projections", "ownership": "space", "apis": ("/api/v1/space/twins",), "events": ("space.twin.updated.v1",)},
    {"id": "knowledge_graph", "category": "platform", "purpose": "Space knowledge graph services", "ownership": "space", "apis": ("/api/v1/space/knowledge-graph",), "events": ("space.knowledge.graph.updated.v1",)},
    {"id": "space_analytics", "category": "platform", "purpose": "Analytics facets via Analytics Platform", "ownership": "analytics_with_space_facets", "apis": ("/api/v1/analytics",), "events": ("analytics.metric.recorded.v1",)},
    {"id": "telemetry_integration", "category": "integration", "purpose": "Telemetry via Integration Platform only", "ownership": "integration_with_space_contracts", "apis": ("/api/v1/integrations",), "events": ("integration.sync.completed.v1",)},
    {"id": "governance_services", "category": "governance", "purpose": "Space governance and oversight", "ownership": "space", "apis": ("/api/v1/space/governance",), "events": ("space.governance.decision.recorded.v1",)},
    {"id": "sustainability_services", "category": "governance", "purpose": "Debris and sustainability attestation", "ownership": "space", "apis": ("/api/v1/space/sustainability",), "events": ("space.sustainability.attested.v1",)},
)
VALUE_NETWORK = (
    {"id": "VN01", "name": "Space Agencies", "role": "mission_authority"},
    {"id": "VN02", "name": "Commercial Operators", "role": "fleet_operator"},
    {"id": "VN03", "name": "Launch Providers", "role": "launch_service"},
    {"id": "VN04", "name": "Ground Stations", "role": "ground_segment"},
    {"id": "VN05", "name": "Research Institutions", "role": "science_consumer"},
    {"id": "VN06", "name": "Universities", "role": "research_partner"},
    {"id": "VN07", "name": "Governments", "role": "regulator_sponsor"},
    {"id": "VN08", "name": "Investors", "role": "capital"},
    {"id": "VN09", "name": "Manufacturers", "role": "hardware_supplier"},
    {"id": "VN10", "name": "Satellite Owners", "role": "asset_owner"},
    {"id": "VN11", "name": "Mission Operators", "role": "mission_execution"},
    {"id": "VN12", "name": "Customers", "role": "service_consumer"},
)
OPERATING_SCENARIOS = (
    {"id": "SC01", "name": "Launch Mission"},
    {"id": "SC02", "name": "Satellite Failure Recovery"},
    {"id": "SC03", "name": "Orbital Collision Avoidance"},
    {"id": "SC04", "name": "Scientific Discovery Mission"},
    {"id": "SC05", "name": "Space Weather Response"},
    {"id": "SC06", "name": "Deep Space Exploration"},
    {"id": "SC07", "name": "Commercial Service Delivery"},
    {"id": "SC08", "name": "Security Incident Response"},
)
GOVERNANCE_LAYERS = (
    "strategic_governance", "portfolio_governance", "mission_governance", "technology_governance",
    "security_governance", "ai_governance", "data_governance", "compliance_governance",
    "operational_governance", "innovation_governance",
)
VALUE_CHAIN = (
    {"stage": 1, "name": "enterprise_strategy"},
    {"stage": 2, "name": "business_capabilities"},
    {"stage": 3, "name": "business_services"},
    {"stage": 4, "name": "processes"},
    {"stage": 5, "name": "applications"},
    {"stage": 6, "name": "platform_services"},
    {"stage": 7, "name": "infrastructure"},
    {"stage": 8, "name": "space_assets"},
    {"stage": 9, "name": "mission_execution"},
    {"stage": 10, "name": "continuous_optimisation"},
)
GOVERNANCE_BODIES = (
    "space_strategy_council", "mission_oversight_board", "orbital_safety_committee",
    "security_council", "compliance_office", "innovation_board",
)
DATA_SOURCES = ("telemetry", "ephemeris", "mission_plans", "scientific_observations", "traffic_catalogues", "space_weather")
DATA_PLATFORMS = ("space_data_lake", "space_knowledge_graph", "space_digital_twin_platform", "telemetry_exchange")
INTEGRATION_TARGETS = ("p214z_ai_master", "p215z_quantum_supreme", "p216z_robotics_supreme", "p217z_bio_nexus", "meos_integration", "meos_security", "meos_workflow", "meos_policy")
INTEGRATION_PATTERNS = ("api_first", "event_driven", "streaming_intelligence", "digital_twin_synchronization", "acl_peer_ids_only")
SECURITY_DOMAINS = ("mission_security", "orbital_cybersecurity", "ground_segment_security", "telemetry_integrity", "ai_decision_security", "strategy_access_controls")
SECURITY_PRINCIPLES = ("zero_trust", "least_privilege", "continuous_verification", "human_mission_oversight", "sustainability_by_design")
SCALE_DIMENSIONS = ("mission_volume", "constellation_scale", "tenant_expansion", "telemetry_volume", "autonomy_workload")
SCALE_REQUIREMENTS = ("multi_tenant_support", "cloud_scaling", "edge_ground_segment", "global_deployment", "mission_critical_isolation")
MATURITY_LEVELS = (
    {"level": 1, "name": "Manual", "characteristics": ("manual_mission_control", "siloed_systems", "paper_workflows")},
    {"level": 2, "name": "Digitised", "characteristics": ("digital_mission_records", "basic_telemetry_dashboards", "digitised_processes")},
    {"level": 3, "name": "Integrated", "characteristics": ("integrated_platforms", "event_driven_ops", "enterprise_integration")},
    {"level": 4, "name": "AI Assisted", "characteristics": ("ai_recommendations", "predictive_anomaly", "decision_support")},
    {"level": 5, "name": "Autonomous", "characteristics": ("gated_autonomy", "robotic_ops", "closed_loop_control")},
    {"level": 6, "name": "Self Optimising", "characteristics": ("continuous_optimisation", "planetary_scale_intelligence", "civilisation_ready_ops")},
)
TRANSFORMATION_PHASES = (
    {"phase": 1, "name": "Space Strategic Foundation", "focus": ("architecture", "capabilities", "governance")},
    {"phase": 2, "name": "Orbital Intelligence Expansion", "focus": ("digital_twin", "space_ai", "satellite_ops")},
    {"phase": 3, "name": "Autonomous Mission Operations", "focus": ("gated_autonomy", "robotics_acl", "commercial_space")},
    {"phase": 4, "name": "Planetary Scale Intelligence", "focus": ("deep_space", "planetary_ops", "ecosystem_intelligence")},
)
COMMANDS = (
    "RegisterSpaceCapabilityCommand", "PublishSpaceOperatingModelCommand", "AssessSpaceMaturityCommand",
    "LaunchSpaceTransformationCommand", "UpdateSpaceServiceCatalogCommand",
)
QUERIES = (
    "GetSpaceArchitectureQuery", "GetSpaceCapabilityModelQuery", "GetSpaceOperatingFrameworkQuery",
    "GetSpaceServiceCatalogQuery", "GetSpaceTransformationStatusQuery",
)
CORE_EVENTS = (
    {"name": "SpaceArchitecturePublishedEvent", "schema": "space.architecture.published.v1", "owner": "strategy_architecture", "consumers": "audit,analytics,governance"},
    {"name": "SpaceCapabilityRegisteredEvent", "schema": "space.capability.registered.v1", "owner": "capability_model", "consumers": "audit,search,analytics"},
    {"name": "SpaceOperatingModelUpdatedEvent", "schema": "space.operating_model.updated.v1", "owner": "operating_framework", "consumers": "audit,workflow,notifications"},
    {"name": "SpaceMaturityAssessedEvent", "schema": "space.maturity.assessed.v1", "owner": "security_scale_maturity", "consumers": "analytics,strategy"},
    {"name": "SpaceTransformationAdvancedEvent", "schema": "space.transformation.advanced.v1", "owner": "security_scale_maturity", "consumers": "analytics,notifications,governance"},
    {"name": "SpaceServiceCatalogUpdatedEvent", "schema": "space.service_catalog.updated.v1", "owner": "service_platform_model", "consumers": "audit,search"},
)
MICROSERVICES = (
    {"id": "space_strategy_architecture_service", "bc": "BC-01", "api": "/space/strategy", "db": "space_*", "events": ("SpaceArchitecturePublishedEvent",), "security": ("space.read",), "scaling": "strategy_replicas"},
    {"id": "capability_model_service", "bc": "BC-02", "api": "/space/strategy/capabilities", "db": "space_*", "events": ("SpaceCapabilityRegisteredEvent",), "security": ("space.read",), "scaling": "capability_workers"},
    {"id": "operating_framework_service", "bc": "BC-03", "api": "/space/strategy/operating-model", "db": "space_*", "events": ("SpaceOperatingModelUpdatedEvent",), "security": ("space.read",), "scaling": "ops_model_replicas"},
    {"id": "service_model_service", "bc": "BC-04", "api": "/space/strategy/services", "db": "space_*", "events": ("SpaceServiceCatalogUpdatedEvent",), "security": ("space.read",), "scaling": "service_catalog_replicas"},
    {"id": "organization_governance_service", "bc": "BC-05", "api": "/space/strategy/governance", "db": "space_*", "events": ("SpaceArchitecturePublishedEvent",), "security": ("space.admin",), "scaling": "governance_replicas"},
    {"id": "data_integration_service", "bc": "BC-06", "api": "/space/strategy/data", "db": "space_*", "events": ("SpaceCapabilityRegisteredEvent",), "security": ("space.read",), "scaling": "data_workers"},
    {"id": "security_architecture_service", "bc": "BC-07", "api": "/space/strategy/security", "db": "space_*", "events": ("SpaceArchitecturePublishedEvent",), "security": ("space.admin",), "scaling": "security_replicas"},
    {"id": "maturity_transformation_service", "bc": "BC-07", "api": "/space/strategy/maturity", "db": "space_*", "events": ("SpaceMaturityAssessedEvent", "SpaceTransformationAdvancedEvent"), "security": ("space.read",), "scaling": "maturity_replicas"},
)
API_SURFACES = (
    "/api/v1/space/strategy",
    "/api/v1/space/strategy/layers",
    "/api/v1/space/strategy/capabilities",
    "/api/v1/space/strategy/operating-model",
    "/api/v1/space/strategy/services",
    "/api/v1/space/strategy/organization",
    "/api/v1/space/strategy/governance",
    "/api/v1/space/strategy/data",
    "/api/v1/space/strategy/integration",
    "/api/v1/space/strategy/security",
    "/api/v1/space/strategy/scalability",
    "/api/v1/space/strategy/maturity",
    "/api/v1/space/strategy/roadmap",
    "/api/v1/space/strategy/cqrs",
    "/api/v1/space/strategy/events",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
SECURITY = {
    "present_required": True,
    "zero_trust": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "never_replace_p218_foundation": True,
    "never_replace_p218_a_mission": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "never_replace_p216_z": True,
    "never_replace_biotechnology": True,
    "never_skip_human_mission_oversight_strategy": True,
    "never_skip_space_cybersecurity_strategy": True,
    "never_skip_space_sustainability_strategy": True,
    "never_opaque_mission_critical_strategy": True,
    "never_ungated_autonomous_mission_strategy": True,
    "domains": list(SECURITY_DOMAINS),
    "principles": list(SECURITY_PRINCIPLES),
}
DEPLOYMENT = {"present_required": True, "cloud_native": True, "components": ("strategy_services_cluster", "capability_model_service", "space_intelligence_plane", "strategic_observability")}
TESTING = (
    "strategy_architecture_testing", "capability_model_testing", "operating_framework_testing",
    "service_model_testing", "governance_testing", "security_architecture_testing",
    "maturity_model_testing", "transformation_roadmap_testing",
)
QUALITY_GATES_REJECT_IF = (
    "space_strategic_architecture_is_missing", "capability_model_is_missing",
    "operating_framework_is_missing", "platform_model_is_missing", "service_model_is_missing",
    "organizational_model_is_missing", "governance_model_is_missing", "security_model_is_missing",
    "data_architecture_is_missing", "integration_architecture_is_missing",
    "scalability_model_is_missing", "maturity_model_is_missing", "transformation_roadmap_is_missing",
    "space_operating_framework_is_missing",
    "cqrs_architecture_is_missing", "event_architecture_is_missing",
    "microservices_architecture_is_missing", "api_first_architecture_is_missing",
    "cloud_native_deployment_is_missing", "sibling_space_bc",
    "replace_p218_foundation", "replace_p218_a_mission",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Space Intelligence Strategic Architecture Framework",
        "architecture_vision": ARCHITECTURE_VISION,
        "goals": list(ARCHITECTURE_GOALS),
        "builds_on_p218": True, "builds_on_p218_a": True,
        "builds_on_p217_z": True, "builds_on_p216_z": True, "builds_on_p215_z": True, "builds_on_p214_z": True,
        "never_replace_p218_foundation": True, "never_replace_p218_a_mission": True,
        "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
    }

def domain_model() -> dict[str, Any]:
    return {"core_domain": CORE_DOMAIN, "supporting_domains": [dict(d) for d in SUPPORTING_DOMAINS], "supporting_count": len(SUPPORTING_DOMAINS)}

def bounded_contexts() -> dict[str, Any]:
    return {"contexts": [dict(c) for c in LOGICAL_BOUNDED_CONTEXTS], "context_count": len(LOGICAL_BOUNDED_CONTEXTS)}

def architecture_layers() -> dict[str, Any]:
    return {"present_required": True, "layers": [dict(x) for x in ARCHITECTURE_LAYERS], "layer_count": len(ARCHITECTURE_LAYERS)}

def reference_architecture() -> dict[str, Any]:
    return {"present_required": True, "domains": [dict(d) for d in REFERENCE_DOMAINS], "domain_count": len(REFERENCE_DOMAINS)}

def capability_model() -> dict[str, Any]:
    return {
        "present_required": True,
        "groups": [dict(g) for g in CAPABILITY_GROUPS],
        "group_count": len(CAPABILITY_GROUPS),
        "l1_capabilities": [dict(c) for c in L1_CAPABILITIES],
        "l1_count": len(L1_CAPABILITIES),
        "domain_count": len(CAPABILITY_GROUPS),
    }

def operating_framework() -> dict[str, Any]:
    return {
        "present_required": True,
        "model": "meos_space_operating_framework",
        "components": [dict(x) for x in OPERATING_COMPONENTS],
        "component_count": len(OPERATING_COMPONENTS),
        "framework_layers": [dict(x) for x in SPACE_OPERATING_FRAMEWORK],
        "framework_layer_count": len(SPACE_OPERATING_FRAMEWORK),
        "scenarios": [dict(s) for s in OPERATING_SCENARIOS],
        "scenario_count": len(OPERATING_SCENARIOS),
        "value_network": [dict(v) for v in VALUE_NETWORK],
        "value_network_count": len(VALUE_NETWORK),
    }

def platform_model() -> dict[str, Any]:
    return {"present_required": True, "teams": [dict(t) for t in PLATFORM_TEAMS], "team_count": len(PLATFORM_TEAMS)}

def service_model() -> dict[str, Any]:
    return {"present_required": True, "services": [dict(s) for s in CORE_SERVICES], "service_count": len(CORE_SERVICES)}

def organizational_model() -> dict[str, Any]:
    return {"present_required": True, "platform_teams": [dict(t) for t in PLATFORM_TEAMS], "governance_bodies": list(GOVERNANCE_BODIES)}

def governance_model() -> dict[str, Any]:
    return {"present_required": True, "bodies": list(GOVERNANCE_BODIES), "layers": list(GOVERNANCE_LAYERS), "layer_count": len(GOVERNANCE_LAYERS)}

def data_architecture() -> dict[str, Any]:
    return {"present_required": True, "sources": list(DATA_SOURCES), "platforms": list(DATA_PLATFORMS)}

def integration_architecture() -> dict[str, Any]:
    return {"present_required": True, "targets": list(INTEGRATION_TARGETS), "patterns": list(INTEGRATION_PATTERNS)}

def security_architecture() -> dict[str, Any]:
    return dict(SECURITY)

def scalability_model() -> dict[str, Any]:
    return {"present_required": True, "dimensions": list(SCALE_DIMENSIONS), "requirements": list(SCALE_REQUIREMENTS)}

def maturity_model() -> dict[str, Any]:
    return {"present_required": True, "levels": [dict(x) for x in MATURITY_LEVELS], "level_count": len(MATURITY_LEVELS)}

def value_chain() -> dict[str, Any]:
    return {"present_required": True, "stages": [dict(s) for s in VALUE_CHAIN], "stage_count": len(VALUE_CHAIN)}

def transformation_roadmap() -> dict[str, Any]:
    return {"present_required": True, "phases": [dict(p) for p in TRANSFORMATION_PHASES], "phase_count": len(TRANSFORMATION_PHASES)}

def cqrs() -> dict[str, Any]:
    return {"present_required": True, "commands": list(COMMANDS), "queries": list(QUERIES)}

def events() -> dict[str, Any]:
    return {"present_required": True, "events": [dict(e) for e in CORE_EVENTS], "event_count": len(CORE_EVENTS)}

def microservices() -> dict[str, Any]:
    return {"services": [dict(s) for s in MICROSERVICES], "service_count": len(MICROSERVICES)}

def api() -> dict[str, Any]:
    return {"present_required": True, "surfaces": list(API_SURFACES), "styles": list(API_STYLES), "api_first": True}

def deployment() -> dict[str, Any]:
    return dict(DEPLOYMENT)

def testing() -> dict[str, Any]:
    return {"suites": list(TESTING)}

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p218_c": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "architecture_vision": ARCHITECTURE_VISION, "principle": ARCHITECTURE_VISION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P218", "P218-A", "P217-Z", "P216-Z", "P215-Z", "P214-Z", "ADR-526", "ADR-527"],
        "vision": vision_pack(), "domain_model": domain_model(), "bounded_contexts": bounded_contexts(),
        "architecture_layers": architecture_layers(), "reference_architecture": reference_architecture(),
        "capability_model": capability_model(), "operating_framework": operating_framework(),
        "platform_model": platform_model(), "service_model": service_model(),
        "organizational_model": organizational_model(), "governance_model": governance_model(),
        "data_architecture": data_architecture(), "integration_architecture": integration_architecture(),
        "security_architecture": security_architecture(), "scalability_model": scalability_model(),
        "maturity_model": maturity_model(), "value_chain": value_chain(),
        "transformation_roadmap": transformation_roadmap(),
        "cqrs": cqrs(), "events": events(), "microservices": microservices(), "api": api(),
        "security": security_architecture(), "deployment": deployment(), "testing": testing(),
        "quality_gates": quality_gates(), "production_readiness": production_readiness(),
        "space_strategic_architecture_present_required": True,
        "capability_model_present_required": True,
        "operating_framework_present_required": True,
        "platform_model_present_required": True,
        "service_model_present_required": True,
        "organizational_model_present_required": True,
        "governance_model_present_required": True,
        "security_model_present_required": True,
        "data_architecture_present_required": True,
        "integration_architecture_present_required": True,
        "scalability_model_present_required": True,
        "maturity_model_present_required": True,
        "transformation_roadmap_present_required": True,
        "space_operating_framework_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "cloud_native_deployment_present_required": True,
        "sibling_space_bc_forbidden": True,
        "never_replace_p218_foundation": True,
        "never_replace_p218_a_mission": True,
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_replace_p216_z": True,
        "never_replace_biotechnology": True,
        "never_skip_human_mission_oversight_strategy": True,
        "never_skip_space_cybersecurity_strategy": True,
        "never_skip_space_sustainability_strategy": True,
        "never_opaque_mission_critical_strategy": True,
        "never_ungated_autonomous_mission_strategy": True,
        "builds_on_p218": True, "builds_on_p218_a": True,
        "builds_on_p217_z": True, "builds_on_p216_z": True, "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p217": True, "via_p216_z": True, "via_p215_z": True, "via_p214_z": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "api_prefix": f"{API_PREFIX}/strategy",
        "forbidden_sibling_bc": [
            "space_strategy_platform",
            "space_capability_platform",
            "space_operating_framework_platform",
        ],
        "foundation_for_p218_c": True,
    }

def strategy_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /space/strategy",
        "GET /space/strategy/layers",
        "GET /space/strategy/capabilities",
        "GET /space/strategy/operating-model",
        "GET /space/strategy/services",
        "GET /space/strategy/organization",
        "GET /space/strategy/governance",
        "GET /space/strategy/data",
        "GET /space/strategy/integration",
        "GET /space/strategy/security",
        "GET /space/strategy/scalability",
        "GET /space/strategy/maturity",
        "GET /space/strategy/roadmap",
        "GET /space/strategy/cqrs",
        "GET /space/strategy/events",
        "GET /space/strategy/readiness",
    ], "foundation_gate_routes": ["GET /space/foundation", "GET /space/foundation/readiness"],
       "mission_gate_routes": ["GET /space/mission", "GET /space/mission/readiness"]}
