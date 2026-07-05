"""Enterprise Journal Engine API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.financial_kernel.container import get_financial_kernel_service
from contexts.financial_kernel.presentation.schemas import (
    BatchJournalRequest,
    CreateJournalVersionRequest,
    SignJournalRequest,
    TypedJournalRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

journal_router = APIRouter(prefix="/financial-kernel/journals", tags=["Journal Engine"])


@journal_router.get("/types")
async def list_journal_types(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.read"))],
):
    return {"data": (await get_financial_kernel_service().list_enterprise_journal_types()).unwrap()}


@journal_router.get("/types/{journal_type}/rules")
async def get_journal_type_rules(
    journal_type: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.read"))],
):
    result = await get_financial_kernel_service().get_journal_type_rules(journal_type)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@journal_router.post("/typed", status_code=status.HTTP_201_CREATED)
async def post_typed_journal(
    body: TypedJournalRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.post"))],
):
    result = await get_financial_kernel_service().post_typed_journal(
        tenant_id=tenant_id,
        journal_type=body.journal_type,
        source_context=body.source_context,
        source_document_id=body.source_document_id,
        lines=[line.model_dump() for line in body.lines],
        currency=body.currency,
        base_currency=body.base_currency,
        exchange_rate=body.exchange_rate,
        correlation_id=correlation_id,
        idempotency_key=body.idempotency_key,
        organization_id=body.organization_id,
        branch_id=body.branch_id,
        require_approval=body.require_approval,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@journal_router.post("/batch", status_code=status.HTTP_201_CREATED)
async def batch_post_journals(
    body: BatchJournalRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.batch"))],
):
    entries = [
        {
            **entry.model_dump(),
            "lines": [line.model_dump() for line in entry.lines],
        }
        for entry in body.entries
    ]
    result = await get_financial_kernel_service().batch_post_journals(
        tenant_id=tenant_id,
        entries=entries,
        correlation_id=correlation_id,
        batch_id=body.batch_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@journal_router.post("/{journal_id}/lock")
async def lock_journal(
    journal_id: str,
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.lock"))],
):
    result = await get_financial_kernel_service().lock_journal(journal_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@journal_router.post("/{journal_id}/sign")
async def sign_journal(
    journal_id: str,
    body: SignJournalRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.sign"))],
):
    result = await get_financial_kernel_service().sign_journal(
        journal_id, body.signer_id, correlation_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@journal_router.post("/{journal_id}/ai-review")
async def ai_review_journal(
    journal_id: str,
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.review"))],
):
    result = await get_financial_kernel_service().ai_review_journal(journal_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@journal_router.post("/{journal_id}/versions", status_code=status.HTTP_201_CREATED)
async def create_journal_version(
    journal_id: str,
    body: CreateJournalVersionRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.version"))],
):
    result = await get_financial_kernel_service().create_journal_version(
        journal_id=journal_id,
        lines=[line.model_dump() for line in body.lines],
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@journal_router.get("/{journal_id}/versions")
async def list_journal_versions(
    journal_id: str,
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.read"))],
):
    result = await get_financial_kernel_service().list_journal_versions(journal_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}
