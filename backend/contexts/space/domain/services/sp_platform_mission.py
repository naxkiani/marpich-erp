"""P218-A Enterprise Space Intelligence Mission, Vision & Strategic Scope — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P218-A"
ADR = 527
SOR = "space"
API_PREFIX = "/api/v1/space"
PRODUCT = "Enterprise Space Intelligence Mission, Vision, Strategic Scope & Space Intelligence Capability Framework"
CAPABILITY = "CAP-PLT-SP-001"
MISSION = (
    "Build a unified enterprise platform capable of planning, operating, monitoring, analysing and "
    "continuously optimising space missions, orbital assets, scientific exploration and future space "
    "economy ecosystems using Artificial Intelligence, autonomous systems and enterprise-grade governance."
)
VISION = (
    "Become the world's most comprehensive Enterprise Space Intelligence Platform capable of orchestrating "
    "satellites, spacecraft, orbital infrastructure, autonomous robotic systems and future planetary "
    "ecosystems through one intelligent operating system."
)
FABRIC = "meos_space_intelligence_strategic_framework"
FOUNDATION_GATE = "P218"
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"
CORE_DOMAIN = "enterprise_space_strategy_management"
SUPPORTING_DOMAINS = (
    {"id": "space_vision", "purpose": "Long-term space intelligence future state."},
    {"id": "business_drivers", "purpose": "DRV-01..10 strategic drivers."},
    {"id": "strategic_objectives", "purpose": "Mission objectives and outcomes."},
    {"id": "capability_framework", "purpose": "Level-1 space capabilities."},
    {"id": "value_streams", "purpose": "VS-01..10 enterprise value streams."},
    {"id": "maturity_model", "purpose": "Space intelligence maturity levels."},
    {"id": "governance_strategy", "purpose": "Mission safety and space governance."},
    {"id": "evolution_roadmap", "purpose": "Five-year strategic roadmap."},
    {"id": "stakeholders_kpis", "purpose": "Stakeholders and strategic KPIs."},
)
LOGICAL_BOUNDED_CONTEXTS = (
    {"id": "mission_vision", "bc": "BC-01", "name": "Space Mission and Vision Context", "purpose": "Mission, vision, and strategic intent."},
    {"id": "strategic_scope", "bc": "BC-02", "name": "Strategic Scope and Drivers Context", "purpose": "Scope boundaries and business drivers."},
    {"id": "capability_framework", "bc": "BC-03", "name": "Space Capability Framework Context", "purpose": "Level-1 capabilities and ownership."},
    {"id": "value_streams", "bc": "BC-04", "name": "Space Value Streams Context", "purpose": "Enterprise space value streams."},
    {"id": "maturity_model", "bc": "BC-05", "name": "Space Maturity Model Context", "purpose": "Maturity levels 01-05."},
    {"id": "governance_strategy", "bc": "BC-06", "name": "Space Governance Strategy Context", "purpose": "Safety, cybersecurity, sustainability governance."},
    {"id": "integration_evolution", "bc": "BC-07", "name": "Integration and Evolution Roadmap Context", "purpose": "MEOS peers and five-year roadmap."},
)
VISION_FUTURE_STATE = ("earth", "orbital_infrastructure", "lunar_operations", "deep_space_operations", "planetary_colonisation_support", "civilisation_scale_space_intelligence")
MISSION_OBJECTIVES = (
    {"id": "OBJ-01", "name": "Enable intelligent space operations"},
    {"id": "OBJ-02", "name": "Support autonomous orbital infrastructure"},
    {"id": "OBJ-03", "name": "Accelerate scientific discovery"},
    {"id": "OBJ-04", "name": "Improve mission safety"},
    {"id": "OBJ-05", "name": "Optimise utilisation of space resources"},
    {"id": "OBJ-06", "name": "Enable commercial space ecosystems"},
    {"id": "OBJ-07", "name": "Support future interplanetary expansion"},
    {"id": "OBJ-08", "name": "Create a trusted enterprise space operating environment"},
)
BUSINESS_DRIVERS = (
    {"id": "DRV-01", "name": "Growth of commercial space economy"},
    {"id": "DRV-02", "name": "Rapid increase in orbital assets"},
    {"id": "DRV-03", "name": "Autonomous mission operations"},
    {"id": "DRV-04", "name": "Satellite constellation management"},
    {"id": "DRV-05", "name": "Space sustainability"},
    {"id": "DRV-06", "name": "Planetary defence"},
    {"id": "DRV-07", "name": "Deep-space exploration"},
    {"id": "DRV-08", "name": "Scientific collaboration"},
    {"id": "DRV-09", "name": "Space resource utilisation"},
    {"id": "DRV-10", "name": "Future space civilisation readiness"},
)
STRATEGIC_SCOPE = {
    "present_required": True,
    "in_scope": (
        "mission_planning", "space_ai", "orbital_operations", "satellite_fleet_management",
        "space_robotics", "ground_segment_intelligence", "telemetry_analytics", "orbital_traffic_management",
        "space_digital_twins", "space_weather_intelligence", "deep_space_communications",
        "scientific_research_support", "space_logistics", "space_economy_intelligence",
        "space_asset_management", "planetary_exploration", "lunar_infrastructure",
        "asteroid_resource_intelligence", "space_sustainability", "space_security",
        "space_governance", "autonomous_mission_control",
    ),
    "out_of_scope": (
        "consumer_astronomy_applications", "personal_telescope_software",
        "entertainment_only_space_applications", "non_enterprise_hobbyist_systems",
    ),
}
L1_CAPABILITIES = (
    {"id": "CAP-L1-01", "name": "Mission Intelligence", "owner": "mission_command", "criticality": "critical"},
    {"id": "CAP-L1-02", "name": "Space AI", "owner": "space_ai_architecture", "criticality": "critical"},
    {"id": "CAP-L1-03", "name": "Orbital Operations", "owner": "operations", "criticality": "critical"},
    {"id": "CAP-L1-04", "name": "Satellite Management", "owner": "operations", "criticality": "high"},
    {"id": "CAP-L1-05", "name": "Space Robotics", "owner": "engineering", "criticality": "high"},
    {"id": "CAP-L1-06", "name": "Ground Operations", "owner": "operations", "criticality": "high"},
    {"id": "CAP-L1-07", "name": "Scientific Intelligence", "owner": "research", "criticality": "medium"},
    {"id": "CAP-L1-08", "name": "Navigation Intelligence", "owner": "engineering", "criticality": "critical"},
    {"id": "CAP-L1-09", "name": "Space Security", "owner": "security", "criticality": "critical"},
    {"id": "CAP-L1-10", "name": "Infrastructure Intelligence", "owner": "engineering", "criticality": "high"},
    {"id": "CAP-L1-11", "name": "Space Economy", "owner": "finance", "criticality": "medium"},
    {"id": "CAP-L1-12", "name": "Resource Intelligence", "owner": "research", "criticality": "medium"},
    {"id": "CAP-L1-13", "name": "Space Governance", "owner": "compliance", "criticality": "critical"},
    {"id": "CAP-L1-14", "name": "Space Sustainability", "owner": "compliance", "criticality": "high"},
    {"id": "CAP-L1-15", "name": "Digital Twin Platform", "owner": "enterprise_architecture", "criticality": "high"},
    {"id": "CAP-L1-16", "name": "Knowledge Graph Platform", "owner": "data_governance", "criticality": "high"},
    {"id": "CAP-L1-17", "name": "Analytics Platform", "owner": "data_governance", "criticality": "medium"},
    {"id": "CAP-L1-18", "name": "Decision Intelligence", "owner": "executive_leadership", "criticality": "high"},
    {"id": "CAP-L1-19", "name": "Autonomous Operations", "owner": "operations", "criticality": "critical"},
    {"id": "CAP-L1-20", "name": "Enterprise Administration", "owner": "enterprise_architecture", "criticality": "medium"},
)
CAPABILITY_FRAMEWORK = {
    "present_required": True,
    "levels": (
        {"level": 1, "name": "foundation_capabilities", "capabilities": ("mission_intelligence", "satellite_management", "ground_operations", "telemetry_analytics", "space_security")},
        {"level": 2, "name": "advanced_capabilities", "capabilities": ("space_ai", "orbital_operations", "digital_twin", "navigation_intelligence", "scientific_intelligence")},
        {"level": 3, "name": "strategic_capabilities", "capabilities": ("autonomous_operations", "space_robotics", "space_economy", "space_sustainability", "decision_intelligence")},
        {"level": 4, "name": "future_capabilities", "capabilities": ("planetary_operations", "deep_space_intelligence", "orbital_civilisation_intelligence", "planetary_scale_operations")},
    ),
    "l1_capabilities": L1_CAPABILITIES,
    "l1_count": len(L1_CAPABILITIES),
}
VALUE_STREAMS = {
    "present_required": True,
    "streams": (
        {"id": "VS-01", "name": "Mission Planning", "input": "mission_objectives", "activities": ("requirements", "trajectory_design", "risk_assessment"), "output": "approved_mission_plan", "kpi": "mission_planning_time"},
        {"id": "VS-02", "name": "Mission Execution", "input": "approved_mission_plan", "activities": ("launch_window", "command_uplink", "autonomous_control"), "output": "mission_execution_state", "kpi": "mission_success_rate"},
        {"id": "VS-03", "name": "Mission Monitoring", "input": "telemetry", "activities": ("health_monitoring", "anomaly_detection", "alerting"), "output": "operational_situation", "kpi": "mean_time_to_detect"},
        {"id": "VS-04", "name": "Scientific Discovery", "input": "observation_data", "activities": ("analysis", "hypothesis", "publication_pipeline"), "output": "scientific_insights", "kpi": "scientific_discovery_velocity"},
        {"id": "VS-05", "name": "Satellite Operations", "input": "constellation_state", "activities": ("scheduling", "manoeuvre", "payload_ops"), "output": "service_availability", "kpi": "satellite_availability"},
        {"id": "VS-06", "name": "Orbital Asset Lifecycle", "input": "asset_registry", "activities": ("commission", "maintain", "decommission"), "output": "asset_health", "kpi": "resource_utilisation"},
        {"id": "VS-07", "name": "Space Resource Intelligence", "input": "survey_data", "activities": ("prospecting", "valuation", "planning"), "output": "resource_opportunities", "kpi": "resource_utilisation"},
        {"id": "VS-08", "name": "Commercial Space Services", "input": "market_demand", "activities": ("service_catalog", "sla", "billing_intent"), "output": "commercial_services", "kpi": "customer_satisfaction"},
        {"id": "VS-09", "name": "Space Sustainability", "input": "debris_and_traffic_data", "activities": ("collision_avoidance", "debris_mitigation", "compliance"), "output": "sustainability_attestation", "kpi": "orbital_collision_risk_reduction"},
        {"id": "VS-10", "name": "Enterprise Governance", "input": "policies_and_events", "activities": ("oversight", "audit", "approval"), "output": "governed_decisions", "kpi": "compliance_score"},
    ),
}
MATURITY_MODEL = {
    "present_required": True,
    "levels": (
        {"level": 1, "name": "enterprise_foundation", "characteristics": ("mission_intelligence", "satellite_operations")},
        {"level": 2, "name": "orbital_intelligence", "characteristics": ("digital_twin", "space_ai")},
        {"level": 3, "name": "autonomous_mission_operations", "characteristics": ("space_robotics", "commercial_space")},
        {"level": 4, "name": "planetary_operations", "characteristics": ("deep_space_intelligence", "space_economy_expansion")},
        {"level": 5, "name": "orbital_civilisation_intelligence", "characteristics": ("planetary_scale_operations", "meos_space_intelligence_core")},
    ),
}
OPERATING_PRINCIPLES = (
    "Mission Safety First", "Autonomous by Default", "Human Supervision Required",
    "Evidence-Based Decisions", "Security by Design", "Data as Strategic Asset",
    "Reusable Services", "API First", "Cloud Native", "Event Driven",
    "Digital Twin First", "Knowledge Graph Native", "Ethics by Design",
    "Continuous Learning", "Continuous Optimisation",
)
STRATEGIC_KPIS = (
    "Mission Success Rate", "Mission Availability", "Satellite Availability", "Telemetry Accuracy",
    "Decision Accuracy", "Autonomous Resolution Rate", "Mean Time to Detect", "Mean Time to Recover",
    "Orbital Collision Risk Reduction", "Mission Planning Time", "Scientific Discovery Velocity",
    "AI Recommendation Acceptance", "Operational Cost Reduction", "Resource Utilisation",
    "Security Incident Rate", "Compliance Score", "Customer Satisfaction", "Innovation Index",
)
STAKEHOLDERS = {
    "internal": ("Mission Command", "Operations", "Engineering", "Research", "Security", "Compliance", "Finance", "Executive Leadership", "Enterprise Architecture", "Data Governance"),
    "external": ("Space Agencies", "Commercial Operators", "Satellite Owners", "Research Institutes", "Universities", "Launch Providers", "Governments", "Defence Organisations", "Regulators", "Partners", "Investors"),
}
GOVERNANCE_STRATEGY = {
    "present_required": True,
    "model": "meos_space_governance_model",
    "domains": ("mission_safety", "space_cybersecurity", "space_sustainability", "autonomy_oversight", "compliance", "ethics"),
    "controls": ("transparency", "human_oversight", "auditability", "zero_trust", "sustainability_gates"),
    "via_policy_engine": True, "via_workflow": True, "via_audit": True,
    "never_opaque_mission_critical_strategy": True,
    "never_ungated_autonomous_mission_strategy": True,
    "never_skip_human_mission_oversight_strategy": True,
    "never_skip_space_cybersecurity_strategy": True,
    "never_skip_space_sustainability_strategy": True,
}
SECURITY_STRATEGY = {
    "present_required": True,
    "framework": "meos_space_strategy_trust_framework",
    "includes": ("space_cybersecurity", "satellite_identity", "mission_authentication", "strategy_access_controls"),
    "via_identity": True, "zero_trust": True,
}
INTEGRATION_STRATEGY = {
    "present_required": True,
    "peers": ("P214-Z", "P215-Z", "P216-Z", "P217", "MEOS Core", "Policy Engine", "Workflow", "Audit", "Integration Platform"),
    "integrations": (
        {"peer": "P214-Z", "provides": ("enterprise_ai_foundation",)},
        {"peer": "P215-Z", "provides": ("quantum_optimisation",)},
        {"peer": "P216-Z", "provides": ("physical_autonomous_systems",)},
        {"peer": "P217", "provides": ("space_biology", "human_life_support", "bio_intelligence")},
        {"peer": "MEOS Core", "provides": ("identity", "security", "events", "workflow", "knowledge_graph", "observability", "governance", "integration", "data_platform")},
    ),
    "via_p214_z": True, "via_p215_z": True, "via_p216_z": True, "via_p217": True,
}
EVOLUTION_ROADMAP = {
    "present_required": True,
    "roadmap": "meos_space_five_year_strategic_roadmap",
    "phases": (
        {"year": 1, "name": "Enterprise Foundation", "foundation": ("mission_intelligence", "satellite_operations")},
        {"year": 2, "name": "Orbital Intelligence", "foundation": ("digital_twin", "space_ai")},
        {"year": 3, "name": "Autonomous Mission Operations", "foundation": ("space_robotics", "commercial_space")},
        {"year": 4, "name": "Planetary Operations", "foundation": ("deep_space_intelligence", "space_economy_expansion")},
        {"year": 5, "name": "Orbital Civilisation Intelligence", "foundation": ("planetary_scale_operations", "meos_space_intelligence_core")},
    ),
}
TARGET_OPERATING_MODEL = (
    "Strategy", "Capabilities", "Business Services", "Applications", "Platforms",
    "Infrastructure", "Space Assets", "Autonomous Operations", "Continuous Intelligence",
)
COMMANDS = ("CreateSpaceStrategyCommand", "DefineSpaceVisionCommand", "AssessSpaceReadinessCommand", "LaunchSpaceInitiativeCommand", "UpdateSpaceRoadmapCommand")
QUERIES = ("GetSpaceMissionQuery", "GetSpaceVisionQuery", "GetStrategicScopeQuery", "GetCapabilityFrameworkQuery", "GetMaturityStatusQuery")
CORE_EVENTS = (
    {"name": "SpaceStrategyCreatedEvent", "owner": "mission_vision", "consumers": "governance,analytics,audit"},
    {"name": "SpaceVisionDefinedEvent", "owner": "mission_vision", "consumers": "strategy,foundation"},
    {"name": "StrategicScopePublishedEvent", "owner": "strategic_scope", "consumers": "capability_framework,roadmap"},
    {"name": "SpaceRoadmapUpdatedEvent", "owner": "integration_evolution", "consumers": "analytics,twin"},
    {"name": "SpaceReadinessImprovedEvent", "owner": "maturity_model", "consumers": "strategy,notifications"},
)
MICROSERVICES = (
    {"id": "space_strategy_service", "bc": "BC-01", "api": "/space/mission", "db": "space_*", "events": ("SpaceStrategyCreatedEvent",), "security": ("space.read",), "scaling": "strategy_replicas"},
    {"id": "space_vision_service", "bc": "BC-01", "api": "/space/mission/vision", "db": "space_*", "events": ("SpaceVisionDefinedEvent",), "security": ("space.read",), "scaling": "vision_replicas"},
    {"id": "capability_framework_service", "bc": "BC-03", "api": "/space/mission/capabilities", "db": "space_*", "events": ("StrategicScopePublishedEvent",), "security": ("space.read",), "scaling": "capability_workers"},
    {"id": "value_streams_service", "bc": "BC-04", "api": "/space/mission/value-streams", "db": "space_*", "events": ("SpaceStrategyCreatedEvent",), "security": ("space.read",), "scaling": "value_replicas"},
    {"id": "maturity_model_service", "bc": "BC-05", "api": "/space/mission/maturity", "db": "space_*", "events": ("SpaceReadinessImprovedEvent",), "security": ("space.read",), "scaling": "maturity_replicas"},
    {"id": "evolution_roadmap_service", "bc": "BC-07", "api": "/space/mission/roadmap", "db": "space_*", "events": ("SpaceRoadmapUpdatedEvent",), "security": ("space.write",), "scaling": "roadmap_workers"},
    {"id": "governance_strategy_service", "bc": "BC-06", "api": "/space/mission/governance", "db": "space_*", "events": ("SpaceStrategyCreatedEvent",), "security": ("space.admin",), "scaling": "governance_replicas"},
    {"id": "integration_strategy_service", "bc": "BC-07", "api": "/space/mission/integration", "db": "space_*", "events": ("SpaceStrategyCreatedEvent",), "security": ("space.admin",), "scaling": "integration_replicas"},
)
QUALITY_GATES_REJECT_IF = (
    "space_mission_framework_is_missing", "space_vision_framework_is_missing",
    "strategic_space_scope_is_missing", "space_capability_framework_is_missing",
    "value_streams_framework_is_missing", "maturity_model_is_missing",
    "governance_framework_is_missing", "meos_integration_strategy_is_missing",
    "future_evolution_roadmap_is_missing", "cqrs_architecture_is_missing",
    "event_architecture_is_missing", "microservices_architecture_is_missing",
    "api_first_architecture_is_missing", "cloud_native_deployment_is_missing",
    "sibling_space_bc", "replace_p218_foundation",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Space Intelligence Strategic Framework",
        "mission": MISSION, "vision": VISION,
        "future_state": list(VISION_FUTURE_STATE),
        "builds_on_p218": True, "builds_on_p217_z": True, "builds_on_p216_z": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "never_replace_p218_foundation": True,
        "foundation_gate": FOUNDATION_GATE, "bio_gate": BIO_GATE,
        "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
    }

def domain_model() -> dict[str, Any]:
    return {"core_domain": CORE_DOMAIN, "supporting_domains": [dict(d) for d in SUPPORTING_DOMAINS], "supporting_count": len(SUPPORTING_DOMAINS)}

def bounded_contexts() -> dict[str, Any]:
    return {"contexts": [dict(c) for c in LOGICAL_BOUNDED_CONTEXTS], "context_count": len(LOGICAL_BOUNDED_CONTEXTS)}

def mission() -> dict[str, Any]:
    return {"present_required": True, "statement": MISSION}

def space_vision() -> dict[str, Any]:
    return {"present_required": True, "statement": VISION, "future_state": list(VISION_FUTURE_STATE)}

def objectives() -> dict[str, Any]:
    return {"present_required": True, "objectives": [dict(o) for o in MISSION_OBJECTIVES], "objective_count": len(MISSION_OBJECTIVES)}

def drivers() -> dict[str, Any]:
    return {"present_required": True, "drivers": [dict(d) for d in BUSINESS_DRIVERS], "driver_count": len(BUSINESS_DRIVERS)}

def strategic_scope() -> dict[str, Any]:
    return dict(STRATEGIC_SCOPE)

def capability_framework() -> dict[str, Any]:
    return dict(CAPABILITY_FRAMEWORK)

def value_streams() -> dict[str, Any]:
    return dict(VALUE_STREAMS) | {"stream_count": len(VALUE_STREAMS["streams"])}

def maturity_model() -> dict[str, Any]:
    return dict(MATURITY_MODEL)

def evolution_roadmap() -> dict[str, Any]:
    return dict(EVOLUTION_ROADMAP) | {"phase_count": len(EVOLUTION_ROADMAP["phases"])}

def governance_strategy() -> dict[str, Any]:
    return dict(GOVERNANCE_STRATEGY)

def security_strategy() -> dict[str, Any]:
    return dict(SECURITY_STRATEGY)

def integration_strategy() -> dict[str, Any]:
    return dict(INTEGRATION_STRATEGY)

def operating_principles() -> dict[str, Any]:
    return {"present_required": True, "principles": list(OPERATING_PRINCIPLES), "principle_count": len(OPERATING_PRINCIPLES)}

def strategic_kpis() -> dict[str, Any]:
    return {"present_required": True, "kpis": list(STRATEGIC_KPIS), "kpi_count": len(STRATEGIC_KPIS)}

def stakeholders() -> dict[str, Any]:
    return {"present_required": True, **{k: list(v) for k, v in STAKEHOLDERS.items()}, "internal_count": len(STAKEHOLDERS["internal"]), "external_count": len(STAKEHOLDERS["external"])}

def target_operating_model() -> dict[str, Any]:
    return {"present_required": True, "layers": list(TARGET_OPERATING_MODEL), "layer_count": len(TARGET_OPERATING_MODEL)}

def cqrs() -> dict[str, Any]:
    return {"commands": list(COMMANDS), "command_count": len(COMMANDS), "queries": list(QUERIES), "query_count": len(QUERIES)}

def events() -> dict[str, Any]:
    return {"core_events": [dict(e) for e in CORE_EVENTS], "core_event_count": len(CORE_EVENTS)}

def microservices() -> dict[str, Any]:
    return {"services": [dict(s) for s in MICROSERVICES], "service_count": len(MICROSERVICES)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p218_b": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "mission_statement": MISSION, "vision_statement": VISION, "principle": MISSION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "bio_gate": BIO_GATE,
        "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P218", "P217-Z", "P216-Z", "P215-Z", "P214-Z", "ADR-526"],
        "vision": vision_pack(), "domain_model": domain_model(), "bounded_contexts": bounded_contexts(),
        "mission": mission(), "space_vision": space_vision(), "objectives": objectives(),
        "drivers": drivers(), "strategic_scope": strategic_scope(),
        "capability_framework": capability_framework(), "value_streams": value_streams(),
        "maturity_model": maturity_model(), "evolution_roadmap": evolution_roadmap(),
        "governance_strategy": governance_strategy(), "security_strategy": security_strategy(),
        "integration_strategy": integration_strategy(),
        "operating_principles": operating_principles(), "strategic_kpis": strategic_kpis(),
        "stakeholders": stakeholders(), "target_operating_model": target_operating_model(),
        "cqrs": cqrs(), "events": events(), "microservices": microservices(),
        "production_readiness": production_readiness(),
        "space_mission_framework_present_required": True,
        "space_vision_framework_present_required": True,
        "strategic_space_scope_present_required": True,
        "space_capability_framework_present_required": True,
        "value_streams_framework_present_required": True,
        "maturity_model_present_required": True,
        "governance_framework_present_required": True,
        "meos_integration_strategy_present_required": True,
        "future_evolution_roadmap_present_required": True,
        "never_replace_p218_foundation": True,
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_replace_p216_z": True,
        "never_replace_biotechnology": True,
        "never_opaque_mission_critical_strategy": True,
        "never_ungated_autonomous_mission_strategy": True,
        "never_skip_human_mission_oversight_strategy": True,
        "never_skip_space_cybersecurity_strategy": True,
        "never_skip_space_sustainability_strategy": True,
        "sibling_space_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/mission",
        "forbidden_sibling_bc": ["space_mission_platform", "space_vision_platform", "space_strategy_platform"],
        "foundation_for_p218_b": True,
    }

def mission_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /space/mission",
        "GET /space/mission/vision",
        "GET /space/mission/objectives",
        "GET /space/mission/scope",
        "GET /space/mission/capabilities",
        "GET /space/mission/value-streams",
        "GET /space/mission/maturity",
        "GET /space/mission/roadmap",
        "GET /space/mission/governance",
        "GET /space/mission/integration",
        "GET /space/mission/readiness",
    ]}
