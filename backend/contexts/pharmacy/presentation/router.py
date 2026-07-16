"""Pharmacy FastAPI router — CAP-HLT-008."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.pharmacy.container import get_pharmacy_service
from contexts.pharmacy.presentation.schemas import DispenseRequest, ReceivePrescriptionRequest

router = APIRouter(prefix="/pharmacy", tags=["Pharmacy"])


@router.post("/prescriptions", status_code=status.HTTP_201_CREATED)
async def receive_prescription(
    body: ReceivePrescriptionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("pharmacy.prescriptions.write"))],
):
    result = await get_pharmacy_service().receive_prescription(
        tenant_id=tenant_id,
        rx_number=body.rx_number,
        patient_ref=body.patient_ref,
        drug_code=body.drug_code,
        drug_name=body.drug_name,
        quantity=body.quantity,
        correlation_id=correlation_id,
        source_encounter_ref=body.source_encounter_ref,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/prescriptions")
async def list_prescriptions(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("pharmacy.prescriptions.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_pharmacy_service().list_prescriptions(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}


@router.post("/dispenses", status_code=status.HTTP_201_CREATED)
async def dispense(
    body: DispenseRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("pharmacy.dispenses.write"))],
):
    result = await get_pharmacy_service().dispense(
        tenant_id=tenant_id,
        prescription_id=body.prescription_id,
        quantity_dispensed=body.quantity_dispensed,
        correlation_id=correlation_id,
        dispensed_by=user.get("sub"),
    )
    if not result.succeeded:
        code = (
            status.HTTP_404_NOT_FOUND
            if "not_found" in (result.error or "")
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(code, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/dispenses")
async def list_dispenses(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("pharmacy.dispenses.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_pharmacy_service().list_dispenses(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}
