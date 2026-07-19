"""Federation Ops / Deploy / SRE REST surface (P200-B11)."""
from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query

from contexts.identity.presentation.dependencies import get_tenant_id, require_permissions
from contexts.identity_federation.application.commands.ops_commands import (
    RecordDrDrillCommand,
    RequestAiOpsRecommendationCommand,
    SignalIncidentCommand,
    handle_record_dr_drill,
    handle_request_ai_ops_recommendation,
    handle_signal_incident,
)
from contexts.identity_federation.application.queries.ops_queries import (
    handle_get_deployment_profile,
    handle_get_dr_profile,
    handle_get_observability_profile,
    handle_get_ops_health,
    handle_get_ops_metrics,
    handle_get_ops_surface,
    handle_get_pipeline_profile,
    handle_get_slo_status,
)

ops_router = APIRouter(prefix="/federation/ops", tags=["federation-ops"])


@ops_router.get(
    "/surface",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def surface() -> dict:
    return {"data": handle_get_ops_surface()}


@ops_router.get(
    "/deployment",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def deployment() -> dict:
    return {"data": handle_get_deployment_profile()}


@ops_router.get(
    "/pipeline",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def pipeline() -> dict:
    return {"data": handle_get_pipeline_profile()}


@ops_router.get(
    "/observability",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def observability() -> dict:
    return {"data": handle_get_observability_profile()}


@ops_router.get(
    "/slo",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def slo(
    availability_ratio: Annotated[float | None, Query()] = None,
) -> dict:
    return {"data": handle_get_slo_status(availability_ratio=availability_ratio)}


@ops_router.get(
    "/dr",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def dr() -> dict:
    return {"data": handle_get_dr_profile()}


@ops_router.get(
    "/health",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def health() -> dict:
    return {"data": handle_get_ops_health()}


@ops_router.get(
    "/metrics",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def metrics() -> dict:
    return {"data": handle_get_ops_metrics()}


@ops_router.post(
    "/incidents/signal",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def signal_incident(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_signal_incident(
            SignalIncidentCommand(
                tenant_id=tenant_id,
                incident_class=str(body.get("incident_class") or "federation_outage"),
                severity=str(body.get("severity") or "medium"),
                summary=str(body.get("summary") or ""),
                signals=dict(body.get("signals") or {}),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@ops_router.post(
    "/dr/drill",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def dr_drill(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_record_dr_drill(
            RecordDrDrillCommand(
                tenant_id=tenant_id,
                mode=str(body.get("mode") or "active_passive"),
                steps_completed=list(body.get("steps_completed") or []),
                passed=bool(body.get("passed", True)),
                notes=str(body.get("notes") or ""),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@ops_router.post(
    "/ai/recommend",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def ai_recommend(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_request_ai_ops_recommendation(
            RequestAiOpsRecommendationCommand(
                tenant_id=tenant_id,
                context=dict(body.get("context") or body),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}
