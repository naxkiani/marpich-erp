"""Clinic FastAPI router — CAP-HLT-002/003."""
from __future__ import annotations

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.clinic.container import get_clinic_service
from contexts.clinic.presentation.schemas import (
    CompleteEncounterRequest,
    CreateReferralRequest,
    RegisterPatientRequest,
    ScheduleAppointmentRequest,
    StartEncounterRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

router = APIRouter(prefix="/clinic", tags=["Clinic"])


@router.post("/patients", status_code=status.HTTP_201_CREATED)
async def register_patient(
    body: RegisterPatientRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("clinic.patients.write"))],
):
    result = await get_clinic_service().register_patient(
        tenant_id=tenant_id,
        patient_number=body.patient_number,
        first_name=body.first_name,
        last_name=body.last_name,
        date_of_birth=body.date_of_birth,
        correlation_id=correlation_id,
        document_id=body.document_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/patients")
async def list_patients(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("clinic.patients.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_clinic_service().list_patients(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}


@router.post("/appointments", status_code=status.HTTP_201_CREATED)
async def schedule_appointment(
    body: ScheduleAppointmentRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("clinic.appointments.write"))],
):
    try:
        scheduled_at = datetime.fromisoformat(body.scheduled_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid scheduled_at") from exc

    result = await get_clinic_service().schedule_appointment(
        tenant_id=tenant_id,
        patient_id=body.patient_id,
        provider_name=body.provider_name,
        scheduled_at=scheduled_at,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/appointments")
async def list_appointments(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("clinic.appointments.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_clinic_service().list_appointments(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}


@router.post("/encounters", status_code=status.HTTP_201_CREATED)
async def start_encounter(
    body: StartEncounterRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("clinic.encounters.write"))],
):
    result = await get_clinic_service().start_encounter(
        tenant_id=tenant_id,
        appointment_id=body.appointment_id,
        patient_id=body.patient_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/encounters")
async def list_encounters(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("clinic.encounters.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_clinic_service().list_encounters(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}


@router.post("/encounters/{encounter_id}/complete")
async def complete_encounter(
    encounter_id: str,
    body: CompleteEncounterRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("clinic.encounters.write"))],
):
    result = await get_clinic_service().complete_encounter(
        tenant_id=tenant_id,
        encounter_id=encounter_id,
        diagnosis_codes=body.diagnosis_codes,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/referrals", status_code=status.HTTP_201_CREATED)
async def create_referral(
    body: CreateReferralRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("clinic.referrals.write"))],
):
    result = await get_clinic_service().create_referral(
        tenant_id=tenant_id,
        encounter_id=body.encounter_id,
        target_specialty=body.target_specialty,
        reason=body.reason,
        correlation_id=correlation_id,
        send=body.send,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
