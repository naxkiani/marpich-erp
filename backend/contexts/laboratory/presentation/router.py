"""Laboratory FastAPI router — CAP-HLT-007."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.laboratory.container import get_laboratory_service
from contexts.laboratory.presentation.schemas import (
    FinalizeResultRequest,
    PlaceOrderRequest,
    ReceiveSampleRequest,
)

router = APIRouter(prefix="/laboratory", tags=["Laboratory"])


@router.post("/orders", status_code=status.HTTP_201_CREATED)
async def place_order(
    body: PlaceOrderRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("laboratory.orders.write"))],
):
    result = await get_laboratory_service().place_order(
        tenant_id=tenant_id,
        order_number=body.order_number,
        patient_ref=body.patient_ref,
        test_code=body.test_code,
        correlation_id=correlation_id,
        source_encounter_ref=body.source_encounter_ref,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/orders")
async def list_orders(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("laboratory.orders.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_laboratory_service().list_orders(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}


@router.post("/samples", status_code=status.HTTP_201_CREATED)
async def receive_sample(
    body: ReceiveSampleRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("laboratory.samples.write"))],
):
    result = await get_laboratory_service().receive_sample(
        tenant_id=tenant_id,
        order_id=body.order_id,
        accession_number=body.accession_number,
        specimen_type=body.specimen_type,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        code = (
            status.HTTP_404_NOT_FOUND
            if "not_found" in (result.error or "")
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(code, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/samples")
async def list_samples(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("laboratory.samples.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_laboratory_service().list_samples(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}


@router.post("/orders/{order_id}/results", status_code=status.HTTP_200_OK)
async def finalize_result(
    order_id: str,
    body: FinalizeResultRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("laboratory.results.write"))],
):
    result = await get_laboratory_service().finalize_result(
        tenant_id=tenant_id,
        order_id=order_id,
        result_value=body.result_value,
        result_unit=body.result_unit,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        code = (
            status.HTTP_404_NOT_FOUND
            if "not_found" in (result.error or "")
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(code, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
