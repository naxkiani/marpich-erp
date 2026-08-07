"""P218-O Enterprise Space Intelligence Logistics Intelligence — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P218-O"
ADR = 541
SOR = "space"
API_PREFIX = "/api/v1/space"
PRODUCT = "Enterprise Space Intelligence Logistics Intelligence & MEOS Space Logistics Intelligence Platform"
CAPABILITY = "CAP-PLT-SP-001"
LOGISTICS_MISSION = (
    "Create an autonomous logistics intelligence ecosystem capable of transporting, managing and "
    "optimizing resources, equipment, cargo and personnel across Earth orbit, lunar infrastructure, "
    "Mars operations and future interplanetary civilization networks."
)
LOGISTICS_VISION = (
    "Transform fragmented orbital freights into an explainable, human-supervised, zero-trust logistics "
    "intelligence fabric spanning autonomous cargo, orbital supply chains and interplanetary transportation corridors."
)
FABRIC = "meos_space_logistics_intelligence_fabric"
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
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

ARCHITECTURE_LAYERS = (
    {"id": "L01", "name": "Space Transportation Layer", "components": ("cargo_spacecraft", "transfer_vehicles", "freighters", "robotic_delivery")},
    {"id": "L02", "name": "Logistics Network Layer", "components": ("orbital_network", "lunar_network", "mars_network", "distribution_nodes")},
    {"id": "L03", "name": "Logistics Intelligence Layer", "components": ("ai_planner", "route_optimization", "demand_forecasting", "risk_prediction")},
    {"id": "L04", "name": "Autonomous Operations Layer", "components": ("cargo_agents", "fleet_agents", "warehouse_agents", "emergency_agents")},
    {"id": "L05", "name": "Economic Logistics Layer", "components": ("freight_marketplace", "contracts", "pricing", "commercial_services")},
)
LIFECYCLE_STAGES = (
    "cargo_registration", "cargo_authentication", "allocation", "route_planning",
    "launch_authorization", "transport", "in_transit_monitoring", "delivery",
    "inventory_update", "mission_closure",
)
CARGO = {
    "present_required": True,
    "platform": "meos_autonomous_cargo_systems_platform",
    "capabilities": (
        "autonomous_loading", "autonomous_unloading", "cargo_tracking", "cargo_prioritization",
        "route_selection", "delivery_verification", "condition_monitoring", "failure_recovery",
    ),
    "cargo_types": (
        "scientific_equipment", "construction_materials", "life_support", "fuel", "water",
        "industrial_components", "manufacturing_materials", "crew_supplies", "robotic_assets",
    ),
}
SUPPLY_CHAIN = {
    "present_required": True,
    "platform": "meos_orbital_supply_chain_platform",
    "domains": (
        "earth_to_orbit", "orbit_to_orbit", "orbital_manufacturing_supply",
        "lunar_supply", "mars_supply", "deep_space_supply",
    ),
    "capabilities": (
        "demand_prediction", "inventory_management", "warehouse_automation", "cargo_scheduling",
        "supply_optimization", "resource_allocation", "supplier_intelligence", "real_time_visibility",
        "predictive_analytics", "autonomous_procurement", "dynamic_routing", "risk_management",
    ),
}
INTERPLANETARY = {
    "present_required": True,
    "platform": "meos_interplanetary_transportation_platform",
    "domains": (
        "earth_moon", "earth_mars", "planetary_transfer", "asteroid_transport", "deep_space_cargo",
    ),
    "capabilities": (
        "trajectory_logistics", "launch_window_optimization", "transfer_planning", "fuel_optimization",
        "cargo_scheduling", "mission_synchronization", "transport_risk_management", "transfer_simulation",
        "route_forecasting", "delay_prediction", "resource_optimization", "mission_coordination",
    ),
}
LOGISTICS_AI = {
    "present_required": True,
    "platform": "meos_space_logistics_ai_platform",
    "capabilities": (
        "demand_forecasting", "route_optimization", "fleet_optimization", "cargo_prioritization",
        "supply_chain_prediction", "failure_prediction", "autonomous_scheduling", "economic_optimization",
    ),
    "models": (
        {"id": "MODEL-01", "name": "Space Logistics Foundation Model"},
        {"id": "MODEL-02", "name": "Transportation Intelligence Model"},
        {"id": "MODEL-03", "name": "Supply Chain Prediction Model"},
        {"id": "MODEL-04", "name": "Cargo Optimization Model"},
        {"id": "MODEL-05", "name": "Fleet Management Model"},
        {"id": "MODEL-06", "name": "Economic Forecasting Model"},
    ),
    "via_p214_z": True,
    "via_p218_e": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
}
ROBOTICS = {
    "present_required": True,
    "platform": "meos_space_logistics_robotics_platform",
    "systems": (
        "cargo_handling", "orbital_warehouse", "docking", "inspection", "maintenance", "surface_logistics",
    ),
    "capabilities": (
        "autonomous_handling", "cargo_transfer", "inventory_management",
        "docking_operations", "asset_inspection", "maintenance_support",
    ),
    "via_p216_z": True,
}
DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_space_logistics_digital_twin",
    "represents": ("cargo_networks", "transport_vehicles", "supply_chains", "warehouses", "spaceports", "orbital_stations", "planetary_bases", "resource_flows"),
    "capabilities": ("logistics_simulation", "route_optimization", "supply_forecasting", "failure_simulation", "capacity_planning", "emergency_scenario_testing", "economic_analysis"),
}
KNOWLEDGE_GRAPH = {
    "present_required": True,
    "platform": "meos_space_logistics_knowledge_graph",
    "entities": ("cargo", "vehicle", "route", "warehouse", "supply_node", "mission", "resource", "supplier", "customer", "transportation_contract"),
    "relationships": (
        "CARGO_TRANSPORTED_BY", "VEHICLE_SERVES_ROUTE", "RESOURCE_STORED_IN",
        "SUPPLY_NODE_CONNECTS", "MISSION_REQUIRES", "CONTRACT_SUPPORTS",
    ),
    "capabilities": ("supply_chain_reasoning", "route_intelligence", "resource_prediction", "logistics_optimization", "economic_intelligence"),
}
GOVERNANCE = {
    "present_required": True,
    "domains": (
        "transportation_governance", "resource_governance", "commercial_governance",
        "safety_governance", "supply_chain_governance", "cargo_security",
        "fleet_security", "communication_security",
    ),
    "approval_gates": (
        "cargo_authentication", "launch_authorization", "route_approval",
        "delivery_verification", "emergency_route_activation", "contract_approval", "mission_closure",
    ),
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "never_ungated_cargo_launch_authorization": True,
    "never_skip_cargo_authentication": True,
    "never_skip_supply_chain_security_controls": True,
    "never_ungated_emergency_route_activation": True,
}
OBSERVABILITY = {
    "present_required": True,
    "dashboards": (
        "fleet_status", "cargo_tracking", "supply_chain_visibility", "route_performance",
        "warehouse_inventory", "interplanetary_transfers", "logistics_ai", "freight_marketplace",
    ),
    "kpis": (
        "on_time_delivery_rate", "cargo_integrity_rate", "fleet_utilization", "route_efficiency",
        "supply_chain_resilience", "autonomous_completion_rate", "fuel_efficiency",
        "emergency_reroute_latency", "inventory_accuracy", "commercial_throughput",
    ),
}
BOUNDED_CONTEXTS = (
    {"id": "BC-LOG-01", "name": "Logistics Management"},
    {"id": "BC-LOG-02", "name": "Cargo Operations"},
    {"id": "BC-LOG-03", "name": "Transportation Management"},
    {"id": "BC-LOG-04", "name": "Supply Chain Management"},
    {"id": "BC-LOG-05", "name": "Fleet Logistics"},
    {"id": "BC-LOG-06", "name": "Warehouse Operations"},
    {"id": "BC-LOG-07", "name": "Resource Distribution"},
    {"id": "BC-LOG-08", "name": "Logistics Governance"},
)
SECURITY = {
    "present_required": True,
    "controls": (
        "zero_trust_logistics", "cargo_authentication", "secure_tracking", "encrypted_data_exchange",
        "identity_management", "audit_trail", "human_override", "supply_chain_security",
    ),
    "via_identity": True, "via_policy_engine": True, "via_workflow": True,
    "via_audit": True, "via_integration": True,
    "never_ungated_cargo_launch_authorization": True,
    "never_skip_cargo_authentication": True,
    "never_skip_supply_chain_security_controls": True,
    "never_ungated_emergency_route_activation": True,
    "never_replace_p218_n_resources": True,
    "space_ai_via_p214z_acl_only": True,
    "no_module_local_llm": True,
}
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p218_foundation", "p218a_mission", "p218b_strategy", "p218c_domain",
        "p218d_infrastructure", "p218e_space_ai", "p218f_satellite", "p218g_orbital",
        "p218h_communications", "p218i_navigation", "p218j_mission_intel", "p218k_scientific",
        "p218l_exploration", "p218m_manufacturing", "p218n_resources",
        "p217z_bio_nexus", "p216z_robotics_supreme", "p215z_quantum_supreme", "p214z_ai_master",
        "policy_engine", "workflow", "audit", "identity", "integration_platform",
        "knowledge_graph", "digital_twin",
    ),
    "mechanisms": ("api_gateway", "event_bus", "acl_peer_ids_only", "outbox", "versioned_contracts"),
}
DEPLOYMENT = {
    "present_required": True,
    "environments": ("logistics_planning", "transport_simulation", "orbital_operations", "logistics_archive"),
    "cloud_native": True,
    "safety_critical": True,
}
COMMANDS = (
    "CreateCargoCommand", "AuthenticateCargoCommand", "AllocateCargoCommand",
    "AuthorizeCargoLaunchCommand", "ScheduleTransportCommand", "OptimizeRouteCommand",
    "ActivateEmergencyRouteCommand", "ConfirmDeliveryCommand",
)
QUERIES = (
    "GetCargoShipmentQuery", "GetTransportVehicleQuery", "GetLogisticsRouteQuery",
    "GetWarehouseQuery", "GetSupplyChainQuery", "GetFleetStatusQuery",
)
CORE_EVENTS = (
    {"name": "CargoCreatedEvent", "schema": "space.logistics.cargo.created.v1", "owner": "BC-LOG-02"},
    {"name": "CargoAllocatedEvent", "schema": "space.logistics.cargo.allocated.v1", "owner": "BC-LOG-02"},
    {"name": "TransportScheduledEvent", "schema": "space.logistics.transport.scheduled.v1", "owner": "BC-LOG-03"},
    {"name": "RouteOptimizedEvent", "schema": "space.logistics.route.optimized.v1", "owner": "BC-LOG-03"},
    {"name": "ShipmentLaunchedEvent", "schema": "space.logistics.shipment.launched.v1", "owner": "BC-LOG-03"},
    {"name": "CargoDeliveredEvent", "schema": "space.logistics.cargo.delivered.v1", "owner": "BC-LOG-02"},
    {"name": "SupplyChainDisruptedEvent", "schema": "space.logistics.supply_chain.disrupted.v1", "owner": "BC-LOG-04"},
    {"name": "EmergencyRouteActivatedEvent", "schema": "space.logistics.emergency.route.activated.v1", "owner": "BC-LOG-08"},
    {"name": "InventoryUpdatedEvent", "schema": "space.logistics.inventory.updated.v1", "owner": "BC-LOG-06"},
    {"name": "LogisticsMissionCompletedEvent", "schema": "space.logistics.mission.completed.v1", "owner": "BC-LOG-01"},
)
MICROSERVICES = (
    {"id": "logistics_intel_service", "api": "/space/logistics", "events": ("CargoCreatedEvent",)},
    {"id": "cargo_service", "api": "/space/logistics/cargo", "events": ("CargoDeliveredEvent",)},
    {"id": "supply_chain_service", "api": "/space/logistics/supply-chain", "events": ("SupplyChainDisruptedEvent",)},
    {"id": "interplanetary_service", "api": "/space/logistics/interplanetary", "events": ("ShipmentLaunchedEvent",)},
    {"id": "logistics_ai_service", "api": "/space/logistics/logistics-ai", "events": ("RouteOptimizedEvent",)},
    {"id": "logistics_robotics_service", "api": "/space/logistics/robotics", "events": ("InventoryUpdatedEvent",)},
    {"id": "logistics_twin_service", "api": "/space/logistics/digital-twin", "events": ("TransportScheduledEvent",)},
    {"id": "logistics_observability_service", "api": "/space/logistics/observability", "events": ("LogisticsMissionCompletedEvent",)},
    {"id": "logistics_governance_service", "api": "/space/logistics/governance", "events": ("EmergencyRouteActivatedEvent",)},
    {"id": "logistics_security_service", "api": "/space/logistics/security", "events": ("CargoAllocatedEvent",)},
)
TESTING = (
    "logistics_lifecycle_testing", "cargo_authentication_testing", "supply_chain_visibility_testing",
    "interplanetary_transfer_testing", "logistics_ai_explainability_testing", "robotics_integration_testing",
    "cargo_launch_authorization_gate_testing", "emergency_route_gate_testing",
)
ROADMAP_PHASES = (
    {"phase": 1, "name": "Space Logistics Foundation"},
    {"phase": 2, "name": "Autonomous Logistics"},
    {"phase": 3, "name": "Interplanetary Logistics"},
    {"phase": 4, "name": "Space Civilization Logistics Network"},
)
QUALITY_GATES_REJECT_IF = (
    "space_logistics_platform_is_missing", "autonomous_cargo_systems_is_missing",
    "orbital_supply_chain_is_missing", "interplanetary_transportation_is_missing",
    "logistics_ai_is_missing", "robotics_integration_is_missing",
    "digital_twin_is_missing", "knowledge_graph_is_missing",
    "governance_is_missing", "security_architecture_is_missing",
    "ungated_cargo_launch_authorization", "skip_cargo_authentication",
    "skip_supply_chain_security_controls", "ungated_emergency_route_activation",
    "replace_p218_n_resources", "module_local_llm", "sibling_space_bc",
)


def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Space Logistics Intelligence Fabric", "mission": LOGISTICS_MISSION,
        "vision": LOGISTICS_VISION, "builds_on_p218": True,
        **{f"builds_on_p218_{x.lower()}": True for x in "ABCDEFGHIJKLMN"},
        "builds_on_p217_z": True, "builds_on_p216_z": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "never_replace_p218_n_resources": True,
        "never_ungated_cargo_launch_authorization": True,
        "never_skip_cargo_authentication": True,
        "never_skip_supply_chain_security_controls": True,
        "never_ungated_emergency_route_activation": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
    }


def architecture() -> dict[str, Any]:
    return {"present_required": True, "layers": [dict(x) for x in ARCHITECTURE_LAYERS], "layer_count": len(ARCHITECTURE_LAYERS)}


def lifecycle() -> dict[str, Any]:
    return {
        "present_required": True, "stages": list(LIFECYCLE_STAGES), "stage_count": len(LIFECYCLE_STAGES),
        "cargo_launch_authorization_gated": True, "cargo_authentication_required": True,
        "supply_chain_security_required": True, "emergency_route_activation_gated": True,
    }


def cargo() -> dict[str, Any]:
    return dict(CARGO) | {"capability_count": len(CARGO["capabilities"]), "cargo_type_count": len(CARGO["cargo_types"])}


def supply_chain() -> dict[str, Any]:
    return dict(SUPPLY_CHAIN) | {"domain_count": len(SUPPLY_CHAIN["domains"]), "capability_count": len(SUPPLY_CHAIN["capabilities"])}


def interplanetary() -> dict[str, Any]:
    return dict(INTERPLANETARY) | {"domain_count": len(INTERPLANETARY["domains"]), "capability_count": len(INTERPLANETARY["capabilities"])}


def logistics_ai() -> dict[str, Any]:
    return dict(LOGISTICS_AI) | {"capability_count": len(LOGISTICS_AI["capabilities"]), "model_count": len(LOGISTICS_AI["models"])}


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
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p218_p": True}


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT,
        "capability": CAPABILITY, "logistics_mission": LOGISTICS_MISSION,
        "logistics_vision": LOGISTICS_VISION, "principle": LOGISTICS_MISSION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "infrastructure_gate": INFRASTRUCTURE_GATE, "space_ai_gate": SPACE_AI_GATE,
        "satellite_gate": SATELLITE_GATE, "orbital_gate": ORBITAL_GATE,
        "communications_gate": COMMUNICATIONS_GATE, "navigation_gate": NAVIGATION_GATE,
        "mission_intel_gate": MISSION_INTEL_GATE, "scientific_gate": SCIENTIFIC_GATE,
        "exploration_gate": EXPLORATION_GATE, "manufacturing_gate": MANUFACTURING_GATE,
        "resources_gate": RESOURCES_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P218"] + [f"P218-{x}" for x in "ABCDEFGHIJKLMN"] + ["P217-Z", "P216-Z", "P215-Z", "P214-Z"] + [f"ADR-{i}" for i in range(526, 541)],
        "vision": vision_pack(), "architecture": architecture(), "lifecycle": lifecycle(),
        "cargo": cargo(), "supply_chain": supply_chain(), "interplanetary": interplanetary(),
        "logistics_ai": logistics_ai(), "robotics": robotics(),
        "digital_twin": digital_twin(), "knowledge_graph": knowledge_graph(),
        "governance": governance(), "observability": observability(), "security": security(),
        "bounded_contexts": bounded_contexts(), "integration": integration(),
        "deployment": deployment(), "cqrs": cqrs(), "events": events(),
        "microservices": microservices(), "testing": testing(), "roadmap": roadmap(),
        "quality_gates": quality_gates(), "production_readiness": production_readiness(),
        "space_logistics_platform_present_required": True,
        "autonomous_cargo_systems_present_required": True,
        "orbital_supply_chain_present_required": True,
        "interplanetary_transportation_present_required": True,
        "logistics_ai_present_required": True,
        "robotics_integration_present_required": True,
        "digital_twin_present_required": True,
        "knowledge_graph_present_required": True,
        "ddd_model_present_required": True, "governance_present_required": True,
        "security_architecture_present_required": True, "observability_present_required": True,
        "deployment_architecture_present_required": True, "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True, "microservices_architecture_present_required": True,
        "sibling_space_bc_forbidden": True,
        "never_replace_p218_n_resources": True,
        "never_ungated_cargo_launch_authorization": True,
        "never_skip_cargo_authentication": True,
        "never_skip_supply_chain_security_controls": True,
        "never_ungated_emergency_route_activation": True,
        "space_ai_via_p214z_acl_only": True, "no_module_local_llm": True,
        "api_prefix": f"{API_PREFIX}/logistics",
        "forbidden_sibling_bc": ["space_logistics_platform", "orbital_supply_chain_bc", "autonomous_cargo_bc"],
        "foundation_for_p218_p": True,
    }


def logistics_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /space/logistics", "GET /space/logistics/vision",
        "GET /space/logistics/architecture", "GET /space/logistics/lifecycle",
        "GET /space/logistics/cargo", "GET /space/logistics/supply-chain",
        "GET /space/logistics/interplanetary", "GET /space/logistics/logistics-ai",
        "GET /space/logistics/robotics", "GET /space/logistics/digital-twin",
        "GET /space/logistics/knowledge-graph", "GET /space/logistics/observability",
        "GET /space/logistics/governance", "GET /space/logistics/security",
        "GET /space/logistics/integration", "GET /space/logistics/deployment",
        "GET /space/logistics/testing", "GET /space/logistics/cqrs",
        "GET /space/logistics/events", "GET /space/logistics/readiness",
    ]}
