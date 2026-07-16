"""Enterprise Connector Framework API."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from contexts.enterprise_connector_framework.container import get_enterprise_connector_framework_service
from contexts.enterprise_connector_framework.presentation.schemas import (
    ExecuteOperationRequest,
    RegisterConnectorRequest,
    RegisterPluginBindingRequest,
)
from contexts.identity.presentation.dependencies import get_correlation_id, get_tenant_id, require_permissions

enterprise_connector_framework_router = APIRouter(
    prefix="/enterprise-connector-framework",
    tags=["Enterprise Connector Framework"],
)


@enterprise_connector_framework_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_connector_framework.read"))],
):
    return {"data": (await get_enterprise_connector_framework_service().list_catalog()).unwrap()}


@enterprise_connector_framework_router.get("/dependency-map")
async def dependency_map(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_connector_framework.read"))],
):
    return {"data": (await get_enterprise_connector_framework_service().get_dependency_map()).unwrap()}


@enterprise_connector_framework_router.get("/connector-catalog")
async def connector_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_connector_framework.read"))],
):
    return {"data": (await get_enterprise_connector_framework_service().get_connector_catalog()).unwrap()}


@enterprise_connector_framework_router.get("/sdk")
async def sdk_info(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_connector_framework.read"))],
):
    return {"data": (await get_enterprise_connector_framework_service().get_sdk_info()).unwrap()}


@enterprise_connector_framework_router.post("/seed")
async def seed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_connector_framework.write"))],
):
    return {"data": (await get_enterprise_connector_framework_service().seed(tenant_id)).unwrap()}


@enterprise_connector_framework_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_connector_framework.read"))],
):
    return {"data": (await get_enterprise_connector_framework_service().get_dashboard(tenant_id)).unwrap()}


@enterprise_connector_framework_router.get("/connectors")
async def list_connectors(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_connector_framework.read"))],
):
    return {"data": (await get_enterprise_connector_framework_service().list_connectors(tenant_id)).unwrap()}


@enterprise_connector_framework_router.post("/connectors")
async def register_connector(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: RegisterConnectorRequest,
    _user: Annotated[dict, Depends(require_permissions("enterprise_connector_framework.write"))],
):
    return {"data": (await get_enterprise_connector_framework_service().register_connector(
        tenant_id,
        connector_type=body.connector_type,
        display_name=body.display_name,
        config=body.config,
        plugin_id=body.plugin_id,
    )).unwrap()}


@enterprise_connector_framework_router.post("/connectors/{instance_ref}/test")
async def test_connection(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    instance_ref: str,
    _user: Annotated[dict, Depends(require_permissions("enterprise_connector_framework.write"))],
):
    return {"data": (await get_enterprise_connector_framework_service().test_connection(tenant_id, instance_ref)).unwrap()}


@enterprise_connector_framework_router.post("/connectors/{instance_ref}/execute")
async def execute_operation(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    instance_ref: str,
    body: ExecuteOperationRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_connector_framework.write"))],
):
    return {"data": (await get_enterprise_connector_framework_service().execute_operation(
        tenant_id,
        instance_ref=instance_ref,
        operation=body.operation,
        payload=body.payload,
        correlation_id=correlation_id,
        idempotency_key=body.idempotency_key,
    )).unwrap()}


@enterprise_connector_framework_router.get("/executions")
async def list_executions(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_connector_framework.read"))],
):
    return {"data": (await get_enterprise_connector_framework_service().list_executions(tenant_id)).unwrap()}


@enterprise_connector_framework_router.get("/health-records")
async def list_health_records(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_connector_framework.read"))],
):
    return {"data": (await get_enterprise_connector_framework_service().list_health_records(tenant_id)).unwrap()}


@enterprise_connector_framework_router.get("/plugin-bindings")
async def list_plugin_bindings(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_connector_framework.read"))],
):
    return {"data": (await get_enterprise_connector_framework_service().list_plugin_bindings(tenant_id)).unwrap()}


@enterprise_connector_framework_router.post("/plugin-bindings")
async def register_plugin_binding(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: RegisterPluginBindingRequest,
    _user: Annotated[dict, Depends(require_permissions("enterprise_connector_framework.admin"))],
):
    return {"data": (await get_enterprise_connector_framework_service().register_plugin_binding(
        tenant_id,
        plugin_id=body.plugin_id,
        instance_ref=body.instance_ref,
        extension_point=body.extension_point,
    )).unwrap()}
