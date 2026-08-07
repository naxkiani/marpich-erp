"""P218-M Enterprise Space Intelligence Manufacturing Intelligence — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P218-M"
ADR = 539
SOR = "space"
API_PREFIX = "/api/v1/space"
PRODUCT = "Enterprise Space Intelligence Manufacturing Intelligence & MEOS Space Manufacturing Intelligence Platform"
CAPABILITY = "CAP-PLT-SP-001"
MANUFACTURING_MISSION = (
    "Create an autonomous space industrial ecosystem capable of designing, producing, assembling "
    "and maintaining complex products beyond Earth using AI, robotics, digital twins and orbital "
    "manufacturing infrastructure."
)
MANUFACTURING_VISION = (
    "Transform Earth-dependent launch logistics into an explainable, human-supervised, circular "
    "space industrial intelligence fabric spanning orbital factories through interplanetary manufacturing networks."
)
FABRIC = "meos_space_manufacturing_intelligence_fabric"
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
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

ARCHITECTURE_LAYERS = (
    {"id": "L01", "name": "Space Industrial Infrastructure Layer", "components": ("orbital_factories", "manufacturing_modules", "energy", "storage")},
    {"id": "L02", "name": "Production Intelligence Layer", "components": ("production_planning_ai", "quality_intelligence", "material_intelligence", "resource_allocation")},
    {"id": "L03", "name": "Manufacturing Execution Layer", "components": ("mes", "scheduler", "robot_orchestration", "inventory")},
    {"id": "L04", "name": "Autonomous Factory Layer", "components": ("factory_ai", "production_agents", "maintenance_agents", "inspection_agents")},
    {"id": "L05", "name": "Space Economy Layer", "components": ("marketplace", "industrial_network", "contracts", "supply_chain")},
)
LIFECYCLE_STAGES = (
    "factory_design", "factory_commissioning", "production_planning", "material_allocation",
    "manufacturing_execution", "quality_validation", "maintenance", "product_delivery",
    "factory_expansion", "decommissioning",
)
IN_ORBIT = {
    "present_required": True,
    "platform": "meos_in_orbit_manufacturing_platform",
    "capabilities": (
        "orbital_assembly", "additive_manufacturing", "materials_processing", "satellite_manufacturing",
        "large_structure_construction", "repair_operations", "component_replacement", "space_based_production",
    ),
    "categories": (
        "metal", "composites", "electronics", "optics", "space_structures",
        "scientific_instruments", "energy_systems", "habitat_components",
    ),
}
INDUSTRIAL = {
    "present_required": True,
    "platform": "meos_orbital_industrial_systems_platform",
    "infrastructure": (
        "orbital_factory", "manufacturing_hub", "assembly_platform", "robotic_service_station",
        "energy_platform", "material_depot", "logistics_interface",
    ),
    "capabilities": (
        "factory_scheduling", "production_coordination", "resource_planning", "industrial_automation",
        "quality_management", "asset_lifecycle", "factory_expansion_planning",
    ),
}
AUTONOMY = {
    "present_required": True,
    "platform": "meos_autonomous_space_production_platform",
    "functions": (
        "production_planning", "material_selection", "manufacturing_execution", "quality_inspection",
        "maintenance_scheduling", "failure_recovery", "resource_optimization", "factory_self_improvement",
    ),
    "agents": (
        "production_manager", "factory_operations", "robotics", "quality",
        "maintenance", "supply_chain", "safety", "optimization",
    ),
    "via_p216_z": True,
    "never_ungated_autonomous_factory_production": True,
    "never_disable_human_override": True,
}
MANUFACTURING_AI = {
    "present_required": True,
    "platform": "meos_space_manufacturing_ai_platform",
    "capabilities": (
        "production_optimization", "material_discovery", "process_optimization", "defect_detection",
        "predictive_maintenance", "resource_forecasting", "factory_scheduling", "manufacturing_simulation",
        "cost_optimization", "quality_prediction",
    ),
    "models": (
        {"id": "MODEL-01", "name": "Space Manufacturing Foundation Model"},
        {"id": "MODEL-02", "name": "Industrial Process Model"},
        {"id": "MODEL-03", "name": "Material Intelligence Model"},
        {"id": "MODEL-04", "name": "Production Optimization Model"},
        {"id": "MODEL-05", "name": "Quality Prediction Model"},
        {"id": "MODEL-06", "name": "Factory Autonomy Model"},
    ),
    "via_p214_z": True,
    "via_p218_e": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
}
MATERIALS = {
    "present_required": True,
    "platform": "meos_space_material_intelligence_platform",
    "domains": (
        "advanced_alloys", "composites", "semiconductors", "optical_materials",
        "biological_materials", "construction_materials", "energy_materials",
    ),
    "capabilities": (
        "material_discovery", "material_simulation", "manufacturing_compatibility",
        "performance_prediction", "environmental_analysis", "lifecycle_optimization",
    ),
    "via_p215_z": True,
    "via_p218_k": True,
}
ROBOTICS = {
    "present_required": True,
    "platform": "meos_space_industrial_robotics_platform",
    "systems": (
        "assembly_robots", "maintenance_robots", "inspection_robots", "mining_robots",
        "construction_robots", "microgravity_robots", "autonomous_manipulators",
    ),
    "capabilities": (
        "precision_assembly", "remote_operations", "self_calibration",
        "collaborative_robotics", "autonomous_repair", "safety_monitoring",
    ),
    "via_p216_z": True,
}
DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_space_manufacturing_digital_twin",
    "represents": ("orbital_factory", "production_lines", "robots", "materials", "products", "inventory", "energy_systems", "supply_chains", "processes"),
    "capabilities": ("factory_simulation", "production_forecasting", "failure_simulation", "process_optimization", "quality_prediction", "expansion_planning", "lifecycle_management"),
}
KNOWLEDGE_GRAPH = {
    "present_required": True,
    "platform": "meos_space_industrial_knowledge_graph",
    "entities": ("factory", "production_line", "robot", "material", "product", "process", "supplier", "resource", "mission", "customer"),
    "relationships": (
        "FACTORY_PRODUCES_PRODUCT", "ROBOT_OPERATES_PROCESS", "MATERIAL_USED_IN_PROCESS",
        "PRODUCT_DEPENDS_ON_RESOURCE", "FACTORY_SUPPORTS_MISSION", "PROCESS_OPTIMIZED_BY_AI",
    ),
    "capabilities": ("industrial_reasoning", "manufacturing_intelligence", "resource_optimization", "production_discovery", "supply_chain_intelligence"),
}
GOVERNANCE = {
    "present_required": True,
    "domains": (
        "production_governance", "quality_governance", "resource_governance",
        "safety_governance", "commercial_governance", "ip_protection",
        "industrial_network_security", "circular_economy",
    ),
    "approval_gates": (
        "factory_commissioning", "industrial_safety_certification", "production_authorization",
        "quality_validation", "product_release", "factory_expansion", "decommissioning",
    ),
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "never_ungated_autonomous_factory_production": True,
    "never_skip_quality_validation": True,
    "never_skip_industrial_safety_certification": True,
    "never_violate_circular_space_economy_principles": True,
}
OBSERVABILITY = {
    "present_required": True,
    "dashboards": (
        "factory_status", "production_throughput", "quality", "robot_fleet",
        "material_inventory", "energy", "supply_chain", "manufacturing_ai",
    ),
    "kpis": (
        "production_yield", "defect_rate", "factory_utilization", "autonomous_completion_rate",
        "material_efficiency", "energy_efficiency", "maintenance_mttr",
        "quality_pass_rate", "circular_reuse_rate", "delivery_on_time",
    ),
}
BOUNDED_CONTEXTS = (
    {"id": "BC-MFG-01", "name": "Space Manufacturing Management"},
    {"id": "BC-MFG-02", "name": "Factory Operations"},
    {"id": "BC-MFG-03", "name": "Production Planning"},
    {"id": "BC-MFG-04", "name": "Material Management"},
    {"id": "BC-MFG-05", "name": "Robotics Operations"},
    {"id": "BC-MFG-06", "name": "Quality Management"},
    {"id": "BC-MFG-07", "name": "Industrial Supply Chain"},
    {"id": "BC-MFG-08", "name": "Manufacturing Governance"},
)
SECURITY = {
    "present_required": True,
    "controls": (
        "zero_trust_industrial", "factory_security", "robot_security", "production_data_security",
        "supply_chain_security", "ip_protection", "human_override", "industrial_compliance",
    ),
    "via_identity": True, "via_policy_engine": True, "via_workflow": True,
    "via_audit": True, "via_integration": True,
    "never_ungated_autonomous_factory_production": True,
    "never_skip_quality_validation": True,
    "never_skip_industrial_safety_certification": True,
    "never_violate_circular_space_economy_principles": True,
    "never_replace_p218_l_exploration": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
}
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p218_foundation", "p218a_mission", "p218b_strategy", "p218c_domain",
        "p218d_infrastructure", "p218e_space_ai", "p218f_satellite", "p218g_orbital",
        "p218h_communications", "p218i_navigation", "p218j_mission_intel", "p218k_scientific",
        "p218l_exploration", "p217z_bio_nexus", "p216z_robotics_supreme",
        "p215z_quantum_supreme", "p214z_ai_master",
        "policy_engine", "workflow", "audit", "identity", "integration_platform",
        "knowledge_graph", "digital_twin",
    ),
    "mechanisms": ("api_gateway", "event_bus", "acl_peer_ids_only", "outbox", "versioned_contracts"),
}
DEPLOYMENT = {
    "present_required": True,
    "environments": ("factory_design", "factory_simulation", "orbital_production", "manufacturing_archive"),
    "cloud_native": True,
    "safety_critical": True,
    "circular_space_economy": True,
}
COMMANDS = (
    "CreateSpaceFactoryCommand", "StartProductionOrderCommand", "AllocateMaterialCommand",
    "AssignRobotCommand", "ValidateQualityCommand", "ScheduleMaintenanceCommand",
    "DeliverProductCommand", "ExpandFactoryCommand",
)
QUERIES = (
    "GetSpaceFactoryQuery", "GetProductionOrderQuery", "GetMaterialInventoryQuery",
    "GetRobotFleetQuery", "GetQualityReportQuery", "GetFactoryCapacityQuery",
)
CORE_EVENTS = (
    {"name": "FactoryCreatedEvent", "schema": "space.manufacturing.factory.created.v1", "owner": "BC-MFG-01"},
    {"name": "ProductionStartedEvent", "schema": "space.manufacturing.production.started.v1", "owner": "BC-MFG-03"},
    {"name": "MaterialAllocatedEvent", "schema": "space.manufacturing.material.allocated.v1", "owner": "BC-MFG-04"},
    {"name": "RobotAssignedEvent", "schema": "space.manufacturing.robot.assigned.v1", "owner": "BC-MFG-05"},
    {"name": "ManufacturingCompletedEvent", "schema": "space.manufacturing.manufacturing.completed.v1", "owner": "BC-MFG-02"},
    {"name": "QualityValidatedEvent", "schema": "space.manufacturing.quality.validated.v1", "owner": "BC-MFG-06"},
    {"name": "DefectDetectedEvent", "schema": "space.manufacturing.defect.detected.v1", "owner": "BC-MFG-06"},
    {"name": "MaintenanceScheduledEvent", "schema": "space.manufacturing.maintenance.scheduled.v1", "owner": "BC-MFG-02"},
    {"name": "ProductDeliveredEvent", "schema": "space.manufacturing.product.delivered.v1", "owner": "BC-MFG-07"},
    {"name": "FactoryExpandedEvent", "schema": "space.manufacturing.factory.expanded.v1", "owner": "BC-MFG-01"},
)
MICROSERVICES = (
    {"id": "manufacturing_intel_service", "api": "/space/manufacturing", "events": ("FactoryCreatedEvent",)},
    {"id": "in_orbit_service", "api": "/space/manufacturing/in-orbit", "events": ("ProductionStartedEvent",)},
    {"id": "industrial_service", "api": "/space/manufacturing/industrial", "events": ("FactoryExpandedEvent",)},
    {"id": "autonomy_service", "api": "/space/manufacturing/autonomy", "events": ("RobotAssignedEvent",)},
    {"id": "manufacturing_ai_service", "api": "/space/manufacturing/manufacturing-ai", "events": ("DefectDetectedEvent",)},
    {"id": "materials_service", "api": "/space/manufacturing/materials", "events": ("MaterialAllocatedEvent",)},
    {"id": "manufacturing_twin_service", "api": "/space/manufacturing/digital-twin", "events": ("ManufacturingCompletedEvent",)},
    {"id": "manufacturing_observability_service", "api": "/space/manufacturing/observability", "events": ("ProductDeliveredEvent",)},
    {"id": "manufacturing_governance_service", "api": "/space/manufacturing/governance", "events": ("QualityValidatedEvent",)},
    {"id": "manufacturing_security_service", "api": "/space/manufacturing/security", "events": ("MaintenanceScheduledEvent",)},
)
TESTING = (
    "manufacturing_lifecycle_testing", "in_orbit_production_testing", "industrial_systems_testing",
    "autonomy_override_testing", "manufacturing_ai_explainability_testing", "robotics_integration_testing",
    "quality_validation_gate_testing", "industrial_safety_gate_testing",
)
ROADMAP_PHASES = (
    {"phase": 1, "name": "Space Manufacturing Foundation"},
    {"phase": 2, "name": "Orbital Factory Operations"},
    {"phase": 3, "name": "Autonomous Space Industry"},
    {"phase": 4, "name": "Orbital Civilization Industry"},
)
QUALITY_GATES_REJECT_IF = (
    "space_manufacturing_platform_is_missing", "in_orbit_manufacturing_is_missing",
    "orbital_industrial_systems_is_missing", "autonomous_production_is_missing",
    "manufacturing_ai_is_missing", "space_robotics_integration_is_missing",
    "digital_twin_is_missing", "industrial_knowledge_graph_is_missing",
    "security_is_missing", "observability_is_missing",
    "ungated_autonomous_factory_production", "skip_quality_validation",
    "skip_industrial_safety_certification", "violate_circular_space_economy_principles",
    "replace_p218_l_exploration", "module_local_llm", "sibling_space_bc",
)


def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Space Manufacturing Intelligence Fabric", "mission": MANUFACTURING_MISSION,
        "vision": MANUFACTURING_VISION, "builds_on_p218": True,
        **{f"builds_on_p218_{x.lower()}": True for x in "ABCDEFGHIJKL"},
        "builds_on_p217_z": True, "builds_on_p216_z": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "never_replace_p218_l_exploration": True,
        "never_ungated_autonomous_factory_production": True,
        "never_skip_quality_validation": True,
        "never_skip_industrial_safety_certification": True,
        "never_violate_circular_space_economy_principles": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
    }


def architecture() -> dict[str, Any]:
    return {"present_required": True, "layers": [dict(x) for x in ARCHITECTURE_LAYERS], "layer_count": len(ARCHITECTURE_LAYERS)}


def lifecycle() -> dict[str, Any]:
    return {
        "present_required": True, "stages": list(LIFECYCLE_STAGES), "stage_count": len(LIFECYCLE_STAGES),
        "quality_validation_required": True, "industrial_safety_certification_required": True,
        "autonomous_factory_production_gated": True, "circular_space_economy": True,
    }


def in_orbit() -> dict[str, Any]:
    return dict(IN_ORBIT) | {"capability_count": len(IN_ORBIT["capabilities"]), "category_count": len(IN_ORBIT["categories"])}


def industrial() -> dict[str, Any]:
    return dict(INDUSTRIAL) | {"infrastructure_count": len(INDUSTRIAL["infrastructure"]), "capability_count": len(INDUSTRIAL["capabilities"])}


def autonomy() -> dict[str, Any]:
    return dict(AUTONOMY) | {"function_count": len(AUTONOMY["functions"]), "agent_count": len(AUTONOMY["agents"])}


def manufacturing_ai() -> dict[str, Any]:
    return dict(MANUFACTURING_AI) | {"capability_count": len(MANUFACTURING_AI["capabilities"]), "model_count": len(MANUFACTURING_AI["models"])}


def materials() -> dict[str, Any]:
    return dict(MATERIALS) | {"domain_count": len(MATERIALS["domains"]), "capability_count": len(MATERIALS["capabilities"])}


def robotics() -> dict[str, Any]:
    return dict(ROBOTICS) | {"system_count": len(ROBOTICS["systems"]), "capability_count": len(ROBOTICS["capabilities"])}


def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN) | {"representation_count": len(DIGITAL_TWIN["represents"]), "capability_count": len(DIGITAL_TWIN["capabilities"])}


def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH) | {"entity_count": len(KNOWLEDGE_GRAPH["entities"]), "relationship_count": len(KNOWLEDGE_GRAPH["relationships"]), "capability_count": len(KNOWLEDGE_GRAPH["capabilities"])}


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
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p218_n": True}


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT,
        "capability": CAPABILITY, "manufacturing_mission": MANUFACTURING_MISSION,
        "manufacturing_vision": MANUFACTURING_VISION, "principle": MANUFACTURING_MISSION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "infrastructure_gate": INFRASTRUCTURE_GATE, "space_ai_gate": SPACE_AI_GATE,
        "satellite_gate": SATELLITE_GATE, "orbital_gate": ORBITAL_GATE,
        "communications_gate": COMMUNICATIONS_GATE, "navigation_gate": NAVIGATION_GATE,
        "mission_intel_gate": MISSION_INTEL_GATE, "scientific_gate": SCIENTIFIC_GATE,
        "exploration_gate": EXPLORATION_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P218"] + [f"P218-{x}" for x in "ABCDEFGHIJKL"] + ["P217-Z", "P216-Z", "P215-Z", "P214-Z"] + [f"ADR-{i}" for i in range(526, 539)],
        "vision": vision_pack(), "architecture": architecture(), "lifecycle": lifecycle(),
        "in_orbit": in_orbit(), "industrial": industrial(), "autonomy": autonomy(),
        "manufacturing_ai": manufacturing_ai(), "materials": materials(), "robotics": robotics(),
        "digital_twin": digital_twin(), "knowledge_graph": knowledge_graph(),
        "governance": governance(), "observability": observability(), "security": security(),
        "bounded_contexts": bounded_contexts(), "integration": integration(),
        "deployment": deployment(), "cqrs": cqrs(), "events": events(),
        "microservices": microservices(), "testing": testing(), "roadmap": roadmap(),
        "quality_gates": quality_gates(), "production_readiness": production_readiness(),
        "space_manufacturing_platform_present_required": True,
        "in_orbit_manufacturing_present_required": True,
        "orbital_industrial_systems_present_required": True,
        "autonomous_production_present_required": True,
        "manufacturing_ai_present_required": True,
        "space_robotics_integration_present_required": True,
        "digital_twin_present_required": True,
        "industrial_knowledge_graph_present_required": True,
        "ddd_model_present_required": True, "security_present_required": True,
        "observability_present_required": True,
        "deployment_architecture_present_required": True, "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True, "microservices_architecture_present_required": True,
        "sibling_space_bc_forbidden": True,
        "never_replace_p218_l_exploration": True,
        "never_ungated_autonomous_factory_production": True,
        "never_skip_quality_validation": True,
        "never_skip_industrial_safety_certification": True,
        "never_violate_circular_space_economy_principles": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
        "api_prefix": f"{API_PREFIX}/manufacturing",
        "forbidden_sibling_bc": ["space_manufacturing_platform", "orbital_factory_bc", "in_orbit_manufacturing_bc"],
        "foundation_for_p218_n": True,
    }


def manufacturing_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /space/manufacturing", "GET /space/manufacturing/vision",
        "GET /space/manufacturing/architecture", "GET /space/manufacturing/lifecycle",
        "GET /space/manufacturing/in-orbit", "GET /space/manufacturing/industrial",
        "GET /space/manufacturing/autonomy", "GET /space/manufacturing/manufacturing-ai",
        "GET /space/manufacturing/materials", "GET /space/manufacturing/robotics",
        "GET /space/manufacturing/digital-twin", "GET /space/manufacturing/knowledge-graph",
        "GET /space/manufacturing/observability", "GET /space/manufacturing/governance",
        "GET /space/manufacturing/security", "GET /space/manufacturing/integration",
        "GET /space/manufacturing/deployment", "GET /space/manufacturing/testing",
        "GET /space/manufacturing/cqrs", "GET /space/manufacturing/events",
        "GET /space/manufacturing/readiness",
    ]}
