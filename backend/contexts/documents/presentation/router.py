"""Documents FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.documents.container import get_documents_service
from contexts.documents.presentation.schemas import (
    AddVersionRequest,
    CreateDocumentRequest,
    CreateFolderRequest,
    SignDocumentRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_current_user,
    get_tenant_id,
    require_permissions,
)

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/folders/root")
async def get_root_folder(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("documents.read"))],
):
    result = await get_documents_service().get_root_folder(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/folders", status_code=status.HTTP_201_CREATED)
async def create_folder(
    body: CreateFolderRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("documents.folders.write"))],
):
    result = await get_documents_service().create_folder(
        tenant_id=tenant_id,
        parent_id=body.parent_id,
        name=body.name,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.get("/folders/{folder_id}/contents")
async def get_folder_contents(
    folder_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("documents.read"))],
):
    result = await get_documents_service().get_folder_contents(tenant_id, folder_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/documents", status_code=status.HTTP_201_CREATED)
async def create_document(
    body: CreateDocumentRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("documents.write"))],
):
    result = await get_documents_service().create_document(
        tenant_id=tenant_id,
        correlation_id=correlation_id,
        folder_id=body.folder_id,
        title=body.title,
        description=body.description,
        file_name=body.file_name,
        content_type=body.content_type,
        content=body.content,
        metadata=body.metadata,
        created_by=user["sub"],
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/documents/{document_id}/versions", status_code=status.HTTP_201_CREATED)
async def add_version(
    document_id: str,
    body: AddVersionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("documents.write"))],
):
    result = await get_documents_service().add_version(
        tenant_id=tenant_id,
        correlation_id=correlation_id,
        document_id=document_id,
        file_name=body.file_name,
        content_type=body.content_type,
        content=body.content,
        created_by=user["sub"],
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/documents/{document_id}")
async def get_document(
    document_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("documents.read"))],
):
    result = await get_documents_service().get_document(tenant_id, document_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.get("/documents/{document_id}/download")
async def download_document(
    document_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("documents.read"))],
):
    result = await get_documents_service().download_current(tenant_id, document_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/documents/{document_id}/sign", status_code=status.HTTP_201_CREATED)
async def sign_document(
    document_id: str,
    body: SignDocumentRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("documents.sign"))],
):
    result = await get_documents_service().request_signature(
        tenant_id=tenant_id,
        correlation_id=correlation_id,
        document_id=document_id,
        signers=body.signers,
        requester_id=user["sub"],
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/documents/{document_id}/archive")
async def archive_document(
    document_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("documents.write"))],
):
    result = await get_documents_service().archive_document(
        tenant_id, correlation_id, document_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
