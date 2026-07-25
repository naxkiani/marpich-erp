"""Hospital FastAPI router — CAP-HLT-001."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.hospital.container import get_hospital_ai_service, get_hospital_service
from contexts.hospital.presentation.schemas import (
    AdmitPatientRequest,
    AiInferRequest,
    AssignBedRequest,
    CompleteEncounterRequest,
    CreateBedRequest,
    DocumentEncounterRequest,
    RegisterPatientRequest,
    StartEncounterRequest,
    TransferAdmissionRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

router = APIRouter(prefix="/hospital", tags=["Hospital"])


@router.post("/patients", status_code=status.HTTP_201_CREATED)
async def register_patient(
    body: RegisterPatientRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.patients.write"))],
):
    result = await get_hospital_service().register_patient(
        tenant_id=tenant_id,
        mrn=body.mrn,
        first_name=body.first_name,
        last_name=body.last_name,
        date_of_birth=body.date_of_birth,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/patients")
async def list_patients(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.patients.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_hospital_service().list_patients(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}


@router.post("/admissions", status_code=status.HTTP_201_CREATED)
async def admit_patient(
    body: AdmitPatientRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.admissions.write"))],
):
    result = await get_hospital_service().admit_patient(
        tenant_id=tenant_id,
        patient_id=body.patient_id,
        ward=body.ward,
        bed_id=body.bed_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/admissions")
async def list_admissions(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.admissions.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_hospital_service().list_admissions(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}


@router.post("/beds", status_code=status.HTTP_201_CREATED)
async def create_bed(
    body: CreateBedRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.beds.write"))],
):
    result = await get_hospital_service().create_bed(
        tenant_id=tenant_id,
        ward=body.ward,
        room=body.room,
        bed_code=body.bed_code,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/beds")
async def list_beds(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.beds.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_hospital_service().list_beds(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}


@router.post("/admissions/{admission_id}/assign-bed")
async def assign_bed(
    admission_id: str,
    body: AssignBedRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.admissions.write"))],
):
    result = await get_hospital_service().assign_bed(
        tenant_id=tenant_id,
        admission_id=admission_id,
        bed_id=body.bed_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/admissions/{admission_id}/transfer")
async def transfer_admission(
    admission_id: str,
    body: TransferAdmissionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.admissions.write"))],
):
    result = await get_hospital_service().transfer_admission(
        tenant_id=tenant_id,
        admission_id=admission_id,
        to_ward=body.to_ward,
        to_bed_id=body.to_bed_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/admissions/{admission_id}/discharge")
async def discharge_admission(
    admission_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.admissions.write"))],
):
    result = await get_hospital_service().discharge_admission(
        tenant_id=tenant_id,
        admission_id=admission_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/encounters", status_code=status.HTTP_201_CREATED)
async def start_encounter(
    body: StartEncounterRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.encounters.write"))],
):
    result = await get_hospital_service().start_encounter(
        tenant_id=tenant_id,
        admission_id=body.admission_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/encounters")
async def list_encounters(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.encounters.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
    admission_id: Annotated[str | None, Query()] = None,
    status: Annotated[str | None, Query()] = None,
):
    result = await get_hospital_service().list_encounters(
        tenant_id,
        limit=limit,
        offset=offset,
        admission_id=admission_id,
        status=status,
    )
    return {"data": result.unwrap()}


@router.post("/encounters/{encounter_id}/document")
async def document_encounter(
    encounter_id: str,
    body: DocumentEncounterRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.encounters.write"))],
):
    result = await get_hospital_service().document_encounter(
        tenant_id=tenant_id,
        encounter_id=encounter_id,
        procedure_codes=body.procedure_codes,
        diagnosis_codes=body.diagnosis_codes,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/encounters/{encounter_id}/complete")
async def complete_encounter(
    encounter_id: str,
    body: CompleteEncounterRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.encounters.write"))],
):
    result = await get_hospital_service().complete_encounter(
        tenant_id=tenant_id,
        encounter_id=encounter_id,
        procedure_codes=body.procedure_codes,
        diagnosis_codes=body.diagnosis_codes,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/encounters/{encounter_id}")
async def get_encounter(
    encounter_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.encounters.read"))],
):
    result = await get_hospital_service().get_encounter(tenant_id, encounter_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.get("/care-events")
async def list_care_events(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.encounters.read"))],
    patient_id: Annotated[str | None, Query()] = None,
    admission_id: Annotated[str | None, Query()] = None,
    encounter_id: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
):
    """Local projections from laboratory/pharmacy integration events (peer IDs only)."""
    result = await get_hospital_service().list_care_events(
        tenant_id,
        patient_id=patient_id,
        admission_id=admission_id,
        encounter_id=encounter_id,
        limit=limit,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.get("/dashboard")
async def hospital_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.patients.read"))],
):
    svc = get_hospital_service()
    await svc.ensure_demo_catalog(tenant_id, correlation_id=correlation_id)
    result = await svc.get_dashboard(tenant_id)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/seed", status_code=status.HTTP_201_CREATED)
async def seed_demo_catalog(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.patients.write"))],
):
    result = await get_hospital_service().ensure_demo_catalog(
        tenant_id, correlation_id=correlation_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/ai/surfaces")
async def hospital_ai_surfaces(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.ai.read"))],
):
    result = await get_hospital_ai_service().list_surfaces()
    return {"data": result.unwrap()}


@router.post("/ai/infer")
async def hospital_ai_infer(
    body: AiInferRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("hospital.ai.infer"))],
):
    result = await get_hospital_ai_service().infer(
        tenant_id,
        surface=body.surface,
        payload=body.payload,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
