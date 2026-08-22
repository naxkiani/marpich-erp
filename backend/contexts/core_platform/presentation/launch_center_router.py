"""P395 Launch Center API. Overlay on Core Platform. No second admin or GO-LIVE."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from contexts.identity.presentation.dependencies import get_current_user, get_tenant_id

launch_center_router = APIRouter(prefix="/launch-center", tags=["Launch Center"])


def _load(name: str):
    repo = Path(__file__).resolve().parents[4]
    path = repo / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"{name}_api", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _workspace() -> dict[str, Any]:
    return _load("meos_p395").workspace()


def _orchestrate(command: str, body: "PlanRequest") -> dict[str, Any]:
    return _load("meos_p396").orchestrate(
        command,
        release=body.release or None,
        provider_name=body.provider,
        environment=body.environment,
        authorize=body.authorize,
    )


class PlanRequest(BaseModel):
    provider: str = Field(default="aws", max_length=32)
    environment: str = Field(default="staging", max_length=32)
    profile: str = Field(default="staging", max_length=32)
    release: str = Field(default="", max_length=64)
    authorize: bool = False


@launch_center_router.get("/status")
async def status(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    data = _workspace()
    return {"data": data}


@launch_center_router.get("/providers")
async def providers(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    data = _workspace()
    return {"data": {"providers": data["providers"], "credentials": data["credentials"]}}


@launch_center_router.get("/environments")
async def environments(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    data = _workspace()
    return {"data": {"environments": data.get("environments") or [], "total": data["environments_total"]}}


@launch_center_router.get("/releases")
async def releases(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    ident = _load("meos_p397").release_identity()
    return {"data": {"releases": [ident], "latest_rejected": True, "factory": "meos_p397"}}


@launch_center_router.get("/jobs")
async def jobs(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    data = _workspace()
    return {"data": {"jobs": data.get("jobs") or [], "active": data["active_jobs"], "failed": data["failed_jobs"]}}


@launch_center_router.post("/plan")
async def create_plan(
    body: PlanRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": {**_orchestrate("plan", body), "STATUS": "VALIDATION_ONLY", "executed": False}}


@launch_center_router.post("/validate")
async def validate_plan(
    body: PlanRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": {**_orchestrate("validate", body), "DEPLOYMENT": "DISABLED", "executed": False}}


@launch_center_router.post("/provision")
async def provision(
    body: PlanRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": _orchestrate("deploy", body)}


@launch_center_router.post("/deployments/plan")
async def deployment_plan(
    body: PlanRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": _orchestrate("plan", body)}


@launch_center_router.post("/deployments/validate")
async def deployment_validate(
    body: PlanRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": _orchestrate("validate", body)}


@launch_center_router.post("/deployments/approve")
async def deployment_approve(
    body: PlanRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": _orchestrate("approve", body)}


@launch_center_router.post("/deployments")
async def deployment_create(
    body: PlanRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": _orchestrate("deploy", body)}


@launch_center_router.post("/deployments/verify")
async def deployment_verify(
    body: PlanRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": _orchestrate("verify", body)}


@launch_center_router.post("/deployments/rollback")
async def deployment_rollback(
    body: PlanRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": _orchestrate("rollback", body)}


@launch_center_router.get("/deployments/history")
async def deployment_history(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": _load("meos_p396").history()}


@launch_center_router.get("/control-plane")
async def control_plane(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": _load("meos_p399").evaluate()}


@launch_center_router.get("/resources")
async def resources(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": _load("meos_p399").resource_catalog()}


@launch_center_router.get("/graph")
async def graph(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": _load("meos_p399").resource_graph()}


@launch_center_router.get("/drift")
async def drift(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": _load("meos_p399").dispatch("drift")}


@launch_center_router.get("/security")
async def security(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": _load("meos_p399").dispatch("security")}


@launch_center_router.get("/cost")
async def cost(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": _load("meos_p399").dispatch("cost")}


@launch_center_router.get("/capacity")
async def capacity(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": _load("meos_p399").dispatch("capacity")}


@launch_center_router.get("/backups")
async def backups(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": _load("meos_p399").evaluate()["backup"]}


@launch_center_router.get("/restores")
async def restores(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": {"STATUS": "NOT_EXECUTED", "authorization_required": True, "executed": False}}


@launch_center_router.get("/autonomous-operations")
async def autonomous_operations(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    return {"data": _load("meos_p400").evaluate()}
