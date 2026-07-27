"""Enterprise Data Governance, Data Mesh & Enterprise Intelligence API (P212-A–B, D–F)."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from contexts.data_governance.container import get_data_governance_service
from contexts.identity.presentation.dependencies import require_permissions

data_governance_router = APIRouter(
    prefix="/data-governance",
    tags=["Enterprise Data Governance, Data Mesh & Enterprise Intelligence"],
)


@data_governance_router.get("/catalog")
async def catalog(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {
        "data": (await get_data_governance_service().list_catalog()).unwrap()
    }


@data_governance_router.get("/strategy")
async def strategy_summary(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().platform_strategy()}


@data_governance_router.get("/strategy/architecture")
async def strategy_architecture(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_architecture()}


@data_governance_router.get("/strategy/domains")
async def strategy_domains(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_domains()}


@data_governance_router.get("/strategy/capabilities")
async def strategy_capabilities(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_capabilities()}


@data_governance_router.get("/strategy/data-mesh")
async def strategy_data_mesh(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_data_mesh()}


@data_governance_router.get("/strategy/knowledge-graph")
async def strategy_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_knowledge_graph()}


@data_governance_router.get("/strategy/digital-twin")
async def strategy_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_digital_twin()}


@data_governance_router.get("/strategy/ai-governance")
async def strategy_ai_governance(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_ai_governance()}


@data_governance_router.get("/strategy/security")
async def strategy_security(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_security()}


@data_governance_router.get("/strategy/privacy")
async def strategy_privacy(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_privacy()}


@data_governance_router.get("/strategy/cqrs")
async def strategy_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_cqrs()}


@data_governance_router.get("/strategy/events")
async def strategy_events(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_events()}


@data_governance_router.get("/strategy/microservices")
async def strategy_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_microservices()}


@data_governance_router.get("/strategy/apis")
async def strategy_apis(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_apis()}


@data_governance_router.get("/strategy/operating-model")
async def strategy_operating_model(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_operating_model()}


@data_governance_router.get("/strategy/deployment")
async def strategy_deployment(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_deployment()}


@data_governance_router.get("/strategy/integrations")
async def strategy_integrations(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_integrations()}


@data_governance_router.get("/strategy/roadmap")
async def strategy_roadmap(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_roadmap()}


@data_governance_router.get("/strategy/outputs")
async def strategy_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_outputs()}


@data_governance_router.get("/strategy/production-readiness")
async def strategy_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {
        "data": get_data_governance_service().strategy_production_readiness()
    }


@data_governance_router.get("/strategy/readiness")
async def strategy_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().strategy_readiness()}


# --- P212-B Mission / Vision / Scope ---


@data_governance_router.get("/mission")
async def mission_summary(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().platform_mission()}


@data_governance_router.get("/mission/statement")
async def mission_statement(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mission_statement()}


@data_governance_router.get("/mission/vision")
async def mission_vision(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mission_vision()}


@data_governance_router.get("/mission/strategic-objectives")
async def mission_objectives(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mission_objectives()}


@data_governance_router.get("/mission/scope")
async def mission_scope(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mission_scope()}


@data_governance_router.get("/mission/operating-model")
async def mission_operating_model(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mission_operating_model()}


@data_governance_router.get("/mission/maturity")
async def mission_maturity(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mission_maturity()}


@data_governance_router.get("/mission/ai-direction")
async def mission_ai_direction(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mission_ai_direction()}


@data_governance_router.get("/mission/boundaries")
async def mission_boundaries(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mission_boundaries()}


@data_governance_router.get("/mission/alignment")
async def mission_alignment(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mission_alignment()}


@data_governance_router.get("/mission/metrics")
async def mission_metrics(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mission_metrics()}


@data_governance_router.get("/mission/position")
async def mission_position(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mission_position()}


@data_governance_router.get("/mission/cqrs")
async def mission_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mission_cqrs()}


@data_governance_router.get("/mission/events")
async def mission_events(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mission_events()}


@data_governance_router.get("/mission/outputs")
async def mission_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mission_outputs()}


@data_governance_router.get("/mission/production-readiness")
async def mission_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {
        "data": get_data_governance_service().mission_production_readiness()
    }


@data_governance_router.get("/mission/readiness")
async def mission_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mission_readiness()}


# --- P212-D Ownership / Stewardship / Accountability ---


@data_governance_router.get("/ownership")
async def ownership_summary(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().platform_ownership()}


@data_governance_router.get("/ownership/owners")
async def ownership_owners(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ownership_owners()}


@data_governance_router.get("/ownership/stewards")
async def ownership_stewards(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ownership_stewards()}


@data_governance_router.get("/ownership/accountability")
async def ownership_accountability(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ownership_accountability()}


@data_governance_router.get("/ownership/intelligence")
async def ownership_intelligence(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ownership_intelligence()}


@data_governance_router.get("/ownership/knowledge-graph")
async def ownership_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ownership_knowledge_graph()}


@data_governance_router.get("/ownership/digital-twin")
async def ownership_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ownership_digital_twin()}


@data_governance_router.get("/ownership/data-mesh")
async def ownership_data_mesh(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ownership_data_mesh()}


@data_governance_router.get("/ownership/cqrs")
async def ownership_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ownership_cqrs()}


@data_governance_router.get("/ownership/events")
async def ownership_events(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ownership_events()}


@data_governance_router.get("/ownership/microservices")
async def ownership_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ownership_microservices()}


@data_governance_router.get("/ownership/apis")
async def ownership_apis(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ownership_apis()}


@data_governance_router.get("/ownership/security")
async def ownership_security(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ownership_security()}


@data_governance_router.get("/ownership/deployment")
async def ownership_deployment(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ownership_deployment()}


@data_governance_router.get("/ownership/outputs")
async def ownership_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ownership_outputs()}


@data_governance_router.get("/ownership/production-readiness")
async def ownership_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {
        "data": get_data_governance_service().ownership_production_readiness()
    }


@data_governance_router.get("/ownership/readiness")
async def ownership_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ownership_readiness()}


# --- P212-E Data Quality Intelligence ---


@data_governance_router.get("/quality")
async def quality_summary(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().platform_quality()}


@data_governance_router.get("/quality/dimensions")
async def quality_dimensions(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().quality_dimensions()}


@data_governance_router.get("/quality/rules")
async def quality_rules(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().quality_rules()}


@data_governance_router.get("/quality/measurement")
async def quality_measurement(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().quality_measurement()}


@data_governance_router.get("/quality/intelligence")
async def quality_intelligence(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().quality_intelligence()}


@data_governance_router.get("/quality/knowledge-graph")
async def quality_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().quality_knowledge_graph()}


@data_governance_router.get("/quality/digital-twin")
async def quality_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().quality_digital_twin()}


@data_governance_router.get("/quality/data-mesh")
async def quality_data_mesh(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().quality_data_mesh()}


@data_governance_router.get("/quality/cqrs")
async def quality_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().quality_cqrs()}


@data_governance_router.get("/quality/events")
async def quality_events(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().quality_events()}


@data_governance_router.get("/quality/microservices")
async def quality_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().quality_microservices()}


@data_governance_router.get("/quality/apis")
async def quality_apis(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().quality_apis()}


@data_governance_router.get("/quality/security")
async def quality_security(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().quality_security()}


@data_governance_router.get("/quality/deployment")
async def quality_deployment(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().quality_deployment()}


@data_governance_router.get("/quality/outputs")
async def quality_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().quality_outputs()}


@data_governance_router.get("/quality/production-readiness")
async def quality_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {
        "data": get_data_governance_service().quality_production_readiness()
    }


@data_governance_router.get("/quality/readiness")
async def quality_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().quality_readiness()}


# --- P212-F Data Mesh & Data Products ---


@data_governance_router.get("/mesh")
async def mesh_summary(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().platform_mesh()}


@data_governance_router.get("/mesh/principles")
async def mesh_principles(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mesh_principles()}


@data_governance_router.get("/mesh/domains")
async def mesh_domains(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mesh_domains()}


@data_governance_router.get("/mesh/products")
async def mesh_products(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mesh_products()}


@data_governance_router.get("/mesh/lifecycle")
async def mesh_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mesh_lifecycle()}


@data_governance_router.get("/mesh/contracts")
async def mesh_contracts(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mesh_contracts()}


@data_governance_router.get("/mesh/quality")
async def mesh_quality(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mesh_quality()}


@data_governance_router.get("/mesh/intelligence")
async def mesh_intelligence(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mesh_intelligence()}


@data_governance_router.get("/mesh/knowledge-graph")
async def mesh_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mesh_knowledge_graph()}


@data_governance_router.get("/mesh/digital-twin")
async def mesh_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mesh_digital_twin()}


@data_governance_router.get("/mesh/cqrs")
async def mesh_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mesh_cqrs()}


@data_governance_router.get("/mesh/events")
async def mesh_events(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mesh_events()}


@data_governance_router.get("/mesh/microservices")
async def mesh_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mesh_microservices()}


@data_governance_router.get("/mesh/apis")
async def mesh_apis(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mesh_apis()}


@data_governance_router.get("/mesh/operating-model")
async def mesh_operating_model(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mesh_operating_model()}


@data_governance_router.get("/mesh/deployment")
async def mesh_deployment(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mesh_deployment()}


@data_governance_router.get("/mesh/outputs")
async def mesh_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mesh_outputs()}


@data_governance_router.get("/mesh/production-readiness")
async def mesh_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {
        "data": get_data_governance_service().mesh_production_readiness()
    }


@data_governance_router.get("/mesh/readiness")
async def mesh_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().mesh_readiness()}


# --- P212-G Enterprise Data Marketplace ---


@data_governance_router.get("/marketplace")
async def marketplace_summary(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().platform_marketplace()}


@data_governance_router.get("/marketplace/capabilities")
async def marketplace_capabilities(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().marketplace_capabilities()}


@data_governance_router.get("/marketplace/catalog")
async def marketplace_catalog(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().marketplace_catalog()}


@data_governance_router.get("/marketplace/discovery")
async def marketplace_discovery(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().marketplace_discovery()}


@data_governance_router.get("/marketplace/consumption")
async def marketplace_consumption(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().marketplace_consumption()}


@data_governance_router.get("/marketplace/access-governance")
async def marketplace_access_governance(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {
        "data": get_data_governance_service().marketplace_access_governance()
    }


@data_governance_router.get("/marketplace/subscriptions")
async def marketplace_subscriptions(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().marketplace_subscriptions()}


@data_governance_router.get("/marketplace/intelligence")
async def marketplace_intelligence(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().marketplace_intelligence()}


@data_governance_router.get("/marketplace/knowledge-graph")
async def marketplace_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {
        "data": get_data_governance_service().marketplace_knowledge_graph()
    }


@data_governance_router.get("/marketplace/digital-twin")
async def marketplace_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().marketplace_digital_twin()}


@data_governance_router.get("/marketplace/cqrs")
async def marketplace_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().marketplace_cqrs()}


@data_governance_router.get("/marketplace/events")
async def marketplace_events(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().marketplace_events()}


@data_governance_router.get("/marketplace/microservices")
async def marketplace_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().marketplace_microservices()}


@data_governance_router.get("/marketplace/apis")
async def marketplace_apis(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().marketplace_apis()}


@data_governance_router.get("/marketplace/security")
async def marketplace_security(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().marketplace_security()}


@data_governance_router.get("/marketplace/operating-model")
async def marketplace_operating_model(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {
        "data": get_data_governance_service().marketplace_operating_model()
    }


@data_governance_router.get("/marketplace/deployment")
async def marketplace_deployment(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().marketplace_deployment()}


@data_governance_router.get("/marketplace/outputs")
async def marketplace_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().marketplace_outputs()}


@data_governance_router.get("/marketplace/production-readiness")
async def marketplace_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {
        "data": get_data_governance_service().marketplace_production_readiness()
    }


@data_governance_router.get("/marketplace/readiness")
async def marketplace_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().marketplace_readiness()}


# --- P212-H Data Policy Management & Governance Automation ---


@data_governance_router.get("/policies")
async def policies_summary(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().platform_policies()}


@data_governance_router.get("/policies/framework")
async def policies_framework(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().policies_framework()}


@data_governance_router.get("/policies/lifecycle")
async def policies_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().policies_lifecycle()}


@data_governance_router.get("/policies/rules")
async def policies_rules(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().policies_rules()}


@data_governance_router.get("/policies/automation")
async def policies_automation(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().policies_automation()}


@data_governance_router.get("/policies/intelligence")
async def policies_intelligence(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().policies_intelligence()}


@data_governance_router.get("/policies/ai")
async def policies_ai(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().policies_ai()}


@data_governance_router.get("/policies/compliance")
async def policies_compliance(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().policies_compliance()}


@data_governance_router.get("/policies/knowledge-graph")
async def policies_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().policies_knowledge_graph()}


@data_governance_router.get("/policies/digital-twin")
async def policies_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().policies_digital_twin()}


@data_governance_router.get("/policies/cqrs")
async def policies_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().policies_cqrs()}


@data_governance_router.get("/policies/events")
async def policies_events(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().policies_events()}


@data_governance_router.get("/policies/microservices")
async def policies_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().policies_microservices()}


@data_governance_router.get("/policies/apis")
async def policies_apis(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().policies_apis()}


@data_governance_router.get("/policies/security")
async def policies_security(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().policies_security()}


@data_governance_router.get("/policies/operating-model")
async def policies_operating_model(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().policies_operating_model()}


@data_governance_router.get("/policies/deployment")
async def policies_deployment(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().policies_deployment()}


@data_governance_router.get("/policies/outputs")
async def policies_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().policies_outputs()}


@data_governance_router.get("/policies/production-readiness")
async def policies_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {
        "data": get_data_governance_service().policies_production_readiness()
    }


@data_governance_router.get("/policies/readiness")
async def policies_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().policies_readiness()}


# --- P212-J Data Intelligence Knowledge Graph ---


@data_governance_router.get("/graph")
async def graph_summary(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().platform_graph()}


@data_governance_router.get("/graph/ontology")
async def graph_ontology(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().graph_ontology()}


@data_governance_router.get("/graph/entities")
async def graph_entities(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().graph_entities()}


@data_governance_router.get("/graph/semantic-fabric")
async def graph_semantic_fabric(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().graph_semantic_fabric()}


@data_governance_router.get("/graph/intelligence")
async def graph_intelligence(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().graph_intelligence()}


@data_governance_router.get("/graph/ai-reasoning")
async def graph_ai_reasoning(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().graph_ai_reasoning()}


@data_governance_router.get("/graph/semantic-search")
async def graph_semantic_search(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().graph_semantic_search()}


@data_governance_router.get("/graph/mesh-alignment")
async def graph_mesh_alignment(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().graph_mesh_alignment()}


@data_governance_router.get("/graph/marketplace")
async def graph_marketplace(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().graph_marketplace()}


@data_governance_router.get("/graph/policies")
async def graph_policies(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().graph_policies()}


@data_governance_router.get("/graph/digital-twin")
async def graph_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().graph_digital_twin()}


@data_governance_router.get("/graph/cqrs")
async def graph_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().graph_cqrs()}


@data_governance_router.get("/graph/events")
async def graph_events(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().graph_events()}


@data_governance_router.get("/graph/microservices")
async def graph_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().graph_microservices()}


@data_governance_router.get("/graph/apis")
async def graph_apis(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().graph_apis()}


@data_governance_router.get("/graph/security")
async def graph_security(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().graph_security()}


@data_governance_router.get("/graph/deployment")
async def graph_deployment(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().graph_deployment()}


@data_governance_router.get("/graph/outputs")
async def graph_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().graph_outputs()}


@data_governance_router.get("/graph/production-readiness")
async def graph_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {
        "data": get_data_governance_service().graph_production_readiness()
    }


@data_governance_router.get("/graph/readiness")
async def graph_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().graph_readiness()}


# --- P212-L Data Governance Digital Twin & Simulation ---


@data_governance_router.get("/twin")
async def twin_summary(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().platform_twin()}


@data_governance_router.get("/twin/state-model")
async def twin_state_model(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().twin_state_model()}


@data_governance_router.get("/twin/simulation")
async def twin_simulation(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().twin_simulation()}


@data_governance_router.get("/twin/what-if")
async def twin_what_if(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().twin_what_if()}


@data_governance_router.get("/twin/risk-prediction")
async def twin_risk_prediction(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().twin_risk_prediction()}


@data_governance_router.get("/twin/optimization")
async def twin_optimization(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().twin_optimization()}


@data_governance_router.get("/twin/ai")
async def twin_ai(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().twin_ai()}


@data_governance_router.get("/twin/knowledge-graph")
async def twin_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().twin_knowledge_graph()}


@data_governance_router.get("/twin/mesh")
async def twin_mesh(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().twin_mesh()}


@data_governance_router.get("/twin/policies")
async def twin_policies(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().twin_policies()}


@data_governance_router.get("/twin/quality")
async def twin_quality(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().twin_quality()}


@data_governance_router.get("/twin/cqrs")
async def twin_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().twin_cqrs()}


@data_governance_router.get("/twin/events")
async def twin_events(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().twin_events()}


@data_governance_router.get("/twin/microservices")
async def twin_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().twin_microservices()}


@data_governance_router.get("/twin/apis")
async def twin_apis(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().twin_apis()}


@data_governance_router.get("/twin/security")
async def twin_security(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().twin_security()}


@data_governance_router.get("/twin/deployment")
async def twin_deployment(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().twin_deployment()}


@data_governance_router.get("/twin/outputs")
async def twin_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().twin_outputs()}


@data_governance_router.get("/twin/production-readiness")
async def twin_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {
        "data": get_data_governance_service().twin_production_readiness()
    }


@data_governance_router.get("/twin/readiness")
async def twin_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().twin_readiness()}


# --- P212-M CQRS, Events, APIs & Microservices ---


@data_governance_router.get("/ops")
async def ops_summary(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().platform_ops()}


@data_governance_router.get("/ops/commands")
async def ops_commands(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_commands()}


@data_governance_router.get("/ops/queries")
async def ops_queries(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_queries()}


@data_governance_router.get("/ops/events")
async def ops_events(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_events()}


@data_governance_router.get("/ops/event-bus")
async def ops_event_bus(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_event_bus()}


@data_governance_router.get("/ops/event-contracts")
async def ops_event_contracts(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_event_contracts()}


@data_governance_router.get("/ops/microservices")
async def ops_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_microservices()}


@data_governance_router.get("/ops/apis")
async def ops_apis(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_apis()}


@data_governance_router.get("/ops/hexagonal")
async def ops_hexagonal(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_hexagonal()}


@data_governance_router.get("/ops/integration")
async def ops_integration(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_integration()}


@data_governance_router.get("/ops/ai")
async def ops_ai(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_ai()}


@data_governance_router.get("/ops/twin")
async def ops_twin(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_twin()}


@data_governance_router.get("/ops/multi-tenant")
async def ops_multi_tenant(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_multi_tenant()}


@data_governance_router.get("/ops/observability")
async def ops_observability(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_observability()}


@data_governance_router.get("/ops/resilience")
async def ops_resilience(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_resilience()}


@data_governance_router.get("/ops/communication")
async def ops_communication(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_communication()}


@data_governance_router.get("/ops/deployment")
async def ops_deployment(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_deployment()}


@data_governance_router.get("/ops/testing")
async def ops_testing(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_testing()}


@data_governance_router.get("/ops/outputs")
async def ops_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_outputs()}


@data_governance_router.get("/ops/production-readiness")
async def ops_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {
        "data": get_data_governance_service().ops_production_readiness()
    }


@data_governance_router.get("/ops/readiness")
async def ops_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().ops_readiness()}


# --- P212-N Deployment, DevSecOps, K8s, Scalability & Observability ---


@data_governance_router.get("/deploy")
async def deploy_summary(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().platform_deploy()}


@data_governance_router.get("/deploy/cloud-native")
async def deploy_cloud_native(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_cloud_native()}


@data_governance_router.get("/deploy/kubernetes")
async def deploy_kubernetes(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_kubernetes()}


@data_governance_router.get("/deploy/devsecops")
async def deploy_devsecops(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_devsecops()}


@data_governance_router.get("/deploy/gitops")
async def deploy_gitops(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_gitops()}


@data_governance_router.get("/deploy/iac")
async def deploy_iac(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_iac()}


@data_governance_router.get("/deploy/service-mesh")
async def deploy_service_mesh(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_service_mesh()}


@data_governance_router.get("/deploy/scalability")
async def deploy_scalability(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_scalability()}


@data_governance_router.get("/deploy/ha")
async def deploy_ha(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_ha()}


@data_governance_router.get("/deploy/observability")
async def deploy_observability(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_observability()}


@data_governance_router.get("/deploy/aiops")
async def deploy_aiops(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_aiops()}


@data_governance_router.get("/deploy/security")
async def deploy_security(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_security()}


@data_governance_router.get("/deploy/multi-region")
async def deploy_multi_region(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_multi_region()}


@data_governance_router.get("/deploy/cqrs-ops")
async def deploy_cqrs_ops(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_cqrs_ops()}


@data_governance_router.get("/deploy/reliability")
async def deploy_reliability(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_reliability()}


@data_governance_router.get("/deploy/model")
async def deploy_model(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_model()}


@data_governance_router.get("/deploy/apis")
async def deploy_apis(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_apis()}


@data_governance_router.get("/deploy/testing")
async def deploy_testing(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_testing()}


@data_governance_router.get("/deploy/outputs")
async def deploy_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_outputs()}


@data_governance_router.get("/deploy/production-readiness")
async def deploy_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {
        "data": get_data_governance_service().deploy_production_readiness()
    }


@data_governance_router.get("/deploy/readiness")
async def deploy_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().deploy_readiness()}


# --- P212-O Testing, Governance, Compliance Validation & DoD ---


@data_governance_router.get("/qa")
async def qa_summary(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().platform_qa()}


@data_governance_router.get("/qa/testing")
async def qa_testing(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().qa_testing()}


@data_governance_router.get("/qa/governance")
async def qa_governance(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().qa_governance()}


@data_governance_router.get("/qa/compliance")
async def qa_compliance(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().qa_compliance()}


@data_governance_router.get("/qa/security")
async def qa_security(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().qa_security()}


@data_governance_router.get("/qa/dod")
async def qa_dod(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().qa_dod()}


@data_governance_router.get("/qa/ai")
async def qa_ai(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().qa_ai()}


@data_governance_router.get("/qa/graph")
async def qa_graph(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().qa_graph()}


@data_governance_router.get("/qa/twin")
async def qa_twin(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().qa_twin()}


@data_governance_router.get("/qa/cqrs")
async def qa_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().qa_cqrs()}


@data_governance_router.get("/qa/events")
async def qa_events(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().qa_events()}


@data_governance_router.get("/qa/microservices")
async def qa_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().qa_microservices()}


@data_governance_router.get("/qa/apis")
async def qa_apis(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().qa_apis()}


@data_governance_router.get("/qa/continuous")
async def qa_continuous(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().qa_continuous()}


@data_governance_router.get("/qa/deploy-validation")
async def qa_deploy_validation(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().qa_deploy_validation()}


@data_governance_router.get("/qa/evidence")
async def qa_evidence(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().qa_evidence()}


@data_governance_router.get("/qa/outputs")
async def qa_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().qa_outputs()}


@data_governance_router.get("/qa/production-readiness")
async def qa_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {
        "data": get_data_governance_service().qa_production_readiness()
    }


@data_governance_router.get("/qa/readiness")
async def qa_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_governance.read"))],
) -> dict:
    return {"data": get_data_governance_service().qa_readiness()}
