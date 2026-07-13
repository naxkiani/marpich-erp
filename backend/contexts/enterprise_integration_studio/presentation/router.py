"""Enterprise Integration Studio Platform API."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.enterprise_integration_studio.container import get_enterprise_integration_studio_service
from contexts.enterprise_integration_studio.presentation.schemas import (
    CreateArtifactRequest,
    CreateProjectRequest,
    DeployArtifactRequest,
    TestArtifactRequest,
)
from contexts.identity.presentation.dependencies import get_tenant_id, require_permissions

enterprise_integration_studio_router = APIRouter(
    prefix="/enterprise-integration-studio",
    tags=["Enterprise Integration Studio"],
)


@enterprise_integration_studio_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.read"))],
):
    return {"data": (await get_enterprise_integration_studio_service().list_catalog()).unwrap()}


@enterprise_integration_studio_router.get("/dependency-map")
async def dependency_map(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.read"))],
):
    return {"data": (await get_enterprise_integration_studio_service().get_dependency_map()).unwrap()}


@enterprise_integration_studio_router.post("/seed")
async def seed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.write"))],
):
    return {"data": (await get_enterprise_integration_studio_service().seed(tenant_id)).unwrap()}


@enterprise_integration_studio_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.read"))],
):
    return {"data": (await get_enterprise_integration_studio_service().get_dashboard(tenant_id)).unwrap()}


@enterprise_integration_studio_router.get("/developer-portal")
async def developer_portal(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.read"))],
):
    return {"data": (await get_enterprise_integration_studio_service().get_developer_portal(tenant_id)).unwrap()}


@enterprise_integration_studio_router.get("/citizen-workspace")
async def citizen_workspace(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.read"))],
):
    result = await get_enterprise_integration_studio_service().get_citizen_workspace(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_403_FORBIDDEN, result.error)
    return {"data": result.unwrap()}


@enterprise_integration_studio_router.get("/marketplace")
async def marketplace(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.read"))],
):
    return {"data": (await get_enterprise_integration_studio_service().list_marketplace(tenant_id)).unwrap()}


@enterprise_integration_studio_router.get("/projects")
async def list_projects(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.read"))],
):
    return {"data": (await get_enterprise_integration_studio_service().list_projects(tenant_id)).unwrap()}


@enterprise_integration_studio_router.post("/projects")
async def create_project(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: CreateProjectRequest,
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.write"))],
):
    return {"data": (await get_enterprise_integration_studio_service().create_project(
        tenant_id,
        name=body.name,
        workspace_type=body.workspace_type,
        description=body.description,
    )).unwrap()}


@enterprise_integration_studio_router.get("/artifacts")
async def list_artifacts(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.read"))],
):
    return {"data": (await get_enterprise_integration_studio_service().list_artifacts(tenant_id)).unwrap()}


@enterprise_integration_studio_router.post("/artifacts")
async def create_artifact(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: CreateArtifactRequest,
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.write"))],
):
    result = await get_enterprise_integration_studio_service().create_artifact(
        tenant_id,
        project_ref=body.project_ref,
        name=body.name,
        artifact_type=body.artifact_type,
        mapping=body.mapping,
        transformation=body.transformation,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@enterprise_integration_studio_router.get("/artifacts/{artifact_ref}/designer")
async def get_designer(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    artifact_ref: str,
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.read"))],
):
    result = await get_enterprise_integration_studio_service().get_designer(tenant_id, artifact_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@enterprise_integration_studio_router.get("/artifacts/{artifact_ref}/documentation")
async def get_documentation(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    artifact_ref: str,
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.read"))],
):
    result = await get_enterprise_integration_studio_service().get_documentation(tenant_id, artifact_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@enterprise_integration_studio_router.post("/artifacts/{artifact_ref}/test")
async def test_artifact(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    artifact_ref: str,
    body: TestArtifactRequest,
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.write"))],
):
    result = await get_enterprise_integration_studio_service().test_artifact(
        tenant_id, artifact_ref, use_mock=body.use_mock,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@enterprise_integration_studio_router.post("/artifacts/{artifact_ref}/publish")
async def publish_version(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    artifact_ref: str,
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.write"))],
):
    result = await get_enterprise_integration_studio_service().publish_version(tenant_id, artifact_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@enterprise_integration_studio_router.post("/artifacts/{artifact_ref}/deploy")
async def deploy_artifact(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    artifact_ref: str,
    body: DeployArtifactRequest,
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.write"))],
):
    result = await get_enterprise_integration_studio_service().deploy_artifact(
        tenant_id, artifact_ref, environment=body.environment,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@enterprise_integration_studio_router.get("/versions")
async def list_versions(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.read"))],
):
    return {"data": (await get_enterprise_integration_studio_service().list_versions(tenant_id)).unwrap()}


@enterprise_integration_studio_router.get("/deployments")
async def list_deployments(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.read"))],
):
    return {"data": (await get_enterprise_integration_studio_service().list_deployments(tenant_id)).unwrap()}


@enterprise_integration_studio_router.get("/test-runs")
async def list_test_runs(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.read"))],
):
    return {"data": (await get_enterprise_integration_studio_service().list_test_runs(tenant_id)).unwrap()}


@enterprise_integration_studio_router.get("/mocks")
async def list_mocks(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_integration_studio.read"))],
):
    return {"data": (await get_enterprise_integration_studio_service().list_mocks(tenant_id)).unwrap()}
