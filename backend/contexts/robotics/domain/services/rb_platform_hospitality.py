"""P216-P Enterprise Hospitality Intelligence — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P216-P"
ADR = 488
SOR = "robotics"
API_PREFIX = "/api/v1/robotics"
PRODUCT = (
    "Enterprise Robotics Hospitality Robotics, Smart Hotels, "
    "Autonomous Guest Services & Intelligent Hospitality Experience Platform"
)
CAPABILITY = "CAP-PLT-RB-001"
HOSPITALITY_VISION = (
    "MEOS Hospitality Intelligence Platform SHALL unify hospitality robotics, "
    "smart hotels, autonomous guest services and hotel digital twins as "
    "intelligent participants within the MEOS Hospitality Intelligence Ecosystem."
)
MISSION = (
    "Create an AI-native, robotics-enabled, guest-centric hospitality ecosystem "
    "that automates hotel operations, enhances guest satisfaction and delivers "
    "personalised experiences."
)
VISION = (
    "Every hotel, guest, room, service, robot, employee, facility asset and "
    "hospitality workflow shall become an intelligent participant inside the "
    "MEOS Hospitality Intelligence Ecosystem."
)
FABRIC = "meos_hospitality_intelligence_fabric"
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
SUPREME_GATE = "P215-Z"
AI_GATE = "P214-Z"
CORE_DOMAIN = "enterprise_hospitality_intelligence"
AGGREGATE = "HospitalityIntelligenceAggregate"

SUPPORTING_DOMAINS = (
    "guest_experience",
    "hotel_operations",
    "hospitality_robotics",
    "room_intelligence",
    "smart_facilities",
    "tourism_intelligence",
    "reservation_intelligence",
    "food_beverage_intelligence",
    "concierge_automation",
    "hospitality_analytics",
    "hospitality_digital_twin",
    "loyalty_intelligence",
)
ENTITIES = (
    "HospitalityEnterprise",
    "Hotel",
    "Property",
    "Room",
    "Guest",
    "Reservation",
    "ServiceRequest",
    "HospitalityRobot",
    "ConciergeRobot",
    "CleaningRobot",
    "DeliveryRobot",
    "RestaurantServiceRobot",
    "FacilityAsset",
    "GuestDigitalTwin",
    "HotelDigitalTwin",
)
VALUE_OBJECTS = (
    "GuestProfile",
    "RoomStatus",
    "ExperienceScore",
    "ServicePriority",
    "ReservationStatus",
    "GuestPreference",
    "OccupancyRate",
    "ServiceQualityScore",
    "RevenueForecast",
    "OperationalStatus",
)
BOUNDED_CONTEXTS = (
    {"id": "BC-01", "name": "Guest Experience Context", "responsibilities": ("guest_lifecycle", "personalisation", "experience_management")},
    {"id": "BC-02", "name": "Hospitality Robotics Context", "responsibilities": ("hotel_robots", "service_automation", "robot_lifecycle")},
    {"id": "BC-03", "name": "Smart Hotel Operations Context", "responsibilities": ("hotel_workflows", "room_operations", "facility_coordination")},
    {"id": "BC-04", "name": "Room Intelligence Context", "responsibilities": ("smart_rooms", "comfort_optimisation", "guest_environment_control")},
    {"id": "BC-05", "name": "Hospitality AI Context", "responsibilities": ("recommendations", "guest_intelligence", "service_prediction")},
    {"id": "BC-06", "name": "Tourism Intelligence Context", "responsibilities": ("destination_intelligence", "travel_recommendations", "visitor_analytics")},
    {"id": "BC-07", "name": "Hospitality Digital Twin Context", "responsibilities": ("hotel_simulation", "occupancy_modelling", "operational_optimisation")},
    {"id": "BC-08", "name": "Hospitality Governance Context", "responsibilities": ("privacy", "compliance", "ai_governance")},
)
HOSPITALITY_ROBOTICS = {
    "present_required": True,
    "platform": "meos_hospitality_robotics_platform",
    "components": (
        "hotel_robot_registry",
        "guest_service_robot_manager",
        "robot_mission_controller",
        "hotel_navigation_engine",
        "room_service_automation_engine",
        "hospitality_operations_dashboard",
    ),
    "supported_robotics": (
        "concierge_robots",
        "room_service_robots",
        "cleaning_robots",
        "luggage_assistance_robots",
        "delivery_robots",
        "information_robots",
    ),
    "capabilities": (
        "guest_assistance",
        "autonomous_delivery",
        "room_support",
        "hotel_navigation",
        "information_services",
        "operational_automation",
    ),
}
SMART_HOTEL = {
    "present_required": True,
    "platform": "meos_smart_hotel_intelligence_platform",
    "capabilities": (
        "smart_rooms",
        "automated_check_in",
        "smart_access_control",
        "energy_optimisation",
        "room_availability_intelligence",
        "facility_automation",
        "guest_comfort_management",
    ),
}
GUEST_EXPERIENCE = {
    "present_required": True,
    "engine": "meos_guest_intelligence_engine",
    "capabilities": (
        "guest_preference_learning",
        "personalised_recommendations",
        "conversational_concierge",
        "experience_prediction",
        "sentiment_analysis",
        "loyalty_intelligence",
        "service_optimisation",
    ),
    "models": (
        "hospitality_foundation_models",
        "conversation_models",
        "recommendation_models",
        "experience_prediction_models",
    ),
    "via_p214_z": True,
    "privacy_by_design": True,
    "human_centered": True,
}
AUTONOMOUS_SERVICES = {
    "present_required": True,
    "platform": "meos_hospitality_automation_platform",
    "capabilities": (
        "automated_housekeeping",
        "service_request_routing",
        "room_preparation",
        "restaurant_automation",
        "facility_management",
        "guest_communication",
        "operational_optimisation",
    ),
}
HOSPITALITY_AI = {
    "present_required": True,
    "engine": "meos_hospitality_ai_platform",
    "capabilities": (
        "recommendations",
        "guest_intelligence",
        "service_prediction",
        "revenue_intelligence",
        "occupancy_forecasting",
    ),
    "via_p214_z": True,
    "responsible_ai": True,
}
HOTEL_DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_hospitality_digital_twin_platform",
    "represents": (
        "hotels", "rooms", "guests", "robots", "employees",
        "facilities", "restaurants", "events", "services",
    ),
    "capabilities": (
        "hotel_simulation",
        "occupancy_optimisation",
        "energy_management",
        "service_forecasting",
        "operational_replay",
        "scenario_planning",
    ),
}
HOSPITALITY_KG = {
    "present_required": True,
    "graph": "meos_hospitality_knowledge_graph",
    "nodes": (
        "guests", "hotels", "rooms", "services", "robots",
        "employees", "reservations", "destinations", "events", "facilities",
    ),
    "relationships": (
        "visits", "books", "uses", "requests", "recommends",
        "operates", "located_at", "optimises",
    ),
    "enables": (
        "guest_reasoning",
        "hospitality_intelligence",
        "personalisation",
        "tourism_analytics",
    ),
}
OBSERVABILITY = {
    "present_required": True,
    "platform": "meos_hospitality_observability_platform",
    "monitors": (
        "guest_satisfaction",
        "robot_performance",
        "hotel_operations",
        "room_utilisation",
        "service_quality",
        "revenue_intelligence",
        "ai_performance",
        "digital_twin_accuracy",
    ),
    "via_platform_observability": True,
}
SECURITY = {
    "present_required": True,
    "framework": "meos_hospitality_zero_trust_framework",
    "domains": (
        "guest_identity",
        "robot_identity",
        "hotel_identity",
        "reservation_security",
        "payment_protection",
        "personal_data_protection",
        "ai_governance",
        "audit_management",
    ),
    "controls": (
        "encryption",
        "access_governance",
        "privacy_management",
        "fraud_detection",
        "continuous_monitoring",
    ),
    "zero_trust": True,
    "privacy_by_design": True,
    "human_centered_hospitality": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "via_integration_platform": True,
    "payment_via_integration_platform_only": True,
    "never_direct_payment_bypass": True,
    "never_duplicate_hotel_pms_core_logic": True,
    "no_module_local_llm": True,
    "physical_ai_via_p214z_acl_only": True,
    "never_replace_p216_foundation": True,
    "never_replace_p216_o_retail": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "ungated_physical_autonomy_strategy_forbidden": True,
    "opaque_safety_strategy_forbidden": True,
}
COMMANDS = (
    "RegisterGuestCommand",
    "AssignHospitalityRobotCommand",
    "CreateReservationCommand",
    "RequestServiceCommand",
    "OptimiseHotelOperationCommand",
    "UpdateHotelTwinCommand",
)
QUERIES = (
    "GetGuestProfileQuery",
    "GetRoomStatusQuery",
    "GetHotelStatusQuery",
    "GetRobotStatusQuery",
    "GetHospitalityTwinQuery",
)
CORE_EVENTS = (
    {"name": "GuestArrivalEvent", "schema": "robotics.hospitality.guest.arrival.v1", "owner": "BC-01", "consumers": "operations,robotics,audit"},
    {"name": "ReservationConfirmedEvent", "schema": "robotics.hospitality.reservation.confirmed.v1", "owner": "BC-03", "consumers": "guest,twin,audit"},
    {"name": "ServiceRequestedEvent", "schema": "robotics.hospitality.service.requested.v1", "owner": "BC-01", "consumers": "robotics,operations,audit"},
    {"name": "RobotMissionCompletedEvent", "schema": "robotics.hospitality.robot.mission.completed.v1", "owner": "BC-02", "consumers": "runtime,operations,audit"},
    {"name": "RoomPreparedEvent", "schema": "robotics.hospitality.room.prepared.v1", "owner": "BC-04", "consumers": "guest,twin,audit"},
    {"name": "GuestExperienceUpdatedEvent", "schema": "robotics.hospitality.guest.experience.updated.v1", "owner": "BC-01", "consumers": "ai,governance,audit"},
    {"name": "HotelOptimisedEvent", "schema": "robotics.hospitality.hotel.optimised.v1", "owner": "BC-03", "consumers": "twin,analytics,audit"},
)
MICROSERVICES = (
    {"id": "guest_intelligence_service", "bc": "BC-01", "api": "/robotics/hospitality/guests", "db": "robotics_*", "events": ("GuestArrivalEvent", "GuestExperienceUpdatedEvent"), "security": ("robotics.write",), "scaling": "guest_replicas", "responsibility": "Guest experience projections and personalisation"},
    {"id": "hospitality_robotics_service", "bc": "BC-02", "api": "/robotics/hospitality/robots", "db": "robotics_*", "events": ("RobotMissionCompletedEvent",), "security": ("robotics.write",), "scaling": "robot_workers", "responsibility": "Hospitality robot mission orchestration"},
    {"id": "hotel_operations_service", "bc": "BC-03", "api": "/robotics/hospitality/hotels", "db": "robotics_*", "events": ("HotelOptimisedEvent", "ReservationConfirmedEvent"), "security": ("robotics.write",), "scaling": "hotel_workers", "responsibility": "Smart hotel operations"},
    {"id": "reservation_intelligence_service", "bc": "BC-03", "api": "/robotics/hospitality/reservations", "db": "robotics_*", "events": ("ReservationConfirmedEvent",), "security": ("robotics.write",), "scaling": "reservation_workers", "responsibility": "Reservation intelligence projections"},
    {"id": "room_intelligence_service", "bc": "BC-04", "api": "/robotics/hospitality/rooms", "db": "robotics_*", "events": ("RoomPreparedEvent",), "security": ("robotics.write",), "scaling": "room_workers", "responsibility": "Smart room intelligence"},
    {"id": "hospitality_ai_service", "bc": "BC-05", "api": "/robotics/hospitality/ai", "db": "robotics_*", "events": ("GuestExperienceUpdatedEvent",), "security": ("robotics.write",), "scaling": "ai_workers", "responsibility": "Hospitality AI via P214-Z ACL"},
    {"id": "tourism_intelligence_service", "bc": "BC-06", "api": "/robotics/hospitality/tourism", "db": "robotics_*", "events": ("GuestArrivalEvent",), "security": ("robotics.read",), "scaling": "tourism_workers", "responsibility": "Tourism intelligence facets"},
    {"id": "digital_twin_service", "bc": "BC-07", "api": "/robotics/hospitality/digital-twin", "db": "robotics_*", "events": ("HotelOptimisedEvent", "RoomPreparedEvent"), "security": ("robotics.read",), "scaling": "twin_workers", "responsibility": "Hotel digital twin sync"},
    {"id": "knowledge_graph_service", "bc": "BC-07", "api": "/robotics/hospitality/knowledge-graph", "db": "robotics_*", "events": ("GuestArrivalEvent", "ReservationConfirmedEvent"), "security": ("robotics.read",), "scaling": "kg_workers", "responsibility": "Hospitality knowledge graph projections"},
    {"id": "analytics_service", "bc": "BC-08", "api": "/robotics/hospitality/analytics", "db": "robotics_*", "events": ("HotelOptimisedEvent", "GuestExperienceUpdatedEvent"), "security": ("robotics.read",), "scaling": "analytics_workers", "responsibility": "Hospitality analytics and governance facets"},
)
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p216d_robotics_os",
        "p216e_physical_ai",
        "p216g_autonomous_logistics",
        "p216h_autonomous_mobility",
        "p216o_retail",
        "p214z_ai_master",
        "p215z_quantum_supreme",
        "erp",
        "crm",
        "booking_platforms",
        "payment_platforms",
        "smart_building_platforms",
        "iot_platforms",
        "tourism_platforms",
        "integration_platform",
    ),
    "mechanisms": (
        "hospitality_apis",
        "robot_mission_interfaces",
        "payment_via_integration_connectors",
        "booking_via_peer_api",
        "pms_via_peer_api",
        "hospitality_event_contracts",
    ),
    "via_p216_d": True,
    "via_p216_e": True,
    "via_p216_g": True,
    "via_p216_h": True,
    "via_p216_o": True,
    "via_p214_z": True,
    "via_p215_z": True,
    "via_p213": True,
    "via_integration_platform": True,
    "never_direct_payment_bypass": True,
    "never_duplicate_hotel_pms_core_logic": True,
}
DEPLOYMENT = {
    "present_required": True,
    "model": "hybrid_hospitality_intelligence_infrastructure",
    "includes": (
        "hotel_edge_platform",
        "smart_room_runtime",
        "hospitality_cloud_platform",
        "ai_compute_cluster",
        "robot_control_platform",
        "digital_twin_cluster",
        "knowledge_graph_cluster",
        "analytics_platform",
        "security_operations_platform",
    ),
    "deployment_models": (
        "single_hotel",
        "hotel_chain",
        "resort_network",
        "global_hospitality_enterprise",
    ),
    "cloud_native": True,
    "edge_native": True,
}
TESTING = (
    "guest_experience_testing",
    "robot_interaction_testing",
    "smart_room_testing",
    "ai_recommendation_testing",
    "digital_twin_validation",
    "security_testing",
    "performance_testing",
    "scalability_testing",
    "resilience_testing",
)
API_SURFACES = (
    "/api/v1/robotics/hospitality",
    "/api/v1/robotics/hospitality/vision",
    "/api/v1/robotics/hospitality/domain",
    "/api/v1/robotics/hospitality/bounded-contexts",
    "/api/v1/robotics/hospitality/robotics",
    "/api/v1/robotics/hospitality/smart-hotel",
    "/api/v1/robotics/hospitality/guest-experience",
    "/api/v1/robotics/hospitality/autonomous-services",
    "/api/v1/robotics/hospitality/ai",
    "/api/v1/robotics/hospitality/digital-twin",
    "/api/v1/robotics/hospitality/knowledge-graph",
    "/api/v1/robotics/hospitality/observability",
    "/api/v1/robotics/hospitality/security",
    "/api/v1/robotics/hospitality/cqrs",
    "/api/v1/robotics/hospitality/events",
    "/api/v1/robotics/hospitality/microservices",
    "/api/v1/robotics/hospitality/integration",
    "/api/v1/robotics/hospitality/deployment",
    "/api/v1/robotics/hospitality/testing",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
QUALITY_GATES_REJECT_IF = (
    "hospitality_robotics_platform_is_missing",
    "smart_hotel_platform_is_missing",
    "autonomous_guest_services_is_missing",
    "hospitality_ai_platform_is_missing",
    "guest_experience_intelligence_is_missing",
    "hotel_digital_twin_is_missing",
    "hospitality_knowledge_graph_is_missing",
    "security_architecture_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "cloud_edge_deployment_is_missing",
    "enterprise_hospitality_integration_is_missing",
    "testing_architecture_is_missing",
    "sibling_robotics_bc",
    "replace_p216_o_retail",
    "direct_payment_bypass",
    "duplicate_hotel_pms_core_logic",
    "module_local_llm",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Hospitality Intelligence Fabric",
        "hospitality_vision": HOSPITALITY_VISION,
        "mission": MISSION,
        "vision": VISION,
        "builds_on_p216": True,
        "builds_on_p216_o": True,
        "builds_on_p216_h": True,
        "builds_on_p216_g": True,
        "builds_on_p216_e": True,
        "builds_on_p216_d": True,
        "builds_on_p215_z": True,
        "builds_on_p214_z": True,
        "never_replace_p216_o_retail": True,
        "foundation_gate": FOUNDATION_GATE,
        "retail_gate": RETAIL_GATE,
        "mobility_gate": MOBILITY_GATE,
        "logistics_gate": LOGISTICS_GATE,
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

def robotics_platform() -> dict[str, Any]:
    return dict(HOSPITALITY_ROBOTICS)

def smart_hotel() -> dict[str, Any]:
    return dict(SMART_HOTEL)

def guest_experience() -> dict[str, Any]:
    return dict(GUEST_EXPERIENCE)

def autonomous_services() -> dict[str, Any]:
    return dict(AUTONOMOUS_SERVICES)

def hospitality_ai() -> dict[str, Any]:
    return dict(HOSPITALITY_AI)

def digital_twin() -> dict[str, Any]:
    return dict(HOTEL_DIGITAL_TWIN)

def knowledge_graph() -> dict[str, Any]:
    return dict(HOSPITALITY_KG)

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
        "retail_gate_api": "/api/v1/robotics/retail",
        "runtime_gate_api": "/api/v1/robotics/runtime",
    }

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p216_q": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "hospitality_vision": HOSPITALITY_VISION, "mission": MISSION, "vision": VISION, "principle": HOSPITALITY_VISION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE, "runtime_gate": RUNTIME_GATE,
        "physical_ai_gate": PHYSICAL_AI_GATE, "industrial_gate": INDUSTRIAL_GATE,
        "logistics_gate": LOGISTICS_GATE, "mobility_gate": MOBILITY_GATE,
        "healthcare_gate": HEALTHCARE_GATE, "construction_gate": CONSTRUCTION_GATE,
        "public_safety_gate": PUBLIC_SAFETY_GATE, "retail_gate": RETAIL_GATE,
        "supreme_gate": SUPREME_GATE, "ai_gate": AI_GATE,
        "builds_on": [
            "P216", "P216-A", "P216-B", "P216-C", "P216-D", "P216-E", "P216-F", "P216-G", "P216-H",
            "P216-I", "P216-K", "P216-L", "P216-O", "P215-Z", "P214-Z", "P213",
            "ADR-472", "ADR-473", "ADR-474", "ADR-475", "ADR-476", "ADR-477", "ADR-478", "ADR-479",
            "ADR-480", "ADR-481", "ADR-483", "ADR-484", "ADR-487",
        ],
        "vision_pack": vision_pack(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "robotics_platform": robotics_platform(),
        "smart_hotel": smart_hotel(),
        "guest_experience": guest_experience(),
        "autonomous_services": autonomous_services(),
        "hospitality_ai": hospitality_ai(),
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
        "hospitality_robotics_platform_present_required": True,
        "smart_hotel_platform_present_required": True,
        "autonomous_guest_services_present_required": True,
        "hospitality_ai_platform_present_required": True,
        "guest_experience_intelligence_present_required": True,
        "hotel_digital_twin_present_required": True,
        "hospitality_knowledge_graph_present_required": True,
        "security_architecture_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "cloud_edge_deployment_present_required": True,
        "enterprise_hospitality_integration_present_required": True,
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
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_direct_payment_bypass": True,
        "payment_via_integration_platform_only": True,
        "never_duplicate_hotel_pms_core_logic": True,
        "no_module_local_llm": True,
        "physical_ai_via_p214z_acl_only": True,
        "privacy_by_design_required": True,
        "human_centered_hospitality_required": True,
        "ungated_physical_autonomy_strategy_forbidden": True,
        "opaque_safety_strategy_forbidden": True,
        "builds_on_p216": True, "builds_on_p216_o": True, "builds_on_p216_h": True,
        "builds_on_p216_g": True, "builds_on_p216_e": True, "builds_on_p216_d": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p216_d": True, "via_p216_e": True, "via_p216_g": True, "via_p216_h": True, "via_p216_o": True,
        "via_p215_z": True, "via_p214_z": True, "via_p213": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "via_integration_platform": True,
        "api_prefix": f"{API_PREFIX}/hospitality",
        "forbidden_sibling_bc": [
            "hospitality_robotics_platform",
            "smart_hotel_platform",
            "autonomous_guest_service_platform",
            "hospitality_ai_intelligence_platform",
        ],
        "foundation_for_p216_q": True,
        "p216_j_agriculture_planned": True,
        "p216_m_space_planned": True,
        "p216_n_environmental_planned": True,
    }

def hospitality_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /robotics/hospitality",
        "GET /robotics/hospitality/vision",
        "GET /robotics/hospitality/domain",
        "GET /robotics/hospitality/bounded-contexts",
        "GET /robotics/hospitality/robotics",
        "GET /robotics/hospitality/smart-hotel",
        "GET /robotics/hospitality/guest-experience",
        "GET /robotics/hospitality/autonomous-services",
        "GET /robotics/hospitality/ai",
        "GET /robotics/hospitality/digital-twin",
        "GET /robotics/hospitality/knowledge-graph",
        "GET /robotics/hospitality/observability",
        "GET /robotics/hospitality/security",
        "GET /robotics/hospitality/cqrs",
        "GET /robotics/hospitality/events",
        "GET /robotics/hospitality/microservices",
        "GET /robotics/hospitality/integration",
        "GET /robotics/hospitality/deployment",
        "GET /robotics/hospitality/testing",
        "GET /robotics/hospitality/readiness",
    ], "retail_gate_routes": ["GET /robotics/retail", "GET /robotics/retail/readiness"]}
