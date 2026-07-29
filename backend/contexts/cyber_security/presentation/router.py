"""Enterprise Cyber Security & Threat Defense Platform API (P210-A–O)."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from contexts.cyber_security.container import get_cyber_security_service
from contexts.identity.presentation.dependencies import require_permissions

cyber_security_router = APIRouter(
    prefix="/cyber-security",
    tags=["Enterprise Cyber Security & Threat Defense"],
)


@cyber_security_router.get("/catalog")
async def catalog(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": (await get_cyber_security_service().list_catalog()).unwrap()}


@cyber_security_router.get("/strategy")
async def strategy_summary(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().platform_strategy()}


@cyber_security_router.get("/strategy/capabilities")
async def strategy_capabilities(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_capabilities()}


@cyber_security_router.get("/strategy/layers")
async def strategy_layers(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_layers()}


@cyber_security_router.get("/strategy/protection-domains")
async def strategy_protection_domains(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_protection_domains()}


@cyber_security_router.get("/strategy/principles")
async def strategy_principles(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_principles()}


@cyber_security_router.get("/strategy/services")
async def strategy_services(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_services()}


@cyber_security_router.get("/strategy/event-sources")
async def strategy_event_sources(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_event_sources()}


@cyber_security_router.get("/strategy/soc")
async def strategy_soc(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_soc()}


@cyber_security_router.get("/strategy/siem")
async def strategy_siem(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_siem()}


@cyber_security_router.get("/strategy/soar")
async def strategy_soar(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_soar()}


@cyber_security_router.get("/strategy/xdr")
async def strategy_xdr(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_xdr()}


@cyber_security_router.get("/strategy/threat-intelligence")
async def strategy_threat_intelligence(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_threat_intelligence()}


@cyber_security_router.get("/strategy/ai")
async def strategy_ai(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_ai()}


@cyber_security_router.get("/strategy/security")
async def strategy_security(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_security()}


@cyber_security_router.get("/strategy/ddd")
async def strategy_ddd(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_ddd()}


@cyber_security_router.get("/strategy/cqrs")
async def strategy_cqrs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_cqrs()}


@cyber_security_router.get("/strategy/events")
async def strategy_events(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_events()}


@cyber_security_router.get("/strategy/microservices")
async def strategy_microservices(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_microservices()}


@cyber_security_router.get("/strategy/integrations")
async def strategy_integrations(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_integrations()}


@cyber_security_router.get("/strategy/roadmap")
async def strategy_roadmap(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_roadmap()}


@cyber_security_router.get("/strategy/outputs")
async def strategy_outputs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_outputs()}


@cyber_security_router.get("/strategy/production-readiness")
async def strategy_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_production_readiness()}


@cyber_security_router.get("/strategy/readiness")
async def strategy_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().strategy_readiness()}


# --- P210-B Mission / Vision / Scope -----------------------------------------


@cyber_security_router.get("/mission")
async def mission_summary(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().platform_mission_scope()}


@cyber_security_router.get("/mission/statement")
async def mission_statement(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_statement()}


@cyber_security_router.get("/mission/vision")
async def mission_vision(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_vision()}


@cyber_security_router.get("/mission/strategic-objectives")
async def mission_strategic_objectives(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_strategic_objectives()}


@cyber_security_router.get("/mission/business-objectives")
async def mission_business_objectives(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_business_objectives()}


@cyber_security_router.get("/mission/scope")
async def mission_scope(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_scope()}


@cyber_security_router.get("/mission/security-domains")
async def mission_security_domains(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_security_domains()}


@cyber_security_router.get("/mission/capabilities")
async def mission_capabilities(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_capabilities()}


@cyber_security_router.get("/mission/principles")
async def mission_principles(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_principles()}


@cyber_security_router.get("/mission/stakeholders")
async def mission_stakeholders(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_stakeholders()}


@cyber_security_router.get("/mission/kpis")
async def mission_kpis(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_kpis()}


@cyber_security_router.get("/mission/risks")
async def mission_risks(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_risks()}


@cyber_security_router.get("/mission/architecture-principles")
async def mission_architecture_principles(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_architecture_principles()}


@cyber_security_router.get("/mission/meos-alignment")
async def mission_meos_alignment(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_meos_alignment()}


@cyber_security_router.get("/mission/ddd")
async def mission_ddd(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_ddd()}


@cyber_security_router.get("/mission/cqrs")
async def mission_cqrs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_cqrs()}


@cyber_security_router.get("/mission/events")
async def mission_events(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_events()}


@cyber_security_router.get("/mission/integrations")
async def mission_integrations(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_integrations()}


@cyber_security_router.get("/mission/outputs")
async def mission_outputs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_outputs()}


@cyber_security_router.get("/mission/production-readiness")
async def mission_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_production_readiness()}


@cyber_security_router.get("/mission/readiness")
async def mission_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().mission_readiness()}


# --- P210-C Domain Architecture (DDD) ----------------------------------------


@cyber_security_router.get("/domain")
async def domain_summary(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().platform_domain()}


@cyber_security_router.get("/domain/strategic-model")
async def domain_strategic_model(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_strategic_model()}


@cyber_security_router.get("/domain/bounded-contexts")
async def domain_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_bounded_contexts()}


@cyber_security_router.get("/domain/context-map")
async def domain_context_map(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_context_map()}


@cyber_security_router.get("/domain/aggregates")
async def domain_aggregates(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_aggregates()}


@cyber_security_router.get("/domain/entities")
async def domain_entities(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_entities()}


@cyber_security_router.get("/domain/value-objects")
async def domain_value_objects(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_value_objects()}


@cyber_security_router.get("/domain/services")
async def domain_services(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_services()}


@cyber_security_router.get("/domain/events")
async def domain_events(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_events()}


@cyber_security_router.get("/domain/repositories")
async def domain_repositories(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_repositories()}


@cyber_security_router.get("/domain/application-services")
async def domain_application_services(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_application_services()}


@cyber_security_router.get("/domain/knowledge-graph")
async def domain_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_knowledge_graph()}


@cyber_security_router.get("/domain/digital-twin")
async def domain_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_digital_twin()}


@cyber_security_router.get("/domain/policies")
async def domain_policies(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_policies()}


@cyber_security_router.get("/domain/acl")
async def domain_acl(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_acl()}


@cyber_security_router.get("/domain/ubiquitous-language")
async def domain_ubiquitous_language(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_ubiquitous_language()}


@cyber_security_router.get("/domain/ddd")
async def domain_ddd(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_ddd()}


@cyber_security_router.get("/domain/cqrs")
async def domain_cqrs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_cqrs()}


@cyber_security_router.get("/domain/outputs")
async def domain_outputs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_outputs()}


@cyber_security_router.get("/domain/production-readiness")
async def domain_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_production_readiness()}


@cyber_security_router.get("/domain/readiness")
async def domain_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().domain_readiness()}


# --- P210-D Security Operations Center (SOC) ---------------------------------


@cyber_security_router.get("/soc")
async def soc_summary(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().platform_soc()}


@cyber_security_router.get("/soc/architecture")
async def soc_architecture(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_architecture()}


@cyber_security_router.get("/soc/domains")
async def soc_domains(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_domains()}


@cyber_security_router.get("/soc/telemetry")
async def soc_telemetry(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_telemetry()}


@cyber_security_router.get("/soc/alerts")
async def soc_alerts(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_alerts()}


@cyber_security_router.get("/soc/incidents")
async def soc_incidents(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_incidents()}


@cyber_security_router.get("/soc/cases")
async def soc_cases(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_cases()}


@cyber_security_router.get("/soc/hunting")
async def soc_hunting(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_hunting()}


@cyber_security_router.get("/soc/ai")
async def soc_ai(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_ai()}


@cyber_security_router.get("/soc/knowledge-graph")
async def soc_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_knowledge_graph()}


@cyber_security_router.get("/soc/digital-twin")
async def soc_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_digital_twin()}


@cyber_security_router.get("/soc/response")
async def soc_response(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_response()}


@cyber_security_router.get("/soc/dashboards")
async def soc_dashboards(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_dashboards()}


@cyber_security_router.get("/soc/ddd")
async def soc_ddd(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_ddd()}


@cyber_security_router.get("/soc/cqrs")
async def soc_cqrs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_cqrs()}


@cyber_security_router.get("/soc/events")
async def soc_events(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_events()}


@cyber_security_router.get("/soc/microservices")
async def soc_microservices(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_microservices()}


@cyber_security_router.get("/soc/integrations")
async def soc_integrations(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_integrations()}


@cyber_security_router.get("/soc/outputs")
async def soc_outputs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_outputs()}


@cyber_security_router.get("/soc/production-readiness")
async def soc_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_production_readiness()}


@cyber_security_router.get("/soc/readiness")
async def soc_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soc_readiness()}


# --- P210-F Enterprise SOAR --------------------------------------------------


@cyber_security_router.get("/soar")
async def soar_summary(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().platform_soar()}


@cyber_security_router.get("/soar/architecture")
async def soar_architecture(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_architecture()}


@cyber_security_router.get("/soar/orchestration")
async def soar_orchestration(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_orchestration()}


@cyber_security_router.get("/soar/playbooks")
async def soar_playbooks(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_playbooks()}


@cyber_security_router.get("/soar/automation")
async def soar_automation(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_automation()}


@cyber_security_router.get("/soar/workflows")
async def soar_workflows(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_workflows()}


@cyber_security_router.get("/soar/approvals")
async def soar_approvals(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_approvals()}


@cyber_security_router.get("/soar/ai")
async def soar_ai(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_ai()}


@cyber_security_router.get("/soar/knowledge-graph")
async def soar_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_knowledge_graph()}


@cyber_security_router.get("/soar/digital-twin")
async def soar_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_digital_twin()}


@cyber_security_router.get("/soar/connectors")
async def soar_connectors(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_connectors()}


@cyber_security_router.get("/soar/evidence")
async def soar_evidence(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_evidence()}


@cyber_security_router.get("/soar/observability")
async def soar_observability(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_observability()}


@cyber_security_router.get("/soar/governance")
async def soar_governance(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_governance()}


@cyber_security_router.get("/soar/ddd")
async def soar_ddd(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_ddd()}


@cyber_security_router.get("/soar/cqrs")
async def soar_cqrs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_cqrs()}


@cyber_security_router.get("/soar/events")
async def soar_events(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_events()}


@cyber_security_router.get("/soar/microservices")
async def soar_microservices(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_microservices()}


@cyber_security_router.get("/soar/integrations")
async def soar_integrations(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_integrations()}


@cyber_security_router.get("/soar/outputs")
async def soar_outputs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_outputs()}


@cyber_security_router.get("/soar/production-readiness")
async def soar_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_production_readiness()}


@cyber_security_router.get("/soar/readiness")
async def soar_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().soar_readiness()}


# --- P210-G Enterprise XDR / EDR / NDR ---------------------------------------


@cyber_security_router.get("/xdr")
async def xdr_summary(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().platform_xdr()}


@cyber_security_router.get("/xdr/architecture")
async def xdr_architecture(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_architecture()}


@cyber_security_router.get("/xdr/edr")
async def xdr_edr(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_edr()}


@cyber_security_router.get("/xdr/ndr")
async def xdr_ndr(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_ndr()}


@cyber_security_router.get("/xdr/correlation")
async def xdr_correlation(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_correlation()}


@cyber_security_router.get("/xdr/detection")
async def xdr_detection(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_detection()}


@cyber_security_router.get("/xdr/ai")
async def xdr_ai(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_ai()}


@cyber_security_router.get("/xdr/hunting")
async def xdr_hunting(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_hunting()}


@cyber_security_router.get("/xdr/response")
async def xdr_response(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_response()}


@cyber_security_router.get("/xdr/knowledge-graph")
async def xdr_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_knowledge_graph()}


@cyber_security_router.get("/xdr/digital-twin")
async def xdr_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_digital_twin()}


@cyber_security_router.get("/xdr/agent")
async def xdr_agent(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_agent()}


@cyber_security_router.get("/xdr/observability")
async def xdr_observability(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_observability()}


@cyber_security_router.get("/xdr/governance")
async def xdr_governance(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_governance()}


@cyber_security_router.get("/xdr/ddd")
async def xdr_ddd(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_ddd()}


@cyber_security_router.get("/xdr/cqrs")
async def xdr_cqrs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_cqrs()}


@cyber_security_router.get("/xdr/events")
async def xdr_events(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_events()}


@cyber_security_router.get("/xdr/microservices")
async def xdr_microservices(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_microservices()}


@cyber_security_router.get("/xdr/integrations")
async def xdr_integrations(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_integrations()}


@cyber_security_router.get("/xdr/outputs")
async def xdr_outputs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_outputs()}


@cyber_security_router.get("/xdr/production-readiness")
async def xdr_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_production_readiness()}


@cyber_security_router.get("/xdr/readiness")
async def xdr_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().xdr_readiness()}


# --- P210-E Enterprise SIEM --------------------------------------------------


@cyber_security_router.get("/siem")
async def siem_summary(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().platform_siem()}


@cyber_security_router.get("/siem/architecture")
async def siem_architecture(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_architecture()}


@cyber_security_router.get("/siem/telemetry")
async def siem_telemetry(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_telemetry()}


@cyber_security_router.get("/siem/ingestion")
async def siem_ingestion(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_ingestion()}


@cyber_security_router.get("/siem/correlation")
async def siem_correlation(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_correlation()}


@cyber_security_router.get("/siem/detection")
async def siem_detection(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_detection()}


@cyber_security_router.get("/siem/analytics")
async def siem_analytics(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_analytics()}


@cyber_security_router.get("/siem/ai")
async def siem_ai(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_ai()}


@cyber_security_router.get("/siem/alerts")
async def siem_alerts(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_alerts()}


@cyber_security_router.get("/siem/storage")
async def siem_storage(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_storage()}


@cyber_security_router.get("/siem/knowledge-graph")
async def siem_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_knowledge_graph()}


@cyber_security_router.get("/siem/digital-twin")
async def siem_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_digital_twin()}


@cyber_security_router.get("/siem/scalability")
async def siem_scalability(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_scalability()}


@cyber_security_router.get("/siem/observability")
async def siem_observability(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_observability()}


@cyber_security_router.get("/siem/governance")
async def siem_governance(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_governance()}


@cyber_security_router.get("/siem/ddd")
async def siem_ddd(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_ddd()}


@cyber_security_router.get("/siem/cqrs")
async def siem_cqrs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_cqrs()}


@cyber_security_router.get("/siem/events")
async def siem_events(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_events()}


@cyber_security_router.get("/siem/microservices")
async def siem_microservices(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_microservices()}


@cyber_security_router.get("/siem/integrations")
async def siem_integrations(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_integrations()}


@cyber_security_router.get("/siem/outputs")
async def siem_outputs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_outputs()}


@cyber_security_router.get("/siem/production-readiness")
async def siem_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_production_readiness()}


@cyber_security_router.get("/siem/readiness")
async def siem_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().siem_readiness()}


# --- P210-H Threat Intelligence & Hunting ------------------------------------


@cyber_security_router.get("/intel")
async def intel_summary(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().platform_intel()}


@cyber_security_router.get("/intel/architecture")
async def intel_architecture(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_architecture()}


@cyber_security_router.get("/intel/sources")
async def intel_sources(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_sources()}


@cyber_security_router.get("/intel/types")
async def intel_types(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_types()}


@cyber_security_router.get("/intel/entities")
async def intel_entities(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_entities()}


@cyber_security_router.get("/intel/hunting")
async def intel_hunting(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_hunting()}


@cyber_security_router.get("/intel/ai")
async def intel_ai(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_ai()}


@cyber_security_router.get("/intel/knowledge-graph")
async def intel_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_knowledge_graph()}


@cyber_security_router.get("/intel/digital-twin")
async def intel_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_digital_twin()}


@cyber_security_router.get("/intel/detection-engineering")
async def intel_detection_engineering(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_detection_engineering()}


@cyber_security_router.get("/intel/sharing")
async def intel_sharing(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_sharing()}


@cyber_security_router.get("/intel/validation")
async def intel_validation(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_validation()}


@cyber_security_router.get("/intel/observability")
async def intel_observability(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_observability()}


@cyber_security_router.get("/intel/governance")
async def intel_governance(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_governance()}


@cyber_security_router.get("/intel/ddd")
async def intel_ddd(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_ddd()}


@cyber_security_router.get("/intel/cqrs")
async def intel_cqrs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_cqrs()}


@cyber_security_router.get("/intel/events")
async def intel_events(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_events()}


@cyber_security_router.get("/intel/microservices")
async def intel_microservices(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_microservices()}


@cyber_security_router.get("/intel/integrations")
async def intel_integrations(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_integrations()}


@cyber_security_router.get("/intel/outputs")
async def intel_outputs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_outputs()}


@cyber_security_router.get("/intel/production-readiness")
async def intel_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_production_readiness()}


@cyber_security_router.get("/intel/readiness")
async def intel_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().intel_readiness()}


# --- P210-I ASM & CTEM -------------------------------------------------------


@cyber_security_router.get("/asm")
async def asm_summary(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().platform_asm()}


@cyber_security_router.get("/asm/architecture")
async def asm_architecture(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_architecture()}


@cyber_security_router.get("/asm/assets")
async def asm_assets(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_assets()}


@cyber_security_router.get("/asm/attack-surface")
async def asm_attack_surface(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_attack_surface()}


@cyber_security_router.get("/asm/exposures")
async def asm_exposures(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_exposures()}


@cyber_security_router.get("/asm/vulnerabilities")
async def asm_vulnerabilities(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_vulnerabilities()}


@cyber_security_router.get("/asm/attack-paths")
async def asm_attack_paths(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_attack_paths()}


@cyber_security_router.get("/asm/risk")
async def asm_risk(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_risk()}


@cyber_security_router.get("/asm/ai")
async def asm_ai(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_ai()}


@cyber_security_router.get("/asm/remediation")
async def asm_remediation(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_remediation()}


@cyber_security_router.get("/asm/ctem")
async def asm_ctem(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_ctem()}


@cyber_security_router.get("/asm/knowledge-graph")
async def asm_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_knowledge_graph()}


@cyber_security_router.get("/asm/digital-twin")
async def asm_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_digital_twin()}


@cyber_security_router.get("/asm/observability")
async def asm_observability(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_observability()}


@cyber_security_router.get("/asm/governance")
async def asm_governance(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_governance()}


@cyber_security_router.get("/asm/ddd")
async def asm_ddd(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_ddd()}


@cyber_security_router.get("/asm/cqrs")
async def asm_cqrs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_cqrs()}


@cyber_security_router.get("/asm/events")
async def asm_events(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_events()}


@cyber_security_router.get("/asm/microservices")
async def asm_microservices(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_microservices()}


@cyber_security_router.get("/asm/integrations")
async def asm_integrations(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_integrations()}


@cyber_security_router.get("/asm/outputs")
async def asm_outputs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_outputs()}


@cyber_security_router.get("/asm/production-readiness")
async def asm_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_production_readiness()}


@cyber_security_router.get("/asm/readiness")
async def asm_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().asm_readiness()}


# --- P210-J AI Security Operations & Autonomous SOC --------------------------


@cyber_security_router.get("/ai-ops")
async def ai_ops_summary(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().platform_ai_ops()}


@cyber_security_router.get("/ai-ops/architecture")
async def ai_ops_architecture(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_architecture()}


@cyber_security_router.get("/ai-ops/agents")
async def ai_ops_agents(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_agents()}


@cyber_security_router.get("/ai-ops/copilot")
async def ai_ops_copilot(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_copilot()}


@cyber_security_router.get("/ai-ops/reasoning")
async def ai_ops_reasoning(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_reasoning()}


@cyber_security_router.get("/ai-ops/memory")
async def ai_ops_memory(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_memory()}


@cyber_security_router.get("/ai-ops/knowledge-graph")
async def ai_ops_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_knowledge_graph()}


@cyber_security_router.get("/ai-ops/autonomous-response")
async def ai_ops_autonomous_response(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_autonomous_response()}


@cyber_security_router.get("/ai-ops/detection")
async def ai_ops_detection(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_detection()}


@cyber_security_router.get("/ai-ops/predictive")
async def ai_ops_predictive(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_predictive()}


@cyber_security_router.get("/ai-ops/digital-twin")
async def ai_ops_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_digital_twin()}


@cyber_security_router.get("/ai-ops/governance")
async def ai_ops_governance(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_governance()}


@cyber_security_router.get("/ai-ops/model-lifecycle")
async def ai_ops_model_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_model_lifecycle()}


@cyber_security_router.get("/ai-ops/observability")
async def ai_ops_observability(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_observability()}


@cyber_security_router.get("/ai-ops/ddd")
async def ai_ops_ddd(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_ddd()}


@cyber_security_router.get("/ai-ops/cqrs")
async def ai_ops_cqrs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_cqrs()}


@cyber_security_router.get("/ai-ops/events")
async def ai_ops_events(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_events()}


@cyber_security_router.get("/ai-ops/microservices")
async def ai_ops_microservices(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_microservices()}


@cyber_security_router.get("/ai-ops/integrations")
async def ai_ops_integrations(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_integrations()}


@cyber_security_router.get("/ai-ops/outputs")
async def ai_ops_outputs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_outputs()}


@cyber_security_router.get("/ai-ops/production-readiness")
async def ai_ops_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_production_readiness()}


@cyber_security_router.get("/ai-ops/readiness")
async def ai_ops_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ai_ops_readiness()}


# --- P210-K Cyber Knowledge Graph & Digital Twin -----------------------------


@cyber_security_router.get("/graph")
async def graph_summary(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().platform_graph()}


@cyber_security_router.get("/graph/architecture")
async def graph_architecture(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().graph_architecture()}


@cyber_security_router.get("/graph/ontology")
async def graph_ontology(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().graph_ontology()}


@cyber_security_router.get("/graph/entity-resolution")
async def graph_entity_resolution(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().graph_entity_resolution()}


@cyber_security_router.get("/graph/attack-paths")
async def graph_attack_paths(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().graph_attack_paths()}


@cyber_security_router.get("/graph/reasoning")
async def graph_reasoning(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().graph_reasoning()}


@cyber_security_router.get("/graph/digital-twin")
async def graph_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().graph_digital_twin()}


@cyber_security_router.get("/graph/simulation")
async def graph_simulation(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().graph_simulation()}


@cyber_security_router.get("/graph/ai")
async def graph_ai(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().graph_ai()}


@cyber_security_router.get("/graph/governance")
async def graph_governance(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().graph_governance()}


@cyber_security_router.get("/graph/observability")
async def graph_observability(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().graph_observability()}


@cyber_security_router.get("/graph/ddd")
async def graph_ddd(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().graph_ddd()}


@cyber_security_router.get("/graph/cqrs")
async def graph_cqrs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().graph_cqrs()}


@cyber_security_router.get("/graph/events")
async def graph_events(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().graph_events()}


@cyber_security_router.get("/graph/microservices")
async def graph_microservices(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().graph_microservices()}


@cyber_security_router.get("/graph/integrations")
async def graph_integrations(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().graph_integrations()}


@cyber_security_router.get("/graph/outputs")
async def graph_outputs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().graph_outputs()}


@cyber_security_router.get("/graph/production-readiness")
async def graph_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().graph_production_readiness()}


@cyber_security_router.get("/graph/readiness")
async def graph_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().graph_readiness()}


# --- P210-L CQRS, Events, APIs & Microservices -------------------------------


@cyber_security_router.get("/ops")
async def ops_summary(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().platform_ops()}


@cyber_security_router.get("/ops/bounded-contexts")
async def ops_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_bounded_contexts()}


@cyber_security_router.get("/ops/cqrs")
async def ops_cqrs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_cqrs()}


@cyber_security_router.get("/ops/commands")
async def ops_commands(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_commands()}


@cyber_security_router.get("/ops/queries")
async def ops_queries(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_queries()}


@cyber_security_router.get("/ops/events")
async def ops_events(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_events()}


@cyber_security_router.get("/ops/event-sourcing")
async def ops_event_sourcing(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_event_sourcing()}


@cyber_security_router.get("/ops/streaming")
async def ops_streaming(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_streaming()}


@cyber_security_router.get("/ops/microservices")
async def ops_microservices(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_microservices()}


@cyber_security_router.get("/ops/communication")
async def ops_communication(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_communication()}


@cyber_security_router.get("/ops/apis")
async def ops_apis(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_apis()}


@cyber_security_router.get("/ops/service-mesh")
async def ops_service_mesh(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_service_mesh()}


@cyber_security_router.get("/ops/data")
async def ops_data(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_data()}


@cyber_security_router.get("/ops/ai")
async def ops_ai(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_ai()}


@cyber_security_router.get("/ops/devsecops")
async def ops_devsecops(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_devsecops()}


@cyber_security_router.get("/ops/observability")
async def ops_observability(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_observability()}


@cyber_security_router.get("/ops/governance")
async def ops_governance(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_governance()}


@cyber_security_router.get("/ops/ddd")
async def ops_ddd(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_ddd()}


@cyber_security_router.get("/ops/integrations")
async def ops_integrations(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_integrations()}


@cyber_security_router.get("/ops/outputs")
async def ops_outputs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_outputs()}


@cyber_security_router.get("/ops/production-readiness")
async def ops_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_production_readiness()}


@cyber_security_router.get("/ops/readiness")
async def ops_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().ops_readiness()}


# --- P210-M AI Security Governance & Compliance ------------------------------


@cyber_security_router.get("/gov")
async def gov_summary(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().platform_gov()}


@cyber_security_router.get("/gov/architecture")
async def gov_architecture(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_architecture()}


@cyber_security_router.get("/gov/inventory")
async def gov_inventory(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_inventory()}


@cyber_security_router.get("/gov/models")
async def gov_models(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_models()}


@cyber_security_router.get("/gov/security")
async def gov_security(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_security()}


@cyber_security_router.get("/gov/responsible-ai")
async def gov_responsible_ai(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_responsible_ai()}


@cyber_security_router.get("/gov/policies")
async def gov_policies(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_policies()}


@cyber_security_router.get("/gov/risk")
async def gov_risk(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_risk()}


@cyber_security_router.get("/gov/monitoring")
async def gov_monitoring(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_monitoring()}


@cyber_security_router.get("/gov/agents")
async def gov_agents(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_agents()}


@cyber_security_router.get("/gov/compliance")
async def gov_compliance(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_compliance()}


@cyber_security_router.get("/gov/knowledge-graph")
async def gov_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_knowledge_graph()}


@cyber_security_router.get("/gov/digital-twin")
async def gov_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_digital_twin()}


@cyber_security_router.get("/gov/mlops")
async def gov_mlops(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_mlops()}


@cyber_security_router.get("/gov/observability")
async def gov_observability(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_observability()}


@cyber_security_router.get("/gov/ddd")
async def gov_ddd(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_ddd()}


@cyber_security_router.get("/gov/cqrs")
async def gov_cqrs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_cqrs()}


@cyber_security_router.get("/gov/events")
async def gov_events(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_events()}


@cyber_security_router.get("/gov/microservices")
async def gov_microservices(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_microservices()}


@cyber_security_router.get("/gov/integrations")
async def gov_integrations(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_integrations()}


@cyber_security_router.get("/gov/outputs")
async def gov_outputs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_outputs()}


@cyber_security_router.get("/gov/production-readiness")
async def gov_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_production_readiness()}


@cyber_security_router.get("/gov/readiness")
async def gov_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().gov_readiness()}


# --- P210-N Deploy / DevSecOps / K8s / Observability -------------------------


@cyber_security_router.get("/deploy")
async def deploy_summary(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().platform_deploy()}


@cyber_security_router.get("/deploy/architecture")
async def deploy_architecture(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_architecture()}


@cyber_security_router.get("/deploy/kubernetes")
async def deploy_kubernetes(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_kubernetes()}


@cyber_security_router.get("/deploy/container-security")
async def deploy_container_security(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_container_security()}


@cyber_security_router.get("/deploy/devsecops")
async def deploy_devsecops(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_devsecops()}


@cyber_security_router.get("/deploy/iac")
async def deploy_iac(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_iac()}


@cyber_security_router.get("/deploy/gitops")
async def deploy_gitops(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_gitops()}


@cyber_security_router.get("/deploy/service-mesh")
async def deploy_service_mesh(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_service_mesh()}


@cyber_security_router.get("/deploy/scalability")
async def deploy_scalability(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_scalability()}


@cyber_security_router.get("/deploy/resilience")
async def deploy_resilience(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_resilience()}


@cyber_security_router.get("/deploy/observability")
async def deploy_observability(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_observability()}


@cyber_security_router.get("/deploy/monitoring")
async def deploy_monitoring(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_monitoring()}


@cyber_security_router.get("/deploy/security-observability")
async def deploy_security_observability(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_security_observability()}


@cyber_security_router.get("/deploy/platform-engineering")
async def deploy_platform_engineering(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_platform_engineering()}


@cyber_security_router.get("/deploy/aiops")
async def deploy_aiops(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_aiops()}


@cyber_security_router.get("/deploy/cqrs")
async def deploy_cqrs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_cqrs()}


@cyber_security_router.get("/deploy/events")
async def deploy_events(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_events()}


@cyber_security_router.get("/deploy/microservices")
async def deploy_microservices(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_microservices()}


@cyber_security_router.get("/deploy/compliance")
async def deploy_compliance(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_compliance()}


@cyber_security_router.get("/deploy/integrations")
async def deploy_integrations(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_integrations()}


@cyber_security_router.get("/deploy/outputs")
async def deploy_outputs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_outputs()}


@cyber_security_router.get("/deploy/production-readiness")
async def deploy_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_production_readiness()}


@cyber_security_router.get("/deploy/readiness")
async def deploy_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().deploy_readiness()}


# --- P210-O Testing / Security Validation / DoD ------------------------------


@cyber_security_router.get("/qa")
async def qa_summary(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().platform_qa()}


@cyber_security_router.get("/qa/architecture")
async def qa_architecture(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_architecture()}


@cyber_security_router.get("/qa/domains")
async def qa_domains(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_domains()}


@cyber_security_router.get("/qa/security-testing")
async def qa_security_testing(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_security_testing()}


@cyber_security_router.get("/qa/penetration")
async def qa_penetration(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_penetration()}


@cyber_security_router.get("/qa/red-team")
async def qa_red_team(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_red_team()}


@cyber_security_router.get("/qa/blue-team")
async def qa_blue_team(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_blue_team()}


@cyber_security_router.get("/qa/purple-team")
async def qa_purple_team(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_purple_team()}


@cyber_security_router.get("/qa/ai-security")
async def qa_ai_security(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_ai_security()}


@cyber_security_router.get("/qa/validation")
async def qa_validation(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_validation()}


@cyber_security_router.get("/qa/chaos")
async def qa_chaos(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_chaos()}


@cyber_security_router.get("/qa/performance")
async def qa_performance(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_performance()}


@cyber_security_router.get("/qa/compliance")
async def qa_compliance(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_compliance()}


@cyber_security_router.get("/qa/automation")
async def qa_automation(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_automation()}


@cyber_security_router.get("/qa/knowledge-graph")
async def qa_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_knowledge_graph()}


@cyber_security_router.get("/qa/digital-twin")
async def qa_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_digital_twin()}


@cyber_security_router.get("/qa/observability")
async def qa_observability(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_observability()}


@cyber_security_router.get("/qa/cqrs")
async def qa_cqrs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_cqrs()}


@cyber_security_router.get("/qa/events")
async def qa_events(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_events()}


@cyber_security_router.get("/qa/microservices")
async def qa_microservices(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_microservices()}


@cyber_security_router.get("/qa/integrations")
async def qa_integrations(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_integrations()}


@cyber_security_router.get("/qa/outputs")
async def qa_outputs(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_outputs()}


@cyber_security_router.get("/qa/production-readiness")
async def qa_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_production_readiness()}


@cyber_security_router.get("/qa/readiness")
async def qa_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("cyber_security.read"))],
) -> dict:
    return {"data": get_cyber_security_service().qa_readiness()}

