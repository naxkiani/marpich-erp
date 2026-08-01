"""P216-G Enterprise Autonomous Logistics — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P216-G"
ADR = 479
SOR = "robotics"
API_PREFIX = "/api/v1/robotics"
PRODUCT = "Enterprise Robotics Autonomous Logistics, Warehouse Automation, Supply Chain Robotics & Intelligent Material Flow Platform"
CAPABILITY = "CAP-PLT-RB-001"
LOGISTICS_VISION = (
    "MEOS Autonomous Logistics Platform SHALL unify warehouse robotics, intelligent material flow, "
    "AI-driven logistics, enterprise planning and cyber-physical execution into one enterprise "
    "logistics operating ecosystem."
)
MISSION = (
    "Create a fully autonomous, intelligent and self-optimising logistics ecosystem capable of "
    "coordinating inventory, robots, warehouses, transportation and fulfilment in real time."
)
FABRIC = "meos_autonomous_logistics_fabric"
FOUNDATION_GATE = "P216"
MISSION_GATE = "P216-A"
STRATEGY_GATE = "P216-B"
DOMAIN_GATE = "P216-C"
RUNTIME_GATE = "P216-D"
PHYSICAL_AI_GATE = "P216-E"
INDUSTRIAL_GATE = "P216-F"
SUPREME_GATE = "P215-Z"
AI_GATE = "P214-Z"
CORE_DOMAIN = "enterprise_autonomous_logistics_intelligence"
AGGREGATE = "EnterpriseAutonomousLogisticsAggregate"

SUPPORTING_DOMAINS = (
    "warehouse_management",
    "warehouse_robotics",
    "inventory_intelligence",
    "material_flow",
    "fulfilment_intelligence",
    "transport_coordination",
    "yard_management",
    "autonomous_delivery",
    "packaging_automation",
    "supply_chain_visibility",
    "logistics_digital_twin",
    "reverse_logistics",
    "cold_chain_intelligence",
)
ENTITIES = (
    "Warehouse",
    "StorageZone",
    "Rack",
    "InventoryItem",
    "MaterialContainer",
    "AutonomousRobot",
    "AMR",
    "AGV",
    "PickingStation",
    "PackingStation",
    "LoadingDock",
    "Shipment",
    "TransportVehicle",
    "DeliveryMission",
    "WarehouseDigitalTwin",
)
VALUE_OBJECTS = (
    "WarehouseLocation",
    "StorageCapacity",
    "RobotCapacity",
    "PickingPriority",
    "RouteScore",
    "TravelTime",
    "InventoryAccuracy",
    "TransportWindow",
    "OrderPriority",
    "SafetyZone",
    "EnergyConsumption",
)
BOUNDED_CONTEXTS = (
    {"id": "BC-01", "name": "Warehouse Management Context", "responsibilities": ("warehouse_lifecycle", "zone_management", "capacity_planning", "warehouse_configuration")},
    {"id": "BC-02", "name": "Warehouse Robotics Context", "responsibilities": ("robot_orchestration", "amr_agv_coordination", "picking_automation", "material_transport")},
    {"id": "BC-03", "name": "Inventory Intelligence Context", "responsibilities": ("inventory_optimisation", "stock_positioning", "replenishment", "cycle_counting")},
    {"id": "BC-04", "name": "Material Flow Context", "responsibilities": ("internal_logistics", "conveyor_optimisation", "bin_movement", "dynamic_routing")},
    {"id": "BC-05", "name": "Order Fulfilment Context", "responsibilities": ("order_allocation", "picking", "packing", "shipping_preparation")},
    {"id": "BC-06", "name": "Transport Coordination Context", "responsibilities": ("dock_scheduling", "vehicle_dispatch", "fleet_coordination", "delivery_planning")},
    {"id": "BC-07", "name": "Supply Chain Visibility Context", "responsibilities": ("end_to_end_tracking", "eta_prediction", "logistics_intelligence", "risk_monitoring")},
    {"id": "BC-08", "name": "Warehouse Digital Twin Context", "responsibilities": ("warehouse_simulation", "robot_simulation", "capacity_simulation", "operational_optimisation")},
)
AUTONOMOUS_WAREHOUSE = {
    "present_required": True,
    "platform": "meos_autonomous_warehouse_platform",
    "components": (
        "warehouse_registry",
        "warehouse_control_centre",
        "robot_fleet_controller",
        "inventory_optimiser",
        "material_flow_engine",
        "fulfilment_engine",
        "dock_management_system",
        "warehouse_analytics",
    ),
    "capabilities": (
        "lights_out_warehouse",
        "dynamic_slotting",
        "autonomous_replenishment",
        "autonomous_picking",
        "autonomous_packing",
        "warehouse_balancing",
        "adaptive_workflows",
    ),
}
SUPPLY_CHAIN_ROBOTICS = {
    "present_required": True,
    "engine": "meos_supply_chain_robotics_engine",
    "supported_robots": (
        "AMR", "AGV", "picking_robots", "sorting_robots", "packing_robots",
        "palletising_robots", "depalletising_robots", "forklift_robots",
        "inventory_drones", "inspection_robots",
    ),
    "capabilities": (
        "multi_robot_collaboration",
        "dynamic_task_allocation",
        "swarm_intelligence",
        "fleet_optimisation",
        "obstacle_avoidance",
        "mission_coordination",
        "continuous_learning",
    ),
}
MATERIAL_FLOW = {
    "present_required": True,
    "engine": "meos_material_flow_intelligence_engine",
    "capabilities": (
        "route_optimisation",
        "adaptive_conveyor_control",
        "dynamic_storage_allocation",
        "cross_docking_optimisation",
        "wave_planning",
        "batch_optimisation",
        "load_balancing",
        "autonomous_transfer_planning",
    ),
    "decision_engines": (
        "flow_optimiser",
        "routing_engine",
        "storage_optimiser",
        "load_optimiser",
        "capacity_planner",
        "congestion_predictor",
    ),
}
AI_LOGISTICS = {
    "present_required": True,
    "engine": "meos_logistics_intelligence_engine",
    "capabilities": (
        "demand_prediction",
        "inventory_forecasting",
        "warehouse_optimisation",
        "transport_optimisation",
        "eta_prediction",
        "order_prioritisation",
        "anomaly_detection",
        "labour_optimisation",
        "energy_optimisation",
        "carbon_footprint_optimisation",
    ),
    "via_p214_z": True,
}
WAREHOUSE_DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_logistics_digital_twin_platform",
    "represents": (
        "warehouses", "storage_zones", "robots", "inventory", "orders",
        "transport_vehicles", "loading_docks", "material_flow", "equipment", "human_operators",
    ),
    "capabilities": (
        "simulation",
        "scenario_analysis",
        "capacity_planning",
        "operational_replay",
        "risk_forecasting",
        "continuous_optimisation",
    ),
}
SUPPLY_CHAIN_KG = {
    "present_required": True,
    "graph": "meos_supply_chain_knowledge_graph",
    "nodes": (
        "warehouses", "products", "inventory", "robots", "orders", "shipments",
        "suppliers", "customers", "vehicles", "routes", "storage_locations", "packaging_units",
    ),
    "relationships": (
        "stored_in", "picked_by", "packed_at", "transported_by", "delivered_to",
        "supplied_by", "depends_on", "moves_through", "allocated_to", "optimises",
    ),
    "enables": (
        "enterprise_logistics_reasoning",
        "inventory_intelligence",
        "supply_chain_optimisation",
        "autonomous_decision_support",
    ),
}
TRANSPORT_COORDINATION = {
    "present_required": True,
    "capabilities": ("dock_scheduling", "vehicle_dispatch", "fleet_coordination", "delivery_planning"),
}
SECURITY = {
    "present_required": True,
    "framework": "meos_autonomous_logistics_zero_trust_framework",
    "domains": (
        "robot_identity",
        "warehouse_device_identity",
        "inventory_integrity",
        "mission_authorisation",
        "dock_security",
        "transport_security",
        "api_security",
        "edge_security",
        "operational_safety",
        "threat_detection",
    ),
    "controls": (
        "continuous_authentication",
        "least_privilege",
        "encrypted_communications",
        "policy_enforcement",
        "real_time_monitoring",
    ),
    "zero_trust": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "never_duplicate_wms_tms_core_logic": True,
    "no_module_local_llm": True,
    "physical_ai_via_p214z_acl_only": True,
    "never_replace_p216_foundation": True,
    "never_replace_p216_f_industrial": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "ungated_physical_autonomy_strategy_forbidden": True,
    "opaque_safety_strategy_forbidden": True,
}
COMMANDS = (
    "ReceiveInventoryCommand",
    "AllocateInventoryCommand",
    "AssignPickingRobotCommand",
    "ExecutePickingMissionCommand",
    "CompletePackingCommand",
    "DispatchShipmentCommand",
    "OptimiseWarehouseCommand",
)
QUERIES = (
    "GetWarehouseStatusQuery",
    "GetInventoryAvailabilityQuery",
    "GetRobotFleetStatusQuery",
    "GetShipmentStatusQuery",
    "GetMaterialFlowQuery",
    "GetWarehouseDigitalTwinQuery",
)
CORE_EVENTS = (
    {"name": "InventoryReceivedEvent", "schema": "robotics.logistics.inventory.received.v1", "owner": "BC-03", "consumers": "wms,audit,fulfilment"},
    {"name": "InventoryReservedEvent", "schema": "robotics.logistics.inventory.reserved.v1", "owner": "BC-03", "consumers": "fulfilment,audit"},
    {"name": "PickingMissionStartedEvent", "schema": "robotics.logistics.picking.mission.started.v1", "owner": "BC-02", "consumers": "runtime,audit,analytics"},
    {"name": "PickingMissionCompletedEvent", "schema": "robotics.logistics.picking.mission.completed.v1", "owner": "BC-02", "consumers": "fulfilment,audit,analytics"},
    {"name": "PackingCompletedEvent", "schema": "robotics.logistics.packing.completed.v1", "owner": "BC-05", "consumers": "transport,audit"},
    {"name": "ShipmentDispatchedEvent", "schema": "robotics.logistics.shipment.dispatched.v1", "owner": "BC-06", "consumers": "tms,visibility,audit"},
    {"name": "TransportArrivedEvent", "schema": "robotics.logistics.transport.arrived.v1", "owner": "BC-06", "consumers": "dock,visibility,audit"},
    {"name": "WarehouseOptimisedEvent", "schema": "robotics.logistics.warehouse.optimised.v1", "owner": "BC-08", "consumers": "analytics,ai,twin"},
    {"name": "RobotFleetBalancedEvent", "schema": "robotics.logistics.robot.fleet.balanced.v1", "owner": "BC-02", "consumers": "runtime,analytics"},
)
MICROSERVICES = (
    {"id": "warehouse_management_service", "bc": "BC-01", "api": "/robotics/logistics/warehouse", "db": "robotics_*", "events": ("WarehouseOptimisedEvent",), "security": ("robotics.admin",), "scaling": "warehouse_replicas", "responsibility": "Warehouse lifecycle and configuration"},
    {"id": "warehouse_robotics_service", "bc": "BC-02", "api": "/robotics/logistics/robots", "db": "robotics_*", "events": ("PickingMissionStartedEvent", "PickingMissionCompletedEvent", "RobotFleetBalancedEvent"), "security": ("robotics.write",), "scaling": "robot_workers", "responsibility": "AMR/AGV and picking robot orchestration"},
    {"id": "inventory_intelligence_service", "bc": "BC-03", "api": "/robotics/logistics/inventory", "db": "robotics_*", "events": ("InventoryReceivedEvent", "InventoryReservedEvent"), "security": ("robotics.write",), "scaling": "inventory_workers", "responsibility": "Inventory intelligence projections"},
    {"id": "material_flow_service", "bc": "BC-04", "api": "/robotics/logistics/material-flow", "db": "robotics_*", "events": ("WarehouseOptimisedEvent",), "security": ("robotics.write",), "scaling": "flow_workers", "responsibility": "Intelligent material flow"},
    {"id": "order_fulfilment_service", "bc": "BC-05", "api": "/robotics/logistics/fulfilment", "db": "robotics_*", "events": ("PackingCompletedEvent",), "security": ("robotics.write",), "scaling": "fulfilment_workers", "responsibility": "Order picking packing preparation"},
    {"id": "dock_management_service", "bc": "BC-06", "api": "/robotics/logistics/docks", "db": "robotics_*", "events": ("TransportArrivedEvent",), "security": ("robotics.write",), "scaling": "dock_workers", "responsibility": "Loading dock scheduling"},
    {"id": "transport_coordination_service", "bc": "BC-06", "api": "/robotics/logistics/transport", "db": "robotics_*", "events": ("ShipmentDispatchedEvent", "TransportArrivedEvent"), "security": ("robotics.write",), "scaling": "transport_workers", "responsibility": "Transport and delivery coordination"},
    {"id": "warehouse_digital_twin_service", "bc": "BC-08", "api": "/robotics/logistics/digital-twin", "db": "robotics_*", "events": ("WarehouseOptimisedEvent",), "security": ("robotics.read",), "scaling": "twin_workers", "responsibility": "Warehouse digital twin sync"},
    {"id": "logistics_analytics_service", "bc": "BC-07", "api": "/robotics/logistics/analytics", "db": "robotics_*", "events": ("WarehouseOptimisedEvent",), "security": ("robotics.read",), "scaling": "analytics_workers", "responsibility": "Logistics analytics facets"},
    {"id": "supply_chain_knowledge_graph_service", "bc": "BC-07", "api": "/robotics/logistics/knowledge-graph", "db": "robotics_*", "events": ("ShipmentDispatchedEvent",), "security": ("robotics.read",), "scaling": "kg_workers", "responsibility": "Supply chain knowledge graph projections"},
    {"id": "cold_chain_monitoring_service", "bc": "BC-07", "api": "/robotics/logistics/cold-chain", "db": "robotics_*", "events": ("TransportArrivedEvent",), "security": ("robotics.read",), "scaling": "cold_chain_workers", "responsibility": "Cold chain monitoring intelligence"},
)
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p216d_robotics_os",
        "p216e_physical_ai",
        "p216f_industrial",
        "p214z_ai_master",
        "p215z_quantum_supreme",
        "erp",
        "scm",
        "wms",
        "tms",
        "mes",
        "crm",
        "iot_platform",
        "digital_twin_platform",
    ),
    "mechanisms": (
        "warehouse_apis",
        "fulfilment_apis",
        "logistics_event_contracts",
        "robot_mission_interfaces",
        "inventory_synchronisation",
        "supply_chain_intelligence_interfaces",
    ),
    "via_p216_d": True,
    "via_p216_e": True,
    "via_p216_f": True,
    "via_p214_z": True,
    "via_p215_z": True,
    "via_p213": True,
    "never_duplicate_wms_tms_core_logic": True,
}
DEPLOYMENT = {
    "present_required": True,
    "model": "hybrid_autonomous_logistics_infrastructure",
    "includes": (
        "warehouse_edge_cluster",
        "cloud_logistics_platform",
        "robot_runtime_cluster",
        "warehouse_ai_cluster",
        "digital_twin_cluster",
        "knowledge_graph_cluster",
        "observability_platform",
        "security_operations_platform",
        "disaster_recovery_platform",
    ),
    "deployment_models": (
        "single_warehouse",
        "multi_warehouse_enterprise",
        "regional_distribution_network",
        "global_supply_chain_network",
    ),
    "cloud_native": True,
    "edge_native": True,
}
TESTING = (
    "warehouse_workflow_testing",
    "robot_coordination_testing",
    "inventory_accuracy_testing",
    "material_flow_testing",
    "transport_integration_testing",
    "digital_twin_validation",
    "performance_testing",
    "scalability_testing",
    "industrial_cybersecurity_testing",
    "disaster_recovery_testing",
    "operational_resilience_testing",
)
API_SURFACES = (
    "/api/v1/robotics/logistics",
    "/api/v1/robotics/logistics/vision",
    "/api/v1/robotics/logistics/domain",
    "/api/v1/robotics/logistics/bounded-contexts",
    "/api/v1/robotics/logistics/warehouse",
    "/api/v1/robotics/logistics/robotics",
    "/api/v1/robotics/logistics/material-flow",
    "/api/v1/robotics/logistics/ai",
    "/api/v1/robotics/logistics/digital-twin",
    "/api/v1/robotics/logistics/knowledge-graph",
    "/api/v1/robotics/logistics/transport",
    "/api/v1/robotics/logistics/security",
    "/api/v1/robotics/logistics/cqrs",
    "/api/v1/robotics/logistics/events",
    "/api/v1/robotics/logistics/microservices",
    "/api/v1/robotics/logistics/integration",
    "/api/v1/robotics/logistics/deployment",
    "/api/v1/robotics/logistics/testing",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
QUALITY_GATES_REJECT_IF = (
    "autonomous_warehouse_platform_is_missing",
    "supply_chain_robotics_platform_is_missing",
    "intelligent_material_flow_platform_is_missing",
    "warehouse_digital_twin_is_missing",
    "ai_logistics_intelligence_is_missing",
    "supply_chain_knowledge_graph_is_missing",
    "transport_coordination_platform_is_missing",
    "warehouse_security_architecture_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "cloud_edge_deployment_is_missing",
    "enterprise_supply_chain_integration_is_missing",
    "testing_architecture_is_missing",
    "sibling_robotics_bc",
    "replace_p216_f_industrial",
    "duplicate_wms_tms_core_logic",
    "module_local_llm",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Autonomous Logistics Fabric",
        "logistics_vision": LOGISTICS_VISION,
        "mission": MISSION,
        "builds_on_p216": True,
        "builds_on_p216_f": True,
        "builds_on_p216_e": True,
        "builds_on_p216_d": True,
        "builds_on_p215_z": True,
        "builds_on_p214_z": True,
        "never_replace_p216_f_industrial": True,
        "foundation_gate": FOUNDATION_GATE,
        "industrial_gate": INDUSTRIAL_GATE,
        "physical_ai_gate": PHYSICAL_AI_GATE,
        "runtime_gate": RUNTIME_GATE,
        "supreme_gate": SUPREME_GATE,
        "ai_gate": AI_GATE,
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

def warehouse() -> dict[str, Any]:
    return dict(AUTONOMOUS_WAREHOUSE)

def robotics_platform() -> dict[str, Any]:
    return dict(SUPPLY_CHAIN_ROBOTICS)

def material_flow() -> dict[str, Any]:
    return dict(MATERIAL_FLOW)

def ai_intelligence() -> dict[str, Any]:
    return dict(AI_LOGISTICS)

def digital_twin() -> dict[str, Any]:
    return dict(WAREHOUSE_DIGITAL_TWIN)

def knowledge_graph() -> dict[str, Any]:
    return dict(SUPPLY_CHAIN_KG)

def transport() -> dict[str, Any]:
    return dict(TRANSPORT_COORDINATION)

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
        "industrial_gate_api": "/api/v1/robotics/industrial",
        "runtime_gate_api": "/api/v1/robotics/runtime",
    }

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p216_h": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "logistics_vision": LOGISTICS_VISION, "mission": MISSION, "principle": LOGISTICS_VISION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE, "runtime_gate": RUNTIME_GATE,
        "physical_ai_gate": PHYSICAL_AI_GATE, "industrial_gate": INDUSTRIAL_GATE,
        "supreme_gate": SUPREME_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P216", "P216-A", "P216-B", "P216-C", "P216-D", "P216-E", "P216-F", "P215-Z", "P214-Z", "P213", "ADR-472", "ADR-473", "ADR-474", "ADR-475", "ADR-476", "ADR-477", "ADR-478"],
        "vision": vision_pack(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "warehouse": warehouse(),
        "robotics_platform": robotics_platform(),
        "material_flow": material_flow(),
        "ai_intelligence": ai_intelligence(),
        "digital_twin": digital_twin(),
        "knowledge_graph": knowledge_graph(),
        "transport": transport(),
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
        "autonomous_warehouse_platform_present_required": True,
        "supply_chain_robotics_platform_present_required": True,
        "intelligent_material_flow_platform_present_required": True,
        "warehouse_digital_twin_present_required": True,
        "ai_logistics_intelligence_present_required": True,
        "supply_chain_knowledge_graph_present_required": True,
        "transport_coordination_platform_present_required": True,
        "warehouse_security_architecture_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "cloud_edge_deployment_present_required": True,
        "enterprise_supply_chain_integration_present_required": True,
        "testing_architecture_present_required": True,
        "sibling_robotics_bc_forbidden": True,
        "never_replace_p216_foundation": True,
        "never_replace_p216_a_mission": True,
        "never_replace_p216_b_strategy": True,
        "never_replace_p216_c_domain": True,
        "never_replace_p216_d_runtime": True,
        "never_replace_p216_e_physical_ai": True,
        "never_replace_p216_f_industrial": True,
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_duplicate_wms_tms_core_logic": True,
        "no_module_local_llm": True,
        "physical_ai_via_p214z_acl_only": True,
        "ungated_physical_autonomy_strategy_forbidden": True,
        "opaque_safety_strategy_forbidden": True,
        "builds_on_p216": True, "builds_on_p216_f": True, "builds_on_p216_e": True, "builds_on_p216_d": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p216_d": True, "via_p216_e": True, "via_p216_f": True, "via_p215_z": True, "via_p214_z": True, "via_p213": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "api_prefix": f"{API_PREFIX}/logistics",
        "forbidden_sibling_bc": [
            "autonomous_logistics_platform",
            "warehouse_automation_platform",
            "supply_chain_robotics_platform",
        ],
        "foundation_for_p216_h": True,
    }

def logistics_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /robotics/logistics",
        "GET /robotics/logistics/vision",
        "GET /robotics/logistics/domain",
        "GET /robotics/logistics/bounded-contexts",
        "GET /robotics/logistics/warehouse",
        "GET /robotics/logistics/robotics",
        "GET /robotics/logistics/material-flow",
        "GET /robotics/logistics/ai",
        "GET /robotics/logistics/digital-twin",
        "GET /robotics/logistics/knowledge-graph",
        "GET /robotics/logistics/transport",
        "GET /robotics/logistics/security",
        "GET /robotics/logistics/cqrs",
        "GET /robotics/logistics/events",
        "GET /robotics/logistics/microservices",
        "GET /robotics/logistics/integration",
        "GET /robotics/logistics/deployment",
        "GET /robotics/logistics/testing",
        "GET /robotics/logistics/readiness",
    ], "industrial_gate_routes": ["GET /robotics/industrial", "GET /robotics/industrial/readiness"]}
