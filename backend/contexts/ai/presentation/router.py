"""AI FastAPI router — Core Platform assist + P214-A foundation catalog."""
from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from contexts.ai.container import get_ai_service
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

router = APIRouter(prefix="/ai", tags=["AI Platform"])


class AssistRequest(BaseModel):
    module_id: str = Field(default="platform", max_length=64)
    surface: str = Field(default="assistant", max_length=64)
    prompt: str = Field(min_length=1, max_length=8000)
    context: dict[str, Any] | None = None


@router.post("/assist", status_code=status.HTTP_200_OK)
async def assist(
    body: AssistRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("ai.assist.infer"))],
):
    result = await get_ai_service().assist(
        tenant_id=tenant_id,
        correlation_id=correlation_id,
        module_id=body.module_id,
        surface=body.surface,
        prompt=body.prompt,
        actor_user_id=user.get("sub"),
        context=body.context,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


# --- P214-A Enterprise AI Intelligence Fabric ---

@router.get("/foundation")
async def ai_foundation(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().platform_foundation()}


@router.get("/foundation/vision")
async def ai_foundation_vision(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_vision()}


@router.get("/foundation/domain")
async def ai_foundation_domain(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_domain()}


@router.get("/foundation/bounded-contexts")
async def ai_foundation_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_bounded_contexts()}


@router.get("/foundation/ai-paas")
async def ai_foundation_ai_paas(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_ai_paas()}


@router.get("/foundation/ml")
async def ai_foundation_ml(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_ml()}


@router.get("/foundation/generative")
async def ai_foundation_generative(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_generative()}


@router.get("/foundation/llm")
async def ai_foundation_llm(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_llm()}


@router.get("/foundation/data")
async def ai_foundation_data(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_data()}


@router.get("/foundation/vectors")
async def ai_foundation_vectors(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_vectors()}


@router.get("/foundation/agents")
async def ai_foundation_agents(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_agents()}


@router.get("/foundation/knowledge")
async def ai_foundation_knowledge(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_knowledge()}


@router.get("/foundation/digital-twin")
async def ai_foundation_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_digital_twin()}


@router.get("/foundation/cqrs")
async def ai_foundation_cqrs(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_cqrs()}


@router.get("/foundation/events")
async def ai_foundation_events(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_events()}


@router.get("/foundation/microservices")
async def ai_foundation_microservices(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_microservices()}


@router.get("/foundation/api")
async def ai_foundation_api(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_api()}


@router.get("/foundation/security")
async def ai_foundation_security(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_security()}


@router.get("/foundation/deployment")
async def ai_foundation_deployment(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_deployment()}


@router.get("/foundation/testing")
async def ai_foundation_testing(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_testing()}


@router.get("/foundation/outputs")
async def ai_foundation_outputs(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_outputs()}


@router.get("/foundation/production-readiness")
async def ai_foundation_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_production_readiness()}


@router.get("/foundation/readiness")
async def ai_foundation_readiness(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().foundation_readiness()}


# --- P214-B Enterprise AI Strategic Intelligence Framework ---

@router.get("/mission")
async def ai_mission(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().platform_mission()}


@router.get("/mission/statement")
async def ai_mission_statement(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_statement()}


@router.get("/mission/vision")
async def ai_mission_vision(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_vision()}


@router.get("/mission/objectives")
async def ai_mission_objectives(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_objectives()}


@router.get("/mission/capability-map")
async def ai_mission_capability_map(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_capability_map()}


@router.get("/mission/operating-model")
async def ai_mission_operating_model(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_operating_model()}


@router.get("/mission/coe")
async def ai_mission_coe(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_coe()}


@router.get("/mission/maturity")
async def ai_mission_maturity(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_maturity()}


@router.get("/mission/value")
async def ai_mission_value(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_value()}


@router.get("/mission/use-cases")
async def ai_mission_use_cases(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_use_cases()}


@router.get("/mission/governance")
async def ai_mission_governance(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_governance()}


@router.get("/mission/meos-alignment")
async def ai_mission_meos_alignment(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_meos_alignment()}


@router.get("/mission/knowledge")
async def ai_mission_knowledge(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_knowledge()}


@router.get("/mission/roadmap")
async def ai_mission_roadmap(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_roadmap()}


@router.get("/mission/responsible-ai")
async def ai_mission_responsible_ai(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_responsible_ai()}


@router.get("/mission/investment")
async def ai_mission_investment(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_investment()}


@router.get("/mission/security")
async def ai_mission_security(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_security()}


@router.get("/mission/metrics")
async def ai_mission_metrics(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_metrics()}


@router.get("/mission/outputs")
async def ai_mission_outputs(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_outputs()}


@router.get("/mission/production-readiness")
async def ai_mission_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_production_readiness()}


@router.get("/mission/readiness")
async def ai_mission_readiness(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mission_readiness()}


# --- P214-C Enterprise AI Domain Fabric ---

@router.get("/domain")
async def ai_domain(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().platform_domain()}


@router.get("/domain/map")
async def ai_domain_map(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_map()}


@router.get("/domain/core")
async def ai_domain_core(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_core()}


@router.get("/domain/strategic")
async def ai_domain_strategic(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_strategic()}


@router.get("/domain/bounded-contexts")
async def ai_domain_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_bounded_contexts()}


@router.get("/domain/tactical")
async def ai_domain_tactical(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_tactical()}


@router.get("/domain/models")
async def ai_domain_models(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_models()}


@router.get("/domain/generative")
async def ai_domain_generative(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_generative()}


@router.get("/domain/agents")
async def ai_domain_agents(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_agents()}


@router.get("/domain/knowledge")
async def ai_domain_knowledge(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_knowledge()}


@router.get("/domain/data")
async def ai_domain_data(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_data()}


@router.get("/domain/security")
async def ai_domain_security(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_security()}


@router.get("/domain/events")
async def ai_domain_events(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_events()}


@router.get("/domain/microservices")
async def ai_domain_microservices(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_microservices()}


@router.get("/domain/integration")
async def ai_domain_integration(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_integration()}


@router.get("/domain/governance")
async def ai_domain_governance(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_governance()}


@router.get("/domain/cqrs")
async def ai_domain_cqrs(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_cqrs()}


@router.get("/domain/outputs")
async def ai_domain_outputs(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_outputs()}


@router.get("/domain/production-readiness")
async def ai_domain_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_production_readiness()}


@router.get("/domain/readiness")
async def ai_domain_readiness(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().domain_readiness()}


# --- P214-D Enterprise Machine Learning Intelligence Fabric ---

@router.get("/mlops")
async def ai_mlops(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().platform_mlops()}


@router.get("/mlops/vision")
async def ai_mlops_vision(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_vision()}


@router.get("/mlops/domain")
async def ai_mlops_domain(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_domain()}


@router.get("/mlops/bounded-contexts")
async def ai_mlops_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_bounded_contexts()}


@router.get("/mlops/lifecycle")
async def ai_mlops_lifecycle(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_lifecycle()}


@router.get("/mlops/experiments")
async def ai_mlops_experiments(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_experiments()}


@router.get("/mlops/features")
async def ai_mlops_features(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_features()}


@router.get("/mlops/training")
async def ai_mlops_training(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_training()}


@router.get("/mlops/registry")
async def ai_mlops_registry(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_registry()}


@router.get("/mlops/validation")
async def ai_mlops_validation(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_validation()}


@router.get("/mlops/deployment")
async def ai_mlops_deployment(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_deployment()}


@router.get("/mlops/monitoring")
async def ai_mlops_monitoring(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_monitoring()}


@router.get("/mlops/continuous-training")
async def ai_mlops_continuous_training(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_continuous_training()}


@router.get("/mlops/pipelines")
async def ai_mlops_pipelines(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_pipelines()}


@router.get("/mlops/cqrs")
async def ai_mlops_cqrs(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_cqrs()}


@router.get("/mlops/events")
async def ai_mlops_events(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_events()}


@router.get("/mlops/microservices")
async def ai_mlops_microservices(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_microservices()}


@router.get("/mlops/security")
async def ai_mlops_security(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_security()}


@router.get("/mlops/infrastructure")
async def ai_mlops_infrastructure(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_infrastructure()}


@router.get("/mlops/testing")
async def ai_mlops_testing(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_testing()}


@router.get("/mlops/outputs")
async def ai_mlops_outputs(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_outputs()}


@router.get("/mlops/production-readiness")
async def ai_mlops_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_production_readiness()}


@router.get("/mlops/readiness")
async def ai_mlops_readiness(
    _user: Annotated[dict, Depends(require_permissions("ai.assist.read"))],
) -> dict:
    return {"data": get_ai_service().mlops_readiness()}
