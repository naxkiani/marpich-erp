"""Enterprise Bank Account Management API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.treasury.container import get_bank_account_service
from contexts.treasury.presentation.bank_account_schemas import (
    AddSignatoryRequest,
    ApproveBankAccountRequest,
    AttachDocumentRequest,
    CreateBankAccountRequest,
)

bank_account_router = APIRouter(
    prefix="/treasury/bank-accounts",
    tags=["Bank Account Management"],
)


@bank_account_router.get("/catalog")
async def list_bank_account_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.read"))],
):
    return {"data": (await get_bank_account_service().list_catalog()).unwrap()}


@bank_account_router.post("", status_code=status.HTTP_201_CREATED)
async def create_bank_account(
    body: CreateBankAccountRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.write"))],
):
    result = await get_bank_account_service().create_account(
        tenant_id=tenant_id,
        bank_id=body.bank_id,
        code=body.code,
        name=body.name,
        account_type=body.account_type,
        currency=body.currency,
        organization_id=body.organization_id,
        branch_id=body.branch_id,
        iban=body.iban,
        swift_bic=body.swift_bic,
        routing_number=body.routing_number,
        account_number=body.account_number,
        virtual_account_ref=body.virtual_account_ref,
        gl_account_code=body.gl_account_code,
        opening_balance=body.opening_balance,
        require_approval=body.require_approval,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@bank_account_router.get("")
async def list_bank_accounts(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.read"))],
    organization_id: str | None = Query(None),
    bank_id: str | None = Query(None),
):
    return {
        "data": (
            await get_bank_account_service().list_accounts(
                tenant_id, organization_id=organization_id, bank_id=bank_id, mask_sensitive=True
            )
        ).unwrap()
    }


@bank_account_router.get("/{account_id}")
async def get_bank_account(
    account_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.read"))],
    reveal: bool = Query(False),
):
    perms = user.get("permissions") or []
    reveal_sensitive = reveal and ("treasury.bank_accounts.secure" in perms or "*" in perms)
    result = await get_bank_account_service().get_account(
        tenant_id, account_id, reveal_sensitive=reveal_sensitive
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@bank_account_router.post("/{account_id}/submit")
async def submit_bank_account(
    account_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.write"))],
):
    result = await get_bank_account_service().submit_account(tenant_id, account_id, correlation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@bank_account_router.post("/{account_id}/approve")
async def approve_bank_account(
    account_id: str,
    body: ApproveBankAccountRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.approve"))],
):
    result = await get_bank_account_service().approve_account(
        tenant_id,
        account_id,
        actor_id=user.get("sub", "system"),
        workflow_instance_id=body.workflow_instance_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@bank_account_router.post("/{account_id}/reject")
async def reject_bank_account(
    account_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.approve"))],
):
    result = await get_bank_account_service().reject_account(tenant_id, account_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@bank_account_router.post("/{account_id}/suspend")
async def suspend_bank_account(
    account_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.approve"))],
):
    result = await get_bank_account_service().suspend_account(tenant_id, account_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@bank_account_router.post("/{account_id}/close")
async def close_bank_account(
    account_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.approve"))],
):
    result = await get_bank_account_service().close_account(tenant_id, account_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@bank_account_router.post("/{account_id}/signatories", status_code=status.HTTP_201_CREATED)
async def add_signatory(
    account_id: str,
    body: AddSignatoryRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.write"))],
):
    result = await get_bank_account_service().add_signatory(
        tenant_id=tenant_id,
        bank_account_id=account_id,
        name=body.name,
        role=body.role,
        organization_id=body.organization_id,
        email=body.email,
        authority_limit=body.authority_limit,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@bank_account_router.get("/{account_id}/signatories")
async def list_signatories(
    account_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.read"))],
):
    result = await get_bank_account_service().list_signatories(tenant_id, account_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@bank_account_router.post("/signatories/{signatory_id}/approve")
async def approve_signatory(
    signatory_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.approve"))],
):
    result = await get_bank_account_service().approve_signatory(
        tenant_id, signatory_id, user.get("sub", "system")
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@bank_account_router.post("/{account_id}/documents", status_code=status.HTTP_201_CREATED)
async def attach_document(
    account_id: str,
    body: AttachDocumentRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.write"))],
):
    result = await get_bank_account_service().attach_document(
        tenant_id=tenant_id,
        bank_account_id=account_id,
        document_type=body.document_type,
        reference=body.reference,
        organization_id=body.organization_id,
        file_name=body.file_name,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@bank_account_router.get("/{account_id}/documents")
async def list_documents(
    account_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.read"))],
):
    result = await get_bank_account_service().list_documents(tenant_id, account_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@bank_account_router.post("/documents/{document_id}/verify")
async def verify_document(
    document_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.approve"))],
):
    result = await get_bank_account_service().verify_document(
        tenant_id, document_id, user.get("sub", "system")
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}
