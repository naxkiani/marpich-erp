"""Enterprise Regulatory Reporting Platform API."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import get_correlation_id, get_tenant_id, require_permissions
from contexts.regulatory_reporting.container import get_enterprise_regulatory_reporting_service
from contexts.regulatory_reporting.presentation.schemas import ConfigureAdapterRequest, GenerateReportRequest

enterprise_regulatory_reporting_router = APIRouter(
    prefix="/regulatory-reporting",
    tags=["Enterprise Regulatory Reporting Platform"],
)


@enterprise_regulatory_reporting_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("regulatory.read"))],
):
    return {"data": (await get_enterprise_regulatory_reporting_service().list_catalog()).unwrap()}


@enterprise_regulatory_reporting_router.get("/dependency-map")
async def dependency_map(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("regulatory.read"))],
):
    return {"data": (await get_enterprise_regulatory_reporting_service().get_dependency_map()).unwrap()}


@enterprise_regulatory_reporting_router.post("/seed")
async def seed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("regulatory.write"))],
):
    return {"data": (await get_enterprise_regulatory_reporting_service().seed(tenant_id)).unwrap()}


@enterprise_regulatory_reporting_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("regulatory.read"))],
):
    return {"data": (await get_enterprise_regulatory_reporting_service().get_dashboard(tenant_id)).unwrap()}


@enterprise_regulatory_reporting_router.get("/adapters")
async def list_adapters(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("regulatory.read"))],
):
    return {"data": (await get_enterprise_regulatory_reporting_service().list_adapters(tenant_id)).unwrap()}


@enterprise_regulatory_reporting_router.post("/adapters", status_code=status.HTTP_201_CREATED)
async def configure_adapter(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: ConfigureAdapterRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("regulatory.write"))],
):
    result = await get_enterprise_regulatory_reporting_service().configure_adapter(
        tenant_id,
        country_code=body.country_code,
        country_name=body.country_name,
        regulator_types=body.regulator_types,
        supported_formats=body.supported_formats,
        package_plugin_id=body.package_plugin_id,
        portal_url=body.portal_url,
        correlation_id=correlation_id,
    )
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@enterprise_regulatory_reporting_router.post("/reports/generate", status_code=status.HTTP_201_CREATED)
async def generate_report(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: GenerateReportRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("regulatory.write"))],
):
    result = await get_enterprise_regulatory_reporting_service().generate_report(
        tenant_id,
        country_code=body.country_code,
        regulator_type=body.regulator_type,
        report_category=body.report_category,
        export_format=body.export_format,
        parameters=body.parameters,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@enterprise_regulatory_reporting_router.get("/submissions")
async def list_submissions(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("regulatory.read"))],
):
    return {"data": (await get_enterprise_regulatory_reporting_service().list_submissions(tenant_id)).unwrap()}


@enterprise_regulatory_reporting_router.get("/submissions/{submission_ref}")
async def get_submission(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    submission_ref: str,
    _user: Annotated[dict, Depends(require_permissions("regulatory.read"))],
):
    result = await get_enterprise_regulatory_reporting_service().get_submission(tenant_id, submission_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@enterprise_regulatory_reporting_router.post("/submissions/{submission_ref}/submit")
async def submit_digitally(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    submission_ref: str,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("regulatory.write"))],
):
    result = await get_enterprise_regulatory_reporting_service().submit_digitally(
        tenant_id, submission_ref, correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
