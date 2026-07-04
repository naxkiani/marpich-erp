"""Localization FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.localization.container import get_localization_service
from contexts.localization.presentation.schemas import (
    DefineKeyRequest,
    ReportMissingKeyRequest,
    UpsertTranslationRequest,
)

router = APIRouter(prefix="/localization", tags=["Localization"])


@router.get("/locales")
async def list_locales(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("localization.locale.read"))],
):
    result = await get_localization_service().list_locales(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/keys", status_code=status.HTTP_201_CREATED)
async def define_key(
    body: DefineKeyRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("localization.translate.write"))],
):
    result = await get_localization_service().define_key(
        tenant_id=tenant_id,
        namespace=body.namespace,
        key=body.key,
        default_value=body.default_value,
        description=body.description,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.put("/bundles/{locale_code}/{namespace}/{key}")
async def upsert_translation(
    locale_code: str,
    namespace: str,
    key: str,
    body: UpsertTranslationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("localization.translate.write"))],
):
    result = await get_localization_service().upsert_translation(
        tenant_id=tenant_id,
        locale_code=locale_code,
        namespace=namespace,
        key=key,
        value=body.value,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/bundles/{locale_code}/{namespace}")
async def get_bundle(
    locale_code: str,
    namespace: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("localization.translate.read"))],
):
    result = await get_localization_service().get_bundle(tenant_id, locale_code, namespace)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/missing-keys", status_code=status.HTTP_202_ACCEPTED)
async def report_missing_key(
    body: ReportMissingKeyRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("localization.translate.read"))],
):
    result = await get_localization_service().report_missing_key(
        tenant_id=tenant_id,
        locale_code=body.locale_code,
        namespace=body.namespace,
        key=body.key,
        correlation_id=correlation_id,
    )
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
