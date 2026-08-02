"""P218-C Enterprise Space Intelligence Domain Architecture (DDD) — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P218-C"
ADR = 529
SOR = "space"
API_PREFIX = "/api/v1/space"
PRODUCT = "Enterprise Space Intelligence Domain Architecture (DDD), Bounded Contexts, Aggregates & Space Intelligence Domain Model"
CAPABILITY = "CAP-PLT-SP-001"
PRIMARY_CAPABILITY = (
    "Enable intelligent space mission discovery, prediction and orbital orchestration "
    "through an isolated DDD domain model inside MEOS."
)
CORE_DOMAIN_NAME = "Enterprise Space Intelligence Domain"
FABRIC = "meos_space_intelligence_domain_architecture_framework"
FOUNDATION_GATE = "P218"
MISSION_GATE = "P218-A"
STRATEGY_GATE = "P218-B"
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

CORE_DOMAINS = (
    "mission_intelligence", "orbital_intelligence", "satellite_intelligence", "navigation_intelligence",
    "space_ai", "scientific_intelligence", "space_economy", "space_security", "space_governance", "space_digital_twin",
)
SUPPORTING_DOMAINS = (
    {"id": "ground_operations", "purpose": "Ground segment operations and mission control support."},
    {"id": "space_communications", "purpose": "Deep-space and orbital communications intelligence."},
    {"id": "infrastructure_management", "purpose": "Space and ground infrastructure lifecycle."},
    {"id": "telemetry_management", "purpose": "Telemetry ingestion via Integration Platform ACL."},
    {"id": "resource_management", "purpose": "Space resource utilisation intelligence."},
    {"id": "identity_access", "purpose": "Identity via Core Platform."},
    {"id": "observability", "purpose": "Observability via Core Platform."},
    {"id": "compliance", "purpose": "Compliance via Policy Engine and Audit."},
)
GENERIC_DOMAINS = (
    "notification", "document_management", "workflow", "configuration",
    "audit", "reporting", "localization", "search",
)
BOUNDED_CONTEXTS = (
    {"id": "BC-01", "name": "Mission Management Context", "type": "CORE", "aggregate": "MissionAggregate", "purpose": "Mission lifecycle, planning, execution, monitoring and recovery.", "dependencies": ("workflow", "BC-02", "BC-03")},
    {"id": "BC-02", "name": "Orbital Operations Context", "type": "CORE", "aggregate": "OrbitAggregate", "purpose": "Orbit management, collision avoidance, optimisation and debris.", "dependencies": ("BC-01", "BC-03", "p215_z")},
    {"id": "BC-03", "name": "Satellite Fleet Context", "type": "CORE", "aggregate": "SatelliteAggregate", "purpose": "Satellite lifecycle, health monitoring and fleet operations.", "dependencies": ("BC-01", "BC-02")},
    {"id": "BC-04", "name": "Space AI Context", "type": "CORE", "aggregate": "AIModelAggregate", "purpose": "Reasoning, prediction and decision intents via P214-Z ACL only.", "dependencies": ("p214_z", "BC-01", "BC-08")},
    {"id": "BC-05", "name": "Scientific Research Context", "type": "SUPPORTING", "aggregate": "ResearchAggregate", "purpose": "Scientific missions, experiments, discovery and publication.", "dependencies": ("BC-01", "BC-04")},
    {"id": "BC-06", "name": "Space Economy Context", "type": "SUPPORTING", "aggregate": "ContractAggregate", "purpose": "Commercial services, contracts, marketplace and billing intents.", "dependencies": ("BC-01", "financial_kernel")},
    {"id": "BC-07", "name": "Space Security Context", "type": "SUPPORTING", "aggregate": "SecurityIncidentAggregate", "purpose": "Cybersecurity, mission security, threats and incidents.", "dependencies": ("policy_engine", "audit", "BC-01")},
    {"id": "BC-08", "name": "Space Digital Twin Context", "type": "SUPPORTING", "aggregate": "DigitalTwinAggregate", "purpose": "Simulation, prediction and digital representation of space assets.", "dependencies": ("BC-01", "BC-02", "BC-03", "BC-04")},
)
CONTEXT_MAP = (
    {"from": "mission_management", "to": "orbital_operations", "type": "customer_supplier"},
    {"from": "orbital_operations", "to": "satellite_fleet", "type": "shared_kernel_light"},
    {"from": "satellite_fleet", "to": "telemetry_via_integration", "type": "acl"},
    {"from": "space_ai", "to": "p214_z", "type": "conformist_acl"},
    {"from": "digital_twin", "to": "mission_management", "type": "published_language"},
    {"from": "scientific_research", "to": "space_ai", "type": "customer_supplier"},
    {"from": "space_economy", "to": "mission_management", "type": "open_host_service"},
    {"from": "space_security", "to": "all_space_contexts", "type": "conformist_policy"},
    {"from": "space_governance", "to": "all_space_contexts", "type": "acl_policy_workflow_audit"},
)
AGGREGATE_CATALOG = (
    {"id": "MissionAggregate", "bc": "BC-01", "consistency": "strong", "entities": ("Mission", "MissionObjective", "MissionPhase", "MissionTask", "MissionTimeline", "MissionAsset"), "value_objects": ("MissionId", "MissionStatus", "MissionPriority", "MissionType", "MissionWindow"), "commands": ("CreateMission", "ApproveMission", "StartMission"), "events": ("MissionCreatedEvent", "MissionApprovedEvent", "MissionStartedEvent")},
    {"id": "OrbitAggregate", "bc": "BC-02", "consistency": "strong", "entities": ("Orbit", "OrbitalPath", "OrbitalAsset", "CollisionAlert", "DebrisObject"), "value_objects": ("OrbitId", "OrbitalCoordinates", "VelocityVector", "OrbitalHealth"), "commands": ("CreateOrbit", "AdjustOrbit", "PredictCollision"), "events": ("OrbitCreatedEvent", "OrbitUpdatedEvent", "CollisionPredictedEvent")},
    {"id": "SatelliteAggregate", "bc": "BC-03", "consistency": "strong", "entities": ("Satellite", "Payload", "Subsystem", "HealthState", "Firmware"), "value_objects": ("SatelliteId", "SatelliteHealth", "PowerStatus", "CommunicationState"), "commands": ("RegisterSatellite", "ActivateSatellite", "RecoverSatellite"), "events": ("SatelliteRegisteredEvent", "SatelliteActivatedEvent", "SatelliteFailureDetectedEvent")},
    {"id": "AIModelAggregate", "bc": "BC-04", "consistency": "eventual", "entities": ("AIModelRef", "InferenceIntent", "Prediction", "Recommendation", "TrainingJobRef"), "value_objects": ("ModelVersion", "ConfidenceScore", "InferenceId"), "commands": ("RequestInference", "AcceptRecommendation"), "events": ("InferenceCompletedEvent", "PredictionGeneratedEvent", "DecisionRecommendedEvent"), "note": "inference_via_p214_z_only"},
    {"id": "ResearchAggregate", "bc": "BC-05", "consistency": "eventual", "entities": ("ResearchProject", "Experiment", "Observation", "Discovery", "Publication"), "value_objects": ("ExperimentId", "ObservationId", "ScientificConfidence"), "commands": ("StartExperiment", "ValidateDiscovery"), "events": ("ExperimentStartedEvent", "DiscoveryValidatedEvent", "ResearchPublishedEvent")},
    {"id": "ContractAggregate", "bc": "BC-06", "consistency": "eventual", "entities": ("Customer", "Partner", "Contract", "Invoice", "MarketplaceListing"), "value_objects": ("ContractId", "ServiceSla", "BillingIntent"), "commands": ("SignContract", "PublishListing"), "events": ("ContractSignedEvent", "MarketplacePublishedEvent", "InvoiceIssuedEvent")},
    {"id": "SecurityIncidentAggregate", "bc": "BC-07", "consistency": "strong", "entities": ("Threat", "Incident", "Policy", "RiskAssessment", "SecurityAlert"), "value_objects": ("ThreatId", "IncidentSeverity", "RiskScore"), "commands": ("DetectThreat", "ResolveIncident"), "events": ("ThreatDetectedEvent", "IncidentCreatedEvent", "IncidentResolvedEvent")},
    {"id": "DigitalTwinAggregate", "bc": "BC-08", "consistency": "eventual", "entities": ("DigitalTwin", "Scenario", "Simulation", "PredictionModel"), "value_objects": ("TwinId", "SimulationState", "PredictionHorizon"), "commands": ("CreateTwin", "RunSimulation"), "events": ("TwinCreatedEvent", "SimulationExecutedEvent", "PredictionUpdatedEvent")},
)
ENTERPRISE_ENTITIES = (
    {"id": "MissionEntity", "represents": "Enterprise space mission", "attributes": ("mission_id", "type", "status", "priority", "window", "assets")},
    {"id": "SatelliteEntity", "represents": "Satellite or spacecraft asset", "attributes": ("satellite_id", "health", "power", "comms", "payloads")},
    {"id": "OrbitEntity", "represents": "Orbital state and path", "attributes": ("orbit_id", "coordinates", "velocity", "health")},
    {"id": "SpaceIntelligenceEntity", "represents": "Space AI insight or prediction intent", "attributes": ("inference_id", "confidence", "model_ref", "decision")},
)
DOMAIN_RELATIONSHIPS = (
    {"from": "MissionAggregate", "relation": "MISSION_EXECUTES", "to": "SatelliteAggregate"},
    {"from": "SatelliteAggregate", "relation": "SATELLITE_OPERATES_IN", "to": "OrbitAggregate"},
    {"from": "OrbitAggregate", "relation": "ORBIT_SUPPORTS", "to": "MissionAggregate"},
    {"from": "AIModelAggregate", "relation": "AI_ANALYZES", "to": "MissionAggregate"},
    {"from": "DigitalTwinAggregate", "relation": "SIMULATION_PREDICTS", "to": "OrbitAggregate"},
    {"from": "SecurityIncidentAggregate", "relation": "THREAT_AFFECTS", "to": "SatelliteAggregate"},
    {"from": "SecurityIncidentAggregate", "relation": "POLICY_GOVERNS", "to": "AllSpaceContexts"},
    {"from": "ContractAggregate", "relation": "PARTNER_COLLABORATES_WITH", "to": "MissionAggregate"},
)
AGGREGATE_RULES = (
    "one_aggregate_one_consistency_boundary",
    "external_communication_via_domain_events",
    "cross_context_updates_asynchronous",
    "transaction_consistency_within_aggregate",
    "domain_ownership_per_bc",
    "independent_evolution",
    "event_publishing_required",
    "microservice_isolation",
    "never_cross_context_aggregate_mutation",
    "never_peer_domain_imports",
    "mission_orbit_satellite_strong_consistency",
    "research_twin_marketplace_eventual_consistency",
)
DOMAIN_SERVICES = (
    {"id": "MissionPlanningService", "responsibility": "Plan and validate mission windows", "dependencies": ("BC-01", "workflow"), "events": ("MissionCreatedEvent",)},
    {"id": "MissionExecutionService", "responsibility": "Execute gated mission commands", "dependencies": ("BC-01", "workflow"), "events": ("MissionStartedEvent",)},
    {"id": "OrbitOptimizationService", "responsibility": "Optimise orbits via Quantum ACL when required", "dependencies": ("BC-02", "p215_z"), "events": ("OrbitUpdatedEvent",)},
    {"id": "FleetManagementService", "responsibility": "Manage satellite fleet lifecycle", "dependencies": ("BC-03",), "events": ("SatelliteActivatedEvent",)},
    {"id": "PredictionService", "responsibility": "Prediction intents via P214-Z", "dependencies": ("BC-04", "p214_z"), "events": ("PredictionGeneratedEvent",)},
    {"id": "DecisionSupportService", "responsibility": "Decision recommendations with human oversight", "dependencies": ("BC-04", "workflow"), "events": ("DecisionRecommendedEvent",)},
    {"id": "ScientificReasoningService", "responsibility": "Scientific experiment reasoning", "dependencies": ("BC-05", "p214_z"), "events": ("DiscoveryValidatedEvent",)},
    {"id": "CollisionAvoidanceService", "responsibility": "Predict and avoid orbital collisions", "dependencies": ("BC-02", "p214_z"), "events": ("CollisionPredictedEvent", "CollisionAvoidedEvent")},
    {"id": "NavigationOptimizationService", "responsibility": "Navigation optimisation", "dependencies": ("BC-02", "p215_z"), "events": ("OrbitUpdatedEvent",)},
    {"id": "DigitalTwinSimulationService", "responsibility": "Run space digital twin simulations", "dependencies": ("BC-08",), "events": ("SimulationExecutedEvent",)},
    {"id": "SecurityRiskAssessmentService", "responsibility": "Assess space security risk via Policy Engine", "dependencies": ("BC-07", "policy_engine"), "events": ("ThreatDetectedEvent",)},
    {"id": "SpaceEconomyOptimizationService", "responsibility": "Optimise commercial space services", "dependencies": ("BC-06",), "events": ("MarketplacePublishedEvent",)},
)
REPOSITORIES = (
    {"id": "MissionRepository", "aggregate": "MissionAggregate", "responsibilities": ("aggregate_persistence", "state_reconstruction", "event_sourcing_support")},
    {"id": "OrbitRepository", "aggregate": "OrbitAggregate", "responsibilities": ("aggregate_persistence", "state_reconstruction", "event_sourcing_support")},
    {"id": "SatelliteRepository", "aggregate": "SatelliteAggregate", "responsibilities": ("aggregate_persistence", "state_reconstruction", "event_sourcing_support")},
    {"id": "ResearchRepository", "aggregate": "ResearchAggregate", "responsibilities": ("aggregate_persistence", "state_reconstruction", "event_sourcing_support")},
    {"id": "AIModelRepository", "aggregate": "AIModelAggregate", "responsibilities": ("intent_persistence", "model_ref_only", "event_sourcing_support")},
    {"id": "SecurityRepository", "aggregate": "SecurityIncidentAggregate", "responsibilities": ("aggregate_persistence", "state_reconstruction", "event_sourcing_support")},
    {"id": "DigitalTwinRepository", "aggregate": "DigitalTwinAggregate", "responsibilities": ("aggregate_persistence", "state_reconstruction", "event_sourcing_support")},
    {"id": "MarketplaceRepository", "aggregate": "ContractAggregate", "responsibilities": ("marketplace_projections", "listing_persistence")},
    {"id": "ContractRepository", "aggregate": "ContractAggregate", "responsibilities": ("contract_persistence", "billing_intent_refs")},
)
CORE_EVENTS = (
    {"name": "MissionCreatedEvent", "schema": "space.mission.created.v1", "owner": "BC-01", "consumers": "audit,analytics,workflow"},
    {"name": "MissionApprovedEvent", "schema": "space.mission.approved.v1", "owner": "BC-01", "consumers": "audit,notifications,orbital"},
    {"name": "OrbitUpdatedEvent", "schema": "space.orbit.updated.v1", "owner": "BC-02", "consumers": "audit,analytics,twin"},
    {"name": "CollisionPredictedEvent", "schema": "space.orbit.collision.predicted.v1", "owner": "BC-02", "consumers": "audit,notifications,security"},
    {"name": "SatelliteActivatedEvent", "schema": "space.satellite.activated.v1", "owner": "BC-03", "consumers": "audit,analytics,mission"},
    {"name": "PredictionGeneratedEvent", "schema": "space.ai.prediction.generated.v1", "owner": "BC-04", "consumers": "audit,analytics,decision"},
    {"name": "DiscoveryValidatedEvent", "schema": "space.research.discovery.validated.v1", "owner": "BC-05", "consumers": "audit,search,analytics"},
    {"name": "ContractSignedEvent", "schema": "space.economy.contract.signed.v1", "owner": "BC-06", "consumers": "audit,financial_kernel"},
    {"name": "ThreatDetectedEvent", "schema": "space.security.threat.detected.v1", "owner": "BC-07", "consumers": "audit,notifications,policy"},
    {"name": "SimulationExecutedEvent", "schema": "space.twin.simulation.executed.v1", "owner": "BC-08", "consumers": "analytics,ai,mission"},
)
COMMANDS = (
    "CreateMissionCommand", "ApproveMissionCommand", "AdjustOrbitCommand",
    "ActivateSatelliteCommand", "RequestSpaceInferenceCommand", "RunSpaceSimulationCommand",
)
QUERIES = (
    "GetMissionQuery", "GetOrbitStateQuery", "GetSatelliteHealthQuery",
    "GetSpacePredictionQuery", "GetDigitalTwinStateQuery",
)
MICROSERVICES = (
    {"id": "mission_management_service", "bc": "BC-01", "api": "/space/domain/missions", "db": "space_*", "events": ("MissionCreatedEvent",), "security": ("space.write",), "scaling": "mission_workers"},
    {"id": "orbital_operations_service", "bc": "BC-02", "api": "/space/domain/orbits", "db": "space_*", "events": ("OrbitUpdatedEvent",), "security": ("space.write",), "scaling": "orbital_workers"},
    {"id": "satellite_fleet_service", "bc": "BC-03", "api": "/space/domain/satellites", "db": "space_*", "events": ("SatelliteActivatedEvent",), "security": ("space.write",), "scaling": "fleet_workers"},
    {"id": "space_ai_service", "bc": "BC-04", "api": "/space/domain/space-ai", "db": "space_*", "events": ("PredictionGeneratedEvent",), "security": ("space.ai.infer",), "scaling": "ai_intent_workers"},
    {"id": "scientific_research_service", "bc": "BC-05", "api": "/space/domain/research", "db": "space_*", "events": ("DiscoveryValidatedEvent",), "security": ("space.write",), "scaling": "research_workers"},
    {"id": "space_economy_service", "bc": "BC-06", "api": "/space/domain/economy", "db": "space_*", "events": ("ContractSignedEvent",), "security": ("space.write",), "scaling": "economy_workers"},
    {"id": "space_security_service", "bc": "BC-07", "api": "/space/domain/security", "db": "space_*", "events": ("ThreatDetectedEvent",), "security": ("space.admin",), "scaling": "security_replicas"},
    {"id": "space_digital_twin_service", "bc": "BC-08", "api": "/space/domain/twins", "db": "space_*", "events": ("SimulationExecutedEvent",), "security": ("space.read",), "scaling": "twin_workers"},
)
KNOWLEDGE_GRAPH = {
    "present_required": True,
    "nodes": ("Mission", "Satellite", "Orbit", "Spacecraft", "Experiment", "Research", "AIModel", "Prediction", "Threat", "Policy", "Partner", "Contract", "DigitalTwin", "Simulation"),
    "relationships": ("MISSION_EXECUTES", "SATELLITE_OPERATES_IN", "ORBIT_SUPPORTS", "AI_ANALYZES", "SIMULATION_PREDICTS", "THREAT_AFFECTS", "POLICY_GOVERNS", "PARTNER_COLLABORATES_WITH"),
}
DIGITAL_TWIN_MAPPING = {
    "present_required": True,
    "states": ("real_state", "desired_state", "predicted_state", "historical_state", "simulation_state", "risk_state", "optimization_state"),
    "aggregates_expose_all_states": True,
}
EVENT_STORMING = {
    "present_required": True,
    "commands": list(COMMANDS),
    "events": [e["name"] for e in CORE_EVENTS],
    "policies": ("human_mission_oversight", "space_cybersecurity", "space_sustainability", "gated_autonomy"),
    "read_models": ("mission_board", "fleet_health", "orbital_traffic", "threat_dashboard"),
    "external_systems": ("integration_platform", "p214_z", "p215_z", "p216_z", "p217_z"),
    "actors": ("mission_command", "operators", "scientists", "security", "partners"),
    "decision_points": ("mission_approval", "collision_manoeuvre", "autonomy_gate"),
    "sagas": ("mission_execution_saga", "collision_avoidance_saga", "incident_response_saga"),
    "compensating_actions": ("mission_rollback", "orbit_reversion", "incident_containment"),
}
API_SURFACES = (
    "/api/v1/space/domain",
    "/api/v1/space/domain/strategy",
    "/api/v1/space/domain/bounded-contexts",
    "/api/v1/space/domain/aggregates",
    "/api/v1/space/domain/entities",
    "/api/v1/space/domain/value-objects",
    "/api/v1/space/domain/services",
    "/api/v1/space/domain/repositories",
    "/api/v1/space/domain/events",
    "/api/v1/space/domain/cqrs",
    "/api/v1/space/domain/microservices",
    "/api/v1/space/domain/integration",
    "/api/v1/space/domain/relationships",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
SECURITY = {
    "present_required": True, "zero_trust": True, "via_identity": True, "via_policy_engine": True,
    "via_workflow": True, "via_audit": True,
    "never_replace_p218_foundation": True, "never_replace_p218_a_mission": True,
    "never_replace_p218_b_strategy": True, "never_replace_core_platform": True,
    "never_replace_ai_platform": True, "never_replace_p215_z": True, "never_replace_p216_z": True,
    "never_replace_biotechnology": True,
    "never_skip_human_mission_oversight_strategy": True,
    "never_skip_space_cybersecurity_strategy": True,
    "never_skip_space_sustainability_strategy": True,
    "never_opaque_mission_critical_strategy": True,
    "never_ungated_autonomous_mission_strategy": True,
    "never_cross_context_aggregate_mutation": True, "never_peer_domain_imports": True,
    "module_local_llm_forbidden": True,
}
INTEGRATION = {
    "present_required": True,
    "targets": ("p214z_ai_master", "p215z_quantum_supreme", "p216z_robotics_supreme", "p217z_bio_nexus", "meos_knowledge_graph", "meos_digital_twin", "policy_engine", "workflow", "audit", "integration_platform"),
    "mechanisms": ("api_gateway", "event_bus", "streaming_platform", "knowledge_graph", "acl_peer_ids_only"),
    "via_p214_z": True, "via_p215_z": True, "via_p216_z": True, "via_p217": True,
}
DEPLOYMENT = {"present_required": True, "cloud_native": True, "components": ("domain_services_cluster", "bc_workers", "event_outbox", "domain_observability")}
TESTING = (
    "domain_strategy_testing", "bounded_context_isolation_testing", "aggregate_invariant_testing",
    "domain_service_testing", "repository_boundary_testing", "event_contract_testing",
    "cqrs_alignment_testing", "microservice_boundary_testing",
)
QUALITY_GATES_REJECT_IF = (
    "space_core_domain_is_missing", "supporting_domains_are_missing", "generic_domains_are_missing",
    "bounded_context_map_is_missing", "aggregates_are_missing", "entities_are_missing",
    "value_objects_are_missing", "domain_services_are_missing", "repository_boundaries_are_missing",
    "domain_events_are_missing", "knowledge_graph_mapping_is_missing", "digital_twin_mapping_is_missing",
    "cqrs_architecture_is_missing", "event_architecture_is_missing",
    "microservices_architecture_is_missing", "api_first_architecture_is_missing",
    "cloud_native_deployment_is_missing", "sibling_space_bc",
    "replace_p218_foundation", "replace_p218_a_mission", "replace_p218_b_strategy",
    "cross_context_aggregate_mutation", "peer_domain_imports",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Space Intelligence Domain Architecture Framework",
        "core_domain": CORE_DOMAIN_NAME, "primary_capability": PRIMARY_CAPABILITY,
        "builds_on_p218": True, "builds_on_p218_a": True, "builds_on_p218_b": True,
        "builds_on_p217_z": True, "builds_on_p216_z": True, "builds_on_p215_z": True, "builds_on_p214_z": True,
        "never_replace_p218_foundation": True, "never_replace_p218_a_mission": True,
        "never_replace_p218_b_strategy": True,
        "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE, "strategy_gate": STRATEGY_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
    }

def domain_strategy() -> dict[str, Any]:
    return {
        "present_required": True, "core_domain": CORE_DOMAIN_NAME, "primary_capability": PRIMARY_CAPABILITY,
        "core_domains": list(CORE_DOMAINS), "supporting_domains": [dict(d) for d in SUPPORTING_DOMAINS],
        "generic_domains": list(GENERIC_DOMAINS),
        "supporting_count": len(SUPPORTING_DOMAINS), "generic_count": len(GENERIC_DOMAINS),
    }

def bounded_contexts() -> dict[str, Any]:
    return {"present_required": True, "contexts": [dict(c) for c in BOUNDED_CONTEXTS], "context_count": len(BOUNDED_CONTEXTS), "context_map": [dict(m) for m in CONTEXT_MAP]}

def aggregates() -> dict[str, Any]:
    return {"present_required": True, "aggregates": [dict(a) for a in AGGREGATE_CATALOG], "aggregate_count": len(AGGREGATE_CATALOG), "rules": list(AGGREGATE_RULES)}

def entities() -> dict[str, Any]:
    nested = []
    for a in AGGREGATE_CATALOG:
        nested.append({"aggregate": a["id"], "entities": list(a["entities"])})
    return {"present_required": True, "enterprise_entities": [dict(e) for e in ENTERPRISE_ENTITIES], "aggregate_entities": nested, "enterprise_count": len(ENTERPRISE_ENTITIES)}

def value_objects() -> dict[str, Any]:
    vos = []
    for a in AGGREGATE_CATALOG:
        for vo in a["value_objects"]:
            vos.append({"aggregate": a["id"], "value_object": vo})
    return {"present_required": True, "value_objects": vos, "value_object_count": len(vos)}

def domain_services() -> dict[str, Any]:
    return {"present_required": True, "services": [dict(s) for s in DOMAIN_SERVICES], "service_count": len(DOMAIN_SERVICES)}

def repositories() -> dict[str, Any]:
    return {"present_required": True, "repositories": [dict(r) for r in REPOSITORIES], "repository_count": len(REPOSITORIES)}

def events() -> dict[str, Any]:
    return {"present_required": True, "core_events": [dict(e) for e in CORE_EVENTS], "core_event_count": len(CORE_EVENTS)}

def cqrs() -> dict[str, Any]:
    return {"present_required": True, "commands": list(COMMANDS), "queries": list(QUERIES)}

def microservices() -> dict[str, Any]:
    return {"present_required": True, "services": [dict(s) for s in MICROSERVICES], "service_count": len(MICROSERVICES)}

def integration() -> dict[str, Any]:
    return dict(INTEGRATION)

def relationships() -> dict[str, Any]:
    return {"present_required": True, "relationships": [dict(r) for r in DOMAIN_RELATIONSHIPS], "relationship_count": len(DOMAIN_RELATIONSHIPS), "knowledge_graph": dict(KNOWLEDGE_GRAPH), "digital_twin_mapping": dict(DIGITAL_TWIN_MAPPING), "event_storming": dict(EVENT_STORMING)}

def api() -> dict[str, Any]:
    return {"surfaces": list(API_SURFACES), "styles": list(API_STYLES), "api_first_present_required": True}

def security() -> dict[str, Any]:
    return dict(SECURITY)

def deployment() -> dict[str, Any]:
    return dict(DEPLOYMENT)

def testing() -> dict[str, Any]:
    return {"suites": list(TESTING)}

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p218_d": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "primary_capability": PRIMARY_CAPABILITY, "core_domain": CORE_DOMAIN_NAME, "principle": PRIMARY_CAPABILITY,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "bio_gate": BIO_GATE,
        "robotics_gate": ROBOTICS_GATE, "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": ["P218", "P218-A", "P218-B", "P217-Z", "P216-Z", "P215-Z", "P214-Z", "ADR-526", "ADR-527", "ADR-528"],
        "vision": vision_pack(), "domain_strategy": domain_strategy(),
        "bounded_contexts": bounded_contexts(), "aggregates": aggregates(),
        "entities": entities(), "value_objects": value_objects(),
        "domain_services": domain_services(), "repositories": repositories(),
        "events": events(), "cqrs": cqrs(), "microservices": microservices(),
        "integration": integration(), "relationships": relationships(),
        "api": api(), "security": security(), "deployment": deployment(),
        "testing": testing(), "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "space_core_domain_present_required": True,
        "supporting_domains_present_required": True,
        "generic_domains_present_required": True,
        "bounded_context_map_present_required": True,
        "aggregates_present_required": True,
        "entities_present_required": True,
        "value_objects_present_required": True,
        "domain_services_present_required": True,
        "repository_boundaries_present_required": True,
        "domain_events_present_required": True,
        "knowledge_graph_mapping_present_required": True,
        "digital_twin_mapping_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "cloud_native_deployment_present_required": True,
        "sibling_space_bc_forbidden": True,
        "never_replace_p218_foundation": True,
        "never_replace_p218_a_mission": True,
        "never_replace_p218_b_strategy": True,
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
        "never_cross_context_aggregate_mutation": True,
        "never_peer_domain_imports": True,
        "module_local_llm_forbidden": True,
        "builds_on_p218": True, "builds_on_p218_a": True, "builds_on_p218_b": True,
        "builds_on_p217_z": True, "builds_on_p216_z": True, "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p217": True, "via_p216_z": True, "via_p215_z": True, "via_p214_z": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "api_prefix": f"{API_PREFIX}/domain",
        "forbidden_sibling_bc": [
            "space_domain_platform",
            "space_ddd_platform",
            "space_intelligence_domain_platform",
        ],
        "foundation_for_p218_d": True,
    }

def domain_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /space/domain",
        "GET /space/domain/strategy",
        "GET /space/domain/bounded-contexts",
        "GET /space/domain/aggregates",
        "GET /space/domain/entities",
        "GET /space/domain/value-objects",
        "GET /space/domain/services",
        "GET /space/domain/repositories",
        "GET /space/domain/events",
        "GET /space/domain/cqrs",
        "GET /space/domain/microservices",
        "GET /space/domain/integration",
        "GET /space/domain/relationships",
        "GET /space/domain/readiness",
    ], "foundation_gate_routes": ["GET /space/foundation", "GET /space/foundation/readiness"],
       "mission_gate_routes": ["GET /space/mission", "GET /space/mission/readiness"],
       "strategy_gate_routes": ["GET /space/strategy", "GET /space/strategy/readiness"]}
