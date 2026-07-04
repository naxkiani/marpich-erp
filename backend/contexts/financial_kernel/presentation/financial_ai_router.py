"""Enterprise Financial AI API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.financial_kernel.container import get_financial_ai_service
from contexts.financial_kernel.presentation.financial_ai_schemas import (
    AnalyzeRequest,
    ChatRequest,
    DocumentOCRRequest,
    InvoiceClassifyRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_current_user,
    get_tenant_id,
    require_permissions,
)

financial_ai_router = APIRouter(
    prefix="/financial-kernel/financial-ai",
    tags=["Financial AI"],
)


@financial_ai_router.get("/capabilities")
async def list_capabilities(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ai.read"))],
):
    result = await get_financial_ai_service().list_capabilities()
    return {"data": result.unwrap()}


@financial_ai_router.get("/dashboard")
async def ai_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.ai.dashboard"))],
):
    result = await get_financial_ai_service().get_dashboard(
        tenant_id=tenant_id,
        correlation_id=correlation_id,
        created_by=user.get("sub"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_ai_router.get("/jobs")
async def list_jobs(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ai.read"))],
    capability: str | None = Query(None),
):
    result = await get_financial_ai_service().list_jobs(tenant_id, capability)
    return {"data": result.unwrap()}


@financial_ai_router.get("/jobs/{job_id}")
async def get_job(
    job_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ai.read"))],
):
    result = await get_financial_ai_service().get_job(tenant_id, job_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@financial_ai_router.post("/analyze/{capability}", status_code=status.HTTP_201_CREATED)
async def analyze(
    capability: str,
    body: AnalyzeRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.ai.analyze"))],
):
    result = await get_financial_ai_service().run_analysis(
        tenant_id=tenant_id,
        capability=capability,
        input_data=body.input_data,
        correlation_id=correlation_id,
        created_by=user.get("sub"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_ai_router.post("/chat", status_code=status.HTTP_201_CREATED)
async def financial_chat(
    body: ChatRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.ai.chat"))],
):
    result = await get_financial_ai_service().chat(
        tenant_id=tenant_id,
        message=body.message,
        session_id=body.session_id,
        correlation_id=correlation_id,
        created_by=user.get("sub"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_ai_router.post("/cfo-assistant", status_code=status.HTTP_201_CREATED)
async def cfo_assistant(
    body: ChatRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.ai.chat"))],
):
    result = await get_financial_ai_service().cfo_assistant(
        tenant_id=tenant_id,
        message=body.message,
        session_id=body.session_id,
        correlation_id=correlation_id,
        created_by=user.get("sub"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_ai_router.post("/invoice/classify", status_code=status.HTTP_201_CREATED)
async def classify_invoice(
    body: InvoiceClassifyRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ai.analyze"))],
):
    result = await get_financial_ai_service().classify_invoice(
        tenant_id=tenant_id,
        text=body.text,
        amount=body.amount,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_ai_router.post("/document/ocr", status_code=status.HTTP_201_CREATED)
async def document_ocr(
    body: DocumentOCRRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ai.analyze"))],
):
    result = await get_financial_ai_service().ocr_document(
        tenant_id=tenant_id,
        text=body.text,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
