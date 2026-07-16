"""AI Identity Intelligence & Copilot API (P198-C2)."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.identity_federation.container import (
    get_fabric_intelligence_service,
    get_identity_federation_ai_service,
)
from contexts.identity_federation.domain.services import federation_privacy_engine
from contexts.identity_federation.presentation.intelligence_schemas import (
    AiFeedbackRequest,
    AiInferRequest,
    AiPredictRequest,
    ConsentRequest,
    CopilotRequest,
    ExplainDecisionRequest,
    ExplainTrustRequest,
)

intelligence_router = APIRouter(
    prefix="/federation/intelligence",
    tags=["Identity Federation Intelligence"],
)


def _fail(result):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.error or "request_failed")


@intelligence_router.get("/models")
async def list_models(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.ai.read"))],
):
    return {"data": (await get_fabric_intelligence_service().list_models()).unwrap()}


@intelligence_router.post("/predict")
async def predict(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: AiPredictRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.ai.infer"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_fabric_intelligence_service().predict(
        tenant_id,
        model_id=body.model_id,
        features=body.features,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        _fail(result)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@intelligence_router.post("/feedback")
async def feedback(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: AiFeedbackRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.ai.infer"))],
):
    return {"data": (await get_fabric_intelligence_service().submit_feedback(
        tenant_id, prediction_id=body.prediction_id, useful=body.useful, label=body.label
    )).unwrap()}


@intelligence_router.get("/analytics")
async def analytics(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.ai.read"))],
):
    return {"data": (await get_fabric_intelligence_service().analytics(tenant_id)).unwrap()}


@intelligence_router.get("/reports/executive")
async def executive_report(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.ai.read"))],
):
    return {"data": (await get_fabric_intelligence_service().executive_report(tenant_id)).unwrap()}


@intelligence_router.get("/reports/operational")
async def operational_report(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.ai.read"))],
):
    return {"data": (await get_fabric_intelligence_service().operational_report(tenant_id)).unwrap()}


@intelligence_router.post("/copilot")
async def copilot(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: CopilotRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.ai.infer"))],
):
    result = await get_fabric_intelligence_service().copilot(
        tenant_id, question=body.question, context=body.context
    )
    if not result.succeeded:
        _fail(result)
    return {"data": result.unwrap()}


@intelligence_router.post("/explain/decision")
async def explain_decision(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: ExplainDecisionRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.ai.read"))],
):
    return {"data": (await get_fabric_intelligence_service().explain_decision(
        tenant_id, decision=body.decision
    )).unwrap()}


@intelligence_router.post("/explain/trust")
async def explain_trust(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: ExplainTrustRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.ai.read"))],
):
    return {"data": (await get_fabric_intelligence_service().explain_trust(
        tenant_id, trust=body.trust
    )).unwrap()}


@intelligence_router.get("/policies/suggestions")
async def policy_suggestions(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.ai.read"))],
):
    return {"data": (await get_fabric_intelligence_service().suggest_policies(tenant_id)).unwrap()}


@intelligence_router.get("/config/problems")
async def config_problems(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.ai.read"))],
):
    return {"data": (await get_fabric_intelligence_service().detect_config_problems(tenant_id)).unwrap()}


@intelligence_router.get("/recommendations")
async def recommendations(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.ai.read"))],
):
    return {"data": (await get_fabric_intelligence_service().security_recommendations(tenant_id)).unwrap()}


@intelligence_router.get("/audit/summary")
async def audit_summary(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.ai.read"))],
):
    return {"data": (await get_fabric_intelligence_service().summarize_audit(tenant_id)).unwrap()}


@intelligence_router.get("/dashboard")
async def intelligence_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.ai.read"))],
):
    return {"data": (await get_fabric_intelligence_service().intelligence_dashboard(tenant_id)).unwrap()}


@intelligence_router.get("/metrics")
async def ai_metrics(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.ai.read"))],
):
    return {"data": (await get_fabric_intelligence_service().ai_metrics()).unwrap()}


@intelligence_router.get("/ai/surfaces")
async def ai_surfaces(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.ai.read"))],
):
    return {"data": (await get_identity_federation_ai_service().list_surfaces()).unwrap()}


@intelligence_router.post("/ai/infer")
async def ai_infer(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: AiInferRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.ai.infer"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_identity_federation_ai_service().infer(
        tenant_id, surface=body.surface, payload=body.payload, correlation_id=correlation_id
    )
    if not result.succeeded:
        _fail(result)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@intelligence_router.get("/compliance/controls")
async def compliance_controls(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.ai.read"))],
):
    return {
        "data": {
            "privacy": federation_privacy_engine.privacy_controls(),
            "retention": federation_privacy_engine.retention_policies(),
            "pia": federation_privacy_engine.privacy_impact_assessment(),
        }
    }


@intelligence_router.post("/compliance/consent")
async def record_consent(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: ConsentRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.write"))],
):
    return {
        "data": federation_privacy_engine.consent_record(
            subject_id=body.subject_id, purpose=body.purpose, granted=body.granted
        )
    }


@intelligence_router.get("/compliance/export-manifest")
async def export_manifest(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.ai.admin"))],
):
    return {"data": federation_privacy_engine.audit_export_manifest(tenant_id=tenant_id)}
