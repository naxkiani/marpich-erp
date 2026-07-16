from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from contexts.identity.presentation.dependencies import get_tenant_id, get_correlation_id, require_permissions
from contexts.identity_digital_twin.container import get_identity_digital_twin_service
from contexts.identity_digital_twin.presentation.schemas import CreateTwinRequest, SyncTwinRequest, SimulateTwinRequest, DetectDriftRequest
identity_digital_twin_router=APIRouter(prefix="/identity-twins", tags=["Enterprise Identity Digital Twin"])
def _unwrap(result):
    if not result.succeeded: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.error or "request_failed")
    return {"data":result.unwrap()}
@identity_digital_twin_router.get("/dashboard")
async def dashboard(tenant_id: Annotated[str,Depends(get_tenant_id)], _: Annotated[dict,Depends(require_permissions("twin.read"))]): return _unwrap(await get_identity_digital_twin_service().get_dashboard(tenant_id))
@identity_digital_twin_router.post("")
async def create(body: CreateTwinRequest, tenant_id: Annotated[str,Depends(get_tenant_id)], correlation_id: Annotated[str,Depends(get_correlation_id)], _: Annotated[dict,Depends(require_permissions("twin.write"))]): return _unwrap(await get_identity_digital_twin_service().create(tenant_id,identity_ref=body.identity_ref,attributes=body.attributes,correlation_id=correlation_id))
@identity_digital_twin_router.get("/{twin_ref}")
async def get(twin_ref: str, tenant_id: Annotated[str,Depends(get_tenant_id)], _: Annotated[dict,Depends(require_permissions("twin.read"))]): return _unwrap(await get_identity_digital_twin_service().get(tenant_id,twin_ref))
@identity_digital_twin_router.post("/{twin_ref}/sync")
async def sync(twin_ref: str, body: SyncTwinRequest, tenant_id: Annotated[str,Depends(get_tenant_id)], correlation_id: Annotated[str,Depends(get_correlation_id)], _: Annotated[dict,Depends(require_permissions("twin.write"))]): return _unwrap(await get_identity_digital_twin_service().sync(tenant_id,twin_ref,projection=body.projection,source_event=body.source_event,correlation_id=correlation_id))
@identity_digital_twin_router.post("/{twin_ref}/simulations")
async def simulate(twin_ref: str, body: SimulateTwinRequest, tenant_id: Annotated[str,Depends(get_tenant_id)], correlation_id: Annotated[str,Depends(get_correlation_id)], _: Annotated[dict,Depends(require_permissions("twin.write"))]): return _unwrap(await get_identity_digital_twin_service().simulate(tenant_id,twin_ref,scenario_type=body.scenario_type,proposed_change=body.proposed_change,correlation_id=correlation_id))
@identity_digital_twin_router.post("/{twin_ref}/drift")
async def drift(twin_ref: str, body: DetectDriftRequest, tenant_id: Annotated[str,Depends(get_tenant_id)], correlation_id: Annotated[str,Depends(get_correlation_id)], _: Annotated[dict,Depends(require_permissions("twin.write"))]): return _unwrap(await get_identity_digital_twin_service().detect_drift(tenant_id,twin_ref,observed_projection=body.observed_projection,source_event=body.source_event,correlation_id=correlation_id))
