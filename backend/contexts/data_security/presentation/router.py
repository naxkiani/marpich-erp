"""Enterprise Data Security & Privacy Intelligence Platform API (P211-A–D)."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from contexts.data_security.container import get_data_security_service
from contexts.identity.presentation.dependencies import require_permissions

data_security_router = APIRouter(
    prefix="/data-security",
    tags=["Enterprise Data Security & Privacy Intelligence"],
)


@data_security_router.get("/catalog")
async def catalog(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": (await get_data_security_service().list_catalog()).unwrap()}


@data_security_router.get("/strategy")
async def strategy_summary(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().platform_strategy()}


@data_security_router.get("/strategy/architecture")
async def strategy_architecture(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_architecture()}


@data_security_router.get("/strategy/domains")
async def strategy_domains(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_domains()}


@data_security_router.get("/strategy/inventory")
async def strategy_inventory(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_inventory()}


@data_security_router.get("/strategy/classification")
async def strategy_classification(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_classification()}


@data_security_router.get("/strategy/intelligence")
async def strategy_intelligence(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_intelligence()}


@data_security_router.get("/strategy/dspm")
async def strategy_dspm(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_dspm()}


@data_security_router.get("/strategy/privacy")
async def strategy_privacy(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_privacy()}


@data_security_router.get("/strategy/zero-trust")
async def strategy_zero_trust(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_zero_trust()}


@data_security_router.get("/strategy/ai-data")
async def strategy_ai_data(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_ai_data()}


@data_security_router.get("/strategy/knowledge-graph")
async def strategy_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_knowledge_graph()}


@data_security_router.get("/strategy/digital-twin")
async def strategy_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_digital_twin()}


@data_security_router.get("/strategy/lineage")
async def strategy_lineage(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_lineage()}


@data_security_router.get("/strategy/compliance")
async def strategy_compliance(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_compliance()}


@data_security_router.get("/strategy/ddd")
async def strategy_ddd(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_ddd()}


@data_security_router.get("/strategy/cqrs")
async def strategy_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_cqrs()}


@data_security_router.get("/strategy/events")
async def strategy_events(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_events()}


@data_security_router.get("/strategy/microservices")
async def strategy_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_microservices()}


@data_security_router.get("/strategy/integrations")
async def strategy_integrations(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_integrations()}


@data_security_router.get("/strategy/roadmap")
async def strategy_roadmap(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_roadmap()}


@data_security_router.get("/strategy/outputs")
async def strategy_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_outputs()}


@data_security_router.get("/strategy/production-readiness")
async def strategy_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_production_readiness()}


@data_security_router.get("/strategy/readiness")
async def strategy_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().strategy_readiness()}


# --- P211-B Mission / Vision / Enterprise Scope ------------------------------


@data_security_router.get("/mission")
async def mission_summary(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().platform_mission_scope()}


@data_security_router.get("/mission/statement")
async def mission_statement(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().mission_statement()}


@data_security_router.get("/mission/vision")
async def mission_vision(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().mission_vision()}


@data_security_router.get("/mission/strategic-objectives")
async def mission_strategic_objectives(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().mission_strategic_objectives()}


@data_security_router.get("/mission/scope")
async def mission_scope(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().mission_scope()}


@data_security_router.get("/mission/operating-model")
async def mission_operating_model(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().mission_operating_model()}


@data_security_router.get("/mission/principles")
async def mission_principles(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().mission_principles()}


@data_security_router.get("/mission/boundaries")
async def mission_boundaries(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().mission_boundaries()}


@data_security_router.get("/mission/maturity")
async def mission_maturity(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().mission_maturity()}


@data_security_router.get("/mission/governance")
async def mission_governance(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().mission_governance()}


@data_security_router.get("/mission/integrations")
async def mission_integrations(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().mission_integrations()}


@data_security_router.get("/mission/cqrs")
async def mission_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().mission_cqrs()}


@data_security_router.get("/mission/events")
async def mission_events(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().mission_events()}


@data_security_router.get("/mission/outputs")
async def mission_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().mission_outputs()}


@data_security_router.get("/mission/production-readiness")
async def mission_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().mission_production_readiness()}


@data_security_router.get("/mission/readiness")
async def mission_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().mission_readiness()}


# --- P211-C Domain Architecture (DDD) ----------------------------------------


@data_security_router.get("/domain")
async def domain_summary(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().platform_domain()}


@data_security_router.get("/domain/map")
async def domain_map(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().domain_map()}


@data_security_router.get("/domain/bounded-contexts")
async def domain_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().domain_bounded_contexts()}


@data_security_router.get("/domain/aggregates")
async def domain_aggregates(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().domain_aggregates()}


@data_security_router.get("/domain/entities")
async def domain_entities(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().domain_entities()}


@data_security_router.get("/domain/ownership")
async def domain_ownership(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().domain_ownership()}


@data_security_router.get("/domain/privacy-security")
async def domain_privacy_security(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().domain_privacy_security()}


@data_security_router.get("/domain/events")
async def domain_events(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().domain_events()}


@data_security_router.get("/domain/microservices")
async def domain_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().domain_microservices()}


@data_security_router.get("/domain/integrations")
async def domain_integrations(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().domain_integrations()}


@data_security_router.get("/domain/cqrs")
async def domain_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().domain_cqrs()}


@data_security_router.get("/domain/outputs")
async def domain_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().domain_outputs()}


@data_security_router.get("/domain/production-readiness")
async def domain_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().domain_production_readiness()}


@data_security_router.get("/domain/readiness")
async def domain_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().domain_readiness()}


# --- P211-D Discovery & Data Inventory ---------------------------------------


@data_security_router.get("/discovery")
async def discovery_summary(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().platform_discovery()}


@data_security_router.get("/discovery/architecture")
async def discovery_architecture(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().discovery_architecture()}


@data_security_router.get("/discovery/inventory")
async def discovery_inventory(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().discovery_inventory()}


@data_security_router.get("/discovery/connectors")
async def discovery_connectors(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().discovery_connectors()}


@data_security_router.get("/discovery/metadata")
async def discovery_metadata(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().discovery_metadata()}


@data_security_router.get("/discovery/profiling")
async def discovery_profiling(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().discovery_profiling()}


@data_security_router.get("/discovery/shadow-data")
async def discovery_shadow_data(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().discovery_shadow_data()}


@data_security_router.get("/discovery/ai")
async def discovery_ai(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().discovery_ai()}


@data_security_router.get("/discovery/knowledge-graph")
async def discovery_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().discovery_knowledge_graph()}


@data_security_router.get("/discovery/digital-twin")
async def discovery_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().discovery_digital_twin()}


@data_security_router.get("/discovery/cqrs")
async def discovery_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().discovery_cqrs()}


@data_security_router.get("/discovery/events")
async def discovery_events(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().discovery_events()}


@data_security_router.get("/discovery/microservices")
async def discovery_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().discovery_microservices()}


@data_security_router.get("/discovery/apis")
async def discovery_apis(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().discovery_apis()}


@data_security_router.get("/discovery/integrations")
async def discovery_integrations(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().discovery_integrations()}


@data_security_router.get("/discovery/outputs")
async def discovery_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().discovery_outputs()}


@data_security_router.get("/discovery/production-readiness")
async def discovery_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().discovery_production_readiness()}


@data_security_router.get("/discovery/readiness")
async def discovery_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().discovery_readiness()}


# --- P211-E Classification & Labeling ----------------------------------------


@data_security_router.get("/classification")
async def classification_summary(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().platform_classification()}


@data_security_router.get("/classification/architecture")
async def classification_architecture(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().classification_architecture()}


@data_security_router.get("/classification/taxonomy")
async def classification_taxonomy(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().classification_taxonomy()}


@data_security_router.get("/classification/sensitive-detection")
async def classification_sensitive_detection(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().classification_sensitive_detection()}


@data_security_router.get("/classification/ai")
async def classification_ai(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().classification_ai()}


@data_security_router.get("/classification/methods")
async def classification_methods(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().classification_methods()}


@data_security_router.get("/classification/labels")
async def classification_labels(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().classification_labels()}


@data_security_router.get("/classification/policies")
async def classification_policies(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().classification_policies()}


@data_security_router.get("/classification/lifecycle")
async def classification_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().classification_lifecycle()}


@data_security_router.get("/classification/knowledge-graph")
async def classification_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().classification_knowledge_graph()}


@data_security_router.get("/classification/digital-twin")
async def classification_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().classification_digital_twin()}


@data_security_router.get("/classification/cqrs")
async def classification_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().classification_cqrs()}


@data_security_router.get("/classification/events")
async def classification_events(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().classification_events()}


@data_security_router.get("/classification/microservices")
async def classification_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().classification_microservices()}


@data_security_router.get("/classification/apis")
async def classification_apis(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().classification_apis()}


@data_security_router.get("/classification/integrations")
async def classification_integrations(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().classification_integrations()}


@data_security_router.get("/classification/outputs")
async def classification_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().classification_outputs()}


@data_security_router.get("/classification/production-readiness")
async def classification_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().classification_production_readiness()}


@data_security_router.get("/classification/readiness")
async def classification_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().classification_readiness()}


# --- P211-F DSPM Posture Management ------------------------------------------


@data_security_router.get("/dspm")
async def dspm_summary(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().platform_dspm()}


@data_security_router.get("/dspm/architecture")
async def dspm_architecture(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_architecture()}


@data_security_router.get("/dspm/domain")
async def dspm_domain(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_domain()}


@data_security_router.get("/dspm/discovery")
async def dspm_discovery(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_discovery()}


@data_security_router.get("/dspm/sensitive")
async def dspm_sensitive(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_sensitive()}


@data_security_router.get("/dspm/posture")
async def dspm_posture(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_posture()}


@data_security_router.get("/dspm/exposure")
async def dspm_exposure(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_exposure()}


@data_security_router.get("/dspm/access-risk")
async def dspm_access_risk(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_access_risk()}


@data_security_router.get("/dspm/ai-risk")
async def dspm_ai_risk(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_ai_risk()}


@data_security_router.get("/dspm/remediation")
async def dspm_remediation(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_remediation()}


@data_security_router.get("/dspm/knowledge-graph")
async def dspm_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_knowledge_graph()}


@data_security_router.get("/dspm/digital-twin")
async def dspm_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_digital_twin()}


@data_security_router.get("/dspm/cqrs")
async def dspm_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_cqrs()}


@data_security_router.get("/dspm/events")
async def dspm_events(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_events()}


@data_security_router.get("/dspm/microservices")
async def dspm_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_microservices()}


@data_security_router.get("/dspm/apis")
async def dspm_apis(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_apis()}


@data_security_router.get("/dspm/integrations")
async def dspm_integrations(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_integrations()}


@data_security_router.get("/dspm/outputs")
async def dspm_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_outputs()}


@data_security_router.get("/dspm/production-readiness")
async def dspm_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_production_readiness()}


@data_security_router.get("/dspm/readiness")
async def dspm_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dspm_readiness()}


# --- P211-G Data Loss Prevention (DLP) ----------------------------------------


@data_security_router.get("/dlp")
async def dlp_summary(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().platform_dlp()}


@data_security_router.get("/dlp/architecture")
async def dlp_architecture(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_architecture()}


@data_security_router.get("/dlp/channels")
async def dlp_channels(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_channels()}


@data_security_router.get("/dlp/monitoring")
async def dlp_monitoring(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_monitoring()}


@data_security_router.get("/dlp/policies")
async def dlp_policies(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_policies()}


@data_security_router.get("/dlp/enforcement")
async def dlp_enforcement(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_enforcement()}


@data_security_router.get("/dlp/ai")
async def dlp_ai(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_ai()}


@data_security_router.get("/dlp/insider-risk")
async def dlp_insider_risk(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_insider_risk()}


@data_security_router.get("/dlp/incidents")
async def dlp_incidents(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_incidents()}


@data_security_router.get("/dlp/knowledge-graph")
async def dlp_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_knowledge_graph()}


@data_security_router.get("/dlp/digital-twin")
async def dlp_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_digital_twin()}


@data_security_router.get("/dlp/cqrs")
async def dlp_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_cqrs()}


@data_security_router.get("/dlp/events")
async def dlp_events(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_events()}


@data_security_router.get("/dlp/microservices")
async def dlp_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_microservices()}


@data_security_router.get("/dlp/apis")
async def dlp_apis(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_apis()}


@data_security_router.get("/dlp/integrations")
async def dlp_integrations(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_integrations()}


@data_security_router.get("/dlp/compliance")
async def dlp_compliance(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_compliance()}


@data_security_router.get("/dlp/outputs")
async def dlp_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_outputs()}


@data_security_router.get("/dlp/production-readiness")
async def dlp_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_production_readiness()}


@data_security_router.get("/dlp/readiness")
async def dlp_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().dlp_readiness()}


# --- P211-H Data Access Governance -------------------------------------------


@data_security_router.get("/access")
async def access_summary(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().platform_access()}


@data_security_router.get("/access/architecture")
async def access_architecture(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_architecture()}


@data_security_router.get("/access/entitlements")
async def access_entitlements(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_entitlements()}


@data_security_router.get("/access/ownership")
async def access_ownership(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_ownership()}


@data_security_router.get("/access/requests")
async def access_requests(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_requests()}


@data_security_router.get("/access/zero-trust")
async def access_zero_trust(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_zero_trust()}


@data_security_router.get("/access/abac")
async def access_abac(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_abac()}


@data_security_router.get("/access/rebac")
async def access_rebac(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_rebac()}


@data_security_router.get("/access/ai")
async def access_ai(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_ai()}


@data_security_router.get("/access/risk")
async def access_risk(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_risk()}


@data_security_router.get("/access/certification")
async def access_certification(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_certification()}


@data_security_router.get("/access/knowledge-graph")
async def access_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_knowledge_graph()}


@data_security_router.get("/access/digital-twin")
async def access_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_digital_twin()}


@data_security_router.get("/access/cqrs")
async def access_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_cqrs()}


@data_security_router.get("/access/events")
async def access_events(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_events()}


@data_security_router.get("/access/microservices")
async def access_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_microservices()}


@data_security_router.get("/access/apis")
async def access_apis(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_apis()}


@data_security_router.get("/access/integrations")
async def access_integrations(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_integrations()}


@data_security_router.get("/access/outputs")
async def access_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_outputs()}


@data_security_router.get("/access/production-readiness")
async def access_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_production_readiness()}


@data_security_router.get("/access/readiness")
async def access_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().access_readiness()}


# --- P211-I Privacy Intelligence ---------------------------------------------


@data_security_router.get("/privacy")
async def privacy_summary(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().platform_privacy()}


@data_security_router.get("/privacy/architecture")
async def privacy_architecture(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_architecture()}


@data_security_router.get("/privacy/domain")
async def privacy_domain(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_domain()}


@data_security_router.get("/privacy/personal-data")
async def privacy_personal_data(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_personal_data()}


@data_security_router.get("/privacy/consent")
async def privacy_consent(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_consent()}


@data_security_router.get("/privacy/dsar")
async def privacy_dsar(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_dsar()}


@data_security_router.get("/privacy/risk")
async def privacy_risk(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_risk()}


@data_security_router.get("/privacy/processing")
async def privacy_processing(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_processing()}


@data_security_router.get("/privacy/dpia")
async def privacy_dpia(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_dpia()}


@data_security_router.get("/privacy/obligations")
async def privacy_obligations(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_obligations()}


@data_security_router.get("/privacy/ai")
async def privacy_ai(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_ai()}


@data_security_router.get("/privacy/knowledge-graph")
async def privacy_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_knowledge_graph()}


@data_security_router.get("/privacy/digital-twin")
async def privacy_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_digital_twin()}


@data_security_router.get("/privacy/cqrs")
async def privacy_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_cqrs()}


@data_security_router.get("/privacy/events")
async def privacy_events(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_events()}


@data_security_router.get("/privacy/microservices")
async def privacy_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_microservices()}


@data_security_router.get("/privacy/apis")
async def privacy_apis(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_apis()}


@data_security_router.get("/privacy/integrations")
async def privacy_integrations(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_integrations()}


@data_security_router.get("/privacy/compliance")
async def privacy_compliance(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_compliance()}


@data_security_router.get("/privacy/outputs")
async def privacy_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_outputs()}


@data_security_router.get("/privacy/production-readiness")
async def privacy_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_production_readiness()}


@data_security_router.get("/privacy/readiness")
async def privacy_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().privacy_readiness()}


# --- P211-J Data Protection (Encrypt/Tokenize/Mask) ---------------------------


@data_security_router.get("/protection")
async def protection_summary(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().platform_protection()}


@data_security_router.get("/protection/architecture")
async def protection_architecture(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_architecture()}


@data_security_router.get("/protection/domain")
async def protection_domain(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_domain()}


@data_security_router.get("/protection/encryption")
async def protection_encryption(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_encryption()}


@data_security_router.get("/protection/tokenization")
async def protection_tokenization(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_tokenization()}


@data_security_router.get("/protection/masking")
async def protection_masking(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_masking()}


@data_security_router.get("/protection/anonymization")
async def protection_anonymization(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_anonymization()}


@data_security_router.get("/protection/decisions")
async def protection_decisions(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_decisions()}


@data_security_router.get("/protection/keys")
async def protection_keys(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_keys()}


@data_security_router.get("/protection/ai")
async def protection_ai(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_ai()}


@data_security_router.get("/protection/knowledge-graph")
async def protection_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_knowledge_graph()}


@data_security_router.get("/protection/digital-twin")
async def protection_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_digital_twin()}


@data_security_router.get("/protection/cqrs")
async def protection_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_cqrs()}


@data_security_router.get("/protection/events")
async def protection_events(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_events()}


@data_security_router.get("/protection/microservices")
async def protection_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_microservices()}


@data_security_router.get("/protection/apis")
async def protection_apis(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_apis()}


@data_security_router.get("/protection/integrations")
async def protection_integrations(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_integrations()}


@data_security_router.get("/protection/compliance")
async def protection_compliance(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_compliance()}


@data_security_router.get("/protection/outputs")
async def protection_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_outputs()}


@data_security_router.get("/protection/production-readiness")
async def protection_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_production_readiness()}


@data_security_router.get("/protection/readiness")
async def protection_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().protection_readiness()}


# --- P211-K Lineage, Metadata & Intelligence Graph ---------------------------


@data_security_router.get("/intelligence")
async def intelligence_summary(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().platform_intelligence()}


@data_security_router.get("/intelligence/architecture")
async def intelligence_architecture(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().intelligence_architecture()}


@data_security_router.get("/intelligence/domain")
async def intelligence_domain(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().intelligence_domain()}


@data_security_router.get("/intelligence/metadata")
async def intelligence_metadata(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().intelligence_metadata()}


@data_security_router.get("/intelligence/lineage")
async def intelligence_lineage(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().intelligence_lineage()}


@data_security_router.get("/intelligence/connectors")
async def intelligence_connectors(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().intelligence_connectors()}


@data_security_router.get("/intelligence/knowledge-graph")
async def intelligence_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().intelligence_knowledge_graph()}


@data_security_router.get("/intelligence/ai")
async def intelligence_ai(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().intelligence_ai()}


@data_security_router.get("/intelligence/impact")
async def intelligence_impact(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().intelligence_impact()}


@data_security_router.get("/intelligence/observability")
async def intelligence_observability(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().intelligence_observability()}


@data_security_router.get("/intelligence/digital-twin")
async def intelligence_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().intelligence_digital_twin()}


@data_security_router.get("/intelligence/cqrs")
async def intelligence_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().intelligence_cqrs()}


@data_security_router.get("/intelligence/events")
async def intelligence_events(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().intelligence_events()}


@data_security_router.get("/intelligence/microservices")
async def intelligence_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().intelligence_microservices()}


@data_security_router.get("/intelligence/apis")
async def intelligence_apis(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().intelligence_apis()}


@data_security_router.get("/intelligence/integrations")
async def intelligence_integrations(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().intelligence_integrations()}


@data_security_router.get("/intelligence/outputs")
async def intelligence_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().intelligence_outputs()}


@data_security_router.get("/intelligence/production-readiness")
async def intelligence_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().intelligence_production_readiness()}


@data_security_router.get("/intelligence/readiness")
async def intelligence_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().intelligence_readiness()}


# --- P211-L AI Intelligence & Autonomous Protection --------------------------


@data_security_router.get("/ai-data")
async def ai_summary(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().platform_ai()}


@data_security_router.get("/ai-data/architecture")
async def ai_architecture(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_architecture()}


@data_security_router.get("/ai-data/domain")
async def ai_domain(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_domain()}


@data_security_router.get("/ai-data/explainability")
async def ai_explainability(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_explainability()}


@data_security_router.get("/ai-data/autonomy")
async def ai_autonomy(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_autonomy()}


@data_security_router.get("/ai-data/risk")
async def ai_risk(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_risk()}


@data_security_router.get("/ai-data/agents")
async def ai_agents(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_agents()}


@data_security_router.get("/ai-data/models")
async def ai_models(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_models()}


@data_security_router.get("/ai-data/decisions")
async def ai_decisions(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_decisions()}


@data_security_router.get("/ai-data/learning")
async def ai_learning(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_learning()}


@data_security_router.get("/ai-data/governance")
async def ai_governance(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_governance()}


@data_security_router.get("/ai-data/oversight")
async def ai_oversight(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_oversight()}


@data_security_router.get("/ai-data/knowledge-graph")
async def ai_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_knowledge_graph()}


@data_security_router.get("/ai-data/digital-twin")
async def ai_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_digital_twin()}


@data_security_router.get("/ai-data/cqrs")
async def ai_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_cqrs()}


@data_security_router.get("/ai-data/events")
async def ai_events(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_events()}


@data_security_router.get("/ai-data/microservices")
async def ai_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_microservices()}


@data_security_router.get("/ai-data/apis")
async def ai_apis(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_apis()}


@data_security_router.get("/ai-data/integrations")
async def ai_integrations(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_integrations()}


@data_security_router.get("/ai-data/outputs")
async def ai_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_outputs()}


@data_security_router.get("/ai-data/production-readiness")
async def ai_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_production_readiness()}


@data_security_router.get("/ai-data/readiness")
async def ai_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ai_readiness()}


# --- P211-M Digital Twin & Privacy Simulation --------------------------------


@data_security_router.get("/twin")
async def twin_summary(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().platform_twin()}


@data_security_router.get("/twin/architecture")
async def twin_architecture(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_architecture()}


@data_security_router.get("/twin/domain")
async def twin_domain(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_domain()}


@data_security_router.get("/twin/representation")
async def twin_representation(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_representation()}


@data_security_router.get("/twin/simulation")
async def twin_simulation(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_simulation()}


@data_security_router.get("/twin/risk")
async def twin_risk(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_risk()}


@data_security_router.get("/twin/compliance")
async def twin_compliance(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_compliance()}


@data_security_router.get("/twin/dpia")
async def twin_dpia(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_dpia()}


@data_security_router.get("/twin/ai-privacy")
async def twin_ai_privacy(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_ai_privacy()}


@data_security_router.get("/twin/controls")
async def twin_controls(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_controls()}


@data_security_router.get("/twin/optimization")
async def twin_optimization(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_optimization()}


@data_security_router.get("/twin/knowledge-graph")
async def twin_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_knowledge_graph()}


@data_security_router.get("/twin/explainability")
async def twin_explainability(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_explainability()}


@data_security_router.get("/twin/cqrs")
async def twin_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_cqrs()}


@data_security_router.get("/twin/events")
async def twin_events(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_events()}


@data_security_router.get("/twin/microservices")
async def twin_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_microservices()}


@data_security_router.get("/twin/apis")
async def twin_apis(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_apis()}


@data_security_router.get("/twin/integrations")
async def twin_integrations(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_integrations()}


@data_security_router.get("/twin/outputs")
async def twin_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_outputs()}


@data_security_router.get("/twin/production-readiness")
async def twin_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_production_readiness()}


@data_security_router.get("/twin/readiness")
async def twin_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().twin_readiness()}


# --- P211-N CQRS, Events, APIs & Microservices -------------------------------


@data_security_router.get("/ops")
async def ops_summary(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().platform_ops()}


@data_security_router.get("/ops/architecture")
async def ops_architecture(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_architecture()}


@data_security_router.get("/ops/domain")
async def ops_domain(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_domain()}


@data_security_router.get("/ops/cqrs")
async def ops_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_cqrs()}


@data_security_router.get("/ops/commands")
async def ops_commands(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_commands()}


@data_security_router.get("/ops/queries")
async def ops_queries(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_queries()}


@data_security_router.get("/ops/events")
async def ops_events(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_events()}


@data_security_router.get("/ops/streaming")
async def ops_streaming(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_streaming()}


@data_security_router.get("/ops/microservices")
async def ops_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_microservices()}


@data_security_router.get("/ops/api-gateway")
async def ops_api_gateway(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_api_gateway()}


@data_security_router.get("/ops/api-governance")
async def ops_api_governance(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_api_governance()}


@data_security_router.get("/ops/communication")
async def ops_communication(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_communication()}


@data_security_router.get("/ops/service-mesh")
async def ops_service_mesh(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_service_mesh()}


@data_security_router.get("/ops/knowledge-graph")
async def ops_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_knowledge_graph()}


@data_security_router.get("/ops/digital-twin")
async def ops_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_digital_twin()}


@data_security_router.get("/ops/ai-events")
async def ops_ai_events(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_ai_events()}


@data_security_router.get("/ops/security")
async def ops_security(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_security()}


@data_security_router.get("/ops/deployment")
async def ops_deployment(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_deployment()}


@data_security_router.get("/ops/integrations")
async def ops_integrations(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_integrations()}


@data_security_router.get("/ops/outputs")
async def ops_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_outputs()}


@data_security_router.get("/ops/production-readiness")
async def ops_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_production_readiness()}


@data_security_router.get("/ops/readiness")
async def ops_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().ops_readiness()}


# --- P211-O Deployment, DevSecOps & Observability ----------------------------


@data_security_router.get("/deploy")
async def deploy_summary(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().platform_deploy()}


@data_security_router.get("/deploy/architecture")
async def deploy_architecture(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_architecture()}


@data_security_router.get("/deploy/domain")
async def deploy_domain(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_domain()}


@data_security_router.get("/deploy/kubernetes")
async def deploy_kubernetes(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_kubernetes()}


@data_security_router.get("/deploy/containers")
async def deploy_containers(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_containers()}


@data_security_router.get("/deploy/devsecops")
async def deploy_devsecops(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_devsecops()}


@data_security_router.get("/deploy/scanning")
async def deploy_scanning(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_scanning()}


@data_security_router.get("/deploy/iac")
async def deploy_iac(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_iac()}


@data_security_router.get("/deploy/gitops")
async def deploy_gitops(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_gitops()}


@data_security_router.get("/deploy/service-mesh")
async def deploy_service_mesh(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_service_mesh()}


@data_security_router.get("/deploy/scaling")
async def deploy_scaling(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_scaling()}


@data_security_router.get("/deploy/ha")
async def deploy_ha(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_ha()}


@data_security_router.get("/deploy/dr")
async def deploy_dr(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_dr()}


@data_security_router.get("/deploy/observability")
async def deploy_observability(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_observability()}


@data_security_router.get("/deploy/security-observability")
async def deploy_security_observability(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_security_observability()}


@data_security_router.get("/deploy/aiops")
async def deploy_aiops(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_aiops()}


@data_security_router.get("/deploy/platform-security")
async def deploy_platform_security(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_platform_security()}


@data_security_router.get("/deploy/compliance")
async def deploy_compliance(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_compliance()}


@data_security_router.get("/deploy/services")
async def deploy_services(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_services()}


@data_security_router.get("/deploy/cqrs")
async def deploy_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_cqrs()}


@data_security_router.get("/deploy/integrations")
async def deploy_integrations(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_integrations()}


@data_security_router.get("/deploy/outputs")
async def deploy_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_outputs()}


@data_security_router.get("/deploy/production-readiness")
async def deploy_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_production_readiness()}


@data_security_router.get("/deploy/readiness")
async def deploy_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().deploy_readiness()}


# --- P211-P Testing, Governance, Compliance & DoD ---------------------------


@data_security_router.get("/qa")
async def qa_summary(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().platform_qa()}


@data_security_router.get("/qa/architecture")
async def qa_architecture(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_architecture()}


@data_security_router.get("/qa/domain")
async def qa_domain(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_domain()}


@data_security_router.get("/qa/testing")
async def qa_testing(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_testing()}


@data_security_router.get("/qa/security")
async def qa_security(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_security()}


@data_security_router.get("/qa/privacy")
async def qa_privacy(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_privacy()}


@data_security_router.get("/qa/ai")
async def qa_ai(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_ai()}


@data_security_router.get("/qa/performance")
async def qa_performance(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_performance()}


@data_security_router.get("/qa/chaos")
async def qa_chaos(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_chaos()}


@data_security_router.get("/qa/compliance")
async def qa_compliance(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_compliance()}


@data_security_router.get("/qa/governance")
async def qa_governance(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_governance()}


@data_security_router.get("/qa/quality-gates")
async def qa_quality_gates(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_quality_gates()}


@data_security_router.get("/qa/evidence")
async def qa_evidence(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_evidence()}


@data_security_router.get("/qa/risk")
async def qa_risk(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_risk()}


@data_security_router.get("/qa/assurance-graph")
async def qa_assurance_graph(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_assurance_graph()}


@data_security_router.get("/qa/twin")
async def qa_twin(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_twin()}


@data_security_router.get("/qa/definition-of-done")
async def qa_definition_of_done(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_definition_of_done()}


@data_security_router.get("/qa/cqrs")
async def qa_cqrs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_cqrs()}


@data_security_router.get("/qa/events")
async def qa_events(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_events()}


@data_security_router.get("/qa/microservices")
async def qa_microservices(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_microservices()}


@data_security_router.get("/qa/integrations")
async def qa_integrations(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_integrations()}


@data_security_router.get("/qa/outputs")
async def qa_outputs(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_outputs()}


@data_security_router.get("/qa/production-readiness")
async def qa_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_production_readiness()}


@data_security_router.get("/qa/readiness")
async def qa_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("data_security.read"))],
) -> dict:
    return {"data": get_data_security_service().qa_readiness()}

