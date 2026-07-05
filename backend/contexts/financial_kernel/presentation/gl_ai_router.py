"""General Ledger AI API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.financial_kernel.container import get_gl_ai_service
from contexts.financial_kernel.presentation.gl_ai_schemas import (
    GLAnalyzeRequest,
    GLExplainJournalRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

gl_ai_router = APIRouter(
    prefix="/financial-kernel/gl-ai",
    tags=["General Ledger AI"],
)


@gl_ai_router.get("/catalog")
async def list_gl_ai_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ai.read"))],
):
    return {"data": (await get_gl_ai_service().list_catalog()).unwrap()}


@gl_ai_router.get("/dashboard")
async def gl_cfo_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.ai.dashboard"))],
):
    result = await get_gl_ai_service().get_cfo_dashboard(
        tenant_id=tenant_id,
        correlation_id=correlation_id,
        created_by=user.get("sub"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@gl_ai_router.get("/recommendations")
async def list_gl_recommendations(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ai.read"))],
    capability: str | None = Query(None),
):
    result = await get_gl_ai_service().list_recommendations(tenant_id, capability)
    return {"data": result.unwrap()}


@gl_ai_router.get("/jobs")
async def list_gl_jobs(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ai.read"))],
    capability: str | None = Query(None),
):
    return {"data": (await get_gl_ai_service().list_jobs(tenant_id, capability)).unwrap()}


@gl_ai_router.get("/jobs/{job_id}")
async def get_gl_job(
    job_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ai.read"))],
):
    result = await get_gl_ai_service().get_job(tenant_id, job_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@gl_ai_router.post("/analyze/{capability}", status_code=status.HTTP_201_CREATED)
async def analyze_gl(
    capability: str,
    body: GLAnalyzeRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.ai.analyze"))],
):
    result = await get_gl_ai_service().run_analysis(
        tenant_id=tenant_id,
        capability=capability,
        input_data=body.input_data,
        correlation_id=correlation_id,
        created_by=user.get("sub"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@gl_ai_router.post("/explain-journal", status_code=status.HTTP_201_CREATED)
async def explain_journal(
    body: GLExplainJournalRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.ai.analyze"))],
):
    result = await get_gl_ai_service().explain_journal(
        tenant_id=tenant_id,
        journal_id=body.journal_id,
        correlation_id=correlation_id,
        created_by=user.get("sub"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
