"""Federation Security / Zero Trust REST surface (P200-B9)."""
from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from contexts.identity.presentation.dependencies import get_tenant_id, require_permissions
from contexts.identity_federation.application.commands.security_control_commands import (
    ApproveExceptionCommand,
    CreateSecurityPolicyCommand,
    DetectThreatCommand,
    EvaluateRiskCommand,
    EvaluateZeroTrustCommand,
    GovernAiActionCommand,
    MitigateThreatCommand,
    RegisterSecurityControlCommand,
    RevokeExceptionCommand,
    RunComplianceAssessmentCommand,
    RunContinuousVerificationCommand,
    handle_approve_exception,
    handle_create_security_policy,
    handle_detect_threat,
    handle_evaluate_risk,
    handle_evaluate_zero_trust,
    handle_govern_ai_action,
    handle_mitigate_threat,
    handle_register_security_control,
    handle_revoke_exception,
    handle_run_compliance_assessment,
    handle_run_continuous_verification,
)
from contexts.identity_federation.application.queries.security_control_queries import (
    GetComplianceStatusQuery,
    GetRiskAssessmentQuery,
    GetSecurityEventsQuery,
    GetThreatStatusQuery,
    handle_get_compliance_status,
    handle_get_risk_assessment,
    handle_get_security_events,
    handle_get_security_posture,
    handle_get_security_surface,
    handle_get_threat_status,
    handle_get_zero_trust_decision,
)

security_router = APIRouter(prefix="/federation/security", tags=["federation-security"])


@security_router.get(
    "/surface",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def surface() -> dict:
    return {"data": handle_get_security_surface()}


@security_router.get(
    "/posture",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def posture(tenant_id: Annotated[str, Depends(get_tenant_id)]) -> dict:
    return {"data": handle_get_security_posture(tenant_id=tenant_id)}


@security_router.post(
    "/controls",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def register_control(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_register_security_control(
            RegisterSecurityControlCommand(
                tenant_id=tenant_id,
                name=str(body.get("name") or "default"),
                control_ref=body.get("control_ref"),
                security_level=int(body.get("security_level") or 1),
                classification=str(body.get("classification") or "internal"),
                baseline=dict(body.get("baseline") or {}),
                rules=list(body.get("rules") or []),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@security_router.post(
    "/policies",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def create_policy(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_create_security_policy(
            CreateSecurityPolicyCommand(
                tenant_id=tenant_id,
                control_ref=str(body.get("control_ref") or ""),
                policy_key=str(body.get("policy_key") or ""),
                conditions=dict(body.get("conditions") or {}),
                version=str(body.get("version") or "1.0.0"),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@security_router.post(
    "/zero-trust/evaluate",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def evaluate_zt(
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    result = await handle_evaluate_zero_trust(
        EvaluateZeroTrustCommand(tenant_id=tenant_id, context=dict(body.get("context") or body))
    )
    return {"data": result}


@security_router.get(
    "/zero-trust/last",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def last_zt(tenant_id: Annotated[str, Depends(get_tenant_id)]) -> dict:
    try:
        return {"data": handle_get_zero_trust_decision(tenant_id=tenant_id)}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@security_router.post(
    "/risk/evaluate",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def evaluate_risk(
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    result = await handle_evaluate_risk(
        EvaluateRiskCommand(
            tenant_id=tenant_id,
            subject_type=str(body.get("subject_type") or "session"),
            subject_id=str(body.get("subject_id") or ""),
            signals=dict(body.get("signals") or {}),
            trust_score=int(body.get("trust_score") or 50),
        )
    )
    return {"data": result}


@security_router.get(
    "/risk/{assessment_ref}",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def get_risk(
    assessment_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_get_risk_assessment(
            GetRiskAssessmentQuery(tenant_id=tenant_id, assessment_ref=assessment_ref)
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"data": result}


@security_router.post(
    "/verification/continuous",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def continuous_verification(
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    result = await handle_run_continuous_verification(
        RunContinuousVerificationCommand(
            tenant_id=tenant_id, context=dict(body.get("context") or body)
        )
    )
    return {"data": result}


@security_router.post(
    "/threats/detect",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def detect_threat(
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    result = await handle_detect_threat(
        DetectThreatCommand(tenant_id=tenant_id, indicators=dict(body.get("indicators") or body))
    )
    return {"data": result}


@security_router.post(
    "/threats/{threat_ref}/mitigate",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def mitigate_threat(
    threat_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_mitigate_threat(
            MitigateThreatCommand(
                tenant_id=tenant_id,
                threat_ref=threat_ref,
                action=str(body.get("action") or "contain"),
                notes=str(body.get("notes") or ""),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@security_router.get(
    "/threats",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def list_threats(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    limit: int = 50,
) -> dict:
    result = await handle_get_threat_status(
        GetThreatStatusQuery(tenant_id=tenant_id, limit=limit)
    )
    return {"data": result}


@security_router.post(
    "/compliance/assess",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def assess_compliance(
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    result = await handle_run_compliance_assessment(
        RunComplianceAssessmentCommand(
            tenant_id=tenant_id,
            control_results=dict(body.get("control_results") or body),
        )
    )
    return {"data": result}


@security_router.get(
    "/compliance",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def compliance_status(tenant_id: Annotated[str, Depends(get_tenant_id)]) -> dict:
    result = await handle_get_compliance_status(GetComplianceStatusQuery(tenant_id=tenant_id))
    return {"data": result}


@security_router.post(
    "/ai/govern",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def govern_ai(
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    result = await handle_govern_ai_action(
        GovernAiActionCommand(
            tenant_id=tenant_id, ai_context=dict(body.get("ai_context") or body)
        )
    )
    return {"data": result}


@security_router.post(
    "/exceptions",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def approve_exception(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_approve_exception(
            ApproveExceptionCommand(
                tenant_id=tenant_id,
                reason=str(body.get("reason") or ""),
                scope=list(body.get("scope") or []),
                days=int(body.get("days") or 7),
                exception_ref=body.get("exception_ref"),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@security_router.post(
    "/exceptions/{exception_ref}/revoke",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def revoke_exception(
    exception_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_revoke_exception(
            RevokeExceptionCommand(
                tenant_id=tenant_id,
                exception_ref=exception_ref,
                reason=str(body.get("reason") or "revoked"),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@security_router.get(
    "/events",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def security_events(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    limit: int = 50,
) -> dict:
    result = await handle_get_security_events(
        GetSecurityEventsQuery(tenant_id=tenant_id, limit=limit)
    )
    return {"data": result}
