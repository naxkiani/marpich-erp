"""Enterprise Financial Documents API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.financial_kernel.container import get_financial_document_service
from contexts.financial_kernel.presentation.financial_document_schemas import (
    AddDocumentVersionRequest,
    CreateFinancialDocumentRequest,
    SignFinancialDocumentRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_current_user,
    get_tenant_id,
    require_permissions,
)

financial_documents_router = APIRouter(
    prefix="/financial-kernel/financial-documents",
    tags=["Financial Documents"],
)


def _line_items(lines):
    if not lines:
        return None
    result = []
    for item in lines:
        d = item.model_dump()
        if d.get("amount") is None:
            d["amount"] = round(d["quantity"] * d["unit_price"], 2)
        result.append(d)
    return result


@financial_documents_router.post("", status_code=status.HTTP_201_CREATED)
async def create_financial_document(
    body: CreateFinancialDocumentRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.documents.write"))],
):
    key = body.idempotency_key or f"{body.source_context}:{body.source_document_id}:{body.document_type}"
    result = await get_financial_document_service().create_document(
        tenant_id=tenant_id,
        source_context=body.source_context,
        source_document_id=body.source_document_id,
        idempotency_key=key,
        document_type=body.document_type,
        currency=body.currency,
        total_amount=body.total_amount,
        counterparty_name=body.counterparty_name,
        reference=body.reference,
        lines=_line_items(body.lines),
        metadata=body.metadata,
        counterparty_id=body.counterparty_id,
        created_by=user.get("sub"),
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_documents_router.get("")
async def list_financial_documents(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.documents.read"))],
):
    result = await get_financial_document_service().list_documents(tenant_id)
    return {"data": result.unwrap()}


@financial_documents_router.get("/verify/{token}")
async def verify_financial_document_qr(token: str):
    result = await get_financial_document_service().verify_qr(token)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@financial_documents_router.get("/{document_id}")
async def get_financial_document(
    document_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.documents.read"))],
):
    result = await get_financial_document_service().get_document(tenant_id, document_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@financial_documents_router.get("/{document_id}/pdf")
async def get_financial_document_pdf(
    document_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.documents.read"))],
):
    result = await get_financial_document_service().get_pdf(tenant_id, document_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@financial_documents_router.post("/{document_id}/versions", status_code=status.HTTP_201_CREATED)
async def add_financial_document_version(
    document_id: str,
    body: AddDocumentVersionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.documents.write"))],
):
    result = await get_financial_document_service().add_version(
        tenant_id=tenant_id,
        document_id=document_id,
        lines=_line_items(body.lines),
        total_amount=body.total_amount,
        metadata=body.metadata,
        created_by=user.get("sub"),
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_documents_router.post("/{document_id}/approval")
async def request_document_approval(
    document_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.documents.approve"))],
):
    result = await get_financial_document_service().request_approval(
        tenant_id=tenant_id,
        document_id=document_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_documents_router.post("/{document_id}/approval/complete")
async def complete_document_approval(
    document_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.documents.approve"))],
):
    result = await get_financial_document_service().complete_approval(
        tenant_id=tenant_id,
        document_id=document_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_documents_router.post("/{document_id}/sign")
async def sign_financial_document(
    document_id: str,
    body: SignFinancialDocumentRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.documents.sign"))],
):
    signer_id = body.signer_id or user.get("sub") or "system"
    result = await get_financial_document_service().sign_document(
        tenant_id=tenant_id,
        document_id=document_id,
        signer_id=signer_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_documents_router.post("/{document_id}/issue")
async def issue_financial_document(
    document_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.documents.issue"))],
):
    result = await get_financial_document_service().issue_document(
        tenant_id=tenant_id,
        document_id=document_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_documents_router.post("/{document_id}/void")
async def void_financial_document(
    document_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.documents.write"))],
):
    result = await get_financial_document_service().void_document(
        tenant_id=tenant_id,
        document_id=document_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}
