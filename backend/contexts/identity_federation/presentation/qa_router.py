"""Federation Quality / Governance / DoD REST surface (P200-B12)."""
from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from contexts.identity.presentation.dependencies import get_tenant_id, require_permissions
from contexts.identity_federation.application.commands.qa_commands import (
    CertifyReleaseCommand,
    EvaluateQualityGateCommand,
    RecordQualityAssessmentCommand,
    handle_certify_release,
    handle_evaluate_quality_gate,
    handle_record_quality_assessment,
)
from contexts.identity_federation.application.queries.qa_queries import (
    handle_get_compliance_validation,
    handle_get_dod_checklist,
    handle_get_governance,
    handle_get_production_readiness,
    handle_get_qa_metrics,
    handle_get_qa_surface,
    handle_get_quality_gates,
    handle_get_testing_catalog,
    handle_get_traceability,
)

qa_router = APIRouter(prefix="/federation/qa", tags=["federation-qa"])


@qa_router.get(
    "/surface",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def surface() -> dict:
    return {"data": handle_get_qa_surface()}


@qa_router.get(
    "/gates",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def gates() -> dict:
    return {"data": handle_get_quality_gates()}


@qa_router.get(
    "/dod",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def dod() -> dict:
    return {"data": handle_get_dod_checklist()}


@qa_router.get(
    "/traceability",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def traceability() -> dict:
    return {"data": handle_get_traceability()}


@qa_router.get(
    "/testing",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def testing() -> dict:
    return {"data": handle_get_testing_catalog()}


@qa_router.get(
    "/governance",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def governance() -> dict:
    return {"data": handle_get_governance()}


@qa_router.get(
    "/compliance",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def compliance() -> dict:
    return {"data": handle_get_compliance_validation()}


@qa_router.get(
    "/readiness",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def readiness() -> dict:
    return {"data": handle_get_production_readiness()}


@qa_router.get(
    "/metrics",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def metrics() -> dict:
    return {"data": handle_get_qa_metrics()}


@qa_router.post(
    "/assessments",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def assessments(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_record_quality_assessment(
            RecordQualityAssessmentCommand(
                tenant_id=tenant_id,
                assessor=str(body.get("assessor") or "ci"),
                checklist_ids=list(body.get("checklist_ids") or []),
                passed=bool(body.get("passed", True)),
                notes=str(body.get("notes") or ""),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@qa_router.post(
    "/gates/evaluate",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def evaluate_gate(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        passed = body.get("passed")
        result = await handle_evaluate_quality_gate(
            EvaluateQualityGateCommand(
                tenant_id=tenant_id,
                gate_id=str(body.get("gate_id") or ""),
                evidence=dict(body.get("evidence") or {}),
                passed=None if passed is None else bool(passed),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@qa_router.post(
    "/release/certify",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def certify_release(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_certify_release(
            CertifyReleaseCommand(
                tenant_id=tenant_id,
                version=str(body.get("version") or "1.0.0"),
                boards_approved=list(body.get("boards_approved") or []),
                require_core_series=bool(body.get("require_core_series", True)),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}
