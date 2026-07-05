"""Enterprise KYC Platform API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.banking.container import get_banking_kyc_platform_service
from contexts.banking.presentation.banking_kyc_schemas import (
    ApproveCaseRequest,
    BiometricHookRequest,
    CompleteBiometricRequest,
    CompleteReviewRequest,
    EvaluatePolicyRequest,
    OpenKycCaseRequest,
    RejectCaseRequest,
    ScheduleReviewRequest,
    ScreeningRequest,
    SubmitAddressRequest,
    SubmitDocumentRequest,
    VerifyAddressRequest,
    VerifyDocumentRequest,
)
from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)

banking_kyc_router = APIRouter(
    prefix="/banking/kyc",
    tags=["Banking KYC Platform"],
)


def _raise(result) -> None:
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)


@banking_kyc_router.get("/catalog")
async def kyc_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.read"))],
):
    return {"data": (await get_banking_kyc_platform_service().list_catalog()).unwrap()}


@banking_kyc_router.get("/policy-keys")
async def kyc_policy_keys(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.read"))],
):
    return {"data": (await get_banking_kyc_platform_service().list_policy_keys()).unwrap()}


@banking_kyc_router.get("/workflow")
async def kyc_workflow(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.read"))],
):
    return {"data": (await get_banking_kyc_platform_service().list_workflow()).unwrap()}


@banking_kyc_router.get("/dashboard")
async def kyc_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.read"))],
):
    return {"data": (await get_banking_kyc_platform_service().get_dashboard(tenant_id)).unwrap()}


@banking_kyc_router.post("/cases", status_code=status.HTTP_201_CREATED)
async def open_case(
    body: OpenKycCaseRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.write"))],
):
    result = await get_banking_kyc_platform_service().open_case(tenant_id=tenant_id, **body.model_dump())
    _raise(result)
    return {"data": result.unwrap()}


@banking_kyc_router.get("/cases")
async def list_cases(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.read"))],
):
    return {"data": (await get_banking_kyc_platform_service().list_cases(tenant_id)).unwrap()}


@banking_kyc_router.get("/cases/{case_id}")
async def get_case(
    case_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.read"))],
):
    result = await get_banking_kyc_platform_service().get_case(case_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_kyc_router.post("/cases/{case_id}/documents", status_code=status.HTTP_201_CREATED)
async def submit_document(
    case_id: str,
    body: SubmitDocumentRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.write"))],
):
    result = await get_banking_kyc_platform_service().submit_document(
        tenant_id=tenant_id, case_id=case_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_kyc_router.post("/documents/{document_id}/verify")
async def verify_document(
    document_id: str,
    body: VerifyDocumentRequest,
    user: Annotated[dict, Depends(require_permissions("banking.kyc.verify"))],
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
):
    result = await get_banking_kyc_platform_service().verify_document(
        document_id=document_id,
        verified_by=body.verified_by,
        actor_id=user.get("sub"),
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_kyc_router.post("/cases/{case_id}/addresses", status_code=status.HTTP_201_CREATED)
async def submit_address(
    case_id: str,
    body: SubmitAddressRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.write"))],
):
    result = await get_banking_kyc_platform_service().submit_address(
        tenant_id=tenant_id, case_id=case_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_kyc_router.post("/addresses/{address_id}/verify")
async def verify_address(
    address_id: str,
    body: VerifyAddressRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.verify"))],
):
    result = await get_banking_kyc_platform_service().verify_address(
        address_id=address_id, verified_by=body.verified_by
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_kyc_router.post("/cases/{case_id}/screening/pep")
async def pep_screening(
    case_id: str,
    body: ScreeningRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("banking.kyc.screen"))],
):
    result = await get_banking_kyc_platform_service().run_pep_screening(
        tenant_id=tenant_id,
        case_id=case_id,
        match_score=body.match_score,
        match_details=body.match_details,
        provider_ref=body.provider_ref,
        screened_by=body.screened_by or user.get("sub"),
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_kyc_router.post("/cases/{case_id}/screening/sanctions")
async def sanctions_screening(
    case_id: str,
    body: ScreeningRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("banking.kyc.screen"))],
):
    result = await get_banking_kyc_platform_service().run_sanctions_screening(
        tenant_id=tenant_id,
        case_id=case_id,
        match_score=body.match_score,
        match_details=body.match_details,
        provider_ref=body.provider_ref,
        screened_by=body.screened_by or user.get("sub"),
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_kyc_router.post("/cases/{case_id}/classify-risk")
async def classify_risk(
    case_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.write"))],
):
    result = await get_banking_kyc_platform_service().classify_risk(
        tenant_id=tenant_id, case_id=case_id
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_kyc_router.post("/cases/{case_id}/submit")
async def submit_for_approval(
    case_id: str,
    user: Annotated[dict, Depends(require_permissions("banking.kyc.write"))],
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
):
    result = await get_banking_kyc_platform_service().submit_for_approval(
        case_id=case_id, actor_id=user.get("sub")
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_kyc_router.post("/cases/{case_id}/approve")
async def approve_case(
    case_id: str,
    body: ApproveCaseRequest,
    user: Annotated[dict, Depends(require_permissions("banking.kyc.approve"))],
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
):
    result = await get_banking_kyc_platform_service().approve_case(
        case_id=case_id,
        approver_id=body.approver_id,
        actor_id=user.get("sub"),
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_kyc_router.post("/cases/{case_id}/reject")
async def reject_case(
    case_id: str,
    body: RejectCaseRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.approve"))],
):
    result = await get_banking_kyc_platform_service().reject_case(
        case_id=case_id, approver_id=body.approver_id, reason=body.reason
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_kyc_router.post("/cases/{case_id}/reviews", status_code=status.HTTP_201_CREATED)
async def schedule_review(
    case_id: str,
    body: ScheduleReviewRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.write"))],
):
    result = await get_banking_kyc_platform_service().schedule_periodic_review(
        tenant_id=tenant_id, case_id=case_id, due_in_days=body.due_in_days
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_kyc_router.post("/reviews/{review_id}/complete")
async def complete_review(
    review_id: str,
    body: CompleteReviewRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.write"))],
):
    result = await get_banking_kyc_platform_service().complete_periodic_review(
        review_id=review_id,
        completed_by=body.completed_by,
        outcome=body.outcome,
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_kyc_router.post("/cases/{case_id}/biometric", status_code=status.HTTP_201_CREATED)
async def request_biometric(
    case_id: str,
    body: BiometricHookRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.write"))],
):
    result = await get_banking_kyc_platform_service().request_biometric_hook(
        tenant_id=tenant_id, case_id=case_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_kyc_router.post("/biometric/{hook_id}/complete")
async def complete_biometric(
    hook_id: str,
    body: CompleteBiometricRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.write"))],
):
    result = await get_banking_kyc_platform_service().complete_biometric_hook(
        hook_id=hook_id,
        status=body.status,
        result_payload=body.result_payload,
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_kyc_router.get("/cases/{case_id}/audit")
async def audit_trail(
    case_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.read"))],
):
    return {"data": (await get_banking_kyc_platform_service().get_audit_trail(case_id)).unwrap()}


@banking_kyc_router.post("/policies/evaluate")
async def evaluate_policy(
    body: EvaluatePolicyRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.read"))],
):
    result = await get_banking_kyc_platform_service().evaluate_policy(
        tenant_id=tenant_id, policy_key=body.policy_key, facts=body.facts
    )
    _raise(result)
    return {"data": result.unwrap()}
