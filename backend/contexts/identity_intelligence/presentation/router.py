"""Identity Intelligence presentation router (P207-A strategy surface)."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from contexts.identity.presentation.dependencies import require_permissions
from contexts.identity_intelligence.container import get_identity_intelligence_service

identity_intelligence_router = APIRouter(
    prefix="/identity-intelligence",
    tags=["Enterprise Identity Intelligence"],
)


@identity_intelligence_router.get("/strategy")
async def ii_strategy_summary(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    return {"data": get_identity_intelligence_service().platform_identity_intelligence()}


@identity_intelligence_router.get("/strategy/capabilities")
async def ii_strategy_capabilities(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.capabilities()}


@identity_intelligence_router.get("/strategy/mission")
async def ii_strategy_mission(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": {"mission": strat.MISSION_STATEMENT}}


@identity_intelligence_router.get("/strategy/vision")
async def ii_strategy_vision(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": {"vision": strat.VISION_STATEMENT}}


@identity_intelligence_router.get("/strategy/autonomous")
async def ii_strategy_autonomous(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.autonomous_operations()}


@identity_intelligence_router.get("/strategy/agents")
async def ii_strategy_agents(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.ai_agents()}


@identity_intelligence_router.get("/strategy/twins")
async def ii_strategy_twins(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.digital_twin()}


@identity_intelligence_router.get("/strategy/graph")
async def ii_strategy_graph(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.knowledge_graph()}


@identity_intelligence_router.get("/strategy/risk")
async def ii_strategy_risk(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.predictive_risk()}


@identity_intelligence_router.get("/strategy/behavior")
async def ii_strategy_behavior(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.behavioral_analytics()}


@identity_intelligence_router.get("/strategy/healing")
async def ii_strategy_healing(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.self_healing()}


@identity_intelligence_router.get("/strategy/access-governance")
async def ii_strategy_access_governance(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.autonomous_access_governance()}


@identity_intelligence_router.get("/strategy/ml")
async def ii_strategy_ml(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.ml_architecture()}


@identity_intelligence_router.get("/strategy/ai-governance")
async def ii_strategy_ai_governance(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.ai_security_governance()}


@identity_intelligence_router.get("/strategy/observability")
async def ii_strategy_observability(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.observability()}


@identity_intelligence_router.get("/strategy/zero-trust")
async def ii_strategy_zero_trust(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.zero_trust()}


@identity_intelligence_router.get("/strategy/ddd")
async def ii_strategy_ddd(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.ddd()}


@identity_intelligence_router.get("/strategy/cqrs")
async def ii_strategy_cqrs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.cqrs()}


@identity_intelligence_router.get("/strategy/events")
async def ii_strategy_events(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    c = strat.cqrs()
    return {"data": {"events": c["events"], "event_count": c["event_count"]}}


@identity_intelligence_router.get("/strategy/microservices")
async def ii_strategy_microservices(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.microservices()}


@identity_intelligence_router.get("/strategy/integrations")
async def ii_strategy_integrations(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.integrations()}


@identity_intelligence_router.get("/strategy/outputs")
async def ii_strategy_outputs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.cursor_outputs()}


@identity_intelligence_router.get("/strategy/production-readiness")
async def ii_strategy_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )

    return {"data": strat.production_readiness()}


@identity_intelligence_router.get("/strategy/readiness")
async def ii_strategy_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services.ii_platform_foundation import (
        validate_ii_strategy_foundation,
    )

    return {"data": validate_ii_strategy_foundation()}


@identity_intelligence_router.get("/mission")
async def ii_mission_summary(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    return {"data": get_identity_intelligence_service().platform_mission_scope()}


@identity_intelligence_router.get("/mission/statement")
async def ii_mission_statement(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_mission_scope as mscope,
    )

    return {"data": mscope.mission()}


@identity_intelligence_router.get("/mission/vision")
async def ii_mission_vision(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_mission_scope as mscope,
    )

    return {"data": mscope.vision()}


@identity_intelligence_router.get("/mission/purpose")
async def ii_mission_purpose(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_mission_scope as mscope,
    )

    return {"data": mscope.purpose()}


@identity_intelligence_router.get("/mission/objectives")
async def ii_mission_objectives(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_mission_scope as mscope,
    )

    return {"data": mscope.strategic_objectives()}


@identity_intelligence_router.get("/mission/scope")
async def ii_mission_scope(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_mission_scope as mscope,
    )

    return {"data": mscope.enterprise_scope()}


@identity_intelligence_router.get("/mission/out-of-scope")
async def ii_mission_out_of_scope(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_mission_scope as mscope,
    )

    scope = mscope.enterprise_scope()
    return {
        "data": {
            "out_of_scope": scope["out_of_scope"],
            "does_not_replace_peers": scope["does_not_replace_peers"],
        }
    }


@identity_intelligence_router.get("/mission/placement")
async def ii_mission_placement(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_mission_scope as mscope,
    )

    return {"data": mscope.meos_placement()}


@identity_intelligence_router.get("/mission/zero-trust")
async def ii_mission_zero_trust(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_mission_scope as mscope,
    )

    return {"data": mscope.zero_trust()}


@identity_intelligence_router.get("/mission/ai-governance")
async def ii_mission_ai_governance(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_mission_scope as mscope,
    )

    return {"data": mscope.ai_governance()}


@identity_intelligence_router.get("/mission/ddd")
async def ii_mission_ddd(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_mission_scope as mscope,
    )

    return {"data": mscope.ddd()}


@identity_intelligence_router.get("/mission/cqrs")
async def ii_mission_cqrs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_mission_scope as mscope,
    )

    return {"data": mscope.cqrs()}


@identity_intelligence_router.get("/mission/events")
async def ii_mission_events(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_mission_scope as mscope,
    )

    c = mscope.cqrs()
    return {"data": {"events": c["events"], "event_count": c["event_count"]}}


@identity_intelligence_router.get("/mission/integrations")
async def ii_mission_integrations(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_mission_scope as mscope,
    )

    return {"data": mscope.integrations()}


@identity_intelligence_router.get("/mission/production-readiness")
async def ii_mission_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_mission_scope as mscope,
    )

    return {"data": mscope.production_readiness()}


@identity_intelligence_router.get("/mission/readiness")
async def ii_mission_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services.ii_mission_foundation import (
        validate_ii_mission_foundation,
    )

    return {"data": validate_ii_mission_foundation()}


@identity_intelligence_router.get("/domain")
async def ii_domain_summary(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    return {"data": get_identity_intelligence_service().platform_domain()}


@identity_intelligence_router.get("/domain/purpose")
async def ii_domain_purpose(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_domain as pdom,
    )

    return {"data": pdom.purpose()}


@identity_intelligence_router.get("/domain/classification")
async def ii_domain_classification(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_domain as pdom,
    )

    return {"data": pdom.classification()}


@identity_intelligence_router.get("/domain/placement")
async def ii_domain_placement(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_domain as pdom,
    )

    return {"data": pdom.meos_placement()}


@identity_intelligence_router.get("/domain/language")
async def ii_domain_language(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_domain as pdom,
    )

    return {"data": pdom.ubiquitous_language()}


@identity_intelligence_router.get("/domain/bounded-contexts")
async def ii_domain_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_domain as pdom,
    )

    d = pdom.ddd()
    return {
        "data": {
            "logical_contexts": d["logical_contexts"],
            "logical_count": d["logical_count"],
            "boundaries_clear": d["boundaries_clear"],
        }
    }


@identity_intelligence_router.get("/domain/aggregates")
async def ii_domain_aggregates(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_domain as pdom,
    )

    d = pdom.ddd()
    return {
        "data": {
            "aggregates": d["aggregates"],
            "aggregate_count": d["aggregate_count"],
            "entities": d["entities"],
            "value_objects": d["value_objects"],
            "domain_services": d["domain_services"],
            "anemic_forbidden": d["anemic_forbidden"],
        }
    }


@identity_intelligence_router.get("/domain/cqrs")
async def ii_domain_cqrs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_domain as pdom,
    )

    return {"data": pdom.cqrs()}


@identity_intelligence_router.get("/domain/events")
async def ii_domain_events(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_domain as pdom,
    )

    c = pdom.cqrs()
    return {"data": {"events": c["events"], "event_count": c["event_count"]}}


@identity_intelligence_router.get("/domain/context-map")
async def ii_domain_context_map(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_domain as pdom,
    )

    return {"data": pdom.context_map()}


@identity_intelligence_router.get("/domain/invariants")
async def ii_domain_invariants(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_domain as pdom,
    )

    return {"data": pdom.invariants()}


@identity_intelligence_router.get("/domain/ai-governance")
async def ii_domain_ai_governance(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_domain as pdom,
    )

    return {"data": pdom.ai_governance()}


@identity_intelligence_router.get("/domain/integrations")
async def ii_domain_integrations(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_domain as pdom,
    )

    return {"data": pdom.integrations()}


@identity_intelligence_router.get("/domain/production-readiness")
async def ii_domain_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_domain as pdom,
    )

    return {"data": pdom.production_readiness()}


@identity_intelligence_router.get("/domain/readiness")
async def ii_domain_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services.ii_domain_foundation import (
        validate_ii_domain_foundation,
    )

    return {"data": validate_ii_domain_foundation()}


@identity_intelligence_router.get("/autonomous")
async def ii_autonomous_summary(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    return {"data": get_identity_intelligence_service().platform_autonomous()}


@identity_intelligence_router.get("/autonomous/capabilities")
async def ii_autonomous_capabilities(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    return {"data": auto.capabilities()}


@identity_intelligence_router.get("/autonomous/lifecycle")
async def ii_autonomous_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    c = auto.capabilities()
    return {
        "data": {
            "lifecycle": c["lifecycle"],
            "principles": c["principles"],
            "hitl_required": c["hitl_required"],
        }
    }


@identity_intelligence_router.get("/autonomous/engine")
async def ii_autonomous_engine(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    return {"data": auto.engine()}


@identity_intelligence_router.get("/autonomous/decision")
async def ii_autonomous_decision(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    return {"data": auto.decision_engine()}


@identity_intelligence_router.get("/autonomous/workflows")
async def ii_autonomous_workflows(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    return {"data": auto.workflows()}


@identity_intelligence_router.get("/autonomous/healing")
async def ii_autonomous_healing(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    return {"data": auto.self_healing()}


@identity_intelligence_router.get("/autonomous/agents")
async def ii_autonomous_agents(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    return {"data": auto.agent_orchestration()}


@identity_intelligence_router.get("/autonomous/use-cases")
async def ii_autonomous_use_cases(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    return {"data": auto.use_cases()}


@identity_intelligence_router.get("/autonomous/twins")
async def ii_autonomous_twins(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    return {"data": auto.digital_twin()}


@identity_intelligence_router.get("/autonomous/graph")
async def ii_autonomous_graph(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    return {"data": auto.knowledge_graph()}


@identity_intelligence_router.get("/autonomous/security")
async def ii_autonomous_security(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    return {"data": auto.security()}


@identity_intelligence_router.get("/autonomous/ai-governance")
async def ii_autonomous_ai_governance(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    return {"data": auto.ai_governance()}


@identity_intelligence_router.get("/autonomous/observability")
async def ii_autonomous_observability(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    return {"data": auto.observability()}


@identity_intelligence_router.get("/autonomous/ddd")
async def ii_autonomous_ddd(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    return {"data": auto.ddd()}


@identity_intelligence_router.get("/autonomous/cqrs")
async def ii_autonomous_cqrs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    return {"data": auto.cqrs()}


@identity_intelligence_router.get("/autonomous/events")
async def ii_autonomous_events(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    c = auto.cqrs()
    return {"data": {"events": c["events"], "event_count": c["event_count"]}}


@identity_intelligence_router.get("/autonomous/microservices")
async def ii_autonomous_microservices(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    return {"data": auto.microservices()}


@identity_intelligence_router.get("/autonomous/integrations")
async def ii_autonomous_integrations(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    return {"data": auto.integrations()}


@identity_intelligence_router.get("/autonomous/outputs")
async def ii_autonomous_outputs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    return {"data": auto.cursor_outputs()}


@identity_intelligence_router.get("/autonomous/production-readiness")
async def ii_autonomous_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )

    return {"data": auto.production_readiness()}


@identity_intelligence_router.get("/autonomous/readiness")
async def ii_autonomous_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services.ii_autonomous_foundation import (
        validate_ii_autonomous_foundation,
    )

    return {"data": validate_ii_autonomous_foundation()}


# --- P207-E Identity AI Agent Platform ---


@identity_intelligence_router.get("/agents")
async def ii_agents(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    return {"data": get_identity_intelligence_service().platform_agents()}


@identity_intelligence_router.get("/agents/capabilities")
async def ii_agents_capabilities(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.capabilities()}


@identity_intelligence_router.get("/agents/catalog")
async def ii_agents_catalog(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.agent_catalog()}


@identity_intelligence_router.get("/agents/architecture")
async def ii_agents_architecture(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.platform_architecture()}


@identity_intelligence_router.get("/agents/orchestration")
async def ii_agents_orchestration(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.orchestration()}


@identity_intelligence_router.get("/agents/memory")
async def ii_agents_memory(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.memory()}


@identity_intelligence_router.get("/agents/rag")
async def ii_agents_rag(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.rag()}


@identity_intelligence_router.get("/agents/tools")
async def ii_agents_tools(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.tools()}


@identity_intelligence_router.get("/agents/decision")
async def ii_agents_decision(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.decision_model()}


@identity_intelligence_router.get("/agents/collaboration")
async def ii_agents_collaboration(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.human_ai_collaboration()}


@identity_intelligence_router.get("/agents/security")
async def ii_agents_security(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.security()}


@identity_intelligence_router.get("/agents/governance")
async def ii_agents_governance(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.model_governance()}


@identity_intelligence_router.get("/agents/observability")
async def ii_agents_observability(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.observability()}


@identity_intelligence_router.get("/agents/ddd")
async def ii_agents_ddd(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.ddd()}


@identity_intelligence_router.get("/agents/cqrs")
async def ii_agents_cqrs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.cqrs()}


@identity_intelligence_router.get("/agents/events")
async def ii_agents_events(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.cqrs()}


@identity_intelligence_router.get("/agents/microservices")
async def ii_agents_microservices(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.microservices()}


@identity_intelligence_router.get("/agents/integrations")
async def ii_agents_integrations(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.integrations()}


@identity_intelligence_router.get("/agents/outputs")
async def ii_agents_outputs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.cursor_outputs()}


@identity_intelligence_router.get("/agents/production-readiness")
async def ii_agents_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )

    return {"data": agents.production_readiness()}


@identity_intelligence_router.get("/agents/readiness")
async def ii_agents_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services.ii_agent_foundation import (
        validate_ii_agent_foundation,
    )

    return {"data": validate_ii_agent_foundation()}


# --- P207-F Identity Digital Twin Platform ---


@identity_intelligence_router.get("/twins")
async def ii_twins(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    return {"data": get_identity_intelligence_service().platform_twins()}


@identity_intelligence_router.get("/twins/capabilities")
async def ii_twins_capabilities(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.capabilities()}


@identity_intelligence_router.get("/twins/purpose")
async def ii_twins_purpose(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.domain_purpose()}


@identity_intelligence_router.get("/twins/architecture")
async def ii_twins_architecture(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.platform_architecture()}


@identity_intelligence_router.get("/twins/model")
async def ii_twins_model(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.twin_model()}


@identity_intelligence_router.get("/twins/lifecycle")
async def ii_twins_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.lifecycle()}


@identity_intelligence_router.get("/twins/synchronization")
async def ii_twins_synchronization(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.synchronization()}


@identity_intelligence_router.get("/twins/simulation")
async def ii_twins_simulation(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.simulation()}


@identity_intelligence_router.get("/twins/impact")
async def ii_twins_impact(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.impact_analysis()}


@identity_intelligence_router.get("/twins/predictive")
async def ii_twins_predictive(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.predictive()}


@identity_intelligence_router.get("/twins/graph")
async def ii_twins_graph(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.knowledge_graph()}


@identity_intelligence_router.get("/twins/agents")
async def ii_twins_agents(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.twin_agents()}


@identity_intelligence_router.get("/twins/security")
async def ii_twins_security(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.security()}


@identity_intelligence_router.get("/twins/observability")
async def ii_twins_observability(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.observability()}


@identity_intelligence_router.get("/twins/ddd")
async def ii_twins_ddd(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.ddd()}


@identity_intelligence_router.get("/twins/cqrs")
async def ii_twins_cqrs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.cqrs()}


@identity_intelligence_router.get("/twins/events")
async def ii_twins_events(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.cqrs()}


@identity_intelligence_router.get("/twins/microservices")
async def ii_twins_microservices(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.microservices()}


@identity_intelligence_router.get("/twins/integrations")
async def ii_twins_integrations(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.integrations()}


@identity_intelligence_router.get("/twins/outputs")
async def ii_twins_outputs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.cursor_outputs()}


@identity_intelligence_router.get("/twins/production-readiness")
async def ii_twins_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )

    return {"data": twins.production_readiness()}


@identity_intelligence_router.get("/twins/readiness")
async def ii_twins_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services.ii_twin_foundation import (
        validate_ii_twin_foundation,
    )

    return {"data": validate_ii_twin_foundation()}


# --- P207-G Predictive Identity Risk Intelligence Engine ---


@identity_intelligence_router.get("/risk")
async def ii_risk(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    return {"data": get_identity_intelligence_service().platform_risk()}


@identity_intelligence_router.get("/risk/capabilities")
async def ii_risk_capabilities(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.capabilities()}


@identity_intelligence_router.get("/risk/domain")
async def ii_risk_domain(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.domain()}


@identity_intelligence_router.get("/risk/architecture")
async def ii_risk_architecture(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.platform_architecture()}


@identity_intelligence_router.get("/risk/model")
async def ii_risk_model(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.risk_model()}


@identity_intelligence_router.get("/risk/signals")
async def ii_risk_signals(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.signals()}


@identity_intelligence_router.get("/risk/calculation")
async def ii_risk_calculation(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.calculation()}


@identity_intelligence_router.get("/risk/prediction")
async def ii_risk_prediction(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.prediction()}


@identity_intelligence_router.get("/risk/trust")
async def ii_risk_trust(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.trust_engine()}


@identity_intelligence_router.get("/risk/behavioral")
async def ii_risk_behavioral(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.behavioral()}


@identity_intelligence_router.get("/risk/graph")
async def ii_risk_graph(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.knowledge_graph()}


@identity_intelligence_router.get("/risk/twins")
async def ii_risk_twins(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.digital_twin()}


@identity_intelligence_router.get("/risk/agents")
async def ii_risk_agents(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.risk_agents()}


@identity_intelligence_router.get("/risk/response")
async def ii_risk_response(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.response_automation()}


@identity_intelligence_router.get("/risk/security")
async def ii_risk_security(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.security_governance()}


@identity_intelligence_router.get("/risk/observability")
async def ii_risk_observability(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.observability()}


@identity_intelligence_router.get("/risk/ddd")
async def ii_risk_ddd(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.ddd()}


@identity_intelligence_router.get("/risk/cqrs")
async def ii_risk_cqrs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.cqrs()}


@identity_intelligence_router.get("/risk/events")
async def ii_risk_events(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.cqrs()}


@identity_intelligence_router.get("/risk/microservices")
async def ii_risk_microservices(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.microservices()}


@identity_intelligence_router.get("/risk/integrations")
async def ii_risk_integrations(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.integrations()}


@identity_intelligence_router.get("/risk/outputs")
async def ii_risk_outputs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.cursor_outputs()}


@identity_intelligence_router.get("/risk/production-readiness")
async def ii_risk_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )

    return {"data": risk.production_readiness()}


@identity_intelligence_router.get("/risk/readiness")
async def ii_risk_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services.ii_risk_foundation import (
        validate_ii_risk_foundation,
    )

    return {"data": validate_ii_risk_foundation()}


# --- P207-H Behavioral Identity Analytics Platform ---


@identity_intelligence_router.get("/behavior")
async def ii_behavior(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    return {"data": get_identity_intelligence_service().platform_behavior()}


@identity_intelligence_router.get("/behavior/capabilities")
async def ii_behavior_capabilities(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.capabilities()}


@identity_intelligence_router.get("/behavior/domain")
async def ii_behavior_domain(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.domain_flow()}


@identity_intelligence_router.get("/behavior/architecture")
async def ii_behavior_architecture(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.platform_architecture()}


@identity_intelligence_router.get("/behavior/profile")
async def ii_behavior_profile(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.behavior_profile()}


@identity_intelligence_router.get("/behavior/collection")
async def ii_behavior_collection(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.collection()}


@identity_intelligence_router.get("/behavior/baseline")
async def ii_behavior_baseline(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.baseline()}


@identity_intelligence_router.get("/behavior/anomaly")
async def ii_behavior_anomaly(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.anomaly_detection()}


@identity_intelligence_router.get("/behavior/ueba")
async def ii_behavior_ueba(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.ueba()}


@identity_intelligence_router.get("/behavior/risk")
async def ii_behavior_risk(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.behavioral_risk()}


@identity_intelligence_router.get("/behavior/graph")
async def ii_behavior_graph(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.knowledge_graph()}


@identity_intelligence_router.get("/behavior/twins")
async def ii_behavior_twins(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.digital_twin()}


@identity_intelligence_router.get("/behavior/agents")
async def ii_behavior_agents(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.behavior_agents()}


@identity_intelligence_router.get("/behavior/trust")
async def ii_behavior_trust(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.continuous_trust()}


@identity_intelligence_router.get("/behavior/security")
async def ii_behavior_security(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.security_privacy()}


@identity_intelligence_router.get("/behavior/observability")
async def ii_behavior_observability(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.observability()}


@identity_intelligence_router.get("/behavior/ddd")
async def ii_behavior_ddd(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.ddd()}


@identity_intelligence_router.get("/behavior/cqrs")
async def ii_behavior_cqrs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.cqrs()}


@identity_intelligence_router.get("/behavior/events")
async def ii_behavior_events(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.cqrs()}


@identity_intelligence_router.get("/behavior/microservices")
async def ii_behavior_microservices(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.microservices()}


@identity_intelligence_router.get("/behavior/integrations")
async def ii_behavior_integrations(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.integrations()}


@identity_intelligence_router.get("/behavior/outputs")
async def ii_behavior_outputs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.cursor_outputs()}


@identity_intelligence_router.get("/behavior/production-readiness")
async def ii_behavior_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )

    return {"data": behavior.production_readiness()}


@identity_intelligence_router.get("/behavior/readiness")
async def ii_behavior_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services.ii_behavior_foundation import (
        validate_ii_behavior_foundation,
    )

    return {"data": validate_ii_behavior_foundation()}


# --- P207-I Self-Healing Identity Fabric Platform ---


@identity_intelligence_router.get("/healing")
async def ii_healing(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    return {"data": get_identity_intelligence_service().platform_healing()}


@identity_intelligence_router.get("/healing/capabilities")
async def ii_healing_capabilities(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.capabilities()}


@identity_intelligence_router.get("/healing/domain")
async def ii_healing_domain(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.domain_flow()}


@identity_intelligence_router.get("/healing/architecture")
async def ii_healing_architecture(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.platform_architecture()}


@identity_intelligence_router.get("/healing/health")
async def ii_healing_health(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.health_model()}


@identity_intelligence_router.get("/healing/detection")
async def ii_healing_detection(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.failure_detection()}


@identity_intelligence_router.get("/healing/rca")
async def ii_healing_rca(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.root_cause_analysis()}


@identity_intelligence_router.get("/healing/remediation")
async def ii_healing_remediation(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.remediation()}


@identity_intelligence_router.get("/healing/use-cases")
async def ii_healing_use_cases(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.use_cases()}


@identity_intelligence_router.get("/healing/twins")
async def ii_healing_twins(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.digital_twin()}


@identity_intelligence_router.get("/healing/graph")
async def ii_healing_graph(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.knowledge_graph()}


@identity_intelligence_router.get("/healing/agents")
async def ii_healing_agents(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.healing_agents()}


@identity_intelligence_router.get("/healing/learning")
async def ii_healing_learning(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.continuous_learning()}


@identity_intelligence_router.get("/healing/security")
async def ii_healing_security(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.security()}


@identity_intelligence_router.get("/healing/observability")
async def ii_healing_observability(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.observability()}


@identity_intelligence_router.get("/healing/ddd")
async def ii_healing_ddd(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.ddd()}


@identity_intelligence_router.get("/healing/cqrs")
async def ii_healing_cqrs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.cqrs()}


@identity_intelligence_router.get("/healing/events")
async def ii_healing_events(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.cqrs()}


@identity_intelligence_router.get("/healing/microservices")
async def ii_healing_microservices(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.microservices()}


@identity_intelligence_router.get("/healing/integrations")
async def ii_healing_integrations(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.integrations()}


@identity_intelligence_router.get("/healing/outputs")
async def ii_healing_outputs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.cursor_outputs()}


@identity_intelligence_router.get("/healing/production-readiness")
async def ii_healing_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )

    return {"data": healing.production_readiness()}


@identity_intelligence_router.get("/healing/readiness")
async def ii_healing_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services.ii_healing_foundation import (
        validate_ii_healing_foundation,
    )

    return {"data": validate_ii_healing_foundation()}


# --- P207-J AI Driven Governance & Access Optimization ---


@identity_intelligence_router.get("/access-gov")
async def ii_access_gov(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    return {"data": get_identity_intelligence_service().platform_access_gov()}


@identity_intelligence_router.get("/access-gov/capabilities")
async def ii_access_gov_capabilities(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.capabilities()}


@identity_intelligence_router.get("/access-gov/domain")
async def ii_access_gov_domain(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.domain_flow()}


@identity_intelligence_router.get("/access-gov/architecture")
async def ii_access_gov_architecture(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.platform_architecture()}


@identity_intelligence_router.get("/access-gov/model")
async def ii_access_gov_model(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.governance_model()}


@identity_intelligence_router.get("/access-gov/entitlement")
async def ii_access_gov_entitlement(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.entitlement_intelligence()}


@identity_intelligence_router.get("/access-gov/optimization")
async def ii_access_gov_optimization(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.optimization()}


@identity_intelligence_router.get("/access-gov/certification")
async def ii_access_gov_certification(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.certification()}


@identity_intelligence_router.get("/access-gov/roles")
async def ii_access_gov_roles(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.role_intelligence()}


@identity_intelligence_router.get("/access-gov/policy")
async def ii_access_gov_policy(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.policy_intelligence()}


@identity_intelligence_router.get("/access-gov/risk")
async def ii_access_gov_risk(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.risk_integration()}


@identity_intelligence_router.get("/access-gov/twins")
async def ii_access_gov_twins(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.digital_twin()}


@identity_intelligence_router.get("/access-gov/agents")
async def ii_access_gov_agents(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.governance_agents()}


@identity_intelligence_router.get("/access-gov/workflows")
async def ii_access_gov_workflows(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.workflows()}


@identity_intelligence_router.get("/access-gov/graph")
async def ii_access_gov_graph(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.knowledge_graph()}


@identity_intelligence_router.get("/access-gov/security")
async def ii_access_gov_security(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.security_compliance()}


@identity_intelligence_router.get("/access-gov/observability")
async def ii_access_gov_observability(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.observability()}


@identity_intelligence_router.get("/access-gov/ddd")
async def ii_access_gov_ddd(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.ddd()}


@identity_intelligence_router.get("/access-gov/cqrs")
async def ii_access_gov_cqrs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.cqrs()}


@identity_intelligence_router.get("/access-gov/events")
async def ii_access_gov_events(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.cqrs()}


@identity_intelligence_router.get("/access-gov/microservices")
async def ii_access_gov_microservices(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.microservices()}


@identity_intelligence_router.get("/access-gov/integrations")
async def ii_access_gov_integrations(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.integrations()}


@identity_intelligence_router.get("/access-gov/outputs")
async def ii_access_gov_outputs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.cursor_outputs()}


@identity_intelligence_router.get("/access-gov/production-readiness")
async def ii_access_gov_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )

    return {"data": access_gov.production_readiness()}


@identity_intelligence_router.get("/access-gov/readiness")
async def ii_access_gov_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services.ii_access_gov_foundation import (
        validate_ii_access_gov_foundation,
    )

    return {"data": validate_ii_access_gov_foundation()}


@identity_intelligence_router.get("/graph")
async def ii_graph_catalog(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    return {"data": get_identity_intelligence_service().platform_graph()}


@identity_intelligence_router.get("/graph/capabilities")
async def ii_graph_capabilities(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.capabilities()}


@identity_intelligence_router.get("/graph/purpose")
async def ii_graph_purpose(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.domain_purpose()}


@identity_intelligence_router.get("/graph/architecture")
async def ii_graph_architecture(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.platform_architecture()}


@identity_intelligence_router.get("/graph/ontology")
async def ii_graph_ontology(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.ontology()}


@identity_intelligence_router.get("/graph/entities")
async def ii_graph_entities(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.entity_model()}


@identity_intelligence_router.get("/graph/relationships")
async def ii_graph_relationships(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.relationship_model()}


@identity_intelligence_router.get("/graph/reasoning")
async def ii_graph_reasoning(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.reasoning()}


@identity_intelligence_router.get("/graph/intelligence")
async def ii_graph_intelligence(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.relationship_intelligence()}


@identity_intelligence_router.get("/graph/attack-path")
async def ii_graph_attack_path(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.attack_path()}


@identity_intelligence_router.get("/graph/twins")
async def ii_graph_twins(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.digital_twin()}


@identity_intelligence_router.get("/graph/agents")
async def ii_graph_agents(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.graph_agents()}


@identity_intelligence_router.get("/graph/risk")
async def ii_graph_risk(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.risk_integration()}


@identity_intelligence_router.get("/graph/search")
async def ii_graph_search(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.semantic_search()}


@identity_intelligence_router.get("/graph/security")
async def ii_graph_security(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.security()}


@identity_intelligence_router.get("/graph/observability")
async def ii_graph_observability(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.observability()}


@identity_intelligence_router.get("/graph/ddd")
async def ii_graph_ddd(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.ddd()}


@identity_intelligence_router.get("/graph/cqrs")
async def ii_graph_cqrs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.cqrs()}


@identity_intelligence_router.get("/graph/events")
async def ii_graph_events(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.cqrs().get("events")}


@identity_intelligence_router.get("/graph/microservices")
async def ii_graph_microservices(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.microservices()}


@identity_intelligence_router.get("/graph/integrations")
async def ii_graph_integrations(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.integrations()}


@identity_intelligence_router.get("/graph/outputs")
async def ii_graph_outputs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.cursor_outputs()}


@identity_intelligence_router.get("/graph/production-readiness")
async def ii_graph_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_graph as graph,
    )

    return {"data": graph.production_readiness()}


@identity_intelligence_router.get("/graph/readiness")
async def ii_graph_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services.ii_graph_foundation import (
        validate_ii_graph_foundation,
    )

    return {"data": validate_ii_graph_foundation()}


@identity_intelligence_router.get("/fabric")
async def ii_fabric_catalog(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    return {"data": get_identity_intelligence_service().platform_fabric()}


@identity_intelligence_router.get("/fabric/capabilities")
async def ii_fabric_capabilities(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.capabilities()}


@identity_intelligence_router.get("/fabric/microservices")
async def ii_fabric_microservices(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.microservice_architecture()}


@identity_intelligence_router.get("/fabric/service-boundaries")
async def ii_fabric_service_boundaries(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.service_boundaries()}


@identity_intelligence_router.get("/fabric/cqrs")
async def ii_fabric_cqrs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.cqrs_design()}


@identity_intelligence_router.get("/fabric/commands")
async def ii_fabric_commands(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.command_catalog()}


@identity_intelligence_router.get("/fabric/queries")
async def ii_fabric_queries(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.query_catalog()}


@identity_intelligence_router.get("/fabric/events")
async def ii_fabric_events(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.event_catalog()}


@identity_intelligence_router.get("/fabric/event-streaming")
async def ii_fabric_event_streaming(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.event_streaming()}


@identity_intelligence_router.get("/fabric/event-sourcing")
async def ii_fabric_event_sourcing(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.event_sourcing()}


@identity_intelligence_router.get("/fabric/apis")
async def ii_fabric_apis(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.api_architecture()}


@identity_intelligence_router.get("/fabric/api-security")
async def ii_fabric_api_security(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.api_security()}


@identity_intelligence_router.get("/fabric/communication")
async def ii_fabric_communication(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.service_communication()}


@identity_intelligence_router.get("/fabric/data-ownership")
async def ii_fabric_data_ownership(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.data_ownership()}


@identity_intelligence_router.get("/fabric/ai-integration")
async def ii_fabric_ai_integration(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.ai_native_integration()}


@identity_intelligence_router.get("/fabric/security")
async def ii_fabric_security(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.microservice_security()}


@identity_intelligence_router.get("/fabric/kubernetes")
async def ii_fabric_kubernetes(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.kubernetes_architecture()}


@identity_intelligence_router.get("/fabric/observability")
async def ii_fabric_observability(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.observability()}


@identity_intelligence_router.get("/fabric/testing")
async def ii_fabric_testing(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.testing_strategy()}


@identity_intelligence_router.get("/fabric/disaster-recovery")
async def ii_fabric_disaster_recovery(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.disaster_recovery()}


@identity_intelligence_router.get("/fabric/ddd")
async def ii_fabric_ddd(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.ddd()}


@identity_intelligence_router.get("/fabric/integrations")
async def ii_fabric_integrations(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.integrations()}


@identity_intelligence_router.get("/fabric/outputs")
async def ii_fabric_outputs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.cursor_outputs()}


@identity_intelligence_router.get("/fabric/production-readiness")
async def ii_fabric_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_fabric as fabric,
    )

    return {"data": fabric.production_readiness_assessment()}


@identity_intelligence_router.get("/fabric/readiness")
async def ii_fabric_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services.ii_fabric_foundation import (
        validate_ii_fabric_foundation,
    )

    return {"data": validate_ii_fabric_foundation()}


@identity_intelligence_router.get("/ai-gov")
async def ii_ai_gov_catalog(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    return {"data": get_identity_intelligence_service().platform_ai_gov()}


@identity_intelligence_router.get("/ai-gov/capabilities")
async def ii_ai_gov_capabilities(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.capabilities()}


@identity_intelligence_router.get("/ai-gov/lifecycle")
async def ii_ai_gov_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.governance_lifecycle()}


@identity_intelligence_router.get("/ai-gov/security")
async def ii_ai_gov_security(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.ai_security_architecture()}


@identity_intelligence_router.get("/ai-gov/inventory")
async def ii_ai_gov_inventory(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.asset_inventory()}


@identity_intelligence_router.get("/ai-gov/identity-access")
async def ii_ai_gov_identity_access(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.ai_identity_access()}


@identity_intelligence_router.get("/ai-gov/responsible-ai")
async def ii_ai_gov_responsible_ai(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.responsible_ai()}


@identity_intelligence_router.get("/ai-gov/explainability")
async def ii_ai_gov_explainability(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.explainability()}


@identity_intelligence_router.get("/ai-gov/risk")
async def ii_ai_gov_risk(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.ai_risk_management()}


@identity_intelligence_router.get("/ai-gov/threats")
async def ii_ai_gov_threats(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.threat_protection()}


@identity_intelligence_router.get("/ai-gov/agents")
async def ii_ai_gov_agents(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.agent_governance()}


@identity_intelligence_router.get("/ai-gov/autonomous")
async def ii_ai_gov_autonomous(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.autonomous_action_governance()}


@identity_intelligence_router.get("/ai-gov/models")
async def ii_ai_gov_models(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.model_governance()}


@identity_intelligence_router.get("/ai-gov/data-governance")
async def ii_ai_gov_data_governance(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.data_governance()}


@identity_intelligence_router.get("/ai-gov/graph")
async def ii_ai_gov_graph(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.graph_ai_governance()}


@identity_intelligence_router.get("/ai-gov/audit")
async def ii_ai_gov_audit(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.audit_compliance()}


@identity_intelligence_router.get("/ai-gov/observability")
async def ii_ai_gov_observability(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.observability()}


@identity_intelligence_router.get("/ai-gov/ddd")
async def ii_ai_gov_ddd(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.ddd()}


@identity_intelligence_router.get("/ai-gov/cqrs")
async def ii_ai_gov_cqrs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.cqrs()}


@identity_intelligence_router.get("/ai-gov/events")
async def ii_ai_gov_events(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.cqrs().get("events")}


@identity_intelligence_router.get("/ai-gov/microservices")
async def ii_ai_gov_microservices(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.microservices()}


@identity_intelligence_router.get("/ai-gov/integrations")
async def ii_ai_gov_integrations(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.integrations()}


@identity_intelligence_router.get("/ai-gov/outputs")
async def ii_ai_gov_outputs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.cursor_outputs()}


@identity_intelligence_router.get("/ai-gov/production-readiness")
async def ii_ai_gov_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ai_gov as ai_gov,
    )

    return {"data": ai_gov.production_readiness()}


@identity_intelligence_router.get("/ai-gov/readiness")
async def ii_ai_gov_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services.ii_ai_gov_foundation import (
        validate_ii_ai_gov_foundation,
    )

    return {"data": validate_ii_ai_gov_foundation()}


@identity_intelligence_router.get("/ops")
async def ii_ops_catalog(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    return {"data": get_identity_intelligence_service().platform_ops()}


@identity_intelligence_router.get("/ops/capabilities")
async def ii_ops_capabilities(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.capabilities()}


@identity_intelligence_router.get("/ops/cloud-native")
async def ii_ops_cloud_native(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.cloud_native_architecture()}


@identity_intelligence_router.get("/ops/kubernetes")
async def ii_ops_kubernetes(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.kubernetes_platform()}


@identity_intelligence_router.get("/ops/containers")
async def ii_ops_containers(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.container_strategy()}


@identity_intelligence_router.get("/ops/devsecops")
async def ii_ops_devsecops(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.devsecops_pipeline()}


@identity_intelligence_router.get("/ops/iac")
async def ii_ops_iac(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.infrastructure_as_code()}


@identity_intelligence_router.get("/ops/gitops")
async def ii_ops_gitops(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.gitops()}


@identity_intelligence_router.get("/ops/service-mesh")
async def ii_ops_service_mesh(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.service_mesh()}


@identity_intelligence_router.get("/ops/scalability")
async def ii_ops_scalability(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.scalability()}


@identity_intelligence_router.get("/ops/high-availability")
async def ii_ops_high_availability(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.high_availability()}


@identity_intelligence_router.get("/ops/disaster-recovery")
async def ii_ops_disaster_recovery(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.disaster_recovery()}


@identity_intelligence_router.get("/ops/observability")
async def ii_ops_observability(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.observability()}


@identity_intelligence_router.get("/ops/identity-monitoring")
async def ii_ops_identity_monitoring(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.identity_monitoring()}


@identity_intelligence_router.get("/ops/ai-ops")
async def ii_ops_ai_ops(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.ai_ops_observability()}


@identity_intelligence_router.get("/ops/security-ops")
async def ii_ops_security_ops(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.security_operations()}


@identity_intelligence_router.get("/ops/platform-security")
async def ii_ops_platform_security(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.platform_security()}


@identity_intelligence_router.get("/ops/cost")
async def ii_ops_cost(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.cost_optimization()}


@identity_intelligence_router.get("/ops/ddd")
async def ii_ops_ddd(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.ddd()}


@identity_intelligence_router.get("/ops/cqrs")
async def ii_ops_cqrs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.cqrs()}


@identity_intelligence_router.get("/ops/events")
async def ii_ops_events(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.cqrs().get("events")}


@identity_intelligence_router.get("/ops/integrations")
async def ii_ops_integrations(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.integrations()}


@identity_intelligence_router.get("/ops/outputs")
async def ii_ops_outputs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.cursor_outputs()}


@identity_intelligence_router.get("/ops/production-readiness")
async def ii_ops_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_ops as ops,
    )

    return {"data": ops.production_readiness()}


@identity_intelligence_router.get("/ops/readiness")
async def ii_ops_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services.ii_ops_foundation import (
        validate_ii_ops_foundation,
    )

    return {"data": validate_ii_ops_foundation()}


@identity_intelligence_router.get("/qa")
async def ii_qa_catalog(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    return {"data": get_identity_intelligence_service().platform_qa()}


@identity_intelligence_router.get("/qa/capabilities")
async def ii_qa_capabilities(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.capabilities()}


@identity_intelligence_router.get("/qa/governance")
async def ii_qa_governance(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.quality_governance()}


@identity_intelligence_router.get("/qa/test-strategy")
async def ii_qa_test_strategy(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.test_strategy()}


@identity_intelligence_router.get("/qa/identity-testing")
async def ii_qa_identity_testing(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.identity_intelligence_testing()}


@identity_intelligence_router.get("/qa/ai-testing")
async def ii_qa_ai_testing(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.ai_testing()}


@identity_intelligence_router.get("/qa/twin-validation")
async def ii_qa_twin_validation(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.digital_twin_validation()}


@identity_intelligence_router.get("/qa/graph-testing")
async def ii_qa_graph_testing(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.knowledge_graph_testing()}


@identity_intelligence_router.get("/qa/security")
async def ii_qa_security(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.security_validation()}


@identity_intelligence_router.get("/qa/chaos")
async def ii_qa_chaos(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.chaos_engineering()}


@identity_intelligence_router.get("/qa/performance")
async def ii_qa_performance(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.performance_scale()}


@identity_intelligence_router.get("/qa/compliance")
async def ii_qa_compliance(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.compliance_governance()}


@identity_intelligence_router.get("/qa/policy")
async def ii_qa_policy(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.policy_validation()}


@identity_intelligence_router.get("/qa/release")
async def ii_qa_release(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.release_governance()}


@identity_intelligence_router.get("/qa/continuous-assurance")
async def ii_qa_continuous_assurance(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.continuous_assurance()}


@identity_intelligence_router.get("/qa/definition-of-done")
async def ii_qa_definition_of_done(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.definition_of_done()}


@identity_intelligence_router.get("/qa/ddd")
async def ii_qa_ddd(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.ddd()}


@identity_intelligence_router.get("/qa/cqrs")
async def ii_qa_cqrs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.cqrs()}


@identity_intelligence_router.get("/qa/events")
async def ii_qa_events(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.cqrs().get("events")}


@identity_intelligence_router.get("/qa/microservices")
async def ii_qa_microservices(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.microservice_testing()}


@identity_intelligence_router.get("/qa/integrations")
async def ii_qa_integrations(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.integrations()}


@identity_intelligence_router.get("/qa/outputs")
async def ii_qa_outputs(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.cursor_outputs()}


@identity_intelligence_router.get("/qa/production-readiness")
async def ii_qa_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services import (
        ii_platform_qa as qa,
    )

    return {"data": qa.production_readiness()}


@identity_intelligence_router.get("/qa/readiness")
async def ii_qa_readiness(
    _user: Annotated[dict, Depends(require_permissions("identity_intelligence.read"))],
) -> dict:
    from contexts.identity_intelligence.domain.services.ii_qa_foundation import (
        validate_ii_qa_foundation,
    )

    return {"data": validate_ii_qa_foundation()}
