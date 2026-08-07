"""Space presentation router — P218 Space Intelligence Fabric."""
from __future__ import annotations
from typing import Annotated
from fastapi import APIRouter, Depends
from contexts.space.container import get_space_service
from contexts.identity.presentation.dependencies import require_permissions

space_router = APIRouter(
    prefix="/space",
    tags=["Enterprise Space Intelligence, Space AI, Orbital Civilization & Autonomous Space Operations"],
)


@space_router.get("/catalog")
async def catalog(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": (await get_space_service().list_catalog()).unwrap()}


@space_router.get("/foundation")
async def foundation_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_foundation()}


@space_router.get("/foundation/vision")
async def foundation_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_vision()}


@space_router.get("/foundation/domain")
async def foundation_domain(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_domain()}


@space_router.get("/foundation/bounded-contexts")
async def foundation_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_bounded_contexts()}


@space_router.get("/foundation/architecture")
async def foundation_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_architecture()}


@space_router.get("/foundation/space-ai")
async def foundation_space_ai(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_space_ai()}


@space_router.get("/foundation/orbital-civilization")
async def foundation_orbital_civilization(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_orbital_civilization()}


@space_router.get("/foundation/autonomous-operations")
async def foundation_autonomous_operations(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_autonomous_operations()}


@space_router.get("/foundation/digital-twin")
async def foundation_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_digital_twin()}


@space_router.get("/foundation/knowledge-graph")
async def foundation_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_knowledge_graph()}


@space_router.get("/foundation/agents")
async def foundation_agents(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_agents()}


@space_router.get("/foundation/governance")
async def foundation_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_governance()}


@space_router.get("/foundation/observability")
async def foundation_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_observability()}


@space_router.get("/foundation/security")
async def foundation_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_security()}


@space_router.get("/foundation/cqrs")
async def foundation_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_cqrs()}


@space_router.get("/foundation/events")
async def foundation_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_events()}


@space_router.get("/foundation/microservices")
async def foundation_microservices(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_microservices()}


@space_router.get("/foundation/integration")
async def foundation_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_integration()}


@space_router.get("/foundation/deployment")
async def foundation_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_deployment()}


@space_router.get("/foundation/roadmap")
async def foundation_roadmap(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_roadmap()}


@space_router.get("/foundation/readiness")
async def foundation_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().foundation_readiness()}


@space_router.get("/mission")
async def mission_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_mission()}


@space_router.get("/mission/vision")
async def mission_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_vision()}


@space_router.get("/mission/objectives")
async def mission_objectives(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_objectives()}


@space_router.get("/mission/scope")
async def mission_scope(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_scope()}


@space_router.get("/mission/capabilities")
async def mission_capabilities(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_capabilities()}


@space_router.get("/mission/value-streams")
async def mission_value_streams(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_value_streams()}


@space_router.get("/mission/maturity")
async def mission_maturity(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_maturity()}


@space_router.get("/mission/roadmap")
async def mission_roadmap(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_roadmap()}


@space_router.get("/mission/governance")
async def mission_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_governance()}


@space_router.get("/mission/integration")
async def mission_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_integration()}


@space_router.get("/mission/readiness")
async def mission_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_readiness()}


@space_router.get("/strategy")
async def strategy_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_strategy()}


@space_router.get("/strategy/layers")
async def strategy_layers(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().strategy_layers()}


@space_router.get("/strategy/capabilities")
async def strategy_capabilities(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().strategy_capabilities()}


@space_router.get("/strategy/operating-model")
async def strategy_operating_model(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().strategy_operating_model()}


@space_router.get("/strategy/services")
async def strategy_services(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().strategy_services()}


@space_router.get("/strategy/organization")
async def strategy_organization(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().strategy_organization()}


@space_router.get("/strategy/governance")
async def strategy_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().strategy_governance()}


@space_router.get("/strategy/data")
async def strategy_data(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().strategy_data()}


@space_router.get("/strategy/integration")
async def strategy_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().strategy_integration()}


@space_router.get("/strategy/security")
async def strategy_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().strategy_security()}


@space_router.get("/strategy/scalability")
async def strategy_scalability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().strategy_scalability()}


@space_router.get("/strategy/maturity")
async def strategy_maturity(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().strategy_maturity()}


@space_router.get("/strategy/roadmap")
async def strategy_roadmap(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().strategy_roadmap()}


@space_router.get("/strategy/cqrs")
async def strategy_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().strategy_cqrs()}


@space_router.get("/strategy/events")
async def strategy_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().strategy_events()}


@space_router.get("/strategy/readiness")
async def strategy_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().strategy_readiness()}


@space_router.get("/domain")
async def domain_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_domain()}


@space_router.get("/domain/strategy")
async def domain_strategy(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().domain_strategy()}


@space_router.get("/domain/bounded-contexts")
async def domain_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().domain_bounded_contexts()}


@space_router.get("/domain/aggregates")
async def domain_aggregates(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().domain_aggregates()}


@space_router.get("/domain/entities")
async def domain_entities(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().domain_entities()}


@space_router.get("/domain/value-objects")
async def domain_value_objects(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().domain_value_objects()}


@space_router.get("/domain/services")
async def domain_services(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().domain_services()}


@space_router.get("/domain/repositories")
async def domain_repositories(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().domain_repositories()}


@space_router.get("/domain/events")
async def domain_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().domain_events()}


@space_router.get("/domain/cqrs")
async def domain_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().domain_cqrs()}


@space_router.get("/domain/microservices")
async def domain_microservices(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().domain_microservices()}


@space_router.get("/domain/integration")
async def domain_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().domain_integration()}


@space_router.get("/domain/relationships")
async def domain_relationships(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().domain_relationships()}


@space_router.get("/domain/readiness")
async def domain_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().domain_readiness()}


@space_router.get("/infrastructure")
async def infrastructure_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_infrastructure()}


@space_router.get("/infrastructure/layers")
async def infrastructure_layers(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().infrastructure_layers()}


@space_router.get("/infrastructure/ground-segment")
async def infrastructure_ground_segment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().infrastructure_ground_segment()}


@space_router.get("/infrastructure/mission-control")
async def infrastructure_mission_control(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().infrastructure_mission_control()}


@space_router.get("/infrastructure/cloud")
async def infrastructure_cloud(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().infrastructure_cloud()}


@space_router.get("/infrastructure/network")
async def infrastructure_network(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().infrastructure_network()}


@space_router.get("/infrastructure/data")
async def infrastructure_data(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().infrastructure_data()}


@space_router.get("/infrastructure/digital-twin")
async def infrastructure_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().infrastructure_digital_twin()}


@space_router.get("/infrastructure/security")
async def infrastructure_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().infrastructure_security()}


@space_router.get("/infrastructure/platform")
async def infrastructure_platform(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().infrastructure_platform()}


@space_router.get("/infrastructure/observability")
async def infrastructure_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().infrastructure_observability()}


@space_router.get("/infrastructure/resilience")
async def infrastructure_resilience(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().infrastructure_resilience()}


@space_router.get("/infrastructure/integration")
async def infrastructure_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().infrastructure_integration()}


@space_router.get("/infrastructure/deployment")
async def infrastructure_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().infrastructure_deployment()}


@space_router.get("/infrastructure/testing")
async def infrastructure_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().infrastructure_testing()}


@space_router.get("/infrastructure/cqrs")
async def infrastructure_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().infrastructure_cqrs()}


@space_router.get("/infrastructure/events")
async def infrastructure_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().infrastructure_events()}


@space_router.get("/infrastructure/readiness")
async def infrastructure_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().infrastructure_readiness()}


@space_router.get("/space-ai")
async def space_ai_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_space_ai()}


@space_router.get("/space-ai/vision")
async def space_ai_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().space_ai_vision()}


@space_router.get("/space-ai/architecture")
async def space_ai_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().space_ai_architecture()}


@space_router.get("/space-ai/foundation-models")
async def space_ai_foundation_models(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().space_ai_foundation_models()}


@space_router.get("/space-ai/engine")
async def space_ai_engine(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().space_ai_engine()}


@space_router.get("/space-ai/mission-intelligence")
async def space_ai_mission_intelligence(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().space_ai_mission_intelligence()}


@space_router.get("/space-ai/decision")
async def space_ai_decision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().space_ai_decision()}


@space_router.get("/space-ai/agents")
async def space_ai_agents(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().space_ai_agents()}


@space_router.get("/space-ai/knowledge-graph")
async def space_ai_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().space_ai_knowledge_graph()}


@space_router.get("/space-ai/lifecycle")
async def space_ai_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().space_ai_lifecycle()}


@space_router.get("/space-ai/governance")
async def space_ai_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().space_ai_governance()}


@space_router.get("/space-ai/security")
async def space_ai_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().space_ai_security()}


@space_router.get("/space-ai/integration")
async def space_ai_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().space_ai_integration()}


@space_router.get("/space-ai/deployment")
async def space_ai_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().space_ai_deployment()}


@space_router.get("/space-ai/testing")
async def space_ai_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().space_ai_testing()}


@space_router.get("/space-ai/cqrs")
async def space_ai_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().space_ai_cqrs()}


@space_router.get("/space-ai/events")
async def space_ai_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().space_ai_events()}


@space_router.get("/space-ai/readiness")
async def space_ai_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().space_ai_readiness()}


@space_router.get("/satellite")
async def satellite_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_satellite()}


@space_router.get("/satellite/vision")
async def satellite_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().satellite_vision()}


@space_router.get("/satellite/architecture")
async def satellite_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().satellite_architecture()}


@space_router.get("/satellite/lifecycle")
async def satellite_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().satellite_lifecycle()}


@space_router.get("/satellite/constellation")
async def satellite_constellation(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().satellite_constellation()}


@space_router.get("/satellite/orbital-assets")
async def satellite_orbital_assets(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().satellite_orbital_assets()}


@space_router.get("/satellite/payload")
async def satellite_payload(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().satellite_payload()}


@space_router.get("/satellite/satellite-ai")
async def satellite_satellite_ai(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().satellite_satellite_ai()}


@space_router.get("/satellite/digital-twin")
async def satellite_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().satellite_digital_twin()}


@space_router.get("/satellite/observability")
async def satellite_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().satellite_observability()}


@space_router.get("/satellite/governance")
async def satellite_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().satellite_governance()}


@space_router.get("/satellite/security")
async def satellite_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().satellite_security()}


@space_router.get("/satellite/integration")
async def satellite_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().satellite_integration()}


@space_router.get("/satellite/deployment")
async def satellite_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().satellite_deployment()}


@space_router.get("/satellite/testing")
async def satellite_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().satellite_testing()}


@space_router.get("/satellite/cqrs")
async def satellite_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().satellite_cqrs()}


@space_router.get("/satellite/events")
async def satellite_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().satellite_events()}


@space_router.get("/satellite/readiness")
async def satellite_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().satellite_readiness()}


@space_router.get("/orbital")
async def orbital_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_orbital()}


@space_router.get("/orbital/vision")
async def orbital_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().orbital_vision()}


@space_router.get("/orbital/architecture")
async def orbital_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().orbital_architecture()}


@space_router.get("/orbital/ssa")
async def orbital_ssa(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().orbital_ssa()}


@space_router.get("/orbital/traffic")
async def orbital_traffic(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().orbital_traffic()}


@space_router.get("/orbital/collision-avoidance")
async def orbital_collision_avoidance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().orbital_collision_avoidance()}


@space_router.get("/orbital/debris")
async def orbital_debris(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().orbital_debris()}


@space_router.get("/orbital/digital-twin")
async def orbital_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().orbital_digital_twin()}


@space_router.get("/orbital/knowledge-graph")
async def orbital_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().orbital_knowledge_graph()}


@space_router.get("/orbital/ai-autonomy")
async def orbital_ai_autonomy(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().orbital_ai_autonomy()}


@space_router.get("/orbital/observability")
async def orbital_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().orbital_observability()}


@space_router.get("/orbital/governance")
async def orbital_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().orbital_governance()}


@space_router.get("/orbital/security")
async def orbital_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().orbital_security()}


@space_router.get("/orbital/integration")
async def orbital_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().orbital_integration()}


@space_router.get("/orbital/deployment")
async def orbital_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().orbital_deployment()}


@space_router.get("/orbital/testing")
async def orbital_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().orbital_testing()}


@space_router.get("/orbital/cqrs")
async def orbital_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().orbital_cqrs()}


@space_router.get("/orbital/events")
async def orbital_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().orbital_events()}


@space_router.get("/orbital/readiness")
async def orbital_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().orbital_readiness()}


@space_router.get("/communications")
async def communications_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_communications()}


@space_router.get("/communications/vision")
async def communications_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().communications_vision()}


@space_router.get("/communications/architecture")
async def communications_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().communications_architecture()}


@space_router.get("/communications/dsn")
async def communications_dsn(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().communications_dsn()}


@space_router.get("/communications/inter-satellite")
async def communications_inter_satellite(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().communications_inter_satellite()}


@space_router.get("/communications/laser")
async def communications_laser(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().communications_laser()}


@space_router.get("/communications/mission-services")
async def communications_mission_services(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().communications_mission_services()}


@space_router.get("/communications/network-ai")
async def communications_network_ai(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().communications_network_ai()}


@space_router.get("/communications/digital-twin")
async def communications_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().communications_digital_twin()}


@space_router.get("/communications/observability")
async def communications_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().communications_observability()}


@space_router.get("/communications/governance")
async def communications_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().communications_governance()}


@space_router.get("/communications/security")
async def communications_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().communications_security()}


@space_router.get("/communications/integration")
async def communications_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().communications_integration()}


@space_router.get("/communications/deployment")
async def communications_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().communications_deployment()}


@space_router.get("/communications/testing")
async def communications_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().communications_testing()}


@space_router.get("/communications/cqrs")
async def communications_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().communications_cqrs()}


@space_router.get("/communications/events")
async def communications_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().communications_events()}


@space_router.get("/communications/readiness")
async def communications_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().communications_readiness()}


@space_router.get("/navigation")
async def navigation_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_navigation()}


@space_router.get("/navigation/vision")
async def navigation_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().navigation_vision()}


@space_router.get("/navigation/architecture")
async def navigation_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().navigation_architecture()}


@space_router.get("/navigation/gnss")
async def navigation_gnss(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().navigation_gnss()}


@space_router.get("/navigation/autonomous")
async def navigation_autonomous(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().navigation_autonomous()}


@space_router.get("/navigation/trajectory")
async def navigation_trajectory(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().navigation_trajectory()}


@space_router.get("/navigation/gnc")
async def navigation_gnc(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().navigation_gnc()}


@space_router.get("/navigation/navigation-ai")
async def navigation_navigation_ai(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().navigation_navigation_ai()}


@space_router.get("/navigation/digital-twin")
async def navigation_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().navigation_digital_twin()}


@space_router.get("/navigation/observability")
async def navigation_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().navigation_observability()}


@space_router.get("/navigation/governance")
async def navigation_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().navigation_governance()}


@space_router.get("/navigation/security")
async def navigation_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().navigation_security()}


@space_router.get("/navigation/integration")
async def navigation_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().navigation_integration()}


@space_router.get("/navigation/deployment")
async def navigation_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().navigation_deployment()}


@space_router.get("/navigation/testing")
async def navigation_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().navigation_testing()}


@space_router.get("/navigation/cqrs")
async def navigation_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().navigation_cqrs()}


@space_router.get("/navigation/events")
async def navigation_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().navigation_events()}


@space_router.get("/navigation/readiness")
async def navigation_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().navigation_readiness()}


@space_router.get("/mission-intel")
async def mission_intel_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_mission_intel()}


@space_router.get("/mission-intel/vision")
async def mission_intel_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_intel_vision()}


@space_router.get("/mission-intel/architecture")
async def mission_intel_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_intel_architecture()}


@space_router.get("/mission-intel/lifecycle")
async def mission_intel_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_intel_lifecycle()}


@space_router.get("/mission-intel/planning")
async def mission_intel_planning(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_intel_planning()}


@space_router.get("/mission-intel/execution")
async def mission_intel_execution(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_intel_execution()}


@space_router.get("/mission-intel/mission-ai")
async def mission_intel_mission_ai(
    _user: Annotated[dict, Depends(require_permissions("space.ai.read"))],
) -> dict:
    return {"data": get_space_service().mission_intel_mission_ai()}


@space_router.get("/mission-intel/resources")
async def mission_intel_resources(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_intel_resources()}


@space_router.get("/mission-intel/digital-twin")
async def mission_intel_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_intel_digital_twin()}


@space_router.get("/mission-intel/observability")
async def mission_intel_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_intel_observability()}


@space_router.get("/mission-intel/governance")
async def mission_intel_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_intel_governance()}


@space_router.get("/mission-intel/security")
async def mission_intel_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_intel_security()}


@space_router.get("/mission-intel/integration")
async def mission_intel_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_intel_integration()}


@space_router.get("/mission-intel/deployment")
async def mission_intel_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_intel_deployment()}


@space_router.get("/mission-intel/testing")
async def mission_intel_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_intel_testing()}


@space_router.get("/mission-intel/cqrs")
async def mission_intel_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_intel_cqrs()}


@space_router.get("/mission-intel/events")
async def mission_intel_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_intel_events()}


@space_router.get("/mission-intel/readiness")
async def mission_intel_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().mission_intel_readiness()}


@space_router.get("/scientific")
async def scientific_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_scientific()}


@space_router.get("/scientific/vision")
async def scientific_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().scientific_vision()}


@space_router.get("/scientific/architecture")
async def scientific_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().scientific_architecture()}


@space_router.get("/scientific/lifecycle")
async def scientific_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().scientific_lifecycle()}


@space_router.get("/scientific/research")
async def scientific_research(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().scientific_research()}


@space_router.get("/scientific/discovery")
async def scientific_discovery(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().scientific_discovery()}


@space_router.get("/scientific/laboratory")
async def scientific_laboratory(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().scientific_laboratory()}


@space_router.get("/scientific/scientific-ai")
async def scientific_scientific_ai(
    _user: Annotated[dict, Depends(require_permissions("space.ai.read"))],
) -> dict:
    return {"data": get_space_service().scientific_scientific_ai()}


@space_router.get("/scientific/experiment")
async def scientific_experiment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().scientific_experiment()}


@space_router.get("/scientific/digital-twin")
async def scientific_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().scientific_digital_twin()}


@space_router.get("/scientific/observability")
async def scientific_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().scientific_observability()}


@space_router.get("/scientific/governance")
async def scientific_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().scientific_governance()}


@space_router.get("/scientific/security")
async def scientific_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().scientific_security()}


@space_router.get("/scientific/integration")
async def scientific_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().scientific_integration()}


@space_router.get("/scientific/deployment")
async def scientific_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().scientific_deployment()}


@space_router.get("/scientific/testing")
async def scientific_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().scientific_testing()}


@space_router.get("/scientific/cqrs")
async def scientific_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().scientific_cqrs()}


@space_router.get("/scientific/events")
async def scientific_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().scientific_events()}


@space_router.get("/scientific/readiness")
async def scientific_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().scientific_readiness()}


@space_router.get("/exploration")
async def exploration_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_exploration()}


@space_router.get("/exploration/vision")
async def exploration_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().exploration_vision()}


@space_router.get("/exploration/architecture")
async def exploration_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().exploration_architecture()}


@space_router.get("/exploration/lifecycle")
async def exploration_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().exploration_lifecycle()}


@space_router.get("/exploration/lunar")
async def exploration_lunar(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().exploration_lunar()}


@space_router.get("/exploration/mars")
async def exploration_mars(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().exploration_mars()}


@space_router.get("/exploration/deep-space")
async def exploration_deep_space(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().exploration_deep_space()}


@space_router.get("/exploration/exploration-ai")
async def exploration_exploration_ai(
    _user: Annotated[dict, Depends(require_permissions("space.ai.read"))],
) -> dict:
    return {"data": get_space_service().exploration_exploration_ai()}


@space_router.get("/exploration/autonomy")
async def exploration_autonomy(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().exploration_autonomy()}


@space_router.get("/exploration/digital-twin")
async def exploration_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().exploration_digital_twin()}


@space_router.get("/exploration/observability")
async def exploration_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().exploration_observability()}


@space_router.get("/exploration/governance")
async def exploration_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().exploration_governance()}


@space_router.get("/exploration/security")
async def exploration_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().exploration_security()}


@space_router.get("/exploration/integration")
async def exploration_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().exploration_integration()}


@space_router.get("/exploration/deployment")
async def exploration_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().exploration_deployment()}


@space_router.get("/exploration/testing")
async def exploration_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().exploration_testing()}


@space_router.get("/exploration/cqrs")
async def exploration_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().exploration_cqrs()}


@space_router.get("/exploration/events")
async def exploration_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().exploration_events()}


@space_router.get("/exploration/readiness")
async def exploration_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().exploration_readiness()}


@space_router.get("/manufacturing")
async def manufacturing_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_manufacturing()}


@space_router.get("/manufacturing/vision")
async def manufacturing_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_vision()}


@space_router.get("/manufacturing/architecture")
async def manufacturing_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_architecture()}


@space_router.get("/manufacturing/lifecycle")
async def manufacturing_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_lifecycle()}


@space_router.get("/manufacturing/in-orbit")
async def manufacturing_in_orbit(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_in_orbit()}


@space_router.get("/manufacturing/industrial")
async def manufacturing_industrial(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_industrial()}


@space_router.get("/manufacturing/autonomy")
async def manufacturing_autonomy(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_autonomy()}


@space_router.get("/manufacturing/manufacturing-ai")
async def manufacturing_manufacturing_ai(
    _user: Annotated[dict, Depends(require_permissions("space.ai.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_manufacturing_ai()}


@space_router.get("/manufacturing/materials")
async def manufacturing_materials(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_materials()}


@space_router.get("/manufacturing/robotics")
async def manufacturing_robotics(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_robotics()}


@space_router.get("/manufacturing/digital-twin")
async def manufacturing_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_digital_twin()}


@space_router.get("/manufacturing/knowledge-graph")
async def manufacturing_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_knowledge_graph()}


@space_router.get("/manufacturing/observability")
async def manufacturing_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_observability()}


@space_router.get("/manufacturing/governance")
async def manufacturing_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_governance()}


@space_router.get("/manufacturing/security")
async def manufacturing_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_security()}


@space_router.get("/manufacturing/integration")
async def manufacturing_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_integration()}


@space_router.get("/manufacturing/deployment")
async def manufacturing_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_deployment()}


@space_router.get("/manufacturing/testing")
async def manufacturing_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_testing()}


@space_router.get("/manufacturing/cqrs")
async def manufacturing_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_cqrs()}


@space_router.get("/manufacturing/events")
async def manufacturing_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_events()}


@space_router.get("/manufacturing/readiness")
async def manufacturing_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().manufacturing_readiness()}


@space_router.get("/resources")
async def resources_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_resources()}


@space_router.get("/resources/vision")
async def resources_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().resources_vision()}


@space_router.get("/resources/architecture")
async def resources_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().resources_architecture()}


@space_router.get("/resources/lifecycle")
async def resources_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().resources_lifecycle()}


@space_router.get("/resources/isru")
async def resources_isru(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().resources_isru()}


@space_router.get("/resources/asteroid")
async def resources_asteroid(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().resources_asteroid()}


@space_router.get("/resources/planetary")
async def resources_planetary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().resources_planetary()}


@space_router.get("/resources/autonomy")
async def resources_autonomy(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().resources_autonomy()}


@space_router.get("/resources/resource-ai")
async def resources_resource_ai(
    _user: Annotated[dict, Depends(require_permissions("space.ai.read"))],
) -> dict:
    return {"data": get_space_service().resources_resource_ai()}


@space_router.get("/resources/digital-twin")
async def resources_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().resources_digital_twin()}


@space_router.get("/resources/economy")
async def resources_economy(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().resources_economy()}


@space_router.get("/resources/observability")
async def resources_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().resources_observability()}


@space_router.get("/resources/governance")
async def resources_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().resources_governance()}


@space_router.get("/resources/security")
async def resources_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().resources_security()}


@space_router.get("/resources/integration")
async def resources_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().resources_integration()}


@space_router.get("/resources/deployment")
async def resources_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().resources_deployment()}


@space_router.get("/resources/testing")
async def resources_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().resources_testing()}


@space_router.get("/resources/cqrs")
async def resources_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().resources_cqrs()}


@space_router.get("/resources/events")
async def resources_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().resources_events()}


@space_router.get("/resources/readiness")
async def resources_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().resources_readiness()}


@space_router.get("/logistics")
async def logistics_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_logistics()}


@space_router.get("/logistics/vision")
async def logistics_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().logistics_vision()}


@space_router.get("/logistics/architecture")
async def logistics_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().logistics_architecture()}


@space_router.get("/logistics/lifecycle")
async def logistics_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().logistics_lifecycle()}


@space_router.get("/logistics/cargo")
async def logistics_cargo(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().logistics_cargo()}


@space_router.get("/logistics/supply-chain")
async def logistics_supply_chain(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().logistics_supply_chain()}


@space_router.get("/logistics/interplanetary")
async def logistics_interplanetary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().logistics_interplanetary()}


@space_router.get("/logistics/logistics-ai")
async def logistics_logistics_ai(
    _user: Annotated[dict, Depends(require_permissions("space.ai.read"))],
) -> dict:
    return {"data": get_space_service().logistics_logistics_ai()}


@space_router.get("/logistics/robotics")
async def logistics_robotics(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().logistics_robotics()}


@space_router.get("/logistics/digital-twin")
async def logistics_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().logistics_digital_twin()}


@space_router.get("/logistics/knowledge-graph")
async def logistics_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().logistics_knowledge_graph()}


@space_router.get("/logistics/observability")
async def logistics_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().logistics_observability()}


@space_router.get("/logistics/governance")
async def logistics_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().logistics_governance()}


@space_router.get("/logistics/security")
async def logistics_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().logistics_security()}


@space_router.get("/logistics/integration")
async def logistics_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().logistics_integration()}


@space_router.get("/logistics/deployment")
async def logistics_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().logistics_deployment()}


@space_router.get("/logistics/testing")
async def logistics_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().logistics_testing()}


@space_router.get("/logistics/cqrs")
async def logistics_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().logistics_cqrs()}


@space_router.get("/logistics/events")
async def logistics_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().logistics_events()}


@space_router.get("/logistics/readiness")
async def logistics_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().logistics_readiness()}


@space_router.get("/security")
async def security_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_security()}


@space_router.get("/security/vision")
async def security_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_vision()}


@space_router.get("/security/architecture")
async def security_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_architecture()}


@space_router.get("/security/lifecycle")
async def security_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_lifecycle()}


@space_router.get("/security/cybersecurity")
async def security_cybersecurity(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_cybersecurity()}


@space_router.get("/security/satellite")
async def security_satellite(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_satellite()}


@space_router.get("/security/orbital-defense")
async def security_orbital_defense(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_orbital_defense()}


@space_router.get("/security/threat-intelligence")
async def security_threat_intelligence(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_threat_intelligence()}


@space_router.get("/security/security-ai")
async def security_security_ai(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_security_ai()}


@space_router.get("/security/autonomy")
async def security_autonomy(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_autonomy()}


@space_router.get("/security/digital-twin")
async def security_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_digital_twin()}


@space_router.get("/security/knowledge-graph")
async def security_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_knowledge_graph()}


@space_router.get("/security/observability")
async def security_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_observability()}


@space_router.get("/security/governance")
async def security_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_governance()}


@space_router.get("/security/controls")
async def security_controls(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_controls()}


@space_router.get("/security/integration")
async def security_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_integration()}


@space_router.get("/security/deployment")
async def security_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_deployment()}


@space_router.get("/security/testing")
async def security_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_testing()}


@space_router.get("/security/cqrs")
async def security_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_cqrs()}


@space_router.get("/security/events")
async def security_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_events()}


@space_router.get("/security/readiness")
async def security_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().security_readiness()}


@space_router.get("/sustainability")
async def sustainability_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_sustainability()}


@space_router.get("/sustainability/vision")
async def sustainability_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_vision()}


@space_router.get("/sustainability/architecture")
async def sustainability_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_architecture()}


@space_router.get("/sustainability/lifecycle")
async def sustainability_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_lifecycle()}


@space_router.get("/sustainability/orbital-environment")
async def sustainability_orbital_environment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_orbital_environment()}


@space_router.get("/sustainability/debris")
async def sustainability_debris(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_debris()}


@space_router.get("/sustainability/autonomy")
async def sustainability_autonomy(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_autonomy()}


@space_router.get("/sustainability/sustainability-ai")
async def sustainability_sustainability_ai(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_sustainability_ai()}


@space_router.get("/sustainability/governance")
async def sustainability_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_governance()}


@space_router.get("/sustainability/planetary-protection")
async def sustainability_planetary_protection(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_planetary_protection()}


@space_router.get("/sustainability/digital-twin")
async def sustainability_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_digital_twin()}


@space_router.get("/sustainability/knowledge-graph")
async def sustainability_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_knowledge_graph()}


@space_router.get("/sustainability/observability")
async def sustainability_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_observability()}


@space_router.get("/sustainability/security")
async def sustainability_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_security()}


@space_router.get("/sustainability/integration")
async def sustainability_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_integration()}


@space_router.get("/sustainability/deployment")
async def sustainability_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_deployment()}


@space_router.get("/sustainability/testing")
async def sustainability_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_testing()}


@space_router.get("/sustainability/cqrs")
async def sustainability_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_cqrs()}


@space_router.get("/sustainability/events")
async def sustainability_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_events()}


@space_router.get("/sustainability/readiness")
async def sustainability_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().sustainability_readiness()}


@space_router.get("/commerce")
async def commerce_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_commerce()}


@space_router.get("/commerce/vision")
async def commerce_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_vision()}


@space_router.get("/commerce/architecture")
async def commerce_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_architecture()}


@space_router.get("/commerce/lifecycle")
async def commerce_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_lifecycle()}


@space_router.get("/commerce/marketplace")
async def commerce_marketplace(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_marketplace()}


@space_router.get("/commerce/operations")
async def commerce_operations(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_operations()}


@space_router.get("/commerce/economy")
async def commerce_economy(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_economy()}


@space_router.get("/commerce/investment")
async def commerce_investment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_investment()}


@space_router.get("/commerce/contracts")
async def commerce_contracts(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_contracts()}


@space_router.get("/commerce/commerce-ai")
async def commerce_commerce_ai(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_commerce_ai()}


@space_router.get("/commerce/digital-twin")
async def commerce_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_digital_twin()}


@space_router.get("/commerce/knowledge-graph")
async def commerce_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_knowledge_graph()}


@space_router.get("/commerce/observability")
async def commerce_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_observability()}


@space_router.get("/commerce/governance")
async def commerce_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_governance()}


@space_router.get("/commerce/security")
async def commerce_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_security()}


@space_router.get("/commerce/integration")
async def commerce_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_integration()}


@space_router.get("/commerce/deployment")
async def commerce_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_deployment()}


@space_router.get("/commerce/testing")
async def commerce_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_testing()}


@space_router.get("/commerce/cqrs")
async def commerce_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_cqrs()}


@space_router.get("/commerce/events")
async def commerce_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_events()}


@space_router.get("/commerce/readiness")
async def commerce_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().commerce_readiness()}


@space_router.get("/education")
async def education_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_education()}


@space_router.get("/education/vision")
async def education_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_vision()}


@space_router.get("/education/architecture")
async def education_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_architecture()}


@space_router.get("/education/lifecycle")
async def education_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_lifecycle()}


@space_router.get("/education/learning")
async def education_learning(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_learning()}


@space_router.get("/education/training")
async def education_training(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_training()}


@space_router.get("/education/simulation")
async def education_simulation(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_simulation()}


@space_router.get("/education/workforce")
async def education_workforce(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_workforce()}


@space_router.get("/education/education-ai")
async def education_education_ai(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_education_ai()}


@space_router.get("/education/knowledge-graph")
async def education_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_knowledge_graph()}


@space_router.get("/education/digital-twin")
async def education_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_digital_twin()}


@space_router.get("/education/marketplace")
async def education_marketplace(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_marketplace()}


@space_router.get("/education/observability")
async def education_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_observability()}


@space_router.get("/education/governance")
async def education_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_governance()}


@space_router.get("/education/security")
async def education_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_security()}


@space_router.get("/education/integration")
async def education_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_integration()}


@space_router.get("/education/deployment")
async def education_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_deployment()}


@space_router.get("/education/testing")
async def education_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_testing()}


@space_router.get("/education/cqrs")
async def education_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_cqrs()}


@space_router.get("/education/events")
async def education_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_events()}


@space_router.get("/education/readiness")
async def education_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().education_readiness()}


@space_router.get("/civilization")
async def civilization_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_civilization()}


@space_router.get("/civilization/vision")
async def civilization_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_vision()}


@space_router.get("/civilization/architecture")
async def civilization_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_architecture()}


@space_router.get("/civilization/lifecycle")
async def civilization_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_lifecycle()}


@space_router.get("/civilization/society")
async def civilization_society(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_society()}


@space_router.get("/civilization/governance")
async def civilization_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_governance()}


@space_router.get("/civilization/future-architecture")
async def civilization_future_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_future_architecture()}


@space_router.get("/civilization/civilization-ai")
async def civilization_civilization_ai(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_civilization_ai()}


@space_router.get("/civilization/digital-twin")
async def civilization_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_digital_twin()}


@space_router.get("/civilization/culture")
async def civilization_culture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_culture()}


@space_router.get("/civilization/knowledge-graph")
async def civilization_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_knowledge_graph()}


@space_router.get("/civilization/economy")
async def civilization_economy(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_economy()}


@space_router.get("/civilization/observability")
async def civilization_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_observability()}


@space_router.get("/civilization/ethics")
async def civilization_ethics(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_ethics()}


@space_router.get("/civilization/security")
async def civilization_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_security()}


@space_router.get("/civilization/integration")
async def civilization_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_integration()}


@space_router.get("/civilization/deployment")
async def civilization_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_deployment()}


@space_router.get("/civilization/testing")
async def civilization_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_testing()}


@space_router.get("/civilization/cqrs")
async def civilization_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_cqrs()}


@space_router.get("/civilization/events")
async def civilization_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_events()}


@space_router.get("/civilization/readiness")
async def civilization_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().civilization_readiness()}


@space_router.get("/human-evolution")
async def human_evolution_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_human_evolution()}


@space_router.get("/human-evolution/vision")
async def human_evolution_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_vision()}


@space_router.get("/human-evolution/architecture")
async def human_evolution_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_architecture()}


@space_router.get("/human-evolution/lifecycle")
async def human_evolution_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_lifecycle()}


@space_router.get("/human-evolution/augmentation")
async def human_evolution_augmentation(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_augmentation()}


@space_router.get("/human-evolution/symbiosis")
async def human_evolution_symbiosis(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_symbiosis()}


@space_router.get("/human-evolution/cognitive")
async def human_evolution_cognitive(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_cognitive()}


@space_router.get("/human-evolution/neural")
async def human_evolution_neural(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_neural()}


@space_router.get("/human-evolution/evolution-ai")
async def human_evolution_evolution_ai(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_evolution_ai()}


@space_router.get("/human-evolution/digital-twin")
async def human_evolution_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_digital_twin()}


@space_router.get("/human-evolution/knowledge-graph")
async def human_evolution_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_knowledge_graph()}


@space_router.get("/human-evolution/ethics")
async def human_evolution_ethics(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_ethics()}


@space_router.get("/human-evolution/governance")
async def human_evolution_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_governance()}


@space_router.get("/human-evolution/observability")
async def human_evolution_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_observability()}


@space_router.get("/human-evolution/security")
async def human_evolution_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_security()}


@space_router.get("/human-evolution/integration")
async def human_evolution_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_integration()}


@space_router.get("/human-evolution/deployment")
async def human_evolution_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_deployment()}


@space_router.get("/human-evolution/testing")
async def human_evolution_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_testing()}


@space_router.get("/human-evolution/cqrs")
async def human_evolution_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_cqrs()}


@space_router.get("/human-evolution/events")
async def human_evolution_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_events()}


@space_router.get("/human-evolution/readiness")
async def human_evolution_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_evolution_readiness()}


@space_router.get("/human-gi")
async def human_gi_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_human_gi()}


@space_router.get("/human-gi/vision")
async def human_gi_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_vision()}


@space_router.get("/human-gi/architecture")
async def human_gi_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_architecture()}


@space_router.get("/human-gi/lifecycle")
async def human_gi_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_lifecycle()}


@space_router.get("/human-gi/core")
async def human_gi_core(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_core()}


@space_router.get("/human-gi/cognitive-civilization")
async def human_gi_cognitive_civilization(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_cognitive_civilization()}


@space_router.get("/human-gi/collective")
async def human_gi_collective(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_collective()}


@space_router.get("/human-gi/reasoning")
async def human_gi_reasoning(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_reasoning()}


@space_router.get("/human-gi/knowledge-graph")
async def human_gi_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_knowledge_graph()}


@space_router.get("/human-gi/digital-twin")
async def human_gi_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_digital_twin()}


@space_router.get("/human-gi/collaboration")
async def human_gi_collaboration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_collaboration()}


@space_router.get("/human-gi/ethics")
async def human_gi_ethics(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_ethics()}


@space_router.get("/human-gi/governance")
async def human_gi_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_governance()}


@space_router.get("/human-gi/observability")
async def human_gi_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_observability()}


@space_router.get("/human-gi/security")
async def human_gi_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_security()}


@space_router.get("/human-gi/integration")
async def human_gi_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_integration()}


@space_router.get("/human-gi/deployment")
async def human_gi_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_deployment()}


@space_router.get("/human-gi/testing")
async def human_gi_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_testing()}


@space_router.get("/human-gi/cqrs")
async def human_gi_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_cqrs()}


@space_router.get("/human-gi/events")
async def human_gi_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_events()}


@space_router.get("/human-gi/readiness")
async def human_gi_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().human_gi_readiness()}


@space_router.get("/collective-si")
async def collective_si_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_collective_si()}


@space_router.get("/collective-si/vision")
async def collective_si_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_vision()}


@space_router.get("/collective-si/architecture")
async def collective_si_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_architecture()}


@space_router.get("/collective-si/lifecycle")
async def collective_si_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_lifecycle()}


@space_router.get("/collective-si/core")
async def collective_si_core(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_core()}


@space_router.get("/collective-si/civilization-network")
async def collective_si_civilization_network(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_civilization_network()}


@space_router.get("/collective-si/cognitive-ecosystem")
async def collective_si_cognitive_ecosystem(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_cognitive_ecosystem()}


@space_router.get("/collective-si/reasoning")
async def collective_si_reasoning(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_reasoning()}


@space_router.get("/collective-si/knowledge-graph")
async def collective_si_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_knowledge_graph()}


@space_router.get("/collective-si/digital-twin")
async def collective_si_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_digital_twin()}


@space_router.get("/collective-si/alignment")
async def collective_si_alignment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_alignment()}


@space_router.get("/collective-si/ethics")
async def collective_si_ethics(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_ethics()}


@space_router.get("/collective-si/governance")
async def collective_si_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_governance()}


@space_router.get("/collective-si/observability")
async def collective_si_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_observability()}


@space_router.get("/collective-si/security")
async def collective_si_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_security()}


@space_router.get("/collective-si/integration")
async def collective_si_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_integration()}


@space_router.get("/collective-si/deployment")
async def collective_si_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_deployment()}


@space_router.get("/collective-si/testing")
async def collective_si_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_testing()}


@space_router.get("/collective-si/cqrs")
async def collective_si_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_cqrs()}


@space_router.get("/collective-si/events")
async def collective_si_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_events()}


@space_router.get("/collective-si/readiness")
async def collective_si_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().collective_si_readiness()}


@space_router.get("/singularity")
async def singularity_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_singularity()}


@space_router.get("/singularity/vision")
async def singularity_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_vision()}


@space_router.get("/singularity/architecture")
async def singularity_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_architecture()}


@space_router.get("/singularity/lifecycle")
async def singularity_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_lifecycle()}


@space_router.get("/singularity/core")
async def singularity_core(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_core()}


@space_router.get("/singularity/human-ai-singularity")
async def singularity_human_ai_singularity(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_human_ai_singularity()}


@space_router.get("/singularity/post-human")
async def singularity_post_human(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_post_human()}


@space_router.get("/singularity/cognitive-evolution")
async def singularity_cognitive_evolution(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_cognitive_evolution()}


@space_router.get("/singularity/transformation")
async def singularity_transformation(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_transformation()}


@space_router.get("/singularity/knowledge-graph")
async def singularity_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_knowledge_graph()}


@space_router.get("/singularity/digital-twin")
async def singularity_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_digital_twin()}


@space_router.get("/singularity/alignment")
async def singularity_alignment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_alignment()}


@space_router.get("/singularity/ethics")
async def singularity_ethics(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_ethics()}


@space_router.get("/singularity/governance")
async def singularity_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_governance()}


@space_router.get("/singularity/observability")
async def singularity_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_observability()}


@space_router.get("/singularity/security")
async def singularity_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_security()}


@space_router.get("/singularity/integration")
async def singularity_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_integration()}


@space_router.get("/singularity/deployment")
async def singularity_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_deployment()}


@space_router.get("/singularity/testing")
async def singularity_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_testing()}


@space_router.get("/singularity/cqrs")
async def singularity_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_cqrs()}


@space_router.get("/singularity/events")
async def singularity_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_events()}


@space_router.get("/singularity/readiness")
async def singularity_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().singularity_readiness()}


@space_router.get("/ultimate-governance")
async def ultimate_governance_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_ultimate_governance()}


@space_router.get("/ultimate-governance/vision")
async def ultimate_governance_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_vision()}


@space_router.get("/ultimate-governance/architecture")
async def ultimate_governance_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_architecture()}


@space_router.get("/ultimate-governance/lifecycle")
async def ultimate_governance_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_lifecycle()}


@space_router.get("/ultimate-governance/core")
async def ultimate_governance_core(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_core()}


@space_router.get("/ultimate-governance/alignment")
async def ultimate_governance_alignment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_alignment()}


@space_router.get("/ultimate-governance/trust")
async def ultimate_governance_trust(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_trust()}


@space_router.get("/ultimate-governance/ethics")
async def ultimate_governance_ethics(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_ethics()}


@space_router.get("/ultimate-governance/safety")
async def ultimate_governance_safety(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_safety()}


@space_router.get("/ultimate-governance/knowledge-graph")
async def ultimate_governance_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_knowledge_graph()}


@space_router.get("/ultimate-governance/digital-twin")
async def ultimate_governance_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_digital_twin()}


@space_router.get("/ultimate-governance/civilization-trust")
async def ultimate_governance_civilization_trust(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_civilization_trust()}


@space_router.get("/ultimate-governance/operating-model")
async def ultimate_governance_operating_model(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_operating_model()}


@space_router.get("/ultimate-governance/governance")
async def ultimate_governance_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_governance()}


@space_router.get("/ultimate-governance/observability")
async def ultimate_governance_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_observability()}


@space_router.get("/ultimate-governance/security")
async def ultimate_governance_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_security()}


@space_router.get("/ultimate-governance/integration")
async def ultimate_governance_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_integration()}


@space_router.get("/ultimate-governance/deployment")
async def ultimate_governance_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_deployment()}


@space_router.get("/ultimate-governance/testing")
async def ultimate_governance_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_testing()}


@space_router.get("/ultimate-governance/cqrs")
async def ultimate_governance_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_cqrs()}


@space_router.get("/ultimate-governance/events")
async def ultimate_governance_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_events()}


@space_router.get("/ultimate-governance/readiness")
async def ultimate_governance_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().ultimate_governance_readiness()}


@space_router.get("/intelligence-nexus")
async def intelligence_nexus_summary(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().platform_intelligence_nexus()}


@space_router.get("/intelligence-nexus/vision")
async def intelligence_nexus_vision(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_vision()}


@space_router.get("/intelligence-nexus/architecture")
async def intelligence_nexus_architecture(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_architecture()}


@space_router.get("/intelligence-nexus/lifecycle")
async def intelligence_nexus_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_lifecycle()}


@space_router.get("/intelligence-nexus/core")
async def intelligence_nexus_core(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_core()}


@space_router.get("/intelligence-nexus/control-plane")
async def intelligence_nexus_control_plane(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_control_plane()}


@space_router.get("/intelligence-nexus/autonomous")
async def intelligence_nexus_autonomous(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_autonomous()}


@space_router.get("/intelligence-nexus/orchestration")
async def intelligence_nexus_orchestration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_orchestration()}


@space_router.get("/intelligence-nexus/decision-engine")
async def intelligence_nexus_decision_engine(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_decision_engine()}


@space_router.get("/intelligence-nexus/knowledge-graph")
async def intelligence_nexus_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_knowledge_graph()}


@space_router.get("/intelligence-nexus/digital-twin")
async def intelligence_nexus_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_digital_twin()}


@space_router.get("/intelligence-nexus/agents")
async def intelligence_nexus_agents(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_agents()}


@space_router.get("/intelligence-nexus/ethics")
async def intelligence_nexus_ethics(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_ethics()}


@space_router.get("/intelligence-nexus/governance")
async def intelligence_nexus_governance(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_governance()}


@space_router.get("/intelligence-nexus/observability")
async def intelligence_nexus_observability(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_observability()}


@space_router.get("/intelligence-nexus/security")
async def intelligence_nexus_security(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_security()}


@space_router.get("/intelligence-nexus/integration")
async def intelligence_nexus_integration(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_integration()}


@space_router.get("/intelligence-nexus/deployment")
async def intelligence_nexus_deployment(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_deployment()}


@space_router.get("/intelligence-nexus/testing")
async def intelligence_nexus_testing(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_testing()}


@space_router.get("/intelligence-nexus/cqrs")
async def intelligence_nexus_cqrs(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_cqrs()}


@space_router.get("/intelligence-nexus/events")
async def intelligence_nexus_events(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_events()}


@space_router.get("/intelligence-nexus/readiness")
async def intelligence_nexus_readiness(
    _user: Annotated[dict, Depends(require_permissions("space.read"))],
) -> dict:
    return {"data": get_space_service().intelligence_nexus_readiness()}
