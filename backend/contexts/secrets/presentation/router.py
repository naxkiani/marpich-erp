"""Enterprise Secrets, PKI, KMS & Cryptographic Trust Platform API."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)
from contexts.secrets.container import get_secrets_service

secrets_router = APIRouter(
    prefix="/secrets",
    tags=["Enterprise Secrets / PKI / Cryptographic Trust"],
)


@secrets_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
):
    return {"data": (await get_secrets_service().list_catalog()).unwrap()}


@secrets_router.get("")
async def secrets_summary(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    return {"data": get_secrets_service().platform_crypto_trust()}


@secrets_router.get("/domains")
async def secrets_domains(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform as plat

    return {"data": plat.domains()}


@secrets_router.get("/pki")
async def secrets_pki(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform as plat

    return {"data": plat.pki()}


@secrets_router.get("/kms")
async def secrets_kms(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform as plat

    return {"data": plat.kms()}


@secrets_router.get("/secrets-management")
async def secrets_management(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform as plat

    return {"data": plat.secrets_management()}


@secrets_router.get("/hsm")
async def secrets_hsm(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    # P209-K deep surface — first-match wins over later duplicate /hsm
    return {"data": get_secrets_service().platform_hsm()}


@secrets_router.get("/workload-identity")
async def secrets_workload_identity(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform as plat

    return {"data": plat.workload_identity()}


@secrets_router.get("/crypto-services")
async def secrets_crypto_services(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform as plat

    return {"data": plat.crypto_services()}


@secrets_router.get("/pqc")
async def secrets_pqc(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform as plat

    return {"data": plat.pqc()}


@secrets_router.get("/knowledge-graph")
async def secrets_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform as plat

    return {"data": plat.knowledge_graph()}


@secrets_router.get("/digital-twin")
async def secrets_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform as plat

    return {"data": plat.digital_twin()}


@secrets_router.get("/ai")
async def secrets_ai(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform as plat

    return {"data": plat.ai()}


@secrets_router.get("/security")
async def secrets_security(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform as plat

    return {"data": plat.security()}


@secrets_router.get("/compliance")
async def secrets_compliance(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform as plat

    return {"data": plat.compliance()}


@secrets_router.get("/ddd")
async def secrets_ddd(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform as plat

    return {"data": plat.ddd()}


@secrets_router.get("/cqrs")
async def secrets_cqrs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform as plat

    return {"data": plat.cqrs()}


@secrets_router.get("/events")
async def secrets_events(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform as plat

    return {"data": {"events": list(plat.DOMAIN_EVENTS)}}


@secrets_router.get("/integrations")
async def secrets_integrations(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform as plat

    return {"data": plat.integrations()}


@secrets_router.get("/outputs")
async def secrets_outputs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform as plat

    return {"data": plat.cursor_outputs()}


@secrets_router.get("/production-readiness")
async def secrets_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform as plat

    return {"data": plat.production_readiness()}


@secrets_router.get("/readiness")
async def secrets_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services.secrets_foundation import (
        validate_secrets_foundation,
    )

    return {"data": validate_secrets_foundation()}


# --- P209-A Strategy surface ---


@secrets_router.get("/strategy")
async def secrets_strategy_summary(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    return {"data": get_secrets_service().platform_strategy()}


@secrets_router.get("/strategy/domains")
async def secrets_strategy_domains(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.primary_domains()}


@secrets_router.get("/strategy/root-of-trust")
async def secrets_strategy_root_of_trust(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.root_of_trust()}


@secrets_router.get("/strategy/pki")
async def secrets_strategy_pki(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.pki()}


@secrets_router.get("/strategy/kms")
async def secrets_strategy_kms(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.kms()}


@secrets_router.get("/strategy/secrets-management")
async def secrets_strategy_secrets_management(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.secrets_management()}


@secrets_router.get("/strategy/vault")
async def secrets_strategy_vault(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.vault()}


@secrets_router.get("/strategy/hsm")
async def secrets_strategy_hsm(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.hsm()}


@secrets_router.get("/strategy/workload-identity")
async def secrets_strategy_workload_identity(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.workload_identity()}


@secrets_router.get("/strategy/crypto-services")
async def secrets_strategy_crypto_services(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.crypto_services()}


@secrets_router.get("/strategy/pqc")
async def secrets_strategy_pqc(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.pqc()}


@secrets_router.get("/strategy/knowledge-graph")
async def secrets_strategy_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.knowledge_graph()}


@secrets_router.get("/strategy/digital-twin")
async def secrets_strategy_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.digital_twin()}


@secrets_router.get("/strategy/ai")
async def secrets_strategy_ai(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.ai()}


@secrets_router.get("/strategy/security")
async def secrets_strategy_security(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.security()}


@secrets_router.get("/strategy/lifecycle")
async def secrets_strategy_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.lifecycle()}


@secrets_router.get("/strategy/capabilities")
async def secrets_strategy_capabilities(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.capability_map()}


@secrets_router.get("/strategy/ddd")
async def secrets_strategy_ddd(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.ddd()}


@secrets_router.get("/strategy/cqrs")
async def secrets_strategy_cqrs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.cqrs()}


@secrets_router.get("/strategy/events")
async def secrets_strategy_events(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": {"events": list(strat.DOMAIN_EVENTS)}}


@secrets_router.get("/strategy/integrations")
async def secrets_strategy_integrations(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.integrations()}


@secrets_router.get("/strategy/outputs")
async def secrets_strategy_outputs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.cursor_outputs()}


@secrets_router.get("/strategy/production-readiness")
async def secrets_strategy_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )

    return {"data": strat.production_readiness()}


@secrets_router.get("/strategy/readiness")
async def secrets_strategy_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services.secrets_strategy_foundation import (
        validate_secrets_strategy_foundation,
    )

    return {"data": validate_secrets_strategy_foundation()}


# --- P209-B Mission / Vision / Scope surface ---


@secrets_router.get("/mission")
async def secrets_mission_summary(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    return {"data": get_secrets_service().platform_mission_scope()}


@secrets_router.get("/mission/vision")
async def secrets_mission_vision(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_mission_scope as mscope,
    )

    return {"data": mscope.vision()}


@secrets_router.get("/mission/objectives")
async def secrets_mission_objectives(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_mission_scope as mscope,
    )

    return {"data": mscope.strategic_objectives()}


@secrets_router.get("/mission/scope")
async def secrets_mission_scope(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_mission_scope as mscope,
    )

    return {"data": mscope.enterprise_scope()}


@secrets_router.get("/mission/boundaries")
async def secrets_mission_boundaries(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_mission_scope as mscope,
    )

    return {"data": mscope.boundaries()}


@secrets_router.get("/mission/capabilities")
async def secrets_mission_capabilities(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_mission_scope as mscope,
    )

    return {"data": mscope.business_capabilities()}


@secrets_router.get("/mission/stakeholders")
async def secrets_mission_stakeholders(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_mission_scope as mscope,
    )

    return {"data": mscope.stakeholders()}


@secrets_router.get("/mission/use-cases")
async def secrets_mission_use_cases(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_mission_scope as mscope,
    )

    return {"data": mscope.use_cases()}


@secrets_router.get("/mission/principles")
async def secrets_mission_principles(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_mission_scope as mscope,
    )

    return {"data": mscope.principles()}


@secrets_router.get("/mission/integrations")
async def secrets_mission_integrations(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_mission_scope as mscope,
    )

    return {"data": mscope.meos_integrations()}


@secrets_router.get("/mission/roadmap")
async def secrets_mission_roadmap(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_mission_scope as mscope,
    )

    return {"data": mscope.evolution_roadmap()}


@secrets_router.get("/mission/kpis")
async def secrets_mission_kpis(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_mission_scope as mscope,
    )

    return {"data": mscope.kpis()}


@secrets_router.get("/mission/ddd")
async def secrets_mission_ddd(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_mission_scope as mscope,
    )

    return {"data": mscope.ddd()}


@secrets_router.get("/mission/cqrs")
async def secrets_mission_cqrs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_mission_scope as mscope,
    )

    return {"data": mscope.cqrs()}


@secrets_router.get("/mission/events")
async def secrets_mission_events(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_mission_scope as mscope,
    )

    return {"data": {"events": list(mscope.DOMAIN_EVENTS)}}


@secrets_router.get("/mission/outputs")
async def secrets_mission_outputs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_mission_scope as mscope,
    )

    return {"data": mscope.cursor_outputs()}


@secrets_router.get("/mission/production-readiness")
async def secrets_mission_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_mission_scope as mscope,
    )

    return {"data": mscope.production_readiness()}


@secrets_router.get("/mission/readiness")
async def secrets_mission_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services.secrets_mission_foundation import (
        validate_secrets_mission_foundation,
    )

    return {"data": validate_secrets_mission_foundation()}


# --- P209-C Domain Architecture surface ---


@secrets_router.get("/domain")
async def secrets_domain_summary(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    return {"data": get_secrets_service().platform_domain()}


@secrets_router.get("/domain/strategic")
async def secrets_domain_strategic(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )

    return {"data": pdom.strategic_design()}


@secrets_router.get("/domain/bounded-contexts")
async def secrets_domain_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )

    return {"data": pdom.bounded_contexts()}


@secrets_router.get("/domain/pki-kms-separation")
async def secrets_domain_pki_kms_separation(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )

    return {"data": pdom.pki_kms_separation()}


@secrets_router.get("/domain/secrets-management")
async def secrets_domain_secrets_management(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )

    return {"data": pdom.secrets_management()}


@secrets_router.get("/domain/trust-model")
async def secrets_domain_trust_model(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )

    return {"data": pdom.trust_model()}


@secrets_router.get("/domain/services")
async def secrets_domain_services(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )

    return {"data": pdom.domain_services()}


@secrets_router.get("/domain/policies")
async def secrets_domain_policies(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )

    return {"data": pdom.domain_policies()}


@secrets_router.get("/domain/aggregates")
async def secrets_domain_aggregates(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )

    return {"data": pdom.aggregates()}


@secrets_router.get("/domain/lifecycle")
async def secrets_domain_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )

    return {"data": pdom.lifecycle()}


@secrets_router.get("/domain/events")
async def secrets_domain_events(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )

    return {"data": pdom.events()}


@secrets_router.get("/domain/cqrs")
async def secrets_domain_cqrs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )

    return {"data": pdom.cqrs()}


@secrets_router.get("/domain/microservices")
async def secrets_domain_microservices(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )

    return {"data": pdom.microservices()}


@secrets_router.get("/domain/knowledge-graph")
async def secrets_domain_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )

    return {"data": pdom.knowledge_graph()}


@secrets_router.get("/domain/digital-twin")
async def secrets_domain_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )

    return {"data": pdom.digital_twin()}


@secrets_router.get("/domain/integrations")
async def secrets_domain_integrations(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )

    return {"data": pdom.integrations()}


@secrets_router.get("/domain/ddd")
async def secrets_domain_ddd(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )

    return {"data": pdom.ddd()}


@secrets_router.get("/domain/outputs")
async def secrets_domain_outputs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )

    return {"data": pdom.cursor_outputs()}


@secrets_router.get("/domain/production-readiness")
async def secrets_domain_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )

    return {"data": pdom.production_readiness()}


@secrets_router.get("/domain/readiness")
async def secrets_domain_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services.secrets_domain_foundation import (
        validate_secrets_domain_foundation,
    )

    return {"data": validate_secrets_domain_foundation()}


# --- P209-D Enterprise PKI surface ---


@secrets_router.get("/pki")
async def secrets_pki_summary(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    return {"data": get_secrets_service().platform_pki()}


@secrets_router.get("/pki/hierarchy")
async def secrets_pki_hierarchy(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.hierarchy()}


@secrets_router.get("/pki/ca-platform")
async def secrets_pki_ca_platform(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.ca_platform()}


@secrets_router.get("/pki/root-ca")
async def secrets_pki_root_ca(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.root_ca()}


@secrets_router.get("/pki/issuing")
async def secrets_pki_issuing(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.issuing()}


@secrets_router.get("/pki/lifecycle")
async def secrets_pki_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.lifecycle()}


@secrets_router.get("/pki/revocation")
async def secrets_pki_revocation(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.revocation()}


@secrets_router.get("/pki/validation")
async def secrets_pki_validation(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.validation()}


@secrets_router.get("/pki/ownership")
async def secrets_pki_ownership(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.ownership()}


@secrets_router.get("/pki/audit")
async def secrets_pki_audit(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.audit()}


@secrets_router.get("/pki/automation")
async def secrets_pki_automation(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.automation()}


@secrets_router.get("/pki/workload")
async def secrets_pki_workload(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.workload_pki()}


@secrets_router.get("/pki/ai")
async def secrets_pki_ai(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.ai()}


@secrets_router.get("/pki/security")
async def secrets_pki_security(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.security()}


@secrets_router.get("/pki/ddd")
async def secrets_pki_ddd(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.ddd()}


@secrets_router.get("/pki/cqrs")
async def secrets_pki_cqrs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.cqrs()}


@secrets_router.get("/pki/events")
async def secrets_pki_events(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": {"events": list(pki.DOMAIN_EVENTS)}}


@secrets_router.get("/pki/microservices")
async def secrets_pki_microservices(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.microservices()}


@secrets_router.get("/pki/integrations")
async def secrets_pki_integrations(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.integrations()}


@secrets_router.get("/pki/outputs")
async def secrets_pki_outputs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.cursor_outputs()}


@secrets_router.get("/pki/production-readiness")
async def secrets_pki_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_pki as pki

    return {"data": pki.production_readiness()}


@secrets_router.get("/pki/readiness")
async def secrets_pki_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services.secrets_pki_foundation import (
        validate_secrets_pki_foundation,
    )

    return {"data": validate_secrets_pki_foundation()}


# --- P209-E Enterprise Certificate Authority & Trust Chain surface ---


@secrets_router.get("/ca")
async def secrets_ca_summary(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    return {"data": get_secrets_service().platform_ca()}


@secrets_router.get("/ca/hierarchy")
async def secrets_ca_hierarchy(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.hierarchy()}


@secrets_router.get("/ca/root-ca")
async def secrets_ca_root_ca(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.root_ca()}


@secrets_router.get("/ca/key-ceremony")
async def secrets_ca_key_ceremony(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.key_ceremony()}


@secrets_router.get("/ca/intermediate")
async def secrets_ca_intermediate(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.intermediate_ca()}


@secrets_router.get("/ca/issuing")
async def secrets_ca_issuing(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.issuing_ca()}


@secrets_router.get("/ca/trust-chain")
async def secrets_ca_trust_chain(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.trust_chain()}


@secrets_router.get("/ca/governance")
async def secrets_ca_governance(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.governance()}


@secrets_router.get("/ca/policy")
async def secrets_ca_policy(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.policy_framework()}


@secrets_router.get("/ca/security")
async def secrets_ca_security(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.security()}


@secrets_router.get("/ca/revocation")
async def secrets_ca_revocation(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.revocation()}


@secrets_router.get("/ca/ownership")
async def secrets_ca_ownership(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.ownership()}


@secrets_router.get("/ca/audit")
async def secrets_ca_audit(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.audit()}


@secrets_router.get("/ca/trust-distribution")
async def secrets_ca_trust_distribution(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.trust_distribution()}


@secrets_router.get("/ca/automation")
async def secrets_ca_automation(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.automation()}


@secrets_router.get("/ca/ai")
async def secrets_ca_ai(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.ai()}


@secrets_router.get("/ca/ddd")
async def secrets_ca_ddd(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.ddd()}


@secrets_router.get("/ca/cqrs")
async def secrets_ca_cqrs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.cqrs()}


@secrets_router.get("/ca/events")
async def secrets_ca_events(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": {"events": list(ca.DOMAIN_EVENTS)}}


@secrets_router.get("/ca/microservices")
async def secrets_ca_microservices(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.microservices()}


@secrets_router.get("/ca/integrations")
async def secrets_ca_integrations(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.integrations()}


@secrets_router.get("/ca/outputs")
async def secrets_ca_outputs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.cursor_outputs()}


@secrets_router.get("/ca/production-readiness")
async def secrets_ca_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ca as ca

    return {"data": ca.production_readiness()}


@secrets_router.get("/ca/readiness")
async def secrets_ca_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services.secrets_ca_foundation import (
        validate_secrets_ca_foundation,
    )

    return {"data": validate_secrets_ca_foundation()}


# --- P209-F Enterprise Key Management Service (KMS) surface ---


@secrets_router.get("/kms")
async def secrets_kms_summary(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    return {"data": get_secrets_service().platform_kms()}


@secrets_router.get("/kms/architecture")
async def secrets_kms_architecture(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.architecture()}


@secrets_router.get("/kms/domain-model")
async def secrets_kms_domain_model(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.domain_model()}


@secrets_router.get("/kms/key-types")
async def secrets_kms_key_types(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.key_types()}


@secrets_router.get("/kms/lifecycle")
async def secrets_kms_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.lifecycle()}


@secrets_router.get("/kms/generation")
async def secrets_kms_generation(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.generation()}


@secrets_router.get("/kms/hsm")
async def secrets_kms_hsm(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.hsm()}


@secrets_router.get("/kms/protection")
async def secrets_kms_protection(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.protection()}


@secrets_router.get("/kms/envelope")
async def secrets_kms_envelope(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.envelope_encryption()}


@secrets_router.get("/kms/access-control")
async def secrets_kms_access_control(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.access_control()}


@secrets_router.get("/kms/policy")
async def secrets_kms_policy(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.crypto_policy()}


@secrets_router.get("/kms/ownership")
async def secrets_kms_ownership(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.ownership()}


@secrets_router.get("/kms/audit")
async def secrets_kms_audit(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.audit()}


@secrets_router.get("/kms/federation")
async def secrets_kms_federation(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.federation()}


@secrets_router.get("/kms/ai")
async def secrets_kms_ai(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.ai()}


@secrets_router.get("/kms/security")
async def secrets_kms_security(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.security()}


@secrets_router.get("/kms/ddd")
async def secrets_kms_ddd(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.ddd()}


@secrets_router.get("/kms/cqrs")
async def secrets_kms_cqrs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.cqrs()}


@secrets_router.get("/kms/events")
async def secrets_kms_events(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": {"events": list(kms.DOMAIN_EVENTS)}}


@secrets_router.get("/kms/microservices")
async def secrets_kms_microservices(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.microservices()}


@secrets_router.get("/kms/integrations")
async def secrets_kms_integrations(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.integrations()}


@secrets_router.get("/kms/outputs")
async def secrets_kms_outputs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.cursor_outputs()}


@secrets_router.get("/kms/production-readiness")
async def secrets_kms_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_kms as kms

    return {"data": kms.production_readiness()}


@secrets_router.get("/kms/readiness")
async def secrets_kms_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services.secrets_kms_foundation import (
        validate_secrets_kms_foundation,
    )

    return {"data": validate_secrets_kms_foundation()}


# --- P209-G Enterprise Secrets Management & Vault surface ---


@secrets_router.get("/vault")
async def secrets_vault_summary(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    return {"data": get_secrets_service().platform_vault()}


@secrets_router.get("/vault/architecture")
async def secrets_vault_architecture(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.architecture()}


@secrets_router.get("/vault/domain-model")
async def secrets_vault_domain_model(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.domain_model()}


@secrets_router.get("/vault/secret-types")
async def secrets_vault_secret_types(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.secret_types()}


@secrets_router.get("/vault/lifecycle")
async def secrets_vault_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.lifecycle()}


@secrets_router.get("/vault/dynamic")
async def secrets_vault_dynamic(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.dynamic_secrets()}


@secrets_router.get("/vault/capabilities")
async def secrets_vault_capabilities(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.vault_capabilities()}


@secrets_router.get("/vault/access-control")
async def secrets_vault_access_control(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.access_control()}


@secrets_router.get("/vault/rotation")
async def secrets_vault_rotation(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.rotation()}


@secrets_router.get("/vault/kubernetes")
async def secrets_vault_kubernetes(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.kubernetes()}


@secrets_router.get("/vault/devsecops")
async def secrets_vault_devsecops(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.devsecops()}


@secrets_router.get("/vault/discovery")
async def secrets_vault_discovery(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.discovery()}


@secrets_router.get("/vault/ownership")
async def secrets_vault_ownership(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.ownership()}


@secrets_router.get("/vault/audit")
async def secrets_vault_audit(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.audit()}


@secrets_router.get("/vault/ai")
async def secrets_vault_ai(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.ai()}


@secrets_router.get("/vault/security")
async def secrets_vault_security(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.security()}


@secrets_router.get("/vault/ddd")
async def secrets_vault_ddd(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.ddd()}


@secrets_router.get("/vault/cqrs")
async def secrets_vault_cqrs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.cqrs()}


@secrets_router.get("/vault/events")
async def secrets_vault_events(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": {"events": list(vault.DOMAIN_EVENTS)}}


@secrets_router.get("/vault/microservices")
async def secrets_vault_microservices(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.microservices()}


@secrets_router.get("/vault/integrations")
async def secrets_vault_integrations(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.integrations()}


@secrets_router.get("/vault/outputs")
async def secrets_vault_outputs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.cursor_outputs()}


@secrets_router.get("/vault/production-readiness")
async def secrets_vault_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_vault as vault

    return {"data": vault.production_readiness()}


@secrets_router.get("/vault/readiness")
async def secrets_vault_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services.secrets_vault_foundation import (
        validate_secrets_vault_foundation,
    )

    return {"data": validate_secrets_vault_foundation()}


# --- P209-H Workload Identity, SPIFFE/SPIRE & mTLS surface ---


@secrets_router.get("/workload")
async def secrets_workload_summary(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    return {"data": get_secrets_service().platform_workload()}


@secrets_router.get("/workload/architecture")
async def secrets_workload_architecture(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.architecture()}


@secrets_router.get("/workload/spiffe")
async def secrets_workload_spiffe(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.spiffe()}


@secrets_router.get("/workload/spire")
async def secrets_workload_spire(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.spire()}


@secrets_router.get("/workload/lifecycle")
async def secrets_workload_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.lifecycle()}


@secrets_router.get("/workload/mtls")
async def secrets_workload_mtls(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.mtls()}


@secrets_router.get("/workload/service-mesh")
async def secrets_workload_service_mesh(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.service_mesh()}


@secrets_router.get("/workload/kubernetes")
async def secrets_workload_kubernetes(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.kubernetes()}


@secrets_router.get("/workload/cloud")
async def secrets_workload_cloud(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.cloud()}


@secrets_router.get("/workload/attestation")
async def secrets_workload_attestation(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.attestation()}


@secrets_router.get("/workload/zero-trust")
async def secrets_workload_zero_trust(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.zero_trust()}


@secrets_router.get("/workload/authorization")
async def secrets_workload_authorization(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.authorization_integration()}


@secrets_router.get("/workload/secretless")
async def secrets_workload_secretless(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.secretless()}


@secrets_router.get("/workload/trust-domain")
async def secrets_workload_trust_domain(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.trust_domain()}


@secrets_router.get("/workload/ownership")
async def secrets_workload_ownership(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.ownership()}


@secrets_router.get("/workload/audit")
async def secrets_workload_audit(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.audit()}


@secrets_router.get("/workload/ai")
async def secrets_workload_ai(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.ai()}


@secrets_router.get("/workload/security")
async def secrets_workload_security(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.security()}


@secrets_router.get("/workload/ddd")
async def secrets_workload_ddd(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.ddd()}


@secrets_router.get("/workload/cqrs")
async def secrets_workload_cqrs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.cqrs()}


@secrets_router.get("/workload/events")
async def secrets_workload_events(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": {"events": list(wl.DOMAIN_EVENTS)}}


@secrets_router.get("/workload/microservices")
async def secrets_workload_microservices(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.microservices()}


@secrets_router.get("/workload/integrations")
async def secrets_workload_integrations(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.integrations()}


@secrets_router.get("/workload/outputs")
async def secrets_workload_outputs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.cursor_outputs()}


@secrets_router.get("/workload/production-readiness")
async def secrets_workload_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_workload as wl

    return {"data": wl.production_readiness()}


@secrets_router.get("/workload/readiness")
async def secrets_workload_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services.secrets_workload_foundation import (
        validate_secrets_workload_foundation,
    )

    return {"data": validate_secrets_workload_foundation()}


# --- P209-I Enterprise Cryptography Services & Encryption surface ---


@secrets_router.get("/crypto")
async def secrets_crypto_summary(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    return {"data": get_secrets_service().platform_crypto()}


@secrets_router.get("/crypto/architecture")
async def secrets_crypto_architecture(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.architecture()}


@secrets_router.get("/crypto/domain-model")
async def secrets_crypto_domain_model(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.domain_model()}


@secrets_router.get("/crypto/encryption")
async def secrets_crypto_encryption(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.encryption()}


@secrets_router.get("/crypto/decryption")
async def secrets_crypto_decryption(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.decryption()}


@secrets_router.get("/crypto/signatures")
async def secrets_crypto_signatures(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.signatures()}


@secrets_router.get("/crypto/hashing")
async def secrets_crypto_hashing(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.hashing()}


@secrets_router.get("/crypto/key-exchange")
async def secrets_crypto_key_exchange(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.key_exchange()}


@secrets_router.get("/crypto/token")
async def secrets_crypto_token(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.token_cryptography()}


@secrets_router.get("/crypto/eaas")
async def secrets_crypto_eaas(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.eaas()}


@secrets_router.get("/crypto/policy")
async def secrets_crypto_policy(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.crypto_policy()}


@secrets_router.get("/crypto/confidential")
async def secrets_crypto_confidential(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.confidential_computing()}


@secrets_router.get("/crypto/unmanaged")
async def secrets_crypto_unmanaged(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.unmanaged()}


@secrets_router.get("/crypto/key-exposure")
async def secrets_crypto_key_exposure(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.key_exposure()}


@secrets_router.get("/crypto/audit")
async def secrets_crypto_audit(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.audit()}


@secrets_router.get("/crypto/ai")
async def secrets_crypto_ai(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.ai()}


@secrets_router.get("/crypto/security")
async def secrets_crypto_security(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.security()}


@secrets_router.get("/crypto/ddd")
async def secrets_crypto_ddd(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.ddd()}


@secrets_router.get("/crypto/cqrs")
async def secrets_crypto_cqrs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.cqrs()}


@secrets_router.get("/crypto/events")
async def secrets_crypto_events(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": {"events": list(crypto.DOMAIN_EVENTS)}}


@secrets_router.get("/crypto/microservices")
async def secrets_crypto_microservices(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.microservices()}


@secrets_router.get("/crypto/integrations")
async def secrets_crypto_integrations(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.integrations()}


@secrets_router.get("/crypto/outputs")
async def secrets_crypto_outputs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.cursor_outputs()}


@secrets_router.get("/crypto/production-readiness")
async def secrets_crypto_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto

    return {"data": crypto.production_readiness()}


@secrets_router.get("/crypto/readiness")
async def secrets_crypto_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services.secrets_crypto_foundation import (
        validate_secrets_crypto_foundation,
    )

    return {"data": validate_secrets_crypto_foundation()}


# --- P209-J Digital Signature, Code Signing & Supply Chain Trust surface ---


@secrets_router.get("/signing")
async def secrets_signing_summary(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    return {"data": get_secrets_service().platform_signing()}


@secrets_router.get("/signing/architecture")
async def secrets_signing_architecture(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.architecture()}


@secrets_router.get("/signing/domain-model")
async def secrets_signing_domain_model(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.domain_model()}


@secrets_router.get("/signing/code-signing")
async def secrets_signing_code_signing(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.code_signing()}


@secrets_router.get("/signing/supply-chain")
async def secrets_signing_supply_chain(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.supply_chain()}


@secrets_router.get("/signing/artifacts")
async def secrets_signing_artifacts(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.artifacts()}


@secrets_router.get("/signing/attestation")
async def secrets_signing_attestation(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.attestation()}


@secrets_router.get("/signing/sbom")
async def secrets_signing_sbom(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.sbom()}


@secrets_router.get("/signing/cicd")
async def secrets_signing_cicd(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.cicd()}


@secrets_router.get("/signing/hsm")
async def secrets_signing_hsm(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.hsm_signing()}


@secrets_router.get("/signing/certificates")
async def secrets_signing_certificates(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.certificate_trust()}


@secrets_router.get("/signing/ai-models")
async def secrets_signing_ai_models(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.ai_model_signing()}


@secrets_router.get("/signing/deployment-trust")
async def secrets_signing_deployment_trust(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.deployment_trust()}


@secrets_router.get("/signing/ownership")
async def secrets_signing_ownership(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.ownership()}


@secrets_router.get("/signing/audit")
async def secrets_signing_audit(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.audit()}


@secrets_router.get("/signing/ai")
async def secrets_signing_ai(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.ai()}


@secrets_router.get("/signing/security")
async def secrets_signing_security(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.security()}


@secrets_router.get("/signing/ddd")
async def secrets_signing_ddd(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.ddd()}


@secrets_router.get("/signing/cqrs")
async def secrets_signing_cqrs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.cqrs()}


@secrets_router.get("/signing/events")
async def secrets_signing_events(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": {"events": list(signing.DOMAIN_EVENTS)}}


@secrets_router.get("/signing/microservices")
async def secrets_signing_microservices(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.microservices()}


@secrets_router.get("/signing/integrations")
async def secrets_signing_integrations(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.integrations()}


@secrets_router.get("/signing/outputs")
async def secrets_signing_outputs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.cursor_outputs()}


@secrets_router.get("/signing/production-readiness")
async def secrets_signing_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )

    return {"data": signing.production_readiness()}


@secrets_router.get("/signing/readiness")
async def secrets_signing_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services.secrets_signing_foundation import (
        validate_secrets_signing_foundation,
    )

    return {"data": validate_secrets_signing_foundation()}


# --- P209-K AI Cryptography, HSM, Confidential Computing & PQC surface ---


@secrets_router.get("/hsm")
async def secrets_hsm_summary(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    return {"data": get_secrets_service().platform_hsm()}


@secrets_router.get("/hsm/architecture")
async def secrets_hsm_architecture(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.architecture()}


@secrets_router.get("/hsm/ai-crypto")
async def secrets_hsm_ai_crypto(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.ai_crypto()}


@secrets_router.get("/hsm/platform")
async def secrets_hsm_platform(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.hsm()}


@secrets_router.get("/hsm/management")
async def secrets_hsm_management(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.hsm_management()}


@secrets_router.get("/hsm/confidential")
async def secrets_hsm_confidential(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.confidential_computing()}


@secrets_router.get("/hsm/confidential-ai")
async def secrets_hsm_confidential_ai(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.confidential_ai()}


@secrets_router.get("/hsm/pqc")
async def secrets_hsm_pqc(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.pqc()}


@secrets_router.get("/hsm/agility")
async def secrets_hsm_agility(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.crypto_agility()}


@secrets_router.get("/hsm/hardware-trust")
async def secrets_hsm_hardware_trust(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.hardware_trust()}


@secrets_router.get("/hsm/risk")
async def secrets_hsm_risk(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.risk()}


@secrets_router.get("/hsm/agents")
async def secrets_hsm_agents(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.agents()}


@secrets_router.get("/hsm/zero-trust")
async def secrets_hsm_zero_trust(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.zero_trust()}


@secrets_router.get("/hsm/security")
async def secrets_hsm_security(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.security()}


@secrets_router.get("/hsm/ddd")
async def secrets_hsm_ddd(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.ddd()}


@secrets_router.get("/hsm/cqrs")
async def secrets_hsm_cqrs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.cqrs()}


@secrets_router.get("/hsm/events")
async def secrets_hsm_events(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": {"events": list(hsm.DOMAIN_EVENTS)}}


@secrets_router.get("/hsm/microservices")
async def secrets_hsm_microservices(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.microservices()}


@secrets_router.get("/hsm/integrations")
async def secrets_hsm_integrations(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.integrations()}


@secrets_router.get("/hsm/outputs")
async def secrets_hsm_outputs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.cursor_outputs()}


@secrets_router.get("/hsm/production-readiness")
async def secrets_hsm_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm

    return {"data": hsm.production_readiness()}


@secrets_router.get("/hsm/readiness")
async def secrets_hsm_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services.secrets_hsm_foundation import (
        validate_secrets_hsm_foundation,
    )

    return {"data": validate_secrets_hsm_foundation()}


# --- P209-L CQRS, Events, APIs & Microservices Platform surface ---


@secrets_router.get("/ops")
async def secrets_ops_summary(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    return {"data": get_secrets_service().platform_ops()}


@secrets_router.get("/ops/architecture")
async def secrets_ops_architecture(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.architecture()}


@secrets_router.get("/ops/microservices")
async def secrets_ops_microservices(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.microservice_map()}


@secrets_router.get("/ops/cqrs")
async def secrets_ops_cqrs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.cqrs()}


@secrets_router.get("/ops/events")
async def secrets_ops_events(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": {"events": list(ops.DOMAIN_EVENTS)}}


@secrets_router.get("/ops/event-streaming")
async def secrets_ops_event_streaming(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.event_streaming()}


@secrets_router.get("/ops/api")
async def secrets_ops_api(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.api_platform()}


@secrets_router.get("/ops/api-security")
async def secrets_ops_api_security(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.api_security()}


@secrets_router.get("/ops/communication")
async def secrets_ops_communication(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.communication()}


@secrets_router.get("/ops/data")
async def secrets_ops_data(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.data_architecture()}


@secrets_router.get("/ops/knowledge-graph")
async def secrets_ops_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.knowledge_graph()}


@secrets_router.get("/ops/digital-twin")
async def secrets_ops_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.digital_twin()}


@secrets_router.get("/ops/ai")
async def secrets_ops_ai(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.ai_operations()}


@secrets_router.get("/ops/observability")
async def secrets_ops_observability(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.observability()}


@secrets_router.get("/ops/deployment")
async def secrets_ops_deployment(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.deployment()}


@secrets_router.get("/ops/resilience")
async def secrets_ops_resilience(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.resilience()}


@secrets_router.get("/ops/security")
async def secrets_ops_security(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.security()}


@secrets_router.get("/ops/ddd")
async def secrets_ops_ddd(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.ddd()}


@secrets_router.get("/ops/integrations")
async def secrets_ops_integrations(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.integrations()}


@secrets_router.get("/ops/outputs")
async def secrets_ops_outputs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.cursor_outputs()}


@secrets_router.get("/ops/production-readiness")
async def secrets_ops_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_ops as ops

    return {"data": ops.production_readiness()}


@secrets_router.get("/ops/readiness")
async def secrets_ops_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services.secrets_ops_foundation import (
        validate_secrets_ops_foundation,
    )

    return {"data": validate_secrets_ops_foundation()}


# --- P209-M AI Security, Cryptographic Governance & Compliance surface ---


@secrets_router.get("/gov")
async def secrets_gov_summary(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    return {"data": get_secrets_service().platform_gov()}


@secrets_router.get("/gov/architecture")
async def secrets_gov_architecture(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.architecture()}


@secrets_router.get("/gov/ai-security")
async def secrets_gov_ai_security(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.ai_security_governance()}


@secrets_router.get("/gov/crypto-governance")
async def secrets_gov_crypto_governance(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.cryptographic_governance()}


@secrets_router.get("/gov/ai-crypto")
async def secrets_gov_ai_crypto(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.ai_crypto_security()}


@secrets_router.get("/gov/risk")
async def secrets_gov_risk(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.risk_intelligence()}


@secrets_router.get("/gov/policy")
async def secrets_gov_policy(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.policy_governance()}


@secrets_router.get("/gov/responsible-ai")
async def secrets_gov_responsible_ai(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.responsible_ai()}


@secrets_router.get("/gov/compliance")
async def secrets_gov_compliance(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.compliance_automation()}


@secrets_router.get("/gov/controls")
async def secrets_gov_controls(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.control_framework()}


@secrets_router.get("/gov/agents")
async def secrets_gov_agents(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.agents()}


@secrets_router.get("/gov/knowledge-graph")
async def secrets_gov_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.knowledge_graph()}


@secrets_router.get("/gov/digital-twin")
async def secrets_gov_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.digital_twin()}


@secrets_router.get("/gov/continuous-validation")
async def secrets_gov_continuous_validation(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.continuous_validation()}


@secrets_router.get("/gov/incident-response")
async def secrets_gov_incident_response(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.incident_response()}


@secrets_router.get("/gov/security")
async def secrets_gov_security(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.security()}


@secrets_router.get("/gov/ddd")
async def secrets_gov_ddd(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.ddd()}


@secrets_router.get("/gov/cqrs")
async def secrets_gov_cqrs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.cqrs()}


@secrets_router.get("/gov/events")
async def secrets_gov_events(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": {"events": list(gov.DOMAIN_EVENTS)}}


@secrets_router.get("/gov/microservices")
async def secrets_gov_microservices(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.microservices()}


@secrets_router.get("/gov/integrations")
async def secrets_gov_integrations(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.integrations()}


@secrets_router.get("/gov/outputs")
async def secrets_gov_outputs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.cursor_outputs()}


@secrets_router.get("/gov/production-readiness")
async def secrets_gov_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_gov as gov

    return {"data": gov.production_readiness()}


@secrets_router.get("/gov/readiness")
async def secrets_gov_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services.secrets_gov_foundation import (
        validate_secrets_gov_foundation,
    )

    return {"data": validate_secrets_gov_foundation()}


# --- P209-N Enterprise Deployment, DevSecOps, K8s & Observability surface ---


@secrets_router.get("/deploy")
async def secrets_deploy_summary(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    return {"data": get_secrets_service().platform_deploy()}


@secrets_router.get("/deploy/architecture")
async def secrets_deploy_architecture(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.architecture()}


@secrets_router.get("/deploy/kubernetes")
async def secrets_deploy_kubernetes(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.kubernetes()}


@secrets_router.get("/deploy/crypto")
async def secrets_deploy_crypto(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.crypto_deployment()}


@secrets_router.get("/deploy/gitops")
async def secrets_deploy_gitops(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.gitops()}


@secrets_router.get("/deploy/devsecops")
async def secrets_deploy_devsecops(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.devsecops()}


@secrets_router.get("/deploy/iac")
async def secrets_deploy_iac(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.iac()}


@secrets_router.get("/deploy/service-mesh")
async def secrets_deploy_service_mesh(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.service_mesh()}


@secrets_router.get("/deploy/scalability")
async def secrets_deploy_scalability(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.scalability()}


@secrets_router.get("/deploy/ha")
async def secrets_deploy_ha(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.high_availability()}


@secrets_router.get("/deploy/observability")
async def secrets_deploy_observability(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.observability()}


@secrets_router.get("/deploy/secops")
async def secrets_deploy_secops(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.secops()}


@secrets_router.get("/deploy/aiops")
async def secrets_deploy_aiops(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.aiops()}


@secrets_router.get("/deploy/disaster-recovery")
async def secrets_deploy_disaster_recovery(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.disaster_recovery()}


@secrets_router.get("/deploy/zero-trust")
async def secrets_deploy_zero_trust(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.zero_trust()}


@secrets_router.get("/deploy/security")
async def secrets_deploy_security(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.security()}


@secrets_router.get("/deploy/ddd")
async def secrets_deploy_ddd(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.ddd()}


@secrets_router.get("/deploy/cqrs")
async def secrets_deploy_cqrs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.cqrs()}


@secrets_router.get("/deploy/events")
async def secrets_deploy_events(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": {"events": list(deploy.DOMAIN_EVENTS)}}


@secrets_router.get("/deploy/microservices")
async def secrets_deploy_microservices(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.microservices()}


@secrets_router.get("/deploy/integrations")
async def secrets_deploy_integrations(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.integrations()}


@secrets_router.get("/deploy/outputs")
async def secrets_deploy_outputs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.cursor_outputs()}


@secrets_router.get("/deploy/production-readiness")
async def secrets_deploy_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy

    return {"data": deploy.production_readiness()}


@secrets_router.get("/deploy/readiness")
async def secrets_deploy_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services.secrets_deploy_foundation import (
        validate_secrets_deploy_foundation,
    )

    return {"data": validate_secrets_deploy_foundation()}


# --- P209-O Testing, Governance, Security Validation & DoD surface ---


@secrets_router.get("/qa")
async def secrets_qa_summary(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    return {"data": get_secrets_service().platform_qa()}


@secrets_router.get("/qa/architecture")
async def secrets_qa_architecture(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.architecture()}


@secrets_router.get("/qa/cryptographic")
async def secrets_qa_cryptographic(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.cryptographic_testing()}


@secrets_router.get("/qa/pki")
async def secrets_qa_pki(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.pki_testing()}


@secrets_router.get("/qa/kms-hsm")
async def secrets_qa_kms_hsm(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.kms_hsm_testing()}


@secrets_router.get("/qa/secrets")
async def secrets_qa_secrets(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.secrets_testing()}


@secrets_router.get("/qa/workload-identity")
async def secrets_qa_workload_identity(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.workload_identity_testing()}


@secrets_router.get("/qa/zero-trust")
async def secrets_qa_zero_trust(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.zero_trust_validation()}


@secrets_router.get("/qa/performance")
async def secrets_qa_performance(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.performance_testing()}


@secrets_router.get("/qa/chaos")
async def secrets_qa_chaos(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.chaos_engineering()}


@secrets_router.get("/qa/security-testing")
async def secrets_qa_security_testing(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.security_testing()}


@secrets_router.get("/qa/devsecops")
async def secrets_qa_devsecops(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.devsecops_validation()}


@secrets_router.get("/qa/governance")
async def secrets_qa_governance(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.governance()}


@secrets_router.get("/qa/compliance")
async def secrets_qa_compliance(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.compliance()}


@secrets_router.get("/qa/continuous-validation")
async def secrets_qa_continuous_validation(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.continuous_validation()}


@secrets_router.get("/qa/knowledge-graph")
async def secrets_qa_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.knowledge_graph()}


@secrets_router.get("/qa/digital-twin")
async def secrets_qa_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.digital_twin()}


@secrets_router.get("/qa/definition-of-done")
async def secrets_qa_definition_of_done(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.definition_of_done()}


@secrets_router.get("/qa/security")
async def secrets_qa_security(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.security()}


@secrets_router.get("/qa/ddd")
async def secrets_qa_ddd(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.ddd()}


@secrets_router.get("/qa/cqrs")
async def secrets_qa_cqrs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.cqrs()}


@secrets_router.get("/qa/events")
async def secrets_qa_events(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": {"events": list(qa.DOMAIN_EVENTS)}}


@secrets_router.get("/qa/microservices")
async def secrets_qa_microservices(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.microservices()}


@secrets_router.get("/qa/integrations")
async def secrets_qa_integrations(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.integrations()}


@secrets_router.get("/qa/outputs")
async def secrets_qa_outputs(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.cursor_outputs()}


@secrets_router.get("/qa/production-readiness")
async def secrets_qa_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services import secrets_platform_qa as qa

    return {"data": qa.production_readiness()}


@secrets_router.get("/qa/readiness")
async def secrets_qa_readiness(
    _user: Annotated[dict, Depends(require_permissions("secrets.read"))],
) -> dict:
    from contexts.secrets.domain.services.secrets_qa_foundation import (
        validate_secrets_qa_foundation,
    )

    return {"data": validate_secrets_qa_foundation()}
